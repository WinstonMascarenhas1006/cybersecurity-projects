<!--
  Module 13 — simple-port-scanner
  Part of cybersecurity-projects laboratory corpus
-->

<div align="center">
  <img src="https://raw.githubusercontent.com/WinstonMascarenhas1006/cybersecurity-projects/main/assets/modules/13-simple-port-scanner.png" alt="simple-port-scanner laboratory module" width="100%" />
</div>

<p align="center">
  <a href="https://github.com/WinstonMascarenhas1006"><img src="https://img.shields.io/badge/Author-Winston_Mascarenhas-0f766e?style=flat-square" alt="Author" /></a>
  &nbsp;
  <img src="https://img.shields.io/badge/Module-13-334155?style=flat-square" alt="Module 13" />
  &nbsp;
  <img src="https://img.shields.io/badge/Stack-C++-1e3a5f?style=flat-square" alt="Stack" />
  &nbsp;
  <img src="https://img.shields.io/badge/Domain-Recon-111827?style=flat-square" alt="Domain" />
  &nbsp;
  <img src="https://img.shields.io/badge/May_2026-0f172a?style=flat-square" alt="Period" />
</p>

<div align="center">
  <img src="https://raw.githubusercontent.com/WinstonMascarenhas1006/cybersecurity-projects/main/assets/module-ethics.png" alt="Authorized labs only" width="100%" />
</div>

<br/>

<p align="center">
  <a href="../README.md"><code>← laboratory corpus</code></a>
</p>

---

# Simple Port Scanner

**Author:** [Winston Mascarenhas](https://github.com/WinstonMascarenhas1006)  
**Development period:** May 2026 (1 month)  
**Started:** 2026-05-13 · **Completed:** 2026-05-22

Asynchronous TCP port scanner written in C++20 with Boost.Asio. It probes a target host for open, closed, and filtered ports, runs many connection attempts in parallel, and tries to grab service banners on open ports.

See the [learn modules](#learn) for background on how port scanning works.

Screenshots and example output: [DEMO.md](DEMO.md)

## What it does

- TCP connect scans with configurable port ranges (single port, comma list, or range like `1-1024`)
- Adjustable concurrency via thread count
- Configurable connection timeout in seconds
- Basic service name mapping for common ports (SSH, HTTP, HTTPS, and others)
- Banner grabbing on open ports when verbose mode is enabled
- Terminal output showing port state and any banner text

## Requirements

- C++20 compiler (GCC, Clang, or MSVC)
- Boost (program_options component)
- CMake 3.31 or newer

On Windows, Boost is not installed by default. This project is easiest to build on Linux or WSL.

## Build

```bash
mkdir build && cd build
cmake ..
cmake --build .
```

The binary is named `simplePortScanner` (or `simplePortScanner.exe` on Windows).

## Usage

```bash
./simplePortScanner -i 127.0.0.1 -p 1-1024
./simplePortScanner -i 192.168.1.1 -p 22,80,443 -t 200
./simplePortScanner -i scanme.nmap.org -p 1-65535 -e 5 -v
```

| Flag | Long | Default | Description |
|------|------|---------|-------------|
| `-i` | `--dname` | `127.0.0.1` | Target IP address or hostname |
| `-p` | `--ports` | `1-1024` | Port or port range |
| `-t` | `--threads` | `100` | Max concurrent connections |
| `-e` | `--expiry_time` | `2` | Timeout in seconds |
| `-v` | `--verbose` | off | Verbose output with banners |
| `-h` | `--help` | | Show help |

Only scan systems you own or have written permission to test.

## Learn

Step-by-step material covering security theory, architecture, and code walkthroughs:

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
