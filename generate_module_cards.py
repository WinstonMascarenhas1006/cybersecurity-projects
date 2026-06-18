"""Generate per-tool module hero cards for cybersecurity-projects READMEs."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "assets" / "modules"
OUT.mkdir(parents=True, exist_ok=True)

INK = (7, 17, 26)
DEEP = (11, 21, 32)
CARD = (15, 28, 40)
LINE = (30, 41, 59)
TEAL = (94, 234, 212)
FOG = (148, 163, 184)
PAPER = (241, 245, 249)
MUTED = (100, 116, 139)


def font(size: int, serif: bool = False):
    path = r"C:\Windows\Fonts\georgia.ttf" if serif else r"C:\Windows\Fonts\segoeui.ttf"
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wash(img: Image.Image, top, bottom) -> None:
    d = ImageDraw.Draw(img)
    w, h = img.size
    for y in range(h):
        t = y / max(h - 1, 1)
        c = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3))
        d.line([(0, y), (w, y)], fill=c)


MODULES = [
    {
        "slug": "base64-tool",
        "num": "01",
        "title": "b64tool",
        "domain": "Recon · Analyze",
        "stack": "Python CLI",
        "period": "Apr 2025",
        "focus": "Recursive layer peeling for encoding and obfuscation analysis",
        "chips": ["Base64", "Hex", "URL", "Peel"],
    },
    {
        "slug": "c2-beacon",
        "num": "02",
        "title": "C2 Beacon",
        "domain": "Detect · Analyze",
        "stack": "Python · React · TS",
        "period": "May–Jun 2025",
        "focus": "Defensive command-and-control laboratory mapped to ATT&CK",
        "chips": ["WebSocket", "ATT&CK", "Dashboard"],
    },
    {
        "slug": "caesar-cipher",
        "num": "03",
        "title": "Caesar Cipher CLI",
        "domain": "Analyze",
        "stack": "Python CLI",
        "period": "Jul 2025",
        "focus": "Frequency-ranked Caesar cryptanalysis practice",
        "chips": ["Crypto", "Frequency", "CTF"],
    },
    {
        "slug": "canary-token-generator",
        "num": "04",
        "title": "Canary Token Generator",
        "domain": "Detect",
        "stack": "Go · Postgres · Redis",
        "period": "Aug–Sep 2025",
        "focus": "Deception lab: honeytokens and event notification pipeline",
        "chips": ["Honeytoken", "Deception", "Alerts"],
    },
    {
        "slug": "dns-lookup",
        "num": "05",
        "title": "DNS Lookup CLI",
        "domain": "Recon",
        "stack": "Python CLI",
        "period": "Oct 2025",
        "focus": "DNS reconnaissance with tracing and WHOIS enrichment",
        "chips": ["DNS", "WHOIS", "Recon"],
    },
    {
        "slug": "firewall-rule-engine",
        "num": "06",
        "title": "Firewall Rule Engine",
        "domain": "Harden",
        "stack": "V CLI",
        "period": "Nov 2025",
        "focus": "Ruleset parsing, conflict detection, hardened baseline generation",
        "chips": ["Firewall", "Rules", "Baseline"],
    },
    {
        "slug": "hash-cracker",
        "num": "07",
        "title": "Hash Cracker",
        "domain": "Analyze",
        "stack": "C++",
        "period": "Dec 2025",
        "focus": "Dictionary and brute-force hash cracking practice for labs",
        "chips": ["Hash", "Dictionary", "Lab"],
    },
    {
        "slug": "keylogger",
        "num": "08",
        "title": "Keylogger",
        "domain": "Detect",
        "stack": "Python",
        "period": "Jan 2026",
        "focus": "Authorized keystroke capture for defensive detection exercises",
        "chips": ["Authorized", "Detection", "Lab"],
    },
    {
        "slug": "linux-cis-hardening-auditor",
        "num": "09",
        "title": "Linux CIS Hardening Auditor",
        "domain": "Harden",
        "stack": "Shell · Python",
        "period": "Feb 2026",
        "focus": "CIS-style compliance checking with actionable remediation",
        "chips": ["CIS", "Audit", "Linux"],
    },
    {
        "slug": "linux-ebpf-security-tracer",
        "num": "10",
        "title": "Linux eBPF Security Tracer",
        "domain": "Detect",
        "stack": "Python · C · eBPF",
        "period": "Mar 2026",
        "focus": "eBPF tracing for detection engineering and monitoring studies",
        "chips": ["eBPF", "Tracing", "Linux"],
    },
    {
        "slug": "metadata-scrubber-tool",
        "num": "11",
        "title": "Metadata Scrubber Tool",
        "domain": "Harden · Analyze",
        "stack": "Python CLI",
        "period": "Apr 2026",
        "focus": "Privacy hardening: metadata and EXIF scrubbing for artifacts",
        "chips": ["EXIF", "Privacy", "Scrub"],
    },
    {
        "slug": "network-traffic-analyzer",
        "num": "12",
        "title": "Network Traffic Analyzer",
        "domain": "Analyze",
        "stack": "Python",
        "period": "May 2026",
        "focus": "PCAP and live traffic analysis with structured outputs",
        "chips": ["PCAP", "Live", "Packets"],
    },
    {
        "slug": "simple-port-scanner",
        "num": "13",
        "title": "Simple Port Scanner",
        "domain": "Recon",
        "stack": "C++",
        "period": "May 2026",
        "focus": "Asynchronous TCP port scanning with clear lab constraints",
        "chips": ["TCP", "Scan", "Async"],
    },
    {
        "slug": "simple-vulnerability-scanner",
        "num": "14",
        "title": "Simple Vulnerability Scanner",
        "domain": "Detect · Analyze",
        "stack": "Go",
        "period": "Jun 2026",
        "focus": "Dependency vulnerability checks and workflow-friendly reporting",
        "chips": ["CVE", "Deps", "Report"],
    },
    {
        "slug": "systemd-persistence-scanner",
        "num": "15",
        "title": "Systemd Persistence Scanner",
        "domain": "Harden · Detect",
        "stack": "Go",
        "period": "Jun 2026",
        "focus": "Persistence discovery and system configuration audit",
        "chips": ["systemd", "Persist", "Audit"],
    },
]


def module_card(m: dict) -> Path:
    w, h = 1280, 420
    img = Image.new("RGB", (w, h))
    wash(img, (7, 17, 26), (12, 40, 42))
    d = ImageDraw.Draw(img, "RGBA")

    for x in range(0, w, 32):
        d.line([(x, 0), (x, h)], fill=(*TEAL, 10))
    for y in range(0, h, 32):
        d.line([(0, y), (w, y)], fill=(*TEAL, 10))

    # right schematic panel
    d.rounded_rectangle([860, 48, 1232, 372], radius=18, fill=CARD, outline=LINE, width=2)
    d.text((892, 72), "MODULE", fill=MUTED, font=font(12))
    d.text((892, 100), m["num"], fill=TEAL, font=font(64, serif=True))
    d.text((892, 190), "DOMAIN", fill=MUTED, font=font(12))
    d.text((892, 214), m["domain"], fill=PAPER, font=font(18, serif=True))
    d.text((892, 270), "STACK", fill=MUTED, font=font(12))
    d.text((892, 294), m["stack"], fill=FOG, font=font(16))
    d.text((892, 330), m["period"], fill=TEAL, font=font(14))

    d.text((56, 48), "LABORATORY MODULE", fill=FOG, font=font(14, serif=True))
    d.text((56, 88), m["title"], fill=PAPER, font=font(42, serif=True))
    d.rectangle([56, 152, 240, 155], fill=TEAL)

    # wrap focus
    focus = m["focus"]
    words = focus.split()
    lines, cur = [], ""
    for word in words:
        trial = f"{cur} {word}".strip()
        if d.textlength(trial, font=font(20, serif=True)) < 760:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    y = 178
    for line in lines[:3]:
        d.text((56, y), line, fill=PAPER, font=font(20, serif=True))
        y += 34

    # chips
    cx = 56
    cy = 320
    for chip in m["chips"]:
        tw = int(d.textlength(chip, font=font(13))) + 24
        d.rounded_rectangle([cx, cy, cx + tw, cy + 34], radius=10, fill=(18, 36, 42), outline=LINE, width=2)
        d.text((cx + 12, cy + 8), chip, fill=TEAL, font=font(13))
        cx += tw + 12

    d.text((56, 378), "cybersecurity-projects  ·  Winston Mascarenhas", fill=MUTED, font=font(13))

    path = OUT / f"{m['num']}-{m['slug']}.png"
    img.save(path, "PNG", optimize=True)
    print(path.name)
    return path


def ethics_strip() -> None:
    """Compact ethics strip for module pages."""
    w, h = 1280, 100
    img = Image.new("RGB", (w, h))
    wash(img, (10, 22, 30), (12, 30, 34))
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle([1, 1, w - 2, h - 2], radius=14, outline=LINE, width=2)
    d.text((40, 24), "Authorized labs only.", fill=PAPER, font=font(22, serif=True))
    d.text(
        (40, 58),
        "Educational tooling — run only on systems you own or have explicit written permission to test.",
        fill=FOG,
        font=font(14),
    )
    path = ROOT / "assets" / "module-ethics.png"
    img.save(path, "PNG", optimize=True)
    print(path.name)


if __name__ == "__main__":
    for m in MODULES:
        module_card(m)
    ethics_strip()
    print(f"wrote {len(MODULES)} module cards → {OUT}")
