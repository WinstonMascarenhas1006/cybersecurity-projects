# Network Traffic Analyzer (C++)

**Author:** [Winston Mascarenhas](https://github.com/WinstonMascarenhas1006)  
**Development period:** May 2026 (1 month)  
**Started:** 2026-05-01 · **Completed:** 2026-05-12

A high-performance CLI network analyzer built with libpcap for raw packet capture and FTXUI for a fully interactive terminal UI. It captures packets directly from a network interface, parses protocol headers manually, and aggregates statistics in real time.

## Privileges

Packet capture requires elevated privileges. Run with:

```bash
sudo ./network-traffic-analyzer
```

Or grant capabilities:

```bash
sudo setcap cap_net_raw,cap_net_admin=eip ./network-traffic-analyzer
```

You can also use the `just` command runner:

```bash
just run
```

## Preview

![Preview](example.png)

## Features

### Live packet capture

- Capture traffic from a selected network interface
- Support for BPF filters (e.g. `tcp`, `port 80`, `udp`)
- Real-time processing using libpcap

### Real-time statistics engine

- Total packets and traffic volume
- Transport protocol distribution (TCP / UDP / ICMP)
- Application-level classification (port-based)
- Top IP addresses
- Top source-to-destination pairs

### Flexible capture modes

- Live capture from a selected network interface (`-i`, `--interface`)
- Offline analysis from a `.pcap` file (`-r`, `--offline`)
- Packet count limit (`-c`)
- Time limit for capture (`-t`)
- Interface discovery (`--interfaces`)

For the full list of CLI options, run `--help`.

## Technologies

- C++20+
- Boost::program_options
- libpcap
- FTXUI
- CMake

## Setup

```bash
cd network-traffic-analyzer
./install.sh
```

## Usage examples

Live capture on eth0:

```bash
just capture -i eth0
```

Capture 100 packets:

```bash
just run -i wlan0 -c 100
```

Analyze an offline pcap file:

```bash
just run --offline traffic.pcap
```

Export results (JSON / CSV):

```bash
just run --json result.json --csv result.csv
```

## Learn more

| Doc | Contents |
|-----|----------|
| [00-OVERVIEW.md](./learn/00-OVERVIEW.md) | Quick start, prerequisites, project structure |
| [01-CONCEPTS.md](./learn/01-CONCEPTS.md) | libpcap internals, BPF filters, protocol header parsing |
| [02-ARCHITECTURE.md](./learn/02-ARCHITECTURE.md) | System design, component breakdown, data flow, threading model |
| [03-IMPLEMENTATION.md](./learn/03-IMPLEMENTATION.md) | Line-by-line code walkthrough |
| [04-CHALLENGES.md](./learn/04-CHALLENGES.md) | Extension ideas and advanced topics |
