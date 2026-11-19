#!/usr/bin/env python3
"""Render the news-image-20261118 entry: one front-page image summing up the
world news of Wednesday 18 November 2026.

Deterministic: no clock, no randomness, no network. Same input -> same bytes.
Run:  python3 generate.py            (writes entry.png next to this file)
Requires Pillow + DejaVu fonts locally; the entry itself (main.ts) only copies
the finished entry.png, so the grader needs nothing beyond Node's stdlib.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (22, 21, 19)
RED = (166, 25, 46)
BLUE = (29, 78, 121)
GOLD = (180, 138, 44)
GREY = (90, 86, 78)
RULE = (201, 194, 176)
TINT_BLUE = (214, 228, 238)
TINT_RED = (240, 216, 212)
TINT_GOLD = (240, 230, 203)
TINT_GREEN = (216, 232, 214)
TINT_GREY = (232, 228, 218)
SEA = (46, 110, 158)
SKY = (178, 208, 230)


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(d, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, fnt, fill=INK, leading=None, spacing=0):
    """Draw lines; leading defaults to 1.25 * size. Returns y after block."""
    lh = leading if leading is not None else int(fnt.size * 1.28)
    for line in lines:
        d.text((x, y), line, font=fnt, fill=fill)
        y += lh
    return y


def hrule(d, x0, x1, y, fill=INK, width=2):
    d.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- icons
def icon_gulf(d, x, y, w, h):
    """Ship on the sea under an explosion burst."""
    d.rectangle([x, y, x + w, y + h], fill=TINT_BLUE)
    # burst
    cx, cy, r = x + w * 0.72, y + h * 0.30, 26
    pts = []
    import math
    for i in range(16):
        ang = math.pi * i / 8
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    d.polygon(pts, fill=(232, 120, 40))
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(246, 196, 70))
    # sea
    d.rectangle([x, y + h * 0.62, x + w, y + h], fill=SEA)
    d.line([(x, y + h * 0.62), (x + w, y + h * 0.62)], fill=(255, 255, 255), width=2)
    # ship
    d.polygon([(x + 18, y + h * 0.62), (x + 150, y + h * 0.62),
               (x + 138, y + h * 0.86), (x + 32, y + h * 0.86)], fill=INK)
    d.rectangle([x + 62, y + h * 0.34, x + 96, y + h * 0.62], fill=INK)
    d.line([(x + 78, y + h * 0.34), (x + 78, y + h * 0.18)], fill=INK, width=3)


def icon_bridge(d, x, y, w, h):
    """Bridge deck with the middle span collapsed into the water."""
    d.rectangle([x, y, x + w, y + h], fill=TINT_GREY)
    # sky / water
    d.rectangle([x, y + h * 0.66, x + w, y + h], fill=SEA)
    # towers
    d.rectangle([x + 30, y + 8, x + 38, y + h * 0.66], fill=INK)
    d.rectangle([x + w - 38, y + 8, x + w - 30, y + h * 0.66], fill=INK)
    # deck, left and right of the gap
    d.rectangle([x, y + h * 0.42, x + w * 0.40, y + h * 0.42 + 8], fill=INK)
    d.rectangle([x + w * 0.60, y + h * 0.42, x + w, y + h * 0.42 + 8], fill=INK)
    # collapsed span, tilted down into the water
    d.polygon([(x + w * 0.40, y + h * 0.42), (x + w * 0.60, y + h * 0.42),
               (x + w * 0.56, y + h * 0.42 + 10), (x + w * 0.44, y + h * 0.80)],
              fill=(120, 30, 30))
    # cables
    d.line([(x + 34, y + 10), (x + w * 0.40, y + h * 0.42)], fill=INK, width=2)
    d.line([(x + w - 34, y + 10), (x + w * 0.60, y + h * 0.42)], fill=INK, width=2)


def icon_senate(d, x, y, w, h):
    """Capitol dome over a ballot box reading 56-44."""
    d.rectangle([x, y, x + w, y + h], fill=TINT_BLUE)
    cx = x + w // 2
    # dome
    d.pieslice([cx - 44, y + 0, cx + 44, y + 44], 180, 360, fill=INK)
    d.rectangle([cx - 48, y + 22, cx + 48, y + 28], fill=INK)
    for i in range(-2, 3):
        d.rectangle([cx + i * 19 - 3, y + 28, cx + i * 20 + 3, y + 40], fill=INK)
    d.rectangle([cx - 54, y + 40, cx + 54, y + 45], fill=INK)
    # ballot box with 56-44 centred inside it
    d.rectangle([cx - 42, y + 50, cx + 42, y + h - 2], fill=(255, 255, 255),
                outline=INK, width=3)
    d.line([(cx - 16, y + 48), (cx + 16, y + 48)], fill=INK, width=4)
    f = SANS_B(16)
    t = "56-44"
    d.text((cx - d.textlength(t, font=f) / 2, y + h - 25), t, font=f, fill=RED)


def icon_chip(d, x, y, w, h):
    """Microchip with a rising chart arrow."""
    d.rectangle([x, y, x + w, y + h], fill=TINT_GREEN)
    # chip
    d.rectangle([x + 84, y + 22, x + 178, y + h - 12], fill=INK)
    d.rectangle([x + 108, y + 42, x + 154, y + h - 32], outline=(120, 200, 120), width=3)
    for i in range(4):
        px = x + 100 + i * 20
        d.line([(px, y + 10), (px, y + 22)], fill=INK, width=4)
        d.line([(px, y + h - 12), (px, y + h - 2)], fill=INK, width=4)
    # rising arrow
    pts = [(x + 196, y + h - 26), (x + 232, y + 44), (x + 258, y + 60),
           (x + 288, y + 18)]
    d.line(pts, fill=RED, width=6)
    d.polygon([(x + 288, y + 18), (x + 268, y + 16), (x + 286, y + 36)], fill=RED)


def icon_ebola(d, x, y, w, h):
    """Spiked microbe."""
    import math
    d.rectangle([x, y, x + w, y + h], fill=TINT_RED)
    cx, cy = x + w // 2, y + h // 2
    for i in range(12):
        ang = math.pi * i / 6
        x1, y1 = cx + 26 * math.cos(ang), cy + 26 * math.sin(ang)
        x2, y2 = cx + 40 * math.cos(ang), cy + 40 * math.sin(ang)
        d.line([(x1, y1), (x2, y2)], fill=RED, width=5)
        d.ellipse([x2 - 4, y2 - 4, x2 + 4, y2 + 4], fill=RED)
    d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=RED)
    d.ellipse([cx - 14, cy - 18, cx - 2, cy - 6], fill=(255, 255, 255))
    d.ellipse([cx + 4, cy + 6, cx + 16, cy + 18], fill=(255, 255, 255))


def icon_cyclone(d, x, y, w, h):
    """Cyclone spiral."""
    import math
    d.rectangle([x, y, x + w, y + h], fill=TINT_BLUE)
    cx, cy = x + w // 2, y + h // 2
    for turn in range(3):
        pts = []
        for i in range(0, 61):
            ang = math.pi * i / 30 + turn * 2.1
            r = 8 + i * 0.55
            pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        d.line(pts, fill=BLUE, width=5)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED)


def draw_flags(d, x, y, w, h):
    """Three flags (China, Russia, USA) over a Shenzhen skyline."""
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    # skyline
    import random
    rnd = random.Random(18)  # fixed seed: same skyline every run
    bx = x + 8
    while bx < x + w - 30:
        bw = rnd.randint(22, 42)
        bh = rnd.randint(40, 110)
        d.rectangle([bx, y + h - bh, bx + bw, y + h], fill=(38, 52, 66))
        for wy in range(y + h - bh + 8, y + h - 8, 14):
            for wx in range(bx + 5, bx + bw - 4, 12):
                if rnd.random() < 0.4:
                    d.rectangle([wx, wy, wx + 5, wy + 7], fill=(246, 196, 70))
        bx += bw + 6
    # ground
    d.rectangle([x, y + h - 14, x + w, y + h], fill=(24, 34, 44))
    # flags on poles, left to right: China, Russia, USA
    fw, fh = 86, 56
    gap = (w - 3 * fw) // 4
    specs = ["CN", "RU", "US"]
    for i, spec in enumerate(specs):
        fx = x + gap + i * (fw + gap)
        fy = y + 16
        d.line([(fx + fw // 2, fy), (fx + fw // 2, y + h - 14)], fill=INK, width=4)
        if spec == "CN":
            d.rectangle([fx, fy, fx + fw, fy + fh], fill=(222, 41, 16))
            d.ellipse([fx + 8, fy + 8, fx + 24, fy + 24], fill=(255, 222, 0))
            for sx, sy in [(34, 10), (44, 18), (44, 30), (34, 38)]:
                d.ellipse([fx + sx, fy + sy, fx + sx + 6, fy + sy + 6],
                          fill=(255, 222, 0))
        elif spec == "RU":
            d.rectangle([fx, fy, fx + fw, fy + fh // 3], fill=(255, 255, 255))
            d.rectangle([fx, fy + fh // 3, fx + fw, fy + 2 * fh // 3], fill=(0, 57, 166))
            d.rectangle([fx, fy + 2 * fh // 3, fx + fw, fy + fh], fill=(213, 0, 0))
        else:
            for s in range(7):
                d.rectangle([fx, fy + s * 8, fx + fw, fy + s * 8 + 8],
                            fill=(178, 34, 52) if s % 2 == 0 else (255, 255, 255))
            d.rectangle([fx, fy, fx + 36, fy + 30], fill=(60, 59, 110))
            for r in range(3):
                for c in range(4):
                    d.ellipse([fx + 4 + c * 9, fy + 4 + r * 9,
                               fx + 7 + c * 9, fy + 7 + r * 9], fill=(255, 255, 255))


# ---------------------------------------------------------------- page
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 28  # margin

    # ---- masthead
    title = "THE WORLD IN ONE DAY"
    f_title = SERIF_B(60)
    d.text(((W - d.textlength(title, font=f_title)) / 2, 18), title,
           font=f_title, fill=INK)
    hrule(d, M, W - M, 96, width=3)
    hrule(d, M, W - M, 101, width=1)
    date_line = "WEDNESDAY  •  18 NOVEMBER 2026"
    f_date = SANS_B(27)
    d.text(((W - d.textlength(date_line, font=f_date)) / 2, 110), date_line,
           font=f_date, fill=RED)
    sub = "Seven stories that defined the day, as reported"
    f_sub = SERIF(20)
    d.text(((W - d.textlength(sub, font=f_sub)) / 2, 146), sub,
           font=f_sub, fill=GREY)
    hrule(d, M, W - M, 178, fill=RULE, width=1)

    # ---- lead story: Shenzhen summit
    lx, ly = M, 192
    lw = 560  # text column width
    d.text((lx, ly), "DIPLOMACY  —  SHENZHEN, CHINA", font=SANS_B(19), fill=RED)
    head = wrap(d, "Three leaders, one summit in Shenzhen", SERIF_B(45), lw)
    y = text_block(d, lx, ly + 28, head, SERIF_B(45), leading=50)
    dek = ("Xi Jinping and Vladimir Putin open talks in Shenzhen, a day "
           "before Thursday's first-ever three-way summit with Donald Trump.")
    y = text_block(d, lx, y + 8, wrap(d, dek, SANS(21), lw), SANS(21), leading=28)
    y = text_block(d, lx, y + 6,
                   wrap(d, "Trump is greeted by Xi on the tarmac as APEC opens.",
                        SANS(18), lw), SANS(18), fill=GREY, leading=24)
    # illustration, right of the lead text
    ix, iy, iw, ih = 620, 192, W - M - 620, 236
    d.rectangle([ix - 1, iy - 1, ix + iw + 1, iy + ih + 1], outline=INK, width=2)
    draw_flags(d, ix, iy, iw, ih)

    hrule(d, M, W - M, 444, width=2)

    # ---- six story cards, 3 x 2
    cards = [
        ("CONFLICT — THE GULF", "US strikes Iran site; Tehran hits back",
         "US jets hit a missile site on Qeshm Island. Iran says it fired "
         "on US sites in Kuwait and Bahrain.", icon_gulf),
        ("WAR IN UKRAINE", "Kerch Bridge road span collapses",
         "A second day of Ukrainian strikes brings down the road arch. "
         "Two killed; rail traffic partly resumes.", icon_bridge),
        ("US MIDTERMS", "Peltola wins Alaska; Senate 56–44",
         "The Democrat beats two-term Republican Dan Sullivan in the last "
         "Senate race to be called.", icon_senate),
        ("TECH — EARNINGS", "Nvidia posts record $115.8bn quarter",
         "Revenue more than doubles in the first report since Jensen Huang "
         "resigned.", icon_chip),
        ("HEALTH — DR CONGO", "Ebola outbreak passes 11,000 cases",
         "The UN says cases have more than doubled in three months, with "
         "5,400 deaths.", icon_ebola),
        ("WEATHER — BAY OF BENGAL", "Cyclone Akvan bears down on India",
         "Landfall is forecast on the Andhra Pradesh coast on Friday, with "
         "gusts to 145 km/h.", icon_cyclone),
    ]
    cw = (W - 2 * M - 2 * 16) // 3
    ch = 238
    for i, (kicker, headline, dek, icon) in enumerate(cards):
        cx = M + (i % 3) * (cw + 16)
        cy = 460 + (i // 3) * (ch + 14)
        icon(d, cx, cy, cw, 84)
        d.text((cx, cy + 92), kicker, font=SANS_B(15), fill=RED)
        hy = text_block(d, cx, cy + 114,
                        wrap(d, headline, SERIF_B(25), cw), SERIF_B(25),
                        leading=29)
        text_block(d, cx, hy + 4, wrap(d, dek, SANS(17), cw), SANS(17),
                   fill=(52, 50, 46), leading=22)

    # ---- ticker
    ty = 956
    hrule(d, M, W - M, ty, width=2)
    ticker = ("ALSO TODAY:   US loses measles-free status after 26 years   •   "
              "Trump hails “very big” Philippines trade deal   •   "
              "Category 5 Cyclone Xavier hits the Cook Islands")
    f_tick = SANS_B(16)
    lines = wrap(d, ticker, f_tick, W - 2 * M)
    text_block(d, M, ty + 8, lines, f_tick, fill=INK, leading=20)

    # ---- footer
    foot = ("Wednesday 18 November 2026  •  All stories as reported on the day  •  "
            "Sources: Reuters, AP, AFP, BBC, PAHO, United Nations")
    f_foot = SANS(13)
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, 1010), foot,
           font=f_foot, fill=GREY)
    return img


def main():
    img = render()
    out = os.path.join(HERE, "entry.png")
    img.save(out, format="PNG", optimize=True)
    print("wrote", out, img.size, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
