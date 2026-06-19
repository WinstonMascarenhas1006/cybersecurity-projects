<!--
  Module 15 — systemd-persistence-scanner
  Part of cybersecurity-projects laboratory corpus
-->

<div align="center">
  <img src="https://raw.githubusercontent.com/WinstonMascarenhas1006/cybersecurity-projects/main/assets/modules/15-systemd-persistence-scanner.png" alt="systemd-persistence-scanner laboratory module" width="100%" />
</div>

<p align="center">
  <a href="https://github.com/WinstonMascarenhas1006"><img src="https://img.shields.io/badge/Author-Winston_Mascarenhas-0f766e?style=flat-square" alt="Author" /></a>
  &nbsp;
  <img src="https://img.shields.io/badge/Module-15-334155?style=flat-square" alt="Module 15" />
  &nbsp;
  <img src="https://img.shields.io/badge/Stack-Go-1e3a5f?style=flat-square" alt="Stack" />
  &nbsp;
  <img src="https://img.shields.io/badge/Domain-Harden-111827?style=flat-square" alt="Domain" />
  &nbsp;
  <img src="https://img.shields.io/badge/Jun_2026-0f172a?style=flat-square" alt="Period" />
</p>

<div align="center">
  <img src="https://raw.githubusercontent.com/WinstonMascarenhas1006/cybersecurity-projects/main/assets/module-ethics.png" alt="Authorized labs only" width="100%" />
</div>

<br/>

<p align="center">
  <a href="../README.md"><code>← laboratory corpus</code></a>
</p>

---

# Systemd Persistence Scanner

**Author:** [Winston Mascarenhas](https://github.com/WinstonMascarenhas1006)  
**Development period:** June 2026 (1 month)  
**Started:** 2026-06-11 · **Completed:** 2026-06-19

Go CLI tool that scans a Linux filesystem for common persistence mechanisms — systemd units, cron jobs, shell profile injections, SSH backdoors, LD_PRELOAD hooks, and more. Each finding includes a severity rating and a MITRE ATT&CK technique reference.

See the [learn modules](#learn) for how each scanner module works.

Screenshots and example output: [DEMO.md](DEMO.md)

## What it does

- Runs 17 scanner modules across persistence categories on a Linux root filesystem
- Heuristic detection for reverse shells, download-and-execute chains, encoded payloads, alias hijacking, and temp-directory abuse
- Severity levels from info through critical, with MITRE ATT&CK mapping on each finding
- Baseline mode: save a clean snapshot, then diff later to show only new findings
- Single static binary with no runtime dependencies
- JSON output for pipeline integration

## Requirements

- Go 1.25 or newer
- A Linux system (or mounted Linux root) to scan — the binary builds on Windows but scanning targets Linux paths

## Build (local copy)

From the project folder:

```powershell
go build -o sentinel.exe ./cmd/sentinel
```

On Linux or macOS:

```bash
go build -o sentinel ./cmd/sentinel
```

Upstream install:

```bash
go install sentinel/cmd/sentinel@latest
```

## Commands

| Command | Description |
|---------|-------------|
| `sentinel scan` | Run all persistence scanners against the local filesystem |
| `sentinel scan --json` | Output findings as JSON |
| `sentinel scan --min-severity high` | Show only high and critical findings |
| `sentinel scan --root /mnt/target` | Scan a mounted filesystem or chroot |
| `sentinel baseline save` | Save current findings as a baseline snapshot |
| `sentinel baseline diff` | Show findings that are new since the baseline |

## Example output

```
  [CRITICAL] Library in ld.so.preload
         Path: /etc/ld.so.preload
         Evidence: /dev/shm/.evil.so
         MITRE: T1574.006

  [HIGH] Suspicious cron entry: download-and-execute chain
         Path: /etc/cron.d/updater
         Evidence: */5 * * * * root curl http://... | bash
         MITRE: T1053.003

  [MEDIUM] Recently modified unit file
         Path: /etc/systemd/system/backdoor.service
         Evidence: Modified within the last 24 hours
         MITRE: T1543.002

  Summary: 1 critical 1 high 1 medium 0 low 4 info
```

## Scanner modules

| Scanner | MITRE | What it checks |
|---------|-------|----------------|
| systemd | T1543.002, T1053.006 | Service and timer units, ExecStart, drop-in overrides |
| cron | T1053.003 | System and user crontabs, cron.d, periodic dirs, anacron |
| profile | T1546.004 | Shell RC files, /etc/profile.d, bashrc/zshrc injections |
| ssh | T1098.004 | authorized_keys options, sshd_config, SSH rc scripts |
| sshrc | T1546.004 | /etc/ssh/sshrc and related login hooks |
| ld_preload | T1574.006 | /etc/ld.so.preload, ld.so.conf.d, /etc/environment |
| kernel | T1547.006 | modules-load.d, modprobe.d install hooks |
| udev | T1546 | Udev rules with RUN+= directives |
| initd | T1037.004 | Init.d scripts, rc.local |
| xdg | T1547.013 | XDG autostart .desktop files |
| atjob | T1053.001 | Pending at job spool |
| motd | T1546 | update-motd.d login scripts |
| pam | T1556.003 | PAM configs, pam_exec.so, pam_permit.so in auth |
| logrotate | T1037 | postrotate/prerotate script hooks |
| netifhook | T1546 | Network interface up/down scripts |
| generator | T1543.002 | systemd generator drop-ins |
| completion | T1546.004 | Shell completion script injections |

## Testing against sample data

The repo includes suspicious and clean fixtures under `testdata/`. Point `--root` at that tree on Linux or WSL:

```bash
sentinel scan --root ./testdata
```

## Learn

| Module | Topic |
|--------|-------|
| [00 - Overview](learn/00-OVERVIEW.md) | Prerequisites and quick start |
| [01 - Concepts](learn/01-CONCEPTS.md) | Linux persistence and MITRE ATT&CK |
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
