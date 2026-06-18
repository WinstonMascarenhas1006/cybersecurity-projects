"""Rewrite tool README headers to use designed module cards."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = "https://raw.githubusercontent.com/WinstonMascarenhas1006/cybersecurity-projects/main"

MODULES = [
    {
        "slug": "base64-tool",
        "num": "01",
        "badge_stack": "Python",
        "badge_domain": "Recon",
        "period": "Apr_2025",
    },
    {
        "slug": "c2-beacon",
        "num": "02",
        "badge_stack": "Python_+_React",
        "badge_domain": "Detect",
        "period": "May-Jun_2025",
    },
    {
        "slug": "caesar-cipher",
        "num": "03",
        "badge_stack": "Python",
        "badge_domain": "Analyze",
        "period": "Jul_2025",
    },
    {
        "slug": "canary-token-generator",
        "num": "04",
        "badge_stack": "Go",
        "badge_domain": "Detect",
        "period": "Aug-Sep_2025",
    },
    {
        "slug": "dns-lookup",
        "num": "05",
        "badge_stack": "Python",
        "badge_domain": "Recon",
        "period": "Oct_2025",
    },
    {
        "slug": "firewall-rule-engine",
        "num": "06",
        "badge_stack": "V",
        "badge_domain": "Harden",
        "period": "Nov_2025",
    },
    {
        "slug": "hash-cracker",
        "num": "07",
        "badge_stack": "C++",
        "badge_domain": "Analyze",
        "period": "Dec_2025",
    },
    {
        "slug": "keylogger",
        "num": "08",
        "badge_stack": "Python",
        "badge_domain": "Detect",
        "period": "Jan_2026",
    },
    {
        "slug": "linux-cis-hardening-auditor",
        "num": "09",
        "badge_stack": "Shell",
        "badge_domain": "Harden",
        "period": "Feb_2026",
    },
    {
        "slug": "linux-ebpf-security-tracer",
        "num": "10",
        "badge_stack": "eBPF",
        "badge_domain": "Detect",
        "period": "Mar_2026",
    },
    {
        "slug": "metadata-scrubber-tool",
        "num": "11",
        "badge_stack": "Python",
        "badge_domain": "Harden",
        "period": "Apr_2026",
    },
    {
        "slug": "network-traffic-analyzer",
        "num": "12",
        "badge_stack": "Python",
        "badge_domain": "Analyze",
        "period": "May_2026",
    },
    {
        "slug": "simple-port-scanner",
        "num": "13",
        "badge_stack": "C++",
        "badge_domain": "Recon",
        "period": "May_2026",
    },
    {
        "slug": "simple-vulnerability-scanner",
        "num": "14",
        "badge_stack": "Go",
        "badge_domain": "Detect",
        "period": "Jun_2026",
    },
    {
        "slug": "systemd-persistence-scanner",
        "num": "15",
        "badge_stack": "Go",
        "badge_domain": "Harden",
        "period": "Jun_2026",
    },
]


def header(m: dict) -> str:
    card = f"{RAW}/assets/modules/{m['num']}-{m['slug']}.png"
    ethics = f"{RAW}/assets/module-ethics.png"
    return f"""<!--
  Module {m['num']} — {m['slug']}
  Part of cybersecurity-projects laboratory corpus
-->

<div align="center">
  <img src="{card}" alt="{m['slug']} laboratory module" width="100%" />
</div>

<p align="center">
  <a href="https://github.com/WinstonMascarenhas1006"><img src="https://img.shields.io/badge/Author-Winston_Mascarenhas-0f766e?style=flat-square" alt="Author" /></a>
  &nbsp;
  <img src="https://img.shields.io/badge/Module-{m['num']}-334155?style=flat-square" alt="Module {m['num']}" />
  &nbsp;
  <img src="https://img.shields.io/badge/Stack-{m['badge_stack']}-1e3a5f?style=flat-square" alt="Stack" />
  &nbsp;
  <img src="https://img.shields.io/badge/Domain-{m['badge_domain']}-111827?style=flat-square" alt="Domain" />
  &nbsp;
  <img src="https://img.shields.io/badge/{m['period']}-0f172a?style=flat-square" alt="Period" />
</p>

<div align="center">
  <img src="{ethics}" alt="Authorized labs only" width="100%" />
</div>

<br/>

<p align="center">
  <a href="../README.md"><code>← laboratory corpus</code></a>
</p>

---

"""


def strip_old_header(text: str) -> str:
    """Remove previous banner / module card / leading blank, keep from first # title."""
    # Drop everything before the first markdown H1 that is the tool title
    # Common patterns: starts with <div banner>, ---, ## Module card, then # Title
    m = re.search(r"^# .+$", text, re.MULTILINE)
    if not m:
        return text
    return text[m.start() :]


def polish_ethics(text: str) -> str:
    """Replace plain ethics section with a designed closer if present."""
    pattern = re.compile(
        r"### Ethics & safety\n\n.*?(?=\n## License|\nLicense|\Z)",
        re.DOTALL,
    )
    replacement = (
        "---\n\n"
        "### Legal & ethics\n\n"
        "These tools are for **education and authorized security testing only**.  \n"
        "Do **not** run offensive capabilities against systems you do not own or lack "
        "**explicit written permission** to test.\n\n"
        "---\n\n"
        '<div align="center">\n\n'
        f"**Module in the lab corpus** — "
        f"[cybersecurity-projects](https://github.com/WinstonMascarenhas1006/cybersecurity-projects)"
        "  \n"
        "[Author](https://github.com/WinstonMascarenhas1006)"
        " · "
        "[Portfolio](https://portfolio-winston-mascarenhas.vercel.app)"
        " · "
        "[Profile](https://github.com/WinstonMascarenhas1006/WinstonMascarenhas1006)\n\n"
        "</div>\n\n"
    )
    if pattern.search(text):
        return pattern.sub(replacement, text)
    # If no ethics section, append footer before License
    lic = re.search(r"^## License\s*$", text, re.MULTILINE)
    if lic:
        return text[: lic.start()] + replacement + text[lic.start() :]
    return text + "\n" + replacement


def main() -> None:
    for m in MODULES:
        path = ROOT / m["slug"] / "README.md"
        body = path.read_text(encoding="utf-8")
        body = strip_old_header(body)
        body = polish_ethics(body)
        path.write_text(header(m) + body, encoding="utf-8", newline="\n")
        print("updated", path.relative_to(ROOT))


if __name__ == "__main__":
    main()
