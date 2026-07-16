"""Generate creative README assets for cybersecurity-projects."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / "assets"
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


def banner() -> None:
    w, h = 1280, 380
    img = Image.new("RGB", (w, h))
    wash(img, (7, 17, 26), (12, 38, 40))
    d = ImageDraw.Draw(img, "RGBA")
    for x in range(0, w, 30):
        d.line([(x, 0), (x, h)], fill=(*TEAL, 12))
    for y in range(0, h, 30):
        d.line([(0, y), (w, y)], fill=(*TEAL, 12))

    # schematic rack of 15 nodes
    for i in range(15):
        x = 820 + (i % 5) * 70
        y = 90 + (i // 5) * 70
        d.rounded_rectangle([x, y, x + 48, y + 48], radius=8, outline=(*TEAL, 90), width=2)
        d.text((x + 14, y + 14), f"{i+1:02d}", fill=(*TEAL, 180), font=font(12))

    d.text((56, 70), "LABORATORY CORPUS", fill=FOG, font=font(15, serif=True))
    d.text((56, 112), "cybersecurity-projects", fill=PAPER, font=font(46, serif=True))
    d.rectangle([56, 178, 280, 181], fill=TEAL)
    d.text((56, 204), "15 hands-on tools for scanning, detection,", fill=PAPER, font=font(22, serif=True))
    d.text((56, 236), "hardening, and analysis — built as reproducible labs.", fill=PAPER, font=font(22, serif=True))
    d.text((56, 300), "Python · Go · C++ · Shell · Linux    ·    Apr 2025 → Jun 2026", fill=MUTED, font=font(14))
    d.text((56, 332), "Author: Winston Mascarenhas", fill=FOG, font=font(14))

    img.save(OUT / "repo-banner.png", "PNG", optimize=True)
    print("repo-banner.png")


def domains() -> None:
    w, h = 1280, 170
    img = Image.new("RGB", (w, h), DEEP)
    d = ImageDraw.Draw(img, "RGBA")
    cards = [
        ("01", "Recon", "DNS · ports · encode"),
        ("02", "Detect", "Logs · canaries · eBPF"),
        ("03", "Harden", "CIS · firewall · persist"),
        ("04", "Analyze", "PCAP · hashes · metadata"),
    ]
    x = 24
    for num, title, sub in cards:
        d.rounded_rectangle([x, 20, x + 296, 150], radius=14, fill=CARD, outline=LINE, width=2)
        d.text((x + 24, 40), num, fill=TEAL, font=font(13))
        d.text((x + 24, 72), title, fill=PAPER, font=font(26, serif=True))
        d.text((x + 24, 112), sub, fill=FOG, font=font(14))
        x += 312
    img.save(OUT / "repo-domains.png", "PNG", optimize=True)
    print("repo-domains.png")


def ethics() -> None:
    w, h = 1280, 120
    img = Image.new("RGB", (w, h))
    wash(img, (10, 22, 30), (12, 30, 34))
    d = ImageDraw.Draw(img, "RGBA")
    d.text((48, 34), "Authorized labs only.", fill=PAPER, font=font(24, serif=True))
    d.text(
        (48, 72),
        "Educational tooling — use exclusively on systems you own or have explicit permission to test.",
        fill=FOG,
        font=font(15),
    )
    img.save(OUT / "repo-ethics.png", "PNG", optimize=True)
    print("repo-ethics.png")


if __name__ == "__main__":
    banner()
    domains()
    ethics()
