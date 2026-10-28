#!/usr/bin/env python3
"""Generate 1200×630 Open Graph / Twitter share cards for the Defrag blog.

Reads Zola +++ TOML front matter under content/, writes PNGs to static/og/.
Home card: static/og/default.png
Post cards: static/og/<slug>.png  (slug = filename stem)
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
OUT = ROOT / "static" / "og"
W, H = 1200, 630

# Brand tokens from sites/defrag styles/main.css
VOID = (7, 8, 12)
PANEL = (13, 16, 23)
LINE = (29, 34, 45)
FOG = (211, 216, 226)
MIST = (127, 136, 153)
SIGNAL = (91, 157, 255)
WHITE = (255, 255, 255)


def load_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = []
    if bold:
        candidates += [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
            "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
        ]
    candidates += [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
        "/usr/share/fonts/TTF/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def parse_front_matter(text: str) -> dict:
    if not text.startswith("+++"):
        return {}
    end = text.find("+++", 3)
    if end < 0:
        return {}
    block = text[3:end]
    data: dict = {"tags": [], "title": "", "description": "", "date": "", "draft": False}
    # simple line parser (good enough for our posts)
    in_tags = False
    for raw in block.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("["):
            in_tags = line == "[taxonomies]"
            continue
        if in_tags and line.startswith("tags"):
            m = re.search(r"\[(.*)\]", line)
            if m:
                data["tags"] = [t.strip().strip('"') for t in m.group(1).split(",") if t.strip()]
            continue
        if "=" not in line:
            continue
        key, _, val = line.partition("=")
        key = key.strip()
        val = val.strip().strip('"')
        if key == "draft":
            data["draft"] = val.lower() == "true"
        elif key in ("title", "description", "date"):
            data[key] = val
    return data


def wrap(draw: ImageDraw.ImageDraw, text: str, font, max_width: int) -> list[str]:
    words = text.split()
    if not words:
        return []
    lines: list[str] = []
    cur = words[0]
    for w in words[1:]:
        trial = f"{cur} {w}"
        if draw.textlength(trial, font=font) <= max_width:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def draw_mark(draw: ImageDraw.ImageDraw, x: int, y: int, size: int = 48) -> None:
    # Four tiles — same mark as favicon / sites/defrag header
    gap = max(2, size // 16)
    tile = (size - gap) // 2
    radii = max(2, size // 16)
    opacities = [0.35, 0.55, 0.75, 1.0]
    coords = [(0, 0), (1, 0), (0, 1), (1, 1)]
    for (cx, cy), op in zip(coords, opacities):
        px = x + cx * (tile + gap)
        py = y + cy * (tile + gap)
        color = tuple(int(SIGNAL[i] * op + VOID[i] * (1 - op)) for i in range(3))
        draw.rounded_rectangle([px, py, px + tile, py + tile], radius=radii, fill=color)


def paint_card(title: str, subtitle: str, tags: list[str] | None = None) -> Image.Image:
    img = Image.new("RGB", (W, H), VOID)
    draw = ImageDraw.Draw(img)

    # Blueprint grid (subtle)
    for x in range(0, W, 44):
        draw.line([(x, 0), (x, H)], fill=LINE)
    for y in range(0, H, 44):
        draw.line([(0, y), (W, y)], fill=LINE)
    # Darken edges so grid reads as ground, not noise
    overlay = Image.new("RGBA", (W, H), (7, 8, 12, 180))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # Panel frame
    margin = 48
    draw.rounded_rectangle(
        [margin, margin, W - margin, H - margin],
        radius=18,
        outline=LINE,
        width=2,
        fill=PANEL,
    )

    draw_mark(draw, margin + 36, margin + 36, 52)

    brand = load_font(28, bold=True)
    draw.text((margin + 104, margin + 48), "DEFRAG", font=brand, fill=SIGNAL)

    kicker = load_font(18)
    draw.text((margin + 104, margin + 84), "engineering notes", font=kicker, fill=MIST)

    title_font = load_font(52, bold=True)
    max_tw = W - 2 * margin - 72
    title_lines = wrap(draw, title, title_font, max_tw)[:3]
    ty = margin + 160
    for line in title_lines:
        draw.text((margin + 36, ty), line, font=title_font, fill=WHITE)
        ty += 62

    if subtitle:
        sub_font = load_font(24)
        for line in wrap(draw, subtitle, sub_font, max_tw)[:2]:
            draw.text((margin + 36, ty + 12), line, font=sub_font, fill=MIST)
            ty += 34

    if tags:
        tag_font = load_font(18)
        tx, ty2 = margin + 36, H - margin - 70
        for tag in tags[:6]:
            label = f"#{tag}"
            tw = int(draw.textlength(label, font=tag_font)) + 24
            if tx + tw > W - margin - 36:
                break
            draw.rounded_rectangle([tx, ty2, tx + tw, ty2 + 34], radius=8, fill=LINE)
            draw.text((tx + 12, ty2 + 7), label, font=tag_font, fill=FOG)
            tx += tw + 10

    return img


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    # Default / home card
    paint_card(
        "Workshop notes from a blockchain skunkworks division.",
        "Indexers · community tools · archives — Rust, Mithril, Cloudflare-native",
        ["rust", "cardano", "cloudflare"],
    ).save(OUT / "default.png", optimize=True)
    print(f"wrote {OUT / 'default.png'}")

    posts = sorted((CONTENT / "posts").glob("*.md"))
    for path in posts:
        if path.name.startswith("_"):
            continue
        data = parse_front_matter(path.read_text())
        title = data.get("title") or path.stem.replace("-", " ").title()
        date = data.get("date") or ""
        tags = data.get("tags") or []
        subtitle = date
        if data.get("draft"):
            subtitle = (subtitle + " · draft").strip(" ·")
        out = OUT / f"{path.stem}.png"
        paint_card(title, subtitle, tags).save(out, optimize=True)
        print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
