"""Development timeline for the 15-project portfolio."""

from __future__ import annotations

from datetime import date

AUTHOR = "Winston Mascarenhas"
GITHUB = "https://github.com/WinstonMascarenhas1006"
PORTFOLIO = "https://portfolio-winston-mascarenhas.vercel.app"

# All dates must be on or before LAST_COMMIT_DAY. GitHub ignores future-dated commits.
TODAY = date(2026, 6, 19)
LAST_COMMIT_DAY = TODAY

# April 2025 start, one project per month; c2-beacon and canary-token-generator get 2 months.
# Last three projects share May-June 2026 (different days) so nothing is dated in the future.
PROJECTS: list[dict] = [
    {
        "num": 1,
        "folder": "base64-tool",
        "name": "b64tool",
        "start": "2025-04-01",
        "end": "2025-04-28",
        "label": "April 2025",
        "duration": "1 month",
        "months": 1,
        "year": 2025,
        "two_month": False,
    },
    {
        "num": 2,
        "folder": "c2-beacon",
        "name": "C2 Beacon",
        "start": "2025-05-01",
        "end": "2025-06-25",
        "label": "May – June 2025",
        "duration": "2 months",
        "months": 2,
        "year": 2025,
        "two_month": True,
    },
    {
        "num": 3,
        "folder": "caesar-cipher",
        "name": "Caesar Cipher",
        "start": "2025-07-01",
        "end": "2025-07-26",
        "label": "July 2025",
        "duration": "1 month",
        "months": 1,
        "year": 2025,
        "two_month": False,
    },
    {
        "num": 4,
        "folder": "canary-token-generator",
        "name": "Canary Token Generator",
        "start": "2025-08-01",
        "end": "2025-09-25",
        "label": "August – September 2025",
        "duration": "2 months",
        "months": 2,
        "year": 2025,
        "two_month": True,
    },
    {
        "num": 5,
        "folder": "dns-lookup",
        "name": "DNS Lookup",
        "start": "2025-10-01",
        "end": "2025-10-26",
        "label": "October 2025",
        "duration": "1 month",
        "months": 1,
        "year": 2025,
        "two_month": False,
    },
    {
        "num": 6,
        "folder": "firewall-rule-engine",
        "name": "Firewall Rule Engine",
        "start": "2025-11-01",
        "end": "2025-11-25",
        "label": "November 2025",
        "duration": "1 month",
        "months": 1,
        "year": 2025,
        "two_month": False,
    },
    {
        "num": 7,
        "folder": "hash-cracker",
        "name": "Hash Cracker",
        "start": "2025-12-01",
        "end": "2025-12-26",
        "label": "December 2025",
        "duration": "1 month",
        "months": 1,
        "year": 2025,
        "two_month": False,
    },
    {
        "num": 8,
        "folder": "keylogger",
        "name": "Keylogger",
        "start": "2026-01-01",
        "end": "2026-01-26",
        "label": "January 2026",
        "duration": "1 month",
        "months": 1,
        "year": 2026,
        "two_month": False,
    },
    {
        "num": 9,
        "folder": "linux-cis-hardening-auditor",
        "name": "CIS Hardening Auditor",
        "start": "2026-02-01",
        "end": "2026-02-23",
        "label": "February 2026",
        "duration": "1 month",
        "months": 1,
        "year": 2026,
        "two_month": False,
    },
    {
        "num": 10,
        "folder": "linux-ebpf-security-tracer",
        "name": "eBPF Security Tracer",
        "start": "2026-03-01",
        "end": "2026-03-26",
        "label": "March 2026",
        "duration": "1 month",
        "months": 1,
        "year": 2026,
        "two_month": False,
    },
    {
        "num": 11,
        "folder": "metadata-scrubber-tool",
        "name": "Metadata Scrubber",
        "start": "2026-04-01",
        "end": "2026-04-25",
        "label": "April 2026",
        "duration": "1 month",
        "months": 1,
        "year": 2026,
        "two_month": False,
    },
    {
        "num": 12,
        "folder": "network-traffic-analyzer",
        "name": "Network Traffic Analyzer",
        "start": "2026-05-01",
        "end": "2026-05-12",
        "label": "May 2026",
        "duration": "1 month",
        "months": 1,
        "year": 2026,
        "two_month": False,
    },
    {
        "num": 13,
        "folder": "simple-port-scanner",
        "name": "Port Scanner",
        "start": "2026-05-13",
        "end": "2026-05-22",
        "label": "May 2026",
        "duration": "1 month",
        "months": 1,
        "year": 2026,
        "two_month": False,
    },
    {
        "num": 14,
        "folder": "simple-vulnerability-scanner",
        "name": "Vulnerability Scanner",
        "start": "2026-06-01",
        "end": "2026-06-10",
        "label": "June 2026",
        "duration": "1 month",
        "months": 1,
        "year": 2026,
        "two_month": False,
    },
    {
        "num": 15,
        "folder": "systemd-persistence-scanner",
        "name": "Persistence Scanner",
        "start": "2026-06-11",
        "end": "2026-06-19",
        "label": "June 2026",
        "duration": "1 month",
        "months": 1,
        "year": 2026,
        "two_month": False,
    },
]

for p in PROJECTS:
    end = date.fromisoformat(p["end"])
    if end > TODAY:
        raise ValueError(f"{p['folder']} end date {p['end']} is after today {TODAY}")

BY_FOLDER = {p["folder"]: p for p in PROJECTS}


def readme_meta(p: dict) -> str:
    return (
        f"**Author:** [{AUTHOR}]({GITHUB})  \n"
        f"**Development period:** {p['label']} ({p['duration']})  \n"
        f"**Started:** {p['start']} · **Completed:** {p['end']}\n"
    )
