# Caesar Cipher CLI

**Author:** [Winston Mascarenhas](https://github.com/WinstonMascarenhas1006)  
**Development period:** July 2025 (1 month)  
**Started:** 2025-07-01 · **Completed:** 2025-07-26

This is a command-line tool I wrote to practice classical cryptography. It implements the Caesar cipher — shifting each letter by a fixed number of positions — and includes a crack command that brute-forces all 26 possible keys and ranks the results using frequency analysis. It is weak encryption by design, but breaking it teaches the same statistical thinking you need for real cryptanalysis.

See [DEMO.md](DEMO.md) for screenshots.

## What it does

- Encrypt text using Caesar cipher with a specified shift key (0–25)
- Decrypt ciphertext back to plaintext when you know the key
- Brute-force crack unknown ciphertext by testing all 26 shifts
- Rank crack results with frequency analysis (chi-squared scoring)
- Display results in colored Rich tables
- Read from arguments, files, or stdin; write output to a file with `--output-file`

## Requirements

- Python 3.12 or higher
- Optional: [uv](https://github.com/astral-sh/uv) for dependency management
- Optional: [just](https://github.com/casey/just) command runner

## Installation

Install from PyPI:

```bash
uv tool install caesar-salad-cipher
```

Or install from source.

On Linux or macOS with uv:

```bash
cd caesar-cipher
uv sync
uv run caesar-cipher --help
```

On Windows with a virtual environment:

```powershell
cd caesar-cipher
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
caesar-cipher --help
```

## Usage

Encrypt with a shift key (default is 3):

```bash
caesar-cipher encrypt "HELLO WORLD" --key 3
# KHOOR ZRUOG

caesar-cipher encrypt "HELLO WORLD" -k 13
```

Decrypt with the same key:

```bash
caesar-cipher decrypt "KHOOR ZRUOG" --key 3
# HELLO WORLD
```

Crack ciphertext without knowing the key:

```bash
caesar-cipher crack "KHOOR ZRUOG"
```

The crack command tries every shift and shows a ranked table — the correct plaintext should appear near the top based on how English-like each result looks.

Read from a file or pipe:

```bash
caesar-cipher encrypt --input-file message.txt --key 5 --output-file encrypted.txt
echo "SECRET MESSAGE" | caesar-cipher encrypt -k 7
```

### Commands

| Command | Description |
|---------|-------------|
| `caesar-cipher encrypt` | Encrypt plaintext using a specified shift key |
| `caesar-cipher decrypt` | Decrypt ciphertext back to plaintext with the original key |
| `caesar-cipher crack` | Brute-force all 26 shifts with frequency analysis ranking |

## Project structure

```
caesar-cipher/
├── src/caesar_cipher/
│   ├── main.py         # CLI entry point (encrypt, decrypt, crack)
│   ├── cipher.py       # Core encryption/decryption logic
│   ├── analyzer.py     # Frequency analysis for cracking
│   └── utils.py        # Input/output helpers
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
