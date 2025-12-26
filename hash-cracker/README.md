<!--
  Module 07 — hash-cracker
  Part of cybersecurity-projects laboratory corpus
-->

<div align="center">
  <img src="https://raw.githubusercontent.com/WinstonMascarenhas1006/cybersecurity-projects/main/assets/modules/07-hash-cracker.png" alt="hash-cracker laboratory module" width="100%" />
</div>

<p align="center">
  <a href="https://github.com/WinstonMascarenhas1006"><img src="https://img.shields.io/badge/Author-Winston_Mascarenhas-0f766e?style=flat-square" alt="Author" /></a>
  &nbsp;
  <img src="https://img.shields.io/badge/Module-07-334155?style=flat-square" alt="Module 07" />
  &nbsp;
  <img src="https://img.shields.io/badge/Stack-C++-1e3a5f?style=flat-square" alt="Stack" />
  &nbsp;
  <img src="https://img.shields.io/badge/Domain-Analyze-111827?style=flat-square" alt="Domain" />
  &nbsp;
  <img src="https://img.shields.io/badge/Dec_2025-0f172a?style=flat-square" alt="Period" />
</p>

<div align="center">
  <img src="https://raw.githubusercontent.com/WinstonMascarenhas1006/cybersecurity-projects/main/assets/module-ethics.png" alt="Authorized labs only" width="100%" />
</div>

<br/>

<p align="center">
  <a href="../README.md"><code>← laboratory corpus</code></a>
</p>

---

# Hash Cracker

**Author:** [Winston Mascarenhas](https://github.com/WinstonMascarenhas1006)  
**Development period:** December 2025 (1 month)  
**Started:** 2025-12-01 · **Completed:** 2025-12-26

This is a multi-threaded hash cracking tool I wrote in C++23 to learn how password hashes get broken in the real world. You give it a hash and it tries to recover the plaintext using a dictionary attack, brute-force search, or rule-based mutations. It supports MD5, SHA1, SHA256, and SHA512 with automatic hash type detection based on digest length. The learn modules at the bottom go deeper into the security theory and how the code is structured.

## What it does

- Cracks MD5, SHA1, SHA256, and SHA512 hashes with auto-detection from hash length
- Dictionary attacks using memory-mapped wordlists for zero-copy handling of large files
- Brute-force attacks with configurable character sets and keyspace partitioning across all CPU cores
- Rule-based mutations: capitalize, leet speak, digit append, reverse, toggle case (and chained combinations with `--chain-rules`)
- Multi-threaded with zero-contention work partitioning
- Salt support with prepend or append positioning
- Rich terminal progress display showing speed in hashes per second, ETA, and a progress bar
- Optional JSON output to a file for scripting

## Requirements

- C++23 compiler (g++ or clang++)
- CMake 3.31 or newer
- Ninja build system
- OpenSSL development libraries (`libssl-dev` on Debian/Ubuntu)
- Boost Program Options (`libboost-program-options-dev` on Debian/Ubuntu)
- `just` command runner (optional but recommended) — install with `curl -sSf https://just.systems/install.sh | bash -s -- --to ~/.local/bin`

The `install.sh` script detects apt, dnf, pacman, or brew and installs the right packages for your system.

## Installation

Run the install script from the project root. It installs dependencies, builds a release binary with CMake, and symlinks it to `~/.local/bin/hashcracker`.

```bash
cd hash-cracker
./install.sh
```

Make sure `~/.local/bin` is in your PATH. After installation, verify it works:

```bash
hashcracker --help
```

You can also build manually:

```bash
cmake --preset release
cmake --build build/release
```

## Usage

The basic pattern is `hashcracker --hash <hash> [attack mode flags]`.

### Dictionary attack

Point it at a wordlist file. Hash type is auto-detected unless you override it with `--type`.

```bash
hashcracker --hash 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8 \
  --wordlist wordlists/10k-most-common.txt
```

Expected output when it finds a match:

```
✔ CRACKED: password
```

### Demo hashes

These all crack instantly against the included `wordlists/10k-most-common.txt`:

| Hash | Type | Plaintext |
|------|------|-----------|
| `5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8` | SHA256 | password |
| `8621ffdbc5698829397d97767ac13db3` | MD5 | dragon |
| `ed9d3d832af899035363a69fd53cd3be8f71501c` | SHA1 | shadow |

Try them:

```bash
hashcracker --hash 8621ffdbc5698829397d97767ac13db3 --wordlist wordlists/10k-most-common.txt
hashcracker --hash ed9d3d832af899035363a69fd53cd3be8f71501c --wordlist wordlists/10k-most-common.txt --rules
hashcracker --hash 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8 --bruteforce --charset lower --max-length 8
```

### Rule-based attack

Apply mutation rules to every word in the dictionary. This expands a 10K wordlist into millions of candidates.

```bash
hashcracker --hash ed9d3d832af899035363a69fd53cd3be8f71501c \
  --wordlist wordlists/10k-most-common.txt --rules
```

Add `--chain-rules` to combine mutations in sequence.

### Brute-force attack

Exhaustively try every combination from a character set up to a max length.

```bash
hashcracker --hash 5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8 \
  --bruteforce --charset lower,digits --max-length 8
```

Character set tokens: `lower`, `upper`, `digits`, `special`. Default is `lower,digits`.

### Other flags

```bash
hashcracker --hash <hash> --type sha256          # force hash type instead of auto-detect
hashcracker --hash <hash> --wordlist list.txt --salt "pepper" --salt-position append
hashcracker --hash <hash> --wordlist list.txt --threads 0   # 0 = auto (all cores)
hashcracker --hash <hash> --wordlist list.txt --output result.json
```

See [DEMO.md](DEMO.md) for screenshots of the dictionary and rule-based attacks in action.

Run `just` to see build, test, and lint commands.

## Learn modules

- [00 - Overview](learn/00-OVERVIEW.md) — prerequisites and quick start
- [01 - Concepts](learn/01-CONCEPTS.md) — security theory and real-world breaches
- [02 - Architecture](learn/02-ARCHITECTURE.md) — system design and data flow
- [03 - Implementation](learn/03-IMPLEMENTATION.md) — code walkthrough
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
