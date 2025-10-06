# DNS Lookup CLI

**Author:** [Winston Mascarenhas](https://github.com/WinstonMascarenhas1006)  
**Development period:** October 2025 (1 month)  
**Started:** 2025-10-01 · **Completed:** 2025-10-26

I made this tool to learn how DNS actually works beyond typing `nslookup` once in a networking class. It queries DNS records, does reverse lookups, traces resolution paths from root servers down to authoritative nameservers, runs batch lookups concurrently, and pulls WHOIS data — all with readable Rich table output or JSON for scripting.

See [DEMO.md](DEMO.md) for screenshots.

## What it does

- Query A, AAAA, MX, NS, TXT, CNAME, and SOA records with colored table output
- Reverse DNS lookup to resolve IP addresses back to hostnames
- Trace DNS resolution path from root servers to authoritative nameservers
- Batch lookups with concurrent queries for processing domain lists from a file
- WHOIS integration for domain registration information
- JSON export with `--json` for pipeline integration
- Custom DNS server selection and configurable timeouts
- No caching — every query is fresh

## Requirements

- Python 3.12 or higher
- Network access for live DNS queries
- Optional: [uv](https://github.com/astral-sh/uv) for dependency management
- Optional: [just](https://github.com/casey/just) command runner

Dependencies: dnspython, rich, typer, python-whois

## Installation

Install from PyPI:

```bash
uv tool install dnslookup-cli
```

Or install from source.

On Linux or macOS with uv:

```bash
cd dns-lookup
uv sync
uv run dnslookup --help
```

On Windows with a virtual environment:

```powershell
cd dns-lookup
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
dnslookup --help
```

## Usage

Query all record types for a domain:

```bash
dnslookup query example.com
```

Query specific record types with a custom DNS server:

```bash
dnslookup query example.com --type A,MX
dnslookup query example.com --type A,MX --server 8.8.8.8
dnslookup query example.com --timeout 10
```

Output as JSON for scripting:

```bash
dnslookup query example.com --json
```

Reverse lookup — resolve an IP to a hostname:

```bash
dnslookup reverse 8.8.8.8
```

Trace the full resolution path:

```bash
dnslookup trace example.com
```

Batch lookup from a file:

```bash
echo "example.com" > domains.txt
echo "example.org" >> domains.txt
dnslookup batch domains.txt --output results.json
```

WHOIS registration info:

```bash
dnslookup whois example.com
dnslookup whois example.com --json
```

### Commands

| Command | Description |
|---------|-------------|
| `dnslookup query` | Query DNS records for a domain with colored table output |
| `dnslookup reverse` | Resolve an IP address back to its hostname |
| `dnslookup trace` | Trace the DNS resolution path from root to authoritative servers |
| `dnslookup batch` | Query multiple domains concurrently from a file |
| `dnslookup whois` | Retrieve WHOIS registration information for a domain |

## Project structure

```
dns-lookup/
├── dnslookup/
│   ├── cli.py            # Typer command interface
│   ├── resolver.py       # Core DNS logic (async queries, trace, batch)
│   ├── output.py         # Rich table formatting and JSON export
│   └── whois_lookup.py   # WHOIS operations
├── tests/
├── learn/
└── pyproject.toml
```

## Learn modules

- [00 - Overview](learn/00-OVERVIEW.md) — prerequisites and quick start
- [01 - Concepts](learn/01-CONCEPTS.md) — security theory and real-world breaches
- [02 - Architecture](learn/02-ARCHITECTURE.md) — system design and data flow
- [03 - Implementation](learn/03-IMPLEMENTATION.md) — code walkthrough
- [04 - Challenges](learn/04-CHALLENGES.md) — extension ideas and exercises

## License

AGPL 3.0
