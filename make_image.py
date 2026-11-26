#!/usr/bin/env python3
"""Draw news.png: six world news stories from Wednesday 25 November 2026.
Everything is drawn in code with Pillow. No AI-generated imagery.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

NAVY = (13, 27, 62)
NAVY_LIGHT = (24, 48, 96)
BG = (232, 236, 242)
WHITE = (255, 255, 255)
INK = (20, 28, 45)
MUTED = (70, 82, 104)
GOLD = (245, 176, 65)

ACCENTS = [
    (214, 48, 49),    # 1 tanker / red
    (230, 126, 34),   # 2 refinery / orange
    (39, 174, 96),    # 3 tariffs / green
    (41, 128, 185),   # 4 space / blue
    (22, 160, 133),   # 5 treaty / teal
    (142, 68, 173),   # 6 samara / purple
]


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_icon(d, kind, box, accent):
    x0, y0, x1, y1 = box
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    if kind == "tanker":
        # sea
        d.rectangle([x0, y1 - 18, x1, y1], fill=(52, 152, 219))
        d.rectangle([x0, y1 - 14, x1, y1 - 10], fill=(41, 128, 185))
        # hull
        d.polygon([(x0 + 8, cy - 6), (x1 - 8, cy - 6), (x1 - 22, cy + 16),
                   (x0 + 22, cy + 16)], fill=(44, 62, 80))
        d.rectangle([x0 + 14, cy - 26, x0 + 34, cy - 6], fill=(236, 240, 241))
        d.rectangle([x0 + 44, cy - 18, x1 - 14, cy - 6], fill=accent)
        d.ellipse([x0 + 40, cy - 34, x0 + 52, cy - 22], fill=(90, 90, 90))
        # flame / smoke above hull
        d.polygon([(cx - 8, cy - 8), (cx + 2, cy - 34), (cx + 12, cy - 8)],
                  fill=(245, 176, 65))
        d.polygon([(cx - 2, cy - 8), (cx + 4, cy - 24), (cx + 9, cy - 8)],
                  fill=(231, 76, 60))
    elif kind == "refinery":
        d.rectangle([x0 + 14, y1 - 34, x0 + 30, y1 - 8], fill=(90, 100, 116))
        d.rectangle([x0 + 38, y1 - 52, x0 + 54, y1 - 8], fill=(70, 82, 104))
        d.rectangle([x0 + 62, y1 - 26, x0 + 78, y1 - 8], fill=(90, 100, 116))
        d.polygon([(cx - 16, y1 - 52), (cx, y1 - 84), (cx + 16, y1 - 52)],
                  fill=(245, 176, 65))
        d.polygon([(cx - 8, y1 - 52), (cx, y1 - 70), (cx + 8, y1 - 52)],
                  fill=(231, 76, 60))
        d.rectangle([x0, y1 - 8, x1, y1], fill=(52, 73, 94))
    elif kind == "chart":
        d.line([x0 + 10, y1 - 12, x1 - 6, y1 - 12], fill=INK, width=3)
        d.line([x0 + 10, y0 + 24, x0 + 10, y1 - 12], fill=INK, width=3)
        bars = [26, 44, 58]
        for i, bh in enumerate(bars):
            bx = x0 + 18 + i * 24
            d.rectangle([bx, y1 - 12 - bh, bx + 16, y1 - 12], fill=accent)
        d.text((x0 + 56, y0 + 2), "20%", font=font(FONT_BOLD, 18), fill=accent)
    elif kind == "rocket":
        for sx, sy in [(x0 + 8, y0 + 10), (x1 - 12, y0 + 22), (x0 + 16, y1 - 16),
                       (x1 - 8, y1 - 8)]:
            d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=GOLD)
        d.polygon([(cx, y0 + 8), (cx + 16, cy + 6), (cx + 10, cy + 34),
                   (cx - 10, cy + 34), (cx - 16, cy + 6)], fill=(236, 240, 241),
                  outline=accent)
        d.ellipse([cx - 6, cy - 2, cx + 6, cy + 10], fill=accent)
        d.polygon([(cx - 10, cy + 34), (cx - 20, cy + 52), (cx - 4, cy + 38)],
                  fill=(231, 76, 60))
        d.polygon([(cx + 10, cy + 34), (cx + 20, cy + 52), (cx + 4, cy + 38)],
                  fill=(231, 76, 60))
        d.polygon([(cx - 6, cy + 34), (cx, cy + 62), (cx + 6, cy + 34)],
                  fill=(245, 176, 65))
    elif kind == "island":
        d.rectangle([x0, y1 - 26, x1, y1], fill=(52, 152, 219))
        d.ellipse([x0 + 14, cy - 6, x1 - 14, cy + 26], fill=(39, 174, 96))
        d.ellipse([x0 + 30, cy - 22, x0 + 58, cy + 2], fill=(39, 174, 96))
        d.line([cx + 4, cy - 20, cx + 4, cy - 52], fill=(101, 67, 33), width=4)
        d.polygon([(cx + 4, cy - 52), (cx + 34, cy - 44), (cx + 4, cy - 36)],
                  fill=accent)
        d.ellipse([x1 - 26, y0 + 8, x1 - 10, y0 + 24], fill=GOLD)
    elif kind == "fire":
        d.rectangle([x0 + 12, y1 - 40, x0 + 28, y1 - 8], fill=(90, 100, 116))
        d.rectangle([x0 + 36, y1 - 58, x0 + 52, y1 - 8], fill=(70, 82, 104))
        d.rectangle([x0 + 60, y1 - 30, x0 + 76, y1 - 8], fill=(90, 100, 116))
        d.polygon([(cx - 20, y1 - 40), (cx - 4, y1 - 82), (cx + 8, y1 - 52),
                   (cx + 22, y1 - 80), (cx + 26, y1 - 40)], fill=(245, 176, 65))
        d.polygon([(cx - 10, y1 - 40), (cx, y1 - 62), (cx + 12, y1 - 40)],
                  fill=(231, 76, 60))
        d.ellipse([x0 + 8, y0 + 6, x0 + 24, y0 + 22], fill=(149, 165, 166))
        d.ellipse([x0 + 24, y0 + 2, x0 + 38, y0 + 16], fill=(189, 195, 199))


STORIES = [
    ("TANKERS HIT IN HORMUZ", "Middle East",
     "Iran's Revolutionary Guard Corps said two oil tankers struck naval mines in the Strait of Hormuz, exploding and catching fire.",
     "tanker"),
    ("HOUTHIS HIT SAUDI REFINERY", "Middle East",
     "Yemen's Houthis said they attacked Saudi Arabia's Ras Tanura oil refinery; a Houthi strike on a Riyadh skyscraper injured 11 people, per Saudi Civil Defense.",
     "refinery"),
    ("US TARIFFS UP TO 20%", "Economy",
     "The Trump administration proposed new tariffs of up to 20% on China, the EU and 12 other major trading partners, after an 8-month probe into excess manufacturing capacity.",
     "chart"),
    ("PAKISTAN'S FIRST ASTRONAUT", "Space",
     "China's Shenzhou-24 reached orbit on 25 November carrying Pakistani Air Force pilot Muhammad Zeeshan Ali alongside two Chinese astronauts; it docked at China's space station.",
     "rocket"),
    ("SOLOMON ISLANDS\u2013AUSTRALIA TREATY", "Pacific",
     "Solomon Islands and Australia signed a treaty precluding any foreign military or security base on Solomon Islands.",
     "island"),
    ("SAMARA REFINERIES HIT", "Ukraine",
     "Ukrainian drones struck two Rosneft refineries in Russia's Samara region overnight into 25 November, setting fires at Syzran and Kuibyshev; the Zaporizhzhia nuclear plant lost external power after shelling and switched to emergency generators (IAEA).",
     "fire"),
]


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # Header
    d.rectangle([0, 0, W, 148], fill=NAVY)
    d.rectangle([0, 148, W, 154], fill=GOLD)
    f_title = font(FONT_BOLD, 58)
    f_date = font(FONT_BOLD, 34)
    title = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(title, font=f_title)) / 2, 18), title,
           font=f_title, fill=WHITE)
    date = "Wednesday 25 November 2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, 92), date,
           font=f_date, fill=GOLD)

    # Panels: 2 cols x 3 rows
    margin = 10
    gap = 10
    pw = (W - 2 * margin - gap) // 2
    ph = (H - 164 - 2 * margin - 2 * gap) // 3
    f_head = font(FONT_BOLD, 21)
    f_tag = font(FONT_BOLD, 13)
    f_sum = font(FONT, 16)

    for i, (headline, tag, summary, kind) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = margin + col * (pw + gap)
        y0 = 164 + margin + row * (ph + gap)
        x1, y1 = x0 + pw, y0 + ph
        accent = ACCENTS[i]
        d.rounded_rectangle([x0, y0, x1, y1], radius=12, fill=WHITE)
        d.rounded_rectangle([x0, y0, x1, y0 + 8], radius=4, fill=accent)
        # icon box (left)
        ix0, iy0, ix1, iy1 = x0 + 14, y0 + 20, x0 + 118, y0 + 118
        d.rectangle([ix0, iy0, ix1, iy1], fill=(238, 242, 247),
                    outline=(210, 218, 228))
        draw_icon(d, kind, (ix0 + 4, iy0 + 4, ix1 - 4, iy1 - 4), accent)
        # tag + headline (right of icon)
        tx = x0 + 132
        tw = x1 - tx - 14
        d.text((tx, y0 + 20), tag.upper(), font=f_tag, fill=accent)
        lines = wrap(d, headline, f_head, tw)
        ly = y0 + 40
        for ln in lines[:3]:
            d.text((tx, ly), ln, font=f_head, fill=INK)
            ly += 25
        # summary below icon row
        sy = y0 + 132
        slines = wrap(d, summary, f_sum, x1 - x0 - 28)
        for ln in slines[:6]:
            d.text((x0 + 14, sy), ln, font=f_sum, fill=MUTED)
            sy += 21

    img.save("news.png", optimize=True)
    print("saved news.png 1024x1024")


if __name__ == "__main__":
    main()
