# Network Traffic Analyzer (Python)

**Author:** [Winston Mascarenhas](https://github.com/WinstonMascarenhas1006)  
**Development period:** May 2026 (1 month)  
**Started:** 2026-05-01 · **Completed:** 2026-05-12

A network traffic capture and analysis CLI with protocol distribution, top talkers, and bandwidth visualization. Built on Scapy for deep packet inspection.

See [DEMO.md](../DEMO.md) for screenshots and the [learn modules](learn/) for architecture and implementation notes.

## What it does

- Captures live network traffic on any interface with a configurable packet count
- Shows real-time protocol distribution with percentage breakdowns
- Identifies top talkers — the most active IP addresses by traffic volume
- Calculates bandwidth with bytes sent and received per endpoint
- Verbose mode logs individual packet flows with source and destination details
- Uses Scapy for deep packet inspection and protocol parsing

## Quick start

```bash
uv tool install netanal
sudo netanal capture -i eth0 -c 100
```

This project also uses [`just`](https://github.com/casey/just) as a command runner. Run `just` to see all available commands. Install with:

```bash
curl -sSf https://just.systems/install.sh | bash -s -- --to ~/.local/bin
```

## Commands

| Command | Description |
|---------|-------------|
| `netanal capture` | Live packet capture with protocol analysis, top talkers, and bandwidth stats |

## Learn

Step-by-step learning materials covering security theory, architecture, and implementation.

| Module | Topic |
|--------|-------|
| [00 - Overview](learn/00-OVERVIEW.md) | Prerequisites and quick start |
| [01 - Concepts](learn/01-CONCEPTS.md) | Security theory and real-world breaches |
| [02 - Architecture](learn/02-ARCHITECTURE.md) | System design and data flow |
| [03 - Implementation](learn/03-IMPLEMENTATION.md) | Code walkthrough |
| [04 - Challenges](learn/04-CHALLENGES.md) | Extension ideas and exercises |

## License

AGPL 3.0
