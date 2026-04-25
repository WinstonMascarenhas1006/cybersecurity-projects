<!--
  Module 11 — metadata-scrubber-tool
  Part of cybersecurity-projects laboratory corpus
-->

<div align="center">
  <img src="https://raw.githubusercontent.com/WinstonMascarenhas1006/cybersecurity-projects/main/assets/modules/11-metadata-scrubber-tool.png" alt="metadata-scrubber-tool laboratory module" width="100%" />
</div>

<p align="center">
  <a href="https://github.com/WinstonMascarenhas1006"><img src="https://img.shields.io/badge/Author-Winston_Mascarenhas-0f766e?style=flat-square" alt="Author" /></a>
  &nbsp;
  <img src="https://img.shields.io/badge/Module-11-334155?style=flat-square" alt="Module 11" />
  &nbsp;
  <img src="https://img.shields.io/badge/Stack-Python-1e3a5f?style=flat-square" alt="Stack" />
  &nbsp;
  <img src="https://img.shields.io/badge/Domain-Harden-111827?style=flat-square" alt="Domain" />
  &nbsp;
  <img src="https://img.shields.io/badge/Apr_2026-0f172a?style=flat-square" alt="Period" />
</p>

<div align="center">
  <img src="https://raw.githubusercontent.com/WinstonMascarenhas1006/cybersecurity-projects/main/assets/module-ethics.png" alt="Authorized labs only" width="100%" />
</div>

<br/>

<p align="center">
  <a href="../README.md"><code>← laboratory corpus</code></a>
</p>

---

# Metadata Scrubber Tool

**Author:** [Winston Mascarenhas](https://github.com/WinstonMascarenhas1006)  
**Development period:** April 2026 (1 month)  
**Started:** 2026-04-01 · **Completed:** 2026-04-25

A privacy-focused CLI that strips sensitive metadata from images, PDFs, and Office documents. I built this to remove GPS coordinates, author names, timestamps, camera data, and other traces before sharing files.

Screenshots and usage examples are in [DEMO.md](DEMO.md). Deeper write-ups are in the [learn modules](#learn).

## What it does

- Strips metadata from JPEG, PNG, PDF, Word, Excel, and PowerPoint files
- Processes files concurrently with ThreadPoolExecutor — handles 1000+ files efficiently
- Dry-run mode previews what would be removed before making changes
- Verification reports show a before/after comparison of metadata fields
- Detects format by file signature, not extension
- Removes GPS coordinates, author info, timestamps, camera data, and software traces

## Quick start

```bash
uv tool install metadata-scrubber
mst scrub photo.jpg
```

This project also uses [`just`](https://github.com/casey/just) as a command runner. Run `just` to see all available commands. Install with:

```bash
curl -sSf https://just.systems/install.sh | bash -s -- --to ~/.local/bin
```

## Commands

| Command | Description |
|---------|-------------|
| `mst read <file>` | Inspect metadata fields present in a file |
| `mst scrub <file>` | Remove all metadata from a file |
| `mst verify <file>` | Confirm metadata was successfully removed |

## Learn

Step-by-step learning materials covering security theory, architecture, and implementation.

| Module | Topic |
|--------|-------|
| [00 - Overview](learn/00-OVERVIEW.md) | Prerequisites and quick start |
| [01 - Concepts](learn/01-CONCEPTS.md) | Security theory and real-world breaches |
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
