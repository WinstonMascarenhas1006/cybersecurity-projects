<!--
  cybersecurity-projects — creative lab corpus README
  Matches profile aesthetic: ink / teal / academic field notes
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

### Development timeline

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

### Laboratory inventory

| # | Project | Stack | Role in the corpus |
|---|--------|-------|--------------------|
| 1 | [base64-tool](./base64-tool/) | Python | Multi-format encode/decode with layer detection |
| 2 | [c2-beacon](./c2-beacon/) | Python | Educational C2 beacon for *defensive* learning |
| 3 | [caesar-cipher](./caesar-cipher/) | Python | Classical cipher + frequency-analysis cracker |
| 4 | [canary-token-generator](./canary-token-generator/) | Go | Honeytoken / canary artifacts for intrusion cues |
| 5 | [dns-lookup](./dns-lookup/) | Python | DNS resolution, WHOIS, structured export |
| 6 | [firewall-rule-engine](./firewall-rule-engine/) | V | Allow/deny decision engine over rule sets |
| 7 | [hash-cracker](./hash-cracker/) | C++ | Dictionary / brute-force hash cracking (lab use) |
| 8 | [keylogger](./keylogger/) | Python | Educational keystroke logger — **authorized use only** |
| 9 | [linux-cis-hardening-auditor](./linux-cis-hardening-auditor/) | Shell/Python | CIS-style compliance checks for Linux |
| 10 | [linux-ebpf-security-tracer](./linux-ebpf-security-tracer/) | Python/C | eBPF syscall tracing for security monitoring |
| 11 | [metadata-scrubber-tool](./metadata-scrubber-tool/) | Python | Strip EXIF / metadata from images & documents |
| 12 | [network-traffic-analyzer](./network-traffic-analyzer/) | Python | PCAP analysis and live capture |
| 13 | [simple-port-scanner](./simple-port-scanner/) | C++ | Async TCP port scanner (Boost.Asio) |
| 14 | [simple-vulnerability-scanner](./simple-vulnerability-scanner/) | Go | Python dependency CVE scan & update helper |
| 15 | [systemd-persistence-scanner](./systemd-persistence-scanner/) | Go | Linux persistence mechanism scanner |

---

### Quick start

From the repo root in PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File setup.ps1
```

What `setup.ps1` does:

- **Python** — creates `.venv`, `pip install -e .`, smoke-tests the CLI  
- **Go** — `go build` + prints `--help`  
- **C++ / V / Linux-only** — builds where possible; skips with a clear message on Windows  

Then:

```powershell
cd base64-tool
.\.venv\Scripts\Activate.ps1
b64tool encode "Hello World"
```

### Status on Windows

| # | Project | Status | After setup |
|---|---------|--------|-------------|
| 1 | base64-tool | Ready | `b64tool encode "Hello World"` |
| 2 | c2-beacon | Deps ready | `docker compose -f dev.compose.yml up -d` |
| 3 | caesar-cipher | Ready | `caesar-cipher encrypt "HELLO" --key 3` |
| 4 | canary-token-generator | Backend built | `just init && just dev-up` (Docker) |
| 5 | dns-lookup | Ready | `dnslookup query google.com --type A --json` |
| 6 | firewall-rule-engine | Needs V | `./install.sh` on Linux/macOS |
| 7 | hash-cracker | Needs Boost/OpenSSL | `./install.sh` on Linux |
| 8 | keylogger | Ready | `python keylogger.py --help` |
| 9 | linux-cis-hardening-auditor | Linux only | WSL: `./install.sh && cisaudit --test` |
| 10 | linux-ebpf-security-tracer | CLI ready | `ebpf-tracer --help` (eBPF needs Linux + bcc) |
| 11 | metadata-scrubber-tool | Ready | `metadata-scrubber --help` |
| 12 | network-traffic-analyzer | Ready | `netanal --help` (Npcap for live capture) |
| 13 | simple-port-scanner | Needs Boost | Linux/WSL `./install.sh` |
| 14 | simple-vulnerability-scanner | Ready | `.\svscan.exe --help` |
| 15 | systemd-persistence-scanner | Ready | `.\sentinel.exe --help` |

### Manual setup by stack

<details>
<summary><b>Python</b></summary>

```powershell
cd <project-folder>
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .
```

Projects: `base64-tool`, `caesar-cipher`, `dns-lookup`, `keylogger`, `linux-ebpf-security-tracer`, `metadata-scrubber-tool`, `network-traffic-analyzer` (`python/`), `c2-beacon` (`backend/`).

</details>

<details>
<summary><b>Go</b></summary>

```powershell
cd <project-folder>
go build -o tool.exe ./cmd/<name>
```

- simple-vulnerability-scanner → `go build -o svscan.exe ./cmd/angela`  
- systemd-persistence-scanner → `go build -o sentinel.exe ./cmd/sentinel`  
- canary-token-generator → `go build -o canary.exe ./cmd/canary`  

</details>

<details>
<summary><b>C++ / Linux-only</b></summary>

```bash
cd <project-folder>
mkdir build && cd build
cmake .. && cmake --build .
```

- **hash-cracker**, **simple-port-scanner** — Boost + modern C++  
- **linux-cis-hardening-auditor**, **linux-ebpf-security-tracer**, **systemd-persistence-scanner** — prefer Linux/WSL  
- **firewall-rule-engine** — [V compiler](https://vlang.io)  
- **c2-beacon**, **canary-token-generator** — Docker Compose for full stacks  

</details>

---

### Legal & ethics

These tools are for **education and authorized security testing only**.  
Do **not** run offensive capabilities (keylogger, C2 beacon, scanners, crackers, etc.) against systems you do not own or lack **explicit written permission** to test.

---

<div align="center">

**Part of a broader cybersecurity practice** — studied seriously, practiced carefully, built in public.

[Author](https://github.com/WinstonMascarenhas1006)
·
[Portfolio](https://portfolio-winston-mascarenhas.vercel.app)
·
[Profile notes](https://github.com/WinstonMascarenhas1006/WinstonMascarenhas1006)

</div>
