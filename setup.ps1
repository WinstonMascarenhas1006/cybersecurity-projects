# Cybersecurity Beginner Projects - Setup Script (run in order)
# Each project gets its own .venv to avoid package name conflicts.
# Usage: powershell -ExecutionPolicy Bypass -File setup.ps1

$ErrorActionPreference = "Continue"
$Root = $PSScriptRoot
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

function New-ProjectVenv($projectPath) {
    $venv = Join-Path $projectPath ".venv"
    if (-not (Test-Path $venv)) {
        python -m venv $venv
    }
    $activate = Join-Path $venv "Scripts\Activate.ps1"
    . $activate
    python -m pip install -q --upgrade pip
    return $venv
}

function Test-Step($num, $name, $script) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host " $num/15  $name" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    try {
        & $script
        Write-Host "[OK] $name" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "[SKIP] $name - $($_.Exception.Message)" -ForegroundColor Yellow
        return $false
    }
}

$results = @{}

# 1. base64-tool
$results["1"] = Test-Step 1 "base64-tool" {
    $p = "$Root\base64-tool"; New-ProjectVenv $p | Out-Null
    Push-Location $p; pip install -e . -q
    $out = b64tool encode "Hello World"
    Write-Host "  -> $out"
    Pop-Location
}

# 2. c2-beacon
$results["2"] = Test-Step 2 "c2-beacon" {
    $p = "$Root\c2-beacon\backend"; New-ProjectVenv $p | Out-Null
    Push-Location $p; pip install fastapi pydantic pydantic-settings aiosqlite "uvicorn[standard]" -q
    Pop-Location
    Write-Host "  Deps installed. Full stack: docker compose -f dev.compose.yml up -d"
}

# 3. caesar-cipher
$results["3"] = Test-Step 3 "caesar-cipher" {
    $p = "$Root\caesar-cipher"; New-ProjectVenv $p | Out-Null
    Push-Location $p; pip install -e . -q
    caesar-cipher encrypt "HELLO" --key 3
    Pop-Location
}

# 4. canary-token-generator
$results["4"] = Test-Step 4 "canary-token-generator" {
    Push-Location "$Root\canary-token-generator\backend"
    go build -o canary.exe ./cmd/canary
    Write-Host "  Backend built. Full stack: just init && just dev-up"
    Pop-Location
}

# 5. dns-lookup
$results["5"] = Test-Step 5 "dns-lookup" {
    $p = "$Root\dns-lookup"; New-ProjectVenv $p | Out-Null
    Push-Location $p; pip install -e . -q
    dnslookup query google.com --type A --json | Select-Object -First 6
    Pop-Location
}

# 6. firewall-rule-engine
$results["6"] = Test-Step 6 "firewall-rule-engine" {
    if (Get-Command v -ErrorAction SilentlyContinue) {
        Push-Location "$Root\firewall-rule-engine"; v -o fwrule src/main.v; Pop-Location
    } else { throw "Install V compiler from https://vlang.io" }
}

# 7. hash-cracker
$results["7"] = Test-Step 7 "hash-cracker" {
    throw "Needs C++23 + Boost + OpenSSL. Run ./install.sh on Linux."
}

# 8. keylogger
$results["8"] = Test-Step 8 "keylogger" {
    $p = "$Root\keylogger"; New-ProjectVenv $p | Out-Null
    Push-Location $p; pip install -e ".[windows]" -q
    python keylogger.py --help | Select-Object -First 4
    Pop-Location
}

# 9. linux-cis-hardening-auditor
$results["9"] = Test-Step 9 "linux-cis-hardening-auditor" {
    throw "Linux only. Use WSL: ./install.sh && cisaudit --test"
}

# 10. linux-ebpf-security-tracer
$results["10"] = Test-Step 10 "linux-ebpf-security-tracer" {
    $p = "$Root\linux-ebpf-security-tracer"; New-ProjectVenv $p | Out-Null
    Push-Location $p; pip install -e . -q
    ebpf-tracer --help | Select-Object -First 4
    Write-Host "  eBPF tracing requires Linux + bcc"
    Pop-Location
}

# 11. metadata-scrubber-tool
$results["11"] = Test-Step 11 "metadata-scrubber-tool" {
    $p = "$Root\metadata-scrubber-tool"; New-ProjectVenv $p | Out-Null
    Push-Location $p; pip install -e . -q
    metadata-scrubber --help | Select-Object -First 4
    Pop-Location
}

# 12. network-traffic-analyzer
$results["12"] = Test-Step 12 "network-traffic-analyzer" {
    $p = "$Root\network-traffic-analyzer\python"; New-ProjectVenv $p | Out-Null
    Push-Location $p; pip install -e . -q
    netanal --help | Select-Object -First 4
    Write-Host "  Live capture needs Npcap: https://npcap.com"
    Pop-Location
}

# 13. simple-port-scanner
$results["13"] = Test-Step 13 "simple-port-scanner" {
    throw "Needs C++20 + Boost. Run ./install.sh on Linux."
}

# 14. simple-vulnerability-scanner
$results["14"] = Test-Step 14 "simple-vulnerability-scanner" {
    Push-Location "$Root\simple-vulnerability-scanner"
    go build -o svscan.exe ./cmd/angela
    .\svscan.exe --help | Select-Object -First 5
    Pop-Location
}

# 15. systemd-persistence-scanner
$results["15"] = Test-Step 15 "systemd-persistence-scanner" {
    Push-Location "$Root\systemd-persistence-scanner"
    go build -o sentinel.exe ./cmd/sentinel
    .\sentinel.exe --help | Select-Object -First 5
    Write-Host "  Scanning requires Linux target"
    Pop-Location
}

Write-Host ""
Write-Host "========== SUMMARY ==========" -ForegroundColor Cyan
1..15 | ForEach-Object {
    $ok = $results["$_"]
    $names = @("base64-tool","c2-beacon","caesar-cipher","canary-token-generator","dns-lookup",
               "firewall-rule-engine","hash-cracker","keylogger","linux-cis-hardening-auditor",
               "linux-ebpf-security-tracer","metadata-scrubber-tool","network-traffic-analyzer",
               "simple-port-scanner","simple-vulnerability-scanner","systemd-persistence-scanner")
    $color = if ($ok) { "Green" } else { "Yellow" }
    Write-Host "  $_/15 $($names[$_-1]): $(if ($ok) {'OK'} else {'NEEDS EXTRA SETUP'})" -ForegroundColor $color
}
