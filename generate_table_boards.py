"""Visual inventory/timeline boards for cybersecurity-projects README."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / "assets"
OUT.mkdir(parents=True, exist_ok=True)

DEEP = (11, 21, 32)
CARD = (15, 28, 40)
LINE = (30, 41, 59)
TEAL = (94, 234, 212)
PAPER = (241, 245, 249)
FOG = (148, 163, 184)
MUTED = (100, 116, 139)


def font(size: int, serif: bool = False):
    path = r"C:\Windows\Fonts\georgia.ttf" if serif else r"C:\Windows\Fonts\segoeui.ttf"
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


TOOLS = [
    ("01", "base64-tool", "Python", "Encode / decode"),
    ("02", "c2-beacon", "Python", "Defensive C2 lab"),
    ("03", "caesar-cipher", "Python", "Classical crypto"),
    ("04", "canary-token-generator", "Go", "Honeytokens"),
    ("05", "dns-lookup", "Python", "DNS + WHOIS"),
    ("06", "firewall-rule-engine", "V", "Allow / deny"),
    ("07", "hash-cracker", "C++", "Dictionary crack"),
    ("08", "keylogger", "Python", "Authorized lab"),
    ("09", "linux-cis-hardening-auditor", "Shell", "CIS checks"),
    ("10", "linux-ebpf-security-tracer", "Python/C", "eBPF tracing"),
    ("11", "metadata-scrubber-tool", "Python", "EXIF strip"),
    ("12", "network-traffic-analyzer", "Python", "PCAP / live"),
    ("13", "simple-port-scanner", "C++", "TCP scan"),
    ("14", "simple-vulnerability-scanner", "Go", "Dep CVEs"),
    ("15", "systemd-persistence-scanner", "Go", "Persistence"),
]

TIMELINE = [
    ("2025 Q2", "base64 · c2-beacon"),
    ("2025 Q3", "caesar · canary"),
    ("2025 Q4", "dns · firewall · hash"),
    ("2026 Q1", "keylogger · CIS · eBPF"),
    ("2026 Q2", "scrubber · PCAP · ports · CVE · persist"),
]

STATUS = [
    ("Ready on Windows", "base64, caesar, dns, keylogger, scrubber, netanal, svscan, sentinel"),
    ("Docker / extra deps", "c2-beacon, canary-token-generator"),
    ("Linux / WSL preferred", "CIS auditor, eBPF tracer, firewall (V), hash-cracker, port-scanner"),
]


def inventory_board() -> None:
    cols, rows = 3, 5
    cell_w, cell_h = 400, 92
    pad, gap = 24, 14
    w = pad * 2 + cols * cell_w + (cols - 1) * gap
    h = 70 + pad + rows * cell_h + (rows - 1) * gap + 20
    img = Image.new("RGB", (w, h), DEEP)
    d = ImageDraw.Draw(img, "RGBA")
    d.text((pad, 22), "Laboratory inventory", fill=TEAL, font=font(24, serif=True))
    d.text((pad, 52), "Fifteen tools · click folder names in the README below", fill=MUTED, font=font(13))

    for i, (num, name, stack, role) in enumerate(TOOLS):
        r, c = divmod(i, cols)
        # wait - 3 cols 5 rows means i//3 is row, i%3 is col for 15 items
        r, c = i // cols, i % cols
        x = pad + c * (cell_w + gap)
        y = 78 + r * (cell_h + gap)
        d.rounded_rectangle([x, y, x + cell_w, y + cell_h], radius=12, fill=CARD, outline=LINE, width=2)
        d.text((x + 16, y + 14), num, fill=TEAL, font=font(12))
        d.text((x + 48, y + 12), name, fill=PAPER, font=font(16, serif=True))
        d.text((x + 16, y + 44), role, fill=FOG, font=font(13))
        # stack chip
        tw = int(d.textlength(stack, font=font(12))) + 16
        d.rounded_rectangle([x + cell_w - tw - 16, y + 48, x + cell_w - 14, y + 72], radius=8, fill=(20, 40, 48), outline=LINE)
        d.text((x + cell_w - tw - 8, y + 52), stack, fill=TEAL, font=font(12))

    img.save(OUT / "inventory-board.png", "PNG", optimize=True)
    print("inventory-board.png", w, h)


def timeline_board() -> None:
    w, h = 1280, 210
    img = Image.new("RGB", (w, h), DEEP)
    d = ImageDraw.Draw(img, "RGBA")
    d.rounded_rectangle([1, 1, w - 2, h - 2], radius=16, outline=LINE, width=2)
    d.text((36, 22), "Build arc", fill=TEAL, font=font(22, serif=True))
    d.text((36, 52), "April 2025 → June 2026", fill=MUTED, font=font(13))
    d.line([(60, 120), (1220, 120)], fill=(*TEAL, 70), width=2)

    xs = [140, 380, 620, 860, 1100]
    for x, (era, tools) in zip(xs, TIMELINE):
        d.ellipse([x - 7, 113, x + 7, 127], fill=TEAL)
        d.text((x - 36, 78), era, fill=TEAL, font=font(13))
        # wrap tools text
        d.text((x - 70, 140), tools, fill=PAPER, font=font(13))

    img.save(OUT / "timeline-board.png", "PNG", optimize=True)
    print("timeline-board.png")


def status_board() -> None:
    w, h = 1280, 220
    img = Image.new("RGB", (w, h), DEEP)
    d = ImageDraw.Draw(img, "RGBA")
    d.text((36, 22), "Runtime map (Windows host)", fill=TEAL, font=font(22, serif=True))
    d.text((36, 52), "Where each tool is happiest to run", fill=MUTED, font=font(13))

    colors = [(15, 60, 55), (40, 45, 30), (30, 40, 60)]
    y = 80
    for i, (title, body) in enumerate(STATUS):
        d.rounded_rectangle([36, y, w - 36, y + 38], radius=10, fill=CARD, outline=LINE)
        d.rectangle([36, y, 44, y + 38], fill=TEAL if i == 0 else (LINE if i == 1 else (70, 100, 140)))
        d.text((58, y + 10), title, fill=PAPER, font=font(14, serif=True))
        d.text((280, y + 11), body, fill=FOG, font=font(12))
        y += 46

    img.save(OUT / "status-board.png", "PNG", optimize=True)
    print("status-board.png")


if __name__ == "__main__":
    inventory_board()
    timeline_board()
    status_board()
