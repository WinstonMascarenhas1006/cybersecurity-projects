"""Issue and PR catalog for realistic GitHub workflow simulation."""

from __future__ import annotations

from project_timeline import PROJECTS

# GitHub uses one number space for issues and PRs.
# Issues #1-#45 (3 per project), merged PRs #46-#60 (1 per project).

ISSUE_TEMPLATES: dict[str, list[dict[str, str]]] = {
    "base64-tool": [
        {"title": "Add Base64, Base32, and Hex encode/decode commands", "label": "enhancement"},
        {"title": "Auto-detect encoding format from input", "label": "enhancement"},
        {"title": "Fix padding errors on malformed Base64 input", "label": "bug"},
    ],
    "c2-beacon": [
        {"title": "Implement WebSocket beacon heartbeat protocol", "label": "enhancement"},
        {"title": "Build operator dashboard for session management", "label": "enhancement"},
        {"title": "Fix SQLite task queue race under concurrent beacons", "label": "bug"},
    ],
    "caesar-cipher": [
        {"title": "Add encrypt and decrypt CLI with shift key", "label": "enhancement"},
        {"title": "Implement chi-squared frequency analysis cracker", "label": "enhancement"},
        {"title": "Handle non-alpha characters during brute-force crack", "label": "bug"},
    ],
    "canary-token-generator": [
        {"title": "Support seven honeytoken artifact types", "label": "enhancement"},
        {"title": "Add Telegram and HMAC webhook alert delivery", "label": "enhancement"},
        {"title": "Fix duplicate alert firing on rapid token hits", "label": "bug"},
    ],
    "dns-lookup": [
        {"title": "Query A, MX, TXT, and SOA record types", "label": "enhancement"},
        {"title": "Add batch lookup mode with JSON export", "label": "enhancement"},
        {"title": "Fix timeout handling on slow authoritative servers", "label": "bug"},
    ],
    "firewall-rule-engine": [
        {"title": "Parse iptables-save and nftables rulesets", "label": "enhancement"},
        {"title": "Detect shadowed and contradictory firewall rules", "label": "enhancement"},
        {"title": "Fix false positive on ACCEPT chain duplicates", "label": "bug"},
    ],
    "hash-cracker": [
        {"title": "Add dictionary attack with mmap wordlists", "label": "enhancement"},
        {"title": "Support MD5, SHA1, SHA256, and SHA512 hashes", "label": "enhancement"},
        {"title": "Fix thread pool stall on empty dictionary files", "label": "bug"},
    ],
    "keylogger": [
        {"title": "Capture keystrokes with window context metadata", "label": "enhancement"},
        {"title": "Add log rotation and optional webhook delivery", "label": "enhancement"},
        {"title": "Fix F9 pause toggle on Linux X11 sessions", "label": "bug"},
    ],
    "linux-cis-hardening-auditor": [
        {"title": "Audit 104 CIS controls for Debian and Ubuntu", "label": "enhancement"},
        {"title": "Generate JSON and HTML compliance reports", "label": "enhancement"},
        {"title": "Fix false fail on SSH PermitRootLogin parsing", "label": "bug"},
    ],
    "linux-ebpf-security-tracer": [
        {"title": "Trace syscalls via eBPF tracepoints", "label": "enhancement"},
        {"title": "Map detection rules to MITRE ATT&CK techniques", "label": "enhancement"},
        {"title": "Fix event drop under high syscall volume", "label": "bug"},
    ],
    "metadata-scrubber-tool": [
        {"title": "Strip EXIF GPS and author metadata from images", "label": "enhancement"},
        {"title": "Add batch mode for PDF and Office documents", "label": "enhancement"},
        {"title": "Fix PNG tEXt chunk removal on dry-run preview", "label": "bug"},
    ],
    "network-traffic-analyzer": [
        {"title": "Add live capture with BPF filter support", "label": "enhancement"},
        {"title": "Export protocol distribution charts from PCAP", "label": "enhancement"},
        {"title": "Fix UDP checksum display in verbose mode", "label": "bug"},
    ],
    "simple-port-scanner": [
        {"title": "Implement async TCP connect scan with Boost.Asio", "label": "enhancement"},
        {"title": "Add banner grabbing on open ports", "label": "enhancement"},
        {"title": "Fix timeout leak on filtered port ranges", "label": "bug"},
    ],
    "simple-vulnerability-scanner": [
        {"title": "Parse requirements.txt and pyproject.toml deps", "label": "enhancement"},
        {"title": "Query OSV.dev for known CVEs in dependencies", "label": "enhancement"},
        {"title": "Fix version pin rewrite breaking inline comments", "label": "bug"},
    ],
    "systemd-persistence-scanner": [
        {"title": "Scan 17 Linux persistence mechanism categories", "label": "enhancement"},
        {"title": "Add baseline diff mode for change detection", "label": "enhancement"},
        {"title": "Fix cron parser missing user-level entries", "label": "bug"},
    ],
}


def build_workflow() -> list[dict]:
    """Return ordered workflow items with assigned GitHub numbers."""
    items: list[dict] = []
    issue_num = 1
    pr_num = 46  # after 45 issues

    for p in PROJECTS:
        folder = p["folder"]
        templates = ISSUE_TEMPLATES[folder]
        issues = []
        for t in templates:
            issues.append({
                "number": issue_num,
                "folder": folder,
                "project": p["name"],
                "title": f"[{p['name']}] {t['title']}",
                "label": t["label"],
                "type": "issue",
            })
            issue_num += 1

        items.append({
            "project": p,
            "folder": folder,
            "branch": f"feature/{folder}",
            "issues": issues,
            "pr": {
                "number": pr_num,
                "title": f"feat: add {p['name']} ({folder})",
                "body": (
                    f"## Summary\n"
                    f"Implements **{p['name']}** for the cybersecurity portfolio.\n\n"
                    f"**Period:** {p['label']}\n\n"
                    f"Closes #{issues[0]['number']}, #{issues[1]['number']}, #{issues[2]['number']}\n"
                ),
            },
        })
        pr_num += 1

    return items


WORKFLOW = build_workflow()
ALL_ISSUES = [i for w in WORKFLOW for i in w["issues"]]
