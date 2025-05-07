# C2 Beacon

**Author:** [Winston Mascarenhas](https://github.com/WinstonMascarenhas1006)  
**Development period:** May – June 2025 (2 months)  
**Started:** 2025-05-01 · **Completed:** 2025-06-25

This is an educational Command and Control (C2) project I built to understand how frameworks like Cobalt Strike and Sliver work under the hood. It has a WebSocket-based beacon implant, a FastAPI server, and a React operator dashboard. Traffic between the beacon and server uses XOR plus Base64 encoding. There are 10 commands mapped to MITRE ATT&CK techniques, a task queue with SQLite persistence, and a real-time dashboard where you can pick a beacon and run commands in a terminal-style session.

Use this only in isolated lab environments. Do not point it at systems you do not own.

## What it does

- WebSocket-based C2 protocol with XOR + Base64 encoding and shared-key authentication
- 10 beacon commands mapped to MITRE ATT&CK: shell, sysinfo, proclist, upload, download, screenshot, keylog, persist, sleep
- Real-time operator dashboard showing connected beacons with live heartbeat tracking
- Terminal-style session page with command history, tab autocomplete, and inline screenshot rendering
- Per-beacon async task queues with SQLite persistence and full task history
- Exponential backoff reconnection with configurable sleep interval and jitter

### Stack

**Backend:** FastAPI, aiosqlite, Pydantic, uvicorn

**Frontend:** React 19, TypeScript, Vite, Zustand, Zod

**Beacon:** asyncio, websockets, psutil, pynput, mss

## Requirements

- Python 3.13+
- Node.js 22+
- Docker and Docker Compose
- Basic understanding of networking, HTTP, and client-server communication

Optional tools:

- **uv** for Python package management
- **pnpm** for Node package management (`corepack enable && corepack prepare pnpm@latest --activate`)
- **just** as a command runner (type `just` to see all commands)

## Installation

Start the development stack with Docker Compose:

```bash
cd c2-beacon
docker compose -f dev.compose.yml up -d
```

Visit `http://localhost:47430` to open the operator dashboard.

Check that all services are running:

```bash
just dev-ps
```

For local development without Docker, you need to set up the backend, frontend, and beacon separately. Copy `.env.example` to `.env` and adjust values as needed.

Backend (from `backend/`):

```bash
cd backend
uv sync
uv run python -m app
```

Frontend (from `frontend/`):

```bash
cd frontend
pnpm install
pnpm dev
```

Beacon (from `beacon/`):

```powershell
cd beacon
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
python beacon.py
```

On Linux or macOS, use `just beacon` instead — it sets the server URL and XOR key from your `.env` file automatically.

## Usage

Start the dev environment:

```bash
docker compose -f dev.compose.yml up -d
```

Open the dashboard at `http://localhost:47430`.

In a second terminal, run a beacon:

```bash
just beacon
```

You should see output like:

```
INFO: Connecting to ws://localhost:47430/api/ws/beacon
INFO: Registered as 3a7f1c29-8b42-4e91-a6d3-9f0e5c8d2b17
```

The beacon appears in the dashboard table with hostname, OS, username, and IP. Click a row to open a session, then try commands:

```
shell whoami
sysinfo
proclist
shell ls -la /tmp
```

Each command goes through the full pipeline: operator dashboard sends JSON to the server over WebSocket, the server queues a task and forwards it (XOR+Base64 encoded) to the beacon, the beacon executes and sends the result back, and the server broadcasts it to the dashboard.

### Useful just commands

```bash
just dev-up          # start dev stack (foreground)
just dev-start       # start dev stack (detached)
just dev-down        # stop and remove containers
just dev-logs        # follow logs
just beacon          # run the beacon implant
just test            # run backend tests
```

Production deployment uses `compose.yml` instead of `dev.compose.yml`:

```bash
docker compose --env-file .env up -d
```

## Project structure

```
c2-beacon/
├── backend/
│   └── app/
│       ├── core/
│       │   ├── encoding.py      # XOR + Base64 encode/decode
│       │   ├── models.py        # Pydantic models
│       │   └── protocol.py      # Message envelope pack/unpack
│       ├── beacon/
│       │   ├── registry.py      # Beacon registry with aiosqlite persistence
│       │   ├── router.py        # WebSocket endpoint for beacons
│       │   └── tasking.py       # Task queue
│       ├── ops/
│       │   ├── manager.py       # Operator WebSocket manager
│       │   └── router.py        # Operator WebSocket + REST endpoints
│       ├── config.py
│       └── database.py
├── beacon/
│   └── beacon.py                # The implant (10 command handlers)
├── frontend/
│   └── src/
│       ├── core/ws.ts           # Zustand store + WebSocket hook
│       └── pages/
│           ├── dashboard/       # Beacon table with live updates
│           └── session/         # Terminal UI
├── infra/
│   ├── docker/                  # Dockerfiles for dev and prod
│   └── nginx/                   # Reverse proxy (WebSocket proxying)
├── dev.compose.yml              # 3-service dev stack: nginx, backend, frontend
├── compose.yml                  # Production compose
├── justfile
└── learn/
```

### How it works (brief)

The beacon connects to the server via WebSocket at `/api/ws/beacon`. On connect it sends a REGISTER message with system info (hostname, OS, username, PID, IP, architecture). The server stores this in a registry backed by aiosqlite and broadcasts a `beacon_connected` event to operators.

The beacon then sends periodic HEARTBEAT messages with jittered timing. When an operator types a command in the session terminal, the frontend sends JSON to the server, which creates a task, queues it, and forwards it to the target beacon as an XOR+Base64 encoded TASK message. The beacon runs the handler and sends back a RESULT message.

Two separate WebSocket channels keep things separated: the beacon channel uses XOR+Base64 (simulating encrypted C2 traffic), and the operator channel uses plain JSON (trusted internal communication).

## Learn modules

- [00 - Overview](learn/00-OVERVIEW.md) — prerequisites and quick start
- [01 - Concepts](learn/01-CONCEPTS.md) — C2 frameworks, MITRE ATT&CK, and detection
- [02 - Architecture](learn/02-ARCHITECTURE.md) — protocol design and data flow
- [03 - Implementation](learn/03-IMPLEMENTATION.md) — code walkthrough
- [04 - Challenges](learn/04-CHALLENGES.md) — extension ideas and exercises

## License

AGPL 3.0
