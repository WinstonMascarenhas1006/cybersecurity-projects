# Keylogger

**Author:** [Winston Mascarenhas](https://github.com/WinstonMascarenhas1006)  
**Development period:** January 2026 (1 month)  
**Started:** 2026-01-01 · **Completed:** 2026-01-26

This is an educational keylogger I built to understand how input capture, window tracking, and remote log delivery actually work under the hood. It records keystrokes with microsecond-precision timestamps, tracks which window is active, rotates log files when they get too big, and can optionally ship events to a webhook. There is a walkthrough video at https://youtu.be/gTd8cNlMD1k if you prefer watching over reading.

**Important:** This is for authorized security research and education only. Running a keylogger on a system you do not own or do not have explicit written permission to monitor is illegal. Only use this on your own machines or in controlled lab environments.

## What it does

- Real-time keyboard event capture with microsecond-precision timestamps
- Active window tracking across Windows, macOS, and Linux
- Log rotation with configurable size limits (default 5 MB per file)
- F9 toggle to pause and resume capture at runtime without restarting
- Remote delivery simulation via webhooks for C2 research (batched HTTP POST)
- Thread-safe operations with proper locking and cleanup on shutdown

Each keystroke is recorded as a `KeyEvent` with a timestamp, the active window title, and the key type (regular character, special key like Enter or Backspace, or unknown). Special keys show up as labeled tokens like `[ENTER]`, `[BACKSPACE]`, `[SPACE]`.

## Requirements

- Python 3.12 or newer
- `uv` package manager — install from https://docs.astral.sh/uv/
- `pynput` for keyboard capture (installed automatically by `uv sync`)
- Platform-specific extras:
  - **Windows:** `pywin32` and `psutil` (for window title lookup)
  - **macOS:** `pyobjc-framework-Cocoa` (for NSWorkspace window tracking)
  - **Linux:** no extra packages needed (uses `xdotool` or `xprop` via subprocess)
- `just` command runner (optional) — install with `curl -sSf https://just.systems/install.sh | bash -s -- --to ~/.local/bin`

## Installation

Clone the repo and set up the virtual environment with uv:

```bash
cd keylogger
uv sync
```

On Windows, install the platform extras:

```bash
uv sync --extra windows
```

On macOS:

```bash
uv sync --extra macos
```

For development (tests, linting):

```bash
just setup
```

Or manually:

```bash
uv sync --all-extras
```

## Usage

Start the keylogger:

```bash
uv run python keylogger.py
```

Or through just (it asks for confirmation first):

```bash
just run
```

While it is running:

- Press **F9** to toggle capture on and off
- Press **Ctrl+C** to stop cleanly (flushes logs and closes the listener)

Logs are written to disk with timestamps. When a log file hits the size limit (5 MB by default), it rotates to a new file automatically.

To run the test suite:

```bash
just test
```

To lint and format:

```bash
just lint
just format
```

Run `just` with no arguments to see all available commands (setup, test, lint, format, clean, run).

## Learn modules

- [00 - Overview](learn/00-OVERVIEW.md) — prerequisites and quick start
- [01 - Concepts](learn/01-CONCEPTS.md) — security theory and real-world breaches
- [02 - Architecture](learn/02-ARCHITECTURE.md) — system design and data flow
- [03 - Implementation](learn/03-IMPLEMENTATION.md) — code walkthrough
- [04 - Challenges](learn/04-CHALLENGES.md) — extension ideas and exercises

## License

AGPL 3.0
