<!--
  cybersecurity-projects — creative lab corpus README
-->

<div align="center">
  <img src="https://raw.githubusercontent.com/WinstonMascarenhas1006/cybersecurity-projects/main/assets/repo-banner.png" alt="cybersecurity-projects laboratory corpus" width="100%" />
</div>

<p align="center">
  <a href="https://github.com/WinstonMascarenhas1006"><img src="https://img.shields.io/badge/Author-Winston_Mascarenhas-0f766e?style=flat-square" alt="Author" /></a>
  &nbsp;
  <a href="https://portfolio-winston-mascarenhas.vercel.app"><img src="https://img.shields.io/badge/Portfolio-Live-1e3a5f?style=flat-square" alt="Portfolio" /></a>
  &nbsp;
  <img src="https://img.shields.io/badge/Tools-15-334155?style=flat-square" alt="15 tools" />
  &nbsp;
  <img src="https://img.shields.io/badge/Timeline-Apr_2025→Jun_2026-111827?style=flat-square" alt="Timeline" />
</p>

<div align="center">
  <img src="https://raw.githubusercontent.com/WinstonMascarenhas1006/cybersecurity-projects/main/assets/repo-ethics.png" alt="Authorized labs only" width="100%" />
</div>

<br/>

### What this is

A **hands-on cybersecurity laboratory corpus** — fifteen tools spanning reconnaissance, detection, hardening, and analysis.  
Each folder is a self-contained learning artifact: source, docs, and a path to run (or build) it.

This is not a random dump of scripts. It is a structured practice ground for **lab-grounded security engineering**.

<div align="center">
  <img src="https://raw.githubusercontent.com/WinstonMascarenhas1006/cybersecurity-projects/main/assets/repo-domains.png" alt="Domains: Recon, Detect, Harden, Analyze" width="100%" />
</div>

<br/>

### Build arc

<div align="center">
  <img src="https://raw.githubusercontent.com/WinstonMascarenhas1006/cybersecurity-projects/main/assets/timeline-board.png" alt="Build arc from 2025 Q2 to 2026 Q2" width="100%" />
</div>

<br/>

### Laboratory inventory

<div align="center">
  <img src="https://raw.githubusercontent.com/WinstonMascarenhas1006/cybersecurity-projects/main/assets/inventory-board.png" alt="Fifteen-tool laboratory inventory" width="100%" />
</div>

<br/>

<p align="center">
  <a href="./base64-tool/"><code>01 base64-tool</code></a>
  ·
  <a href="./c2-beacon/"><code>02 c2-beacon</code></a>
  ·
  <a href="./caesar-cipher/"><code>03 caesar-cipher</code></a>
  ·
  <a href="./canary-token-generator/"><code>04 canary</code></a>
  ·
  <a href="./dns-lookup/"><code>05 dns-lookup</code></a>
</p>
<p align="center">
  <a href="./firewall-rule-engine/"><code>06 firewall</code></a>
  ·
  <a href="./hash-cracker/"><code>07 hash-cracker</code></a>
  ·
  <a href="./keylogger/"><code>08 keylogger</code></a>
  ·
  <a href="./linux-cis-hardening-auditor/"><code>09 CIS auditor</code></a>
  ·
  <a href="./linux-ebpf-security-tracer/"><code>10 eBPF tracer</code></a>
</p>
<p align="center">
  <a href="./metadata-scrubber-tool/"><code>11 scrubber</code></a>
  ·
  <a href="./network-traffic-analyzer/"><code>12 traffic</code></a>
  ·
  <a href="./simple-port-scanner/"><code>13 ports</code></a>
  ·
  <a href="./simple-vulnerability-scanner/"><code>14 vuln-scan</code></a>
  ·
  <a href="./systemd-persistence-scanner/"><code>15 persistence</code></a>
</p>

---

### Quick start

```powershell
powershell -ExecutionPolicy Bypass -File setup.ps1
```

- **Python** → `.venv` + `pip install -e .` + CLI smoke test  
- **Go** → `go build` + `--help`  
- **C++ / V / Linux-only** → builds where possible; clear skip message on Windows  

```powershell
cd base64-tool
.\.venv\Scripts\Activate.ps1
b64tool encode "Hello World"
```

### Runtime map

<div align="center">
  <img src="https://raw.githubusercontent.com/WinstonMascarenhas1006/cybersecurity-projects/main/assets/status-board.png" alt="Windows runtime map" width="100%" />
</div>

<br/>

<details>
<summary><b>Stack-specific setup</b></summary>

<br/>

**Python**

```powershell
cd <project-folder>
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

`base64-tool` · `caesar-cipher` · `dns-lookup` · `keylogger` · `linux-ebpf-security-tracer` · `metadata-scrubber-tool` · `network-traffic-analyzer` · `c2-beacon`

**Go**

```powershell
go build -o svscan.exe ./cmd/angela      # simple-vulnerability-scanner
go build -o sentinel.exe ./cmd/sentinel  # systemd-persistence-scanner
go build -o canary.exe ./cmd/canary      # canary-token-generator
```

**C++ / Linux**

```bash
mkdir build && cd build && cmake .. && cmake --build .
```

Prefer Linux/WSL for CIS auditor, eBPF tracer, firewall (V), hash-cracker, and port-scanner. Docker Compose for full c2-beacon / canary stacks.

</details>

---

### Legal & ethics

These tools are for **education and authorized security testing only**.  
Do **not** run offensive capabilities against systems you do not own or lack **explicit written permission** to test.

---

<div align="center">

**Lab corpus** — studied seriously, practiced carefully, built in public.

[Author](https://github.com/WinstonMascarenhas1006)
·
[Portfolio](https://portfolio-winston-mascarenhas.vercel.app)
·
[Profile](https://github.com/WinstonMascarenhas1006/WinstonMascarenhas1006)

</div>
