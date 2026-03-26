<!--
  Module 10 — linux-ebpf-security-tracer
  Part of cybersecurity-projects laboratory corpus
-->

<div align="center">
  <img src="https://raw.githubusercontent.com/WinstonMascarenhas1006/cybersecurity-projects/main/assets/modules/10-linux-ebpf-security-tracer.png" alt="linux-ebpf-security-tracer laboratory module" width="100%" />
</div>

<p align="center">
  <a href="https://github.com/WinstonMascarenhas1006"><img src="https://img.shields.io/badge/Author-Winston_Mascarenhas-0f766e?style=flat-square" alt="Author" /></a>
  &nbsp;
  <img src="https://img.shields.io/badge/Module-10-334155?style=flat-square" alt="Module 10" />
  &nbsp;
  <img src="https://img.shields.io/badge/Stack-eBPF-1e3a5f?style=flat-square" alt="Stack" />
  &nbsp;
  <img src="https://img.shields.io/badge/Domain-Detect-111827?style=flat-square" alt="Domain" />
  &nbsp;
  <img src="https://img.shields.io/badge/Mar_2026-0f172a?style=flat-square" alt="Period" />
</p>

<div align="center">
  <img src="https://raw.githubusercontent.com/WinstonMascarenhas1006/cybersecurity-projects/main/assets/module-ethics.png" alt="Authorized labs only" width="100%" />
</div>

<br/>

<p align="center">
  <a href="../README.md"><code>← laboratory corpus</code></a>
</p>

---

# Linux eBPF Security Tracer

**Author:** [Winston Mascarenhas](https://github.com/WinstonMascarenhas1006)  
**Development period:** March 2026 (1 month)  
**Started:** 2026-03-01 · **Completed:** 2026-03-26

A real-time syscall tracing tool built on eBPF for security observability. It watches process execution, file access, network connections, privilege changes, and other system operations, then flags suspicious behavior against a set of built-in detection rules.

More background, architecture notes, and a code walkthrough are in the [learn modules](#learn).

## What it does

- Monitors syscalls in real time via eBPF tracepoints (process, file, network, privilege, system)
- Ships with 10 detection rules mapped to MITRE ATT&CK techniques
- Correlates events across steps to catch multi-stage attacks (reverse shells, privilege escalation chains)
- Outputs a live color-coded stream, JSON, or a table summary
- Filters by severity: LOW, MEDIUM, HIGH, CRITICAL
- Enriches events from `/proc` (parent process, username)
- Handles signals cleanly and tears down eBPF programs on exit

## Quick start

```bash
./install.sh
sudo uv run ebpf-tracer
```

This project also uses [`just`](https://github.com/casey/just) as a command runner. Run `just` to see all available commands. Install with:

```bash
curl -sSf https://just.systems/install.sh | bash -s -- --to ~/.local/bin
```

## Usage

```bash
sudo uv run ebpf-tracer                       # trace all syscalls (live mode)
sudo uv run ebpf-tracer -f json -s MEDIUM      # JSON output, MEDIUM+ severity
sudo uv run ebpf-tracer -t network             # only network events
sudo uv run ebpf-tracer --detections           # only show detection alerts
sudo uv run ebpf-tracer -c nginx               # filter by process name
sudo uv run ebpf-tracer -o events.jsonl        # write events to file while streaming
```

## Detection rules

| ID | Name | Severity | MITRE ATT&CK | Trigger |
|----|------|----------|--------------|---------|
| D001 | Privilege Escalation | CRITICAL | T1548 | setuid(0) by non-root |
| D002 | Sensitive File Read | MEDIUM | T1003.008 | /etc/shadow access by non-root |
| D003 | SSH Key Access | MEDIUM | T1552.004 | SSH key file access |
| D004 | Process Injection | MEDIUM | T1055.008 | ptrace ATTACH/SEIZE |
| D005 | Kernel Module Load | HIGH | T1547.006 | init_module syscall |
| D006 | Reverse Shell | CRITICAL | T1059.004 | connect + shell execve sequence |
| D007 | Persistence via Cron | MEDIUM | T1053.003 | Write to cron directories |
| D008 | Persistence via Systemd | MEDIUM | T1543.002 | Write to systemd unit dirs |
| D009 | Log Tampering | MEDIUM | T1070.002 | Log file deletion/truncation |
| D010 | Suspicious Mount | HIGH | T1611 | mount syscall |

## Learn

Step-by-step learning materials covering security theory, architecture, and implementation.

| Module | Topic |
|--------|-------|
| [00 - Overview](learn/00-OVERVIEW.md) | Prerequisites and quick start |
| [01 - Concepts](learn/01-CONCEPTS.md) | eBPF theory and security observability |
| [02 - Architecture](learn/02-ARCHITECTURE.md) | System design and data flow |
| [03 - Implementation](learn/03-IMPLEMENTATION.md) | Code walkthrough |
| [04 - Challenges](learn/04-CHALLENGES.md) | Extension ideas and exercises |

---

### Legal & ethics

These tools are for **education and authorized security testing only**.  
Do **not** run offensive capabilities against systems you do not own or lack **explicit written permission** to test.

---

<div align="center">

**Module in the lab corpus** — [cybersecurity-projects](https://github.com/WinstonMascarenhas1006/cybersecurity-projects)  
[Author](https://github.com/WinstonMascarenhas1006) · [Portfolio](https://portfolio-winston-mascarenhas.vercel.app) · [Profile](https://github.com/WinstonMascarenhas1006/WinstonMascarenhas1006)

</div>


## License

AGPL 3.0
