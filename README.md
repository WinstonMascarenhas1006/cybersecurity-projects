# Cybersecurity Beginner Projects

Personal portfolio of 15 beginner-level security tools built between **April 2025 and June 2026**, one project per month (longer multi-stack builds took two months).

**Author:** [Winston Mascarenhas](https://github.com/WinstonMascarenhas1006)  
**GitHub:** [github.com/WinstonMascarenhas1006](https://github.com/WinstonMascarenhas1006)  
**Portfolio:** [portfolio-winston-mascarenhas.vercel.app](https://portfolio-winston-mascarenhas.vercel.app)

## Development timeline

| # | Folder | Period | Duration |
|---|--------|--------|----------|
| 1 | [base64-tool](./base64-tool/) | April 2025 | 1 month |
| 2 | [c2-beacon](./c2-beacon/) | May – June 2025 | 2 months |
| 3 | [caesar-cipher](./caesar-cipher/) | July 2025 | 1 month |
| 4 | [canary-token-generator](./canary-token-generator/) | August – September 2025 | 2 months |
| 5 | [dns-lookup](./dns-lookup/) | October 2025 | 1 month |
| 6 | [firewall-rule-engine](./firewall-rule-engine/) | November 2025 | 1 month |
| 7 | [hash-cracker](./hash-cracker/) | December 2025 | 1 month |
| 8 | [keylogger](./keylogger/) | January 2026 | 1 month |
| 9 | [linux-cis-hardening-auditor](./linux-cis-hardening-auditor/) | February 2026 | 1 month |
| 10 | [linux-ebpf-security-tracer](./linux-ebpf-security-tracer/) | March 2026 | 1 month |
| 11 | [metadata-scrubber-tool](./metadata-scrubber-tool/) | April 2026 | 1 month |
| 12 | [network-traffic-analyzer](./network-traffic-analyzer/) | May 2026 | 1 month |
| 13 | [simple-port-scanner](./simple-port-scanner/) | May 2026 | 1 month |
| 14 | [simple-vulnerability-scanner](./simple-vulnerability-scanner/) | June 2026 | 1 month |
| 15 | [systemd-persistence-scanner](./systemd-persistence-scanner/) | June 2026 | 1 month |

## All projects

| # | Folder | Language | What it is |
|---|--------|----------|------------|
| 1 | [base64-tool](./base64-tool/) | Python | Multi-format encode/decode CLI with layer detection |
| 2 | [c2-beacon](./c2-beacon/) | Python | Educational C2 beacon simulation for defensive learning |
| 3 | [caesar-cipher](./caesar-cipher/) | Python | Caesar cipher encrypt, decrypt, and frequency-analysis cracking |
| 4 | [canary-token-generator](./canary-token-generator/) | Go | Honeytoken and canary file generator for intrusion detection |
| 5 | [dns-lookup](./dns-lookup/) | Python | DNS resolution with WHOIS and structured output |
| 6 | [firewall-rule-engine](./firewall-rule-engine/) | V | Rule-based firewall engine for allow/deny decisions |
| 7 | [hash-cracker](./hash-cracker/) | C++ | Dictionary and brute-force hash cracking |
| 8 | [keylogger](./keylogger/) | Python | Educational keystroke logger (authorized use only) |
| 9 | [linux-cis-hardening-auditor](./linux-cis-hardening-auditor/) | Shell/Python | CIS benchmark compliance checks for Linux |
| 10 | [linux-ebpf-security-tracer](./linux-ebpf-security-tracer/) | Python/C | eBPF syscall tracer for Linux security monitoring |
| 11 | [metadata-scrubber-tool](./metadata-scrubber-tool/) | Python | Strip EXIF and metadata from images and documents |
| 12 | [network-traffic-analyzer](./network-traffic-analyzer/) | Python | PCAP analysis and live traffic capture |
| 13 | [simple-port-scanner](./simple-port-scanner/) | C++ | Async TCP port scanner with Boost.Asio |
| 14 | [simple-vulnerability-scanner](./simple-vulnerability-scanner/) | Go | Python dependency CVE scanner and updater (angela) |
| 15 | [systemd-persistence-scanner](./systemd-persistence-scanner/) | Go | Linux persistence mechanism scanner (sentinel) |

## Setup

The fastest way to get everything installed is the root setup script. It walks through all 15 projects in order, creates a separate `.venv` for each Python project (to avoid package name clashes), and reports what succeeded or needs extra tooling.

From the repo root in PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File setup.ps1
```

What the script does per project type:

- **Python projects** — creates `.venv`, runs `pip install -e .`, and smoke-tests the CLI
- **Go projects** — runs `go build` and prints `--help` output
- **C++ / V / Linux-only projects** — attempts build where possible; skips with a message when Windows lacks dependencies

After setup, activate a Python project's venv before running commands:

```powershell
cd base64-tool
.\.venv\Scripts\Activate.ps1
b64tool encode "Hello World"
```

## Status on Windows

This table matches what `setup.ps1` expects on a typical Windows machine. Items marked "needs extra setup" still have source code you can read; some require Linux, WSL, Docker, or additional compilers.

| # | Project | Status | How to run after setup |
|---|---------|--------|--------------------------|
| 1 | base64-tool | Ready | `b64tool encode "Hello World"` |
| 2 | c2-beacon | Deps ready | `docker compose -f dev.compose.yml up -d` (needs Docker) |
| 3 | caesar-cipher | Ready | `caesar-cipher encrypt "HELLO" --key 3` |
| 4 | canary-token-generator | Backend built | `just init && just dev-up` (needs Docker) |
| 5 | dns-lookup | Ready | `dnslookup query google.com --type A --json` |
| 6 | firewall-rule-engine | Needs V compiler | `./install.sh` on Linux or macOS |
| 7 | hash-cracker | Needs Boost/OpenSSL | `./install.sh` on Linux |
| 8 | keylogger | Ready | `python keylogger.py --help` |
| 9 | linux-cis-hardening-auditor | Linux only | `./install.sh && cisaudit --test` in WSL |
| 10 | linux-ebpf-security-tracer | CLI ready | `ebpf-tracer --help` (eBPF needs Linux + bcc) |
| 11 | metadata-scrubber-tool | Ready | `metadata-scrubber --help` |
| 12 | network-traffic-analyzer | Ready | `netanal --help` (live capture needs [Npcap](https://npcap.com)) |
| 13 | simple-port-scanner | Needs Boost | `./install.sh` on Linux or WSL |
| 14 | simple-vulnerability-scanner | Ready | `.\svscan.exe --help` |
| 15 | systemd-persistence-scanner | Ready | `.\sentinel.exe --help` (scanning needs Linux) |

## Manual setup by stack

### Python projects

Most Python folders use a standard editable install inside a local venv:

```powershell
cd <project-folder>
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

Projects: base64-tool, caesar-cipher, dns-lookup, keylogger, linux-ebpf-security-tracer, metadata-scrubber-tool, network-traffic-analyzer (under `python/`), c2-beacon (under `backend/`).

### Go projects

```powershell
cd <project-folder>
go build -o tool.exe ./cmd/<name>
```

- simple-vulnerability-scanner → `go build -o svscan.exe ./cmd/angela`
- systemd-persistence-scanner → `go build -o sentinel.exe ./cmd/sentinel`
- canary-token-generator → `go build -o canary.exe ./cmd/canary`

### C++ projects

```bash
cd <project-folder>
mkdir build && cd build
cmake ..
cmake --build .
```

Projects: hash-cracker, simple-port-scanner. Both need Boost and a recent C++ toolchain.

### Linux-only or special cases

- **linux-cis-hardening-auditor** — run on Linux or WSL
- **linux-ebpf-security-tracer** — CLI installs on Windows; kernel tracing needs Linux with bcc
- **systemd-persistence-scanner** — builds on Windows; point `--root` at a Linux filesystem to scan
- **simple-port-scanner** — build on Linux/WSL where Boost is available
- **firewall-rule-engine** — needs the [V compiler](https://vlang.io)
- **c2-beacon** and **canary-token-generator** — full stacks use Docker Compose

## Legal notice

These tools are for educational use and authorized security testing only. Do not run offensive tools (keylogger, C2 beacon, port scanners, hash crackers, etc.) against systems you do not own or lack explicit written permission to test.
