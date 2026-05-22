<!--
  Module 12 — network-traffic-analyzer
  Part of cybersecurity-projects laboratory corpus
-->

<div align="center">
  <img src="https://raw.githubusercontent.com/WinstonMascarenhas1006/cybersecurity-projects/main/assets/modules/12-network-traffic-analyzer.png" alt="network-traffic-analyzer laboratory module" width="100%" />
</div>

<p align="center">
  <a href="https://github.com/WinstonMascarenhas1006"><img src="https://img.shields.io/badge/Author-Winston_Mascarenhas-0f766e?style=flat-square" alt="Author" /></a>
  &nbsp;
  <img src="https://img.shields.io/badge/Module-12-334155?style=flat-square" alt="Module 12" />
  &nbsp;
  <img src="https://img.shields.io/badge/Stack-Python-1e3a5f?style=flat-square" alt="Stack" />
  &nbsp;
  <img src="https://img.shields.io/badge/Domain-Analyze-111827?style=flat-square" alt="Domain" />
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

# Network Traffic Analyzer

**Author:** [Winston Mascarenhas](https://github.com/WinstonMascarenhas1006)  
**Development period:** May 2026 (1 month)  
**Started:** 2026-05-01 · **Completed:** 2026-05-12

Two implementations of the same network traffic analyzer — one in Python, one in C++. Both capture packets at the kernel level, parse protocol headers, and display real-time statistics.

Screenshots and a usage demo are in [DEMO.md](DEMO.md).

## Implementations

| Implementation | Stack | Highlights |
|---|---|---|
| [C++](./cpp) | C++20, libpcap, FTXUI | Interactive TUI, polymorphic IP parser, mutex-protected stats engine |
| [Python](./python) | Python 3.14, Scapy, Rich | Producer-consumer threading, BPF filter builder, Matplotlib chart export |

## Quick start

**C++ — high-performance interactive TUI:**

```bash
cd cpp
./install.sh
just run -i eth0
```

**Python — scriptable with chart export:**

```bash
cd python
uv sync
sudo netanal capture -i eth0
```

Both require root or the `CAP_NET_RAW` capability for packet capture.

---

### Legal & ethics

These tools are for **education and authorized security testing only**.  
Do **not** run offensive capabilities against systems you do not own or lack **explicit written permission** to test.

---

<div align="center">

**Module in the lab corpus** — [cybersecurity-projects](https://github.com/WinstonMascarenhas1006/cybersecurity-projects)  
[Author](https://github.com/WinstonMascarenhas1006) · [Portfolio](https://portfolio-winston-mascarenhas.vercel.app) · [Profile](https://github.com/WinstonMascarenhas1006/WinstonMascarenhas1006)

</div>

