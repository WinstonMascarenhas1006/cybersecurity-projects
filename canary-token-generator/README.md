<!--
  Module 04 — canary-token-generator
  Part of cybersecurity-projects laboratory corpus
-->

<div align="center">
  <img src="https://raw.githubusercontent.com/WinstonMascarenhas1006/cybersecurity-projects/main/assets/modules/04-canary-token-generator.png" alt="canary-token-generator laboratory module" width="100%" />
</div>

<p align="center">
  <a href="https://github.com/WinstonMascarenhas1006"><img src="https://img.shields.io/badge/Author-Winston_Mascarenhas-0f766e?style=flat-square" alt="Author" /></a>
  &nbsp;
  <img src="https://img.shields.io/badge/Module-04-334155?style=flat-square" alt="Module 04" />
  &nbsp;
  <img src="https://img.shields.io/badge/Stack-Go-1e3a5f?style=flat-square" alt="Stack" />
  &nbsp;
  <img src="https://img.shields.io/badge/Domain-Detect-111827?style=flat-square" alt="Domain" />
  &nbsp;
  <img src="https://img.shields.io/badge/Aug-Sep_2025-0f172a?style=flat-square" alt="Period" />
</p>

<div align="center">
  <img src="https://raw.githubusercontent.com/WinstonMascarenhas1006/cybersecurity-projects/main/assets/module-ethics.png" alt="Authorized labs only" width="100%" />
</div>

<br/>

<p align="center">
  <a href="../README.md"><code>← laboratory corpus</code></a>
</p>

---

# Canary Token Generator

