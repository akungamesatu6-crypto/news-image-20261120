#!/usr/bin/env python3
"""Compose the 20 Nov 2026 front page: 4 AI-illustrated panels + crisp PIL text.

Deterministic: same inputs -> same bytes. Output is JPEG bytes written to
entry.png (the bounty rules say the file is told apart by its first bytes
and the name stays entry.png either way). 1024x1024, well under 1 MiB.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
PANELS = os.path.join(HERE, "panels")

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (20, 20, 20)
GREY = (74, 74, 74)
RED = (178, 28, 28)
NAVY = (27, 42, 74)
NAVY_BAND = (16, 28, 54)

F_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
F_REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def tracked(draw, xy, text, fnt, fill, tracking=2):
    """Draw text with letter tracking; returns width used."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + tracking
    return x


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def crop_to(img, tw, th):
    """Center-crop to target aspect, then resize with LANCZOS."""
    sw, sh = img.size
    ta, sa = tw / th, sw / sh
    if sa > ta:  # too wide
        nw = int(sh * ta)
        x0 = (sw - nw) // 2
        img = img.crop((x0, 0, x0 + nw, sh))
    else:  # too tall
        nh = int(sw / ta)
        y0 = (sh - nh) // 2
        img = img.crop((0, y0, sw, y0 + nh))
    return img.resize((tw, th), Image.LANCZOS)


def main():
    page = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(page)

    # ---- Masthead -------------------------------------------------------
    d.text((26, 22), "THE WORLD IN ONE IMAGE", font=font(F_BOLD, 21), fill=NAVY)
    d.text((W - 26 - d.textlength("FRIDAY", font=font(F_BOLD, 21)), 22),
           "FRIDAY", font=font(F_BOLD, 21), fill=RED)
    d.text((26, 48), "20 NOVEMBER 2026", font=font(F_BOLD, 46), fill=INK)
    d.text((W - 26 - d.textlength("SIX STORIES · ONE DAY", font=font(F_BOLD, 17)), 66),
           "SIX STORIES · ONE DAY", font=font(F_BOLD, 17), fill=GREY)
    d.rectangle([26, 104, W - 26, 107], fill=INK)
    d.rectangle([26, 110, W - 26, 113], fill=RED)

    # ---- 2x2 grid --------------------------------------------------------
    stories = [
        ("icj.webp", "THE HAGUE · JUSTICE",
         "WORLD COURT RULES MYANMAR COMMITTED GENOCIDE",
         "First such finding against a state — the Rohingya, 9–6."),
        ("shenzhen.webp", "SHENZHEN · DIPLOMACY",
         "TRUMP, XI AND PUTIN MEET — AND SIGN A PEACE PACT",
         "First three-way summit ends in a joint declaration."),
        ("kyiv.webp", "KYIV · WAR",
         "RUSSIAN STRIKES KILL 8 AS KYIV'S BRIDGES BURN",
         "Ukraine hits the Crimea Bridge for a third time this week."),
        ("riyadh.webp", "RIYADH · CONFLICT",
         "HOUTHI MISSILE HITS RIYADH'S FINANCE TOWER",
         "Saudi defences intercept another missile and five drones."),
    ]
    col_w, img_h = 478, 272
    xs = [26, 26 + col_w + 16]
    ys = [130, 532]
    for i, (fn, kicker, head, deck) in enumerate(stories):
        x, y = xs[i % 2], ys[i // 2]
        img = Image.open(os.path.join(PANELS, fn)).convert("RGB")
        page.paste(crop_to(img, col_w, img_h), (x, y))
        d.rectangle([x, y, x + col_w - 1, y + img_h - 1], outline=INK, width=2)
        cy = y + img_h + 12
        tracked(d, (x, cy), kicker, font(F_BOLD, 15), RED, tracking=1)
        cy += 22
        for line in wrap(d, head, font(F_BOLD, 24), col_w)[:2]:
            d.text((x, cy), line, font=font(F_BOLD, 24), fill=INK)
            cy += 28
        for line in wrap(d, deck, font(F_REG, 16), col_w)[:2]:
            d.text((x, cy), line, font=font(F_REG, 16), fill=GREY)
            cy += 21

    # ---- Markets band ----------------------------------------------------
    d.rectangle([26, 934, W - 26, 978], fill=NAVY_BAND)
    d.text((40, 946), "MARKETS   S&P 500 −2.0%  ·  Nikkei −4.8%  ·  SoftBank −16%",
           font=font(F_BOLD, 18), fill=(255, 255, 255))
    d.text((40, 946), "MARKETS", font=font(F_BOLD, 18), fill=(255, 196, 66))
    d.text((W - 40 - d.textlength("ANTHROPIC IPO +17%", font=font(F_BOLD, 18)), 946),
           "ANTHROPIC IPO +17%", font=font(F_BOLD, 18), fill=(120, 220, 140))

    # ---- Footer ----------------------------------------------------------
    foot = "ALSO: KENYA DECLARES EBOLA OVER  ·  COP31 DROPS FOSSIL-FUEL PHASEOUT  ·  EU–UK SUMMIT IN BRUSSELS"
    d.text(((W - d.textlength(foot, font=font(F_REG, 14))) / 2, 990),
           foot, font=font(F_REG, 14), fill=GREY)

    out = os.path.join(HERE, "entry.png")
    page.save(out, "JPEG", quality=88, optimize=True)
    n = os.path.getsize(out)
    print(f"wrote {out}: {n} bytes ({n/1024:.0f} KiB), 1024x1024")
    assert n <= 1048576, "over 1 MiB!"
    # preview copy for visual check (same bytes)
    page.save(os.path.join(HERE, "entry_preview.jpg"), "JPEG", quality=88, optimize=True)


if __name__ == "__main__":
    main()
