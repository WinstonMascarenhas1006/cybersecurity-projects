# b64tool

**Author:** [Winston Mascarenhas](https://github.com/WinstonMascarenhas1006)  
**Development period:** April 2025 (1 month)  
**Started:** 2025-04-01 · **Completed:** 2025-04-28

I built this CLI because I kept running into encoded data during security labs and CTFs — JWT tokens, hex dumps, URL-encoded payloads — and I wanted one tool that could handle all of it instead of jumping between online decoders. The standout feature is recursive layer peeling, which strips stacked encodings the same way attackers use them to hide malware or bypass WAFs.

See [DEMO.md](DEMO.md) for screenshots of the tool in action.

## What it does

- Encode and decode Base64, Base64URL, Base32, Hex, and URL formats
- Auto-detect encoding format with confidence scoring
- Peel command recursively strips multi-layered encoding (useful for WAF bypass analysis)
- Chain multiple encoding steps to test obfuscation patterns
- Read input from arguments, files, or stdin — works well in pipelines

## Requirements

- Python 3.12 or higher
- Optional: [uv](https://github.com/astral-sh/uv) for dependency management
- Optional: [just](https://github.com/casey/just) command runner (type `just` to see available commands)

## Installation

Install from PyPI:

```bash
uv tool install b64tool
```

Or clone the repo and install locally.

On Linux or macOS with uv:

```bash
cd base64-tool
uv sync
uv run b64tool --help
```

On Windows with a virtual environment:

```powershell
cd base64-tool
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
b64tool --help
```

For development dependencies:

```bash
uv sync --all-extras
```

## Usage

Basic encode and decode:

```bash
b64tool encode "Hello World"
# SGVsbG8gV29ybGQ=

b64tool decode "SGVsbG8gV29ybGQ="
# Hello World
```

Pick a format with `--format` (or `-f`). Options: `base64`, `base64url`, `base32`, `hex`, `url`.

```bash
b64tool encode "Hello World" --format hex
b64tool decode "48656c6c6f20576f726c64" --format hex
```

Auto-detect the encoding:

```bash
b64tool detect "SGVsbG8gV29ybGQ="
```

Peel stacked layers until you reach the original data:

```bash
b64tool chain "alert('xss')" --steps base64,hex
b64tool peel "5957786c636e516f4a33687a63796370"
```

Read from a file or pipe:

```bash
b64tool decode --file encoded_payload.txt
echo "SGVsbG8=" | b64tool decode
cat encoded_payload.txt | b64tool peel
```

### Commands

| Command | Description |
|---------|-------------|
| `b64tool encode` | Encode text into Base64, Base64URL, Base32, Hex, or URL format |
| `b64tool decode` | Decode encoded text back to plaintext |
| `b64tool detect` | Auto-detect the encoding format with confidence scoring |
| `b64tool peel` | Recursively strip multi-layered encoding to reveal original data |
| `b64tool chain` | Chain multiple encoding steps together for obfuscation testing |

## Project structure

```
base64-tool/
├── src/base64_tool/
│   ├── cli.py          # Typer commands (encode, decode, detect, peel, chain)
│   ├── constants.py    # Enums, thresholds, character sets
│   ├── encoders.py     # Pure encode/decode functions + registry
│   ├── detector.py     # Format detection with confidence scoring
│   ├── peeler.py       # Recursive multi-layer decoding
│   ├── formatter.py    # Rich terminal output
│   └── utils.py        # Input resolution, text helpers
├── tests/
├── learn/              # Step-by-step learning materials
├── pyproject.toml
└── Justfile
```

## Learn modules

- [00 - Overview](learn/00-OVERVIEW.md) — prerequisites and quick start
- [01 - Concepts](learn/01-CONCEPTS.md) — security theory and real-world breaches
- [02 - Architecture](learn/02-ARCHITECTURE.md) — system design and data flow
- [03 - Implementation](learn/03-IMPLEMENTATION.md) — code walkthrough
- [04 - Challenges](learn/04-CHALLENGES.md) — extension ideas and exercises

## License

AGPL 3.0