**Author:** [Winston Mascarenhas](https://github.com/WinstonMascarenhas1006)  
**Development period:** August – September 2025 (2 months)  
**Started:** 2025-08-01 · **Completed:** 2025-09-25

I built this as a self-hosted honeytoken generator — a way to plant fake credentials, documents, and URLs around your network that look real enough for an attacker to grab, but actually alert you the moment someone touches them. When a token fires, you get a notification on Telegram or a webhook. See the learn modules at the bottom for the theory and code walkthrough.

## What it does

The app mints seven different kinds of tripwire artifacts, each disguised as something an attacker would actually try to use:

- **webbug** — a URL pointing to a 1x1 JPEG pixel. Any HTTP GET on the URL triggers it. Good for hiding in HTML emails, internal wikis, or "do-not-touch" docs.
- **slowredirect** — a URL with a delayed redirect. When someone clicks it, a 3-second JavaScript interstitial runs first to collect browser fingerprint data, then redirects to a real destination you configure. Useful for fake admin panel URLs or phishing-bait links.
- **pdf** — a patched PDF file. When Acrobat opens it, the `/AA /O /URI` page-open action fires automatically. Plant it as something like `payroll-q3.pdf` on a shared drive.
- **docx** — a patched Word document. Word or LibreOffice loads a footer containing a remote URI when the file opens. Think `customer-list.docx` or `passwords.docx` in a Documents folder.
- **envfile** — a plain-text `.env` file. The generator picks recipes from AWS, database, GitHub, and Stripe config templates, shuffles the sections, and buries a single canary line (`INTERNAL_METRICS_ENDPOINT=https://your-host/c/{tokenID}`) among plausible production secrets. An attacker harvesting the file gets a fistful of fake credentials to chase, and trips the wire as soon as one gets touched.
- **kubeconfig** — a YAML kubeconfig file. When someone runs `kubectl --kubeconfig=stolen.yaml ...`, the server logs the bearer token from the request. Drop it in `~/.kube/config`, on an ops laptop, or a CI runner home directory.
- **mysql** — a `mysql://...` connection string pointing at a real TCP listener that speaks the MySQL v10 wire protocol. An attacker connecting with the `mysql` CLI gets a proper handshake and then an `Access denied` packet. Hide it in `.env` files, `database.yml`, or internal wiki snippets.

Beyond the token types themselves, the system handles per-token Telegram or webhook alerts the instant a token fires (webhooks are HMAC-signed). Notifications go through an async worker pool with per-channel timeouts and dedup gating — there is a 15-minute Redis silence window per `{token, source_ip}` so a curious attacker reloading the page does not spam you. Every event gets GeoIP enrichment via MaxMind GeoLite2 (country, region, city, ASN, ASN org). The `slowredirect` type captures browser fingerprints via a POST endpoint after the interstitial. You get a public manage URL (UUID-gated) so you can share a single link with a teammate to view triggers without giving them operator credentials. There is an operator-only admin API (constant-time bearer comparison) for global stats, token listing, and force-disable. Token creation is protected by Cloudflare Turnstile and dual-window rate limiting (per-minute and per-hour) keyed by browser fingerprint. You can optionally expose the service publicly through a Cloudflare Tunnel overlay without opening a port or maintaining your own TLS cert. For observability there is OpenTelemetry tracing, slog structured logs, a `/healthz` liveness endpoint, and graceful shutdown with a load-balancer drain delay.

### HTTP API

Token creation, manage view, and admin routes are mounted under `/api/`. Trigger routes live at the root so artifacts can carry short URLs. The MySQL listener is separate — it is a TCP server, not HTTP.

**Token and admin routes (`/api/`):**

- `POST /api/tokens` — mint a new token. Requires Turnstile verification and rate limiting. Body includes `type`, `memo`, `alert_channel`, channel config, and type-specific metadata.
- `GET /api/tokens/types` — public list of available token types and their metadata schemas.
- `GET /api/m/{manageId}` — token details, paginated event feed, and dedup silence counter. Requires the manage UUID.
- `DELETE /api/m/{manageId}` — soft-disable the token (events stop, history retained). Requires the manage UUID.
- `GET /api/admin/stats` — tokens count, events count, breakdowns by type and alert channel. Requires bearer token.
- `GET /api/admin/tokens` — all tokens, offset paginated. Requires bearer token.
- `POST /api/admin/tokens/{id}/disable` — force-disable any token. Requires bearer token.
- `GET /healthz` — liveness and readiness probe used by Docker healthchecks.

**Trigger routes (root level):**

- `GET /c/{tokenID}` — the main trigger route. Records the event, fires the notification, and returns the artifact body (pixel, GIF, HTML interstitial, etc.).
- `POST /c/{tokenID}/fingerprint` — receives JSON fingerprint payload from the `slowredirect` interstitial.
- `* /k/{tokenID}[/*]` — kubeconfig trigger that matches `kubectl`'s wildcard API paths.

### Stack

**Backend:** Go 1.25, chi router, pgx + sqlx, goose migrations, koanf config, slog, validator/v10, OpenTelemetry, pdfcpu, MaxMind GeoLite2, miniredis (tests), testcontainers (integration)

**Frontend:** React 19, TypeScript, Vite, TanStack Query, Zod, Axios, Biome, Stylelint

**Storage:** PostgreSQL 18 (`tokens` and `events` tables with INET and JSONB columns), Redis 7 (dedup gate and rate-limit token buckets)

**Infra:** Docker Compose (dev stack: nginx + Vite HMR + Air hot-reload + Postgres + Redis + Jaeger; prod stack: nginx + Go binary + Postgres + Redis), optional `cloudflared` overlay

### Project layout

```
canary-token-generator/
├── backend/
│   ├── cmd/canary/                main.go — wiring, signal handling, MySQL listener, retention loop
│   └── internal/
│       ├── token/                 service, repository, handler, generator interface
│       │   └── generators/        webbug, pixel, pdf, docx, envfile, kubeconfig, mysql, slowredirect
│       ├── event/                 event entity, geo enrich → insert → dedup → notify
│       ├── notify/                worker pool, webhook (HMAC-signed), telegram
│       ├── middleware/            request_id, logging, recovery, realip, fingerprint, ratelimit, turnstile
│       ├── geoip/                 MaxMind MMDB lookup (nop when no DB present)
│       ├── admin/                 stats, listing, force-disable
│       └── server/                chi router with graceful shutdown
├── frontend/src/pages/            landing (token creation) and manage (event table)
├── infra/nginx/                   prod and dev nginx configs
├── infra/docker/                  Dockerfiles for prod, Air, and Vite
├── compose.yml                    production stack
├── dev.compose.yml                dev stack with Jaeger
├── cloudflared.compose.yml        tunnel overlay
├── justfile                       command runner recipes
└── learn/                         step-by-step learning modules
```

## Requirements

- Docker and Docker Compose (the whole stack runs in containers)
- `just` command runner — install with `curl -sSf https://just.systems/install.sh | bash -s -- --to ~/.local/bin`
- OpenSSL (used by the init script to generate secrets)
- Optional: MaxMind account ID and license key in `.env` if you want GeoIP enrichment (the init script downloads GeoLite2-City.mmdb automatically when those are set)
- Optional: Cloudflare Turnstile site key and secret if you want bot protection on token creation
- Optional: Telegram bot token or webhook URL for alert delivery

## Installation

Clone the repo and run the init script first. It creates `.env` and `.env.development` from the examples, generates random Postgres password and operator token values, and optionally downloads the GeoIP database.

```bash
cd canary-token-generator
just init
```

Then start the development stack:

```bash
just dev-up
```

Open the URL printed by `just init` (typically something like `http://localhost:22784`). Mint a token, open the manage page, trigger the token from another browser tab, and refresh the manage page to see the event come in.

For production deployment:

```bash
just build
just start
```

To expose the service through a Cloudflare Tunnel without opening ports:

```bash
just tunnel-start
```

Run `just` with no arguments to see every available recipe grouped by area (frontend, backend, lint, compose, tunnel, dev, util).

## Usage

After `just dev-up`, open the frontend URL in your browser. Pick a token type, fill in the memo and alert channel (Telegram or webhook), complete the Turnstile challenge, and click create. The page shows you the artifact to deploy — a URL, a downloadable file, or a connection string depending on the type.

To test a webbug token, paste the trigger URL into another browser tab or run:

```bash
curl -v "http://localhost:22784/c/YOUR_TOKEN_ID"
```

For a PDF or DOCX token, download the file from the result page and open it on another machine. For an envfile token, place the generated `.env` somewhere an attacker might look and try curling the fake endpoint baked into it.

The manage page URL (something like `/manage/{uuid}`) lets you watch events roll in without needing the operator bearer token. Share that link with a teammate if you want them to monitor triggers.

Admin operations use the operator bearer token from your `.env` file:

```bash
curl -H "Authorization: Bearer YOUR_OPERATOR_TOKEN" http://localhost:22784/api/admin/stats
curl -H "Authorization: Bearer YOUR_OPERATOR_TOKEN" http://localhost:22784/api/admin/tokens
```

Other useful commands:

```bash
just dev-logs          # tail all dev container logs
just dev-down          # stop the dev stack
just lint              # run backend and frontend linters
just test              # run backend tests
just ports             # re-randomize dev port assignments
```

## Learn modules

- [00 - Overview](learn/00-OVERVIEW.md) — prerequisites, quick start, project structure
- [01 - Concepts](learn/01-CONCEPTS.md) — honeytokens, deception defense, Thinkst Canary, MITRE Engage, real breaches
- [02 - Architecture](learn/02-ARCHITECTURE.md) — system design, request lifecycle, schema, dedup gate, notification pipeline
- [03 - Implementation](learn/03-IMPLEMENTATION.md) — code walkthrough: generators, trigger handler, event service, MySQL protocol
- [04 - Challenges](learn/04-CHALLENGES.md) — extension ideas: new token types, alert channels, evasion resistance

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
