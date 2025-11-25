<!--
  Module 06 — firewall-rule-engine
  Part of cybersecurity-projects laboratory corpus
-->

<div align="center">
  <img src="https://raw.githubusercontent.com/WinstonMascarenhas1006/cybersecurity-projects/main/assets/modules/06-firewall-rule-engine.png" alt="firewall-rule-engine laboratory module" width="100%" />
</div>

<p align="center">
  <a href="https://github.com/WinstonMascarenhas1006"><img src="https://img.shields.io/badge/Author-Winston_Mascarenhas-0f766e?style=flat-square" alt="Author" /></a>
  &nbsp;
  <img src="https://img.shields.io/badge/Module-06-334155?style=flat-square" alt="Module 06" />
  &nbsp;
  <img src="https://img.shields.io/badge/Stack-V-1e3a5f?style=flat-square" alt="Stack" />
  &nbsp;
  <img src="https://img.shields.io/badge/Domain-Harden-111827?style=flat-square" alt="Domain" />
  &nbsp;
  <img src="https://img.shields.io/badge/Nov_2025-0f172a?style=flat-square" alt="Period" />
</p>

<div align="center">
  <img src="https://raw.githubusercontent.com/WinstonMascarenhas1006/cybersecurity-projects/main/assets/module-ethics.png" alt="Authorized labs only" width="100%" />
</div>

<br/>

<p align="center">
  <a href="../README.md"><code>← laboratory corpus</code></a>
</p>

---

# Firewall Rule Engine

**Author:** [Winston Mascarenhas](https://github.com/WinstonMascarenhas1006)  
**Development period:** November 2025 (1 month)  
**Started:** 2025-11-01 · **Completed:** 2025-11-25

I wrote this tool in V to help me understand firewall rules beyond just copy-pasting iptables commands from Stack Overflow. It parses iptables-save and nftables ruleset files into a unified internal model, detects conflicts like shadowed or contradictory rules, suggests optimizations, generates hardened rulesets from scratch, converts between iptables and nftables formats, and diffs two rulesets to show what changed. Output is color-coded in the terminal with severity levels so you can spot problems quickly.

## What it does

- Parse iptables-save and nftables list ruleset formats into a unified rule model
- Detect shadowed rules, contradictions, duplicates, and redundant entries
- Suggest optimizations: port merging, rule reordering, missing rate limits, missing conntrack
- Generate hardened rulesets with default-deny, anti-spoofing, ICMP rate limiting, and connection tracking
- Export rulesets between iptables and nftables formats
- Diff two rulesets to find what changed between versions
- Colored terminal output with severity-coded findings

## Requirements

- V compiler (version 0.5.x) — the install script builds it from source if you do not have it
- git and make (needed only if the install script has to compile V)
- `just` command runner (optional) — install with `curl -sSf https://just.systems/install.sh | bash -s -- --to ~/.local/bin`

The `install.sh` script handles V installation, builds the project, and copies the binary to `~/.local/bin/fwrule`.

## Installation

Run the install script from the project root:

```bash
cd firewall-rule-engine
./install.sh
```

This checks for the V compiler, installs it from source if missing, builds `fwrule` with `-prod`, and copies it to `~/.local/bin/fwrule`. Make sure `~/.local/bin` is in your PATH.

Verify the install:

```bash
fwrule version
```

You can also build manually if V is already installed:

```bash
v -prod -o bin/fwrule src/
```

Run tests with:

```bash
just test
```

## Usage

The CLI takes a subcommand as the first argument. Run `fwrule help` to see everything.

### Load and display a ruleset

Parse a file and print the rules in a table:

```bash
fwrule load testdata/iptables_basic.rules
```

Works with both iptables-save and nftables formats — the parser auto-detects which one you gave it.

### Analyze for conflicts

Run conflict detection and optimization analysis together:

```bash
fwrule analyze testdata/iptables_conflicts.rules
fwrule analyze /etc/iptables.rules
```

This flags shadowed rules (a later rule that never matches because an earlier one catches the same traffic), contradictions, duplicates, and redundant entries.

### Optimization suggestions only

If you just want the suggestions without the full conflict report:

```bash
fwrule optimize testdata/iptables_conflicts.rules
```

### Generate a hardened ruleset

Build a secure baseline from scratch with default-deny, anti-spoofing, ICMP rate limiting, and connection tracking:

```bash
fwrule harden
fwrule harden -s ssh,http,https,dns -f nftables
```

Harden options:

- `-s, --services` — comma-separated services to allow (default: `ssh,http,https`)
- `-i, --iface` — public-facing network interface (default: `eth0`)
- `-f, --format` — output format: `iptables` or `nftables` (default: `iptables`)

### Export between formats

Convert an existing ruleset to the other format:

```bash
fwrule export testdata/iptables_basic.rules -f nftables
```

### Diff two rulesets

Compare what changed between two files:

```bash
fwrule diff testdata/iptables_basic.rules testdata/nftables_basic.rules
```

The project includes test fixtures under `testdata/` for iptables and nftables in basic, complex, and conflict scenarios. Good files to experiment with before pointing the tool at your production rules.

Run `just` to see build and test commands.

## Learn modules

- [00 - Overview](learn/00-OVERVIEW.md) — prerequisites and quick start
- [01 - Concepts](learn/01-CONCEPTS.md) — firewall theory, netfilter, and real-world breaches
- [02 - Architecture](learn/02-ARCHITECTURE.md) — system design, module layout, and data flow
- [03 - Implementation](learn/03-IMPLEMENTATION.md) — code walkthrough with file references
- [04 - Challenges](learn/04-CHALLENGES.md) — extension ideas and exercises

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
