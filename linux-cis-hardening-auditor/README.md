<!--
  Module 09 — linux-cis-hardening-auditor
  Part of cybersecurity-projects laboratory corpus
-->

<div align="center">
  <img src="https://raw.githubusercontent.com/WinstonMascarenhas1006/cybersecurity-projects/main/assets/modules/09-linux-cis-hardening-auditor.png" alt="linux-cis-hardening-auditor laboratory module" width="100%" />
</div>

<p align="center">
  <a href="https://github.com/WinstonMascarenhas1006"><img src="https://img.shields.io/badge/Author-Winston_Mascarenhas-0f766e?style=flat-square" alt="Author" /></a>
  &nbsp;
  <img src="https://img.shields.io/badge/Module-09-334155?style=flat-square" alt="Module 09" />
  &nbsp;
  <img src="https://img.shields.io/badge/Stack-Shell-1e3a5f?style=flat-square" alt="Stack" />
  &nbsp;
  <img src="https://img.shields.io/badge/Domain-Harden-111827?style=flat-square" alt="Domain" />
  &nbsp;
  <img src="https://img.shields.io/badge/Feb_2026-0f172a?style=flat-square" alt="Period" />
</p>

<div align="center">
  <img src="https://raw.githubusercontent.com/WinstonMascarenhas1006/cybersecurity-projects/main/assets/module-ethics.png" alt="Authorized labs only" width="100%" />
</div>

<br/>

<p align="center">
  <a href="../README.md"><code>← laboratory corpus</code></a>
</p>

---

# Linux CIS Hardening Auditor

**Author:** [Winston Mascarenhas](https://github.com/WinstonMascarenhas1006)  
**Development period:** February 2026 (1 month)  
**Started:** 2026-02-01 · **Completed:** 2026-02-23

A CIS Benchmark compliance auditor for Linux systems. It checks your machine against the benchmark, scores the results, compares them to a saved baseline, and prints remediation commands for anything that fails.

See the [learn modules](#learn) for how the checks are organized and how to extend them.

## What it does

- Audits Linux systems against 104 CIS Benchmark controls (Debian/Ubuntu)
- Checks filesystem hardening, services, network parameters, logging, SSH, and user accounts
- Generates scored compliance reports in terminal, JSON, or HTML
- Compares results to a saved baseline to spot regressions and improvements
- Provides specific remediation commands for every failed control
- Supports Level 1 and Level 2 benchmark profiles
- Runs in test mode against mock fixtures without root access

## Quick start

```bash
./install.sh
sudo cisaudit
```

This project also uses [`just`](https://github.com/casey/just) as a command runner. Run `just` to see all available commands. Install with:

```bash
curl -sSf https://just.systems/install.sh | bash -s -- --to ~/.local/bin
```

## Commands

| Command | Description |
|---------|-------------|
| `sudo cisaudit` | Run full audit with terminal output |
| `sudo cisaudit -l 1` | Audit Level 1 controls only |
| `sudo cisaudit -f json -o report.json` | Generate JSON report |
| `sudo cisaudit -f html -o report.html` | Generate HTML report |
| `sudo cisaudit -c 5` | Audit only Section 5 (Access/Auth) |
| `cisaudit --list-controls` | List all 104 registered controls |
| `sudo cisaudit -s baseline.json` | Save current results as baseline |
| `sudo cisaudit -b baseline.json` | Compare against a previous baseline |
| `cisaudit -t testdata/fixtures` | Run against test fixtures (no root needed) |

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `-l, --level` | `all` | Benchmark level: `1`, `2`, or `all` |
| `-f, --format` | `terminal` | Output format: `terminal`, `json`, `html` |
| `-o, --output` | stdout | Write report to file |
| `-c, --categories` | `all` | Categories to audit: `1,2,3,4,5,6` |
| `-t, --test-root` | `/` | System root for testing |
| `--threshold` | `0` | Minimum pass % to exit 0 |
| `-q, --quiet` | off | Suppress progress output |

## CIS Benchmark sections

| # | Section | Controls |
|---|---------|----------|
| 1 | Initial Setup | 20 |
| 2 | Services | 18 |
| 3 | Network Configuration | 20 |
| 4 | Logging and Auditing | 18 |
| 5 | Access, Authentication and Authorization | 18 |
| 6 | System Maintenance | 10 |
| | **Total** | **104** |

## Examples

```bash
sudo cisaudit -l 1 -f json -o report.json

sudo cisaudit -c 3,5 -f terminal

sudo cisaudit -s baselines/march.json
sudo cisaudit -b baselines/march.json

cisaudit -t testdata/fixtures -f json | python3 -m json.tool
```

## Learn

Step-by-step learning materials covering security theory, architecture, and implementation.

| Module | Topic |
|--------|-------|
| [00 - Overview](learn/00-OVERVIEW.md) | Prerequisites and quick start |
| [01 - Concepts](learn/01-CONCEPTS.md) | CIS benchmarks, real breaches, and compliance frameworks |
| [02 - Architecture](learn/02-ARCHITECTURE.md) | System design, module layout, and data flow |
| [03 - Implementation](learn/03-IMPLEMENTATION.md) | Code walkthrough with file references |
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
