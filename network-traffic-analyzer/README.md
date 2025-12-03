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
