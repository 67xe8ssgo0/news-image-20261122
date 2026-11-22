#!/usr/bin/env python3
"""Draw v3 of the entry image: an even denser front page summing up
Sunday 22 November 2026's world news in one 1024x1024 image.

42 dated stories, each reported that day (sources: Reuters, AP, BBC,
Al Jazeera, The Guardian, One Turn's day report). Output:
news-2026-11-22-v3.png (<= 1024x1024, <= 1 MiB).
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FONT_DIR = "/usr/share/fonts/truetype/noto"
BLACK = f"{FONT_DIR}/NotoSans-Black.ttf"
XBOLD = f"{FONT_DIR}/NotoSans-ExtraBold.ttf"
BOLD = f"{FONT_DIR}/NotoSans-Bold.ttf"
SEMI = f"{FONT_DIR}/NotoSans-SemiBold.ttf"
REG = f"{FONT_DIR}/NotoSans-Regular.ttf"

BG = (8, 10, 16)
PANEL = (17, 21, 32)
PANEL2 = (23, 29, 44)
WHITE = (246, 248, 251)
MUTED = (165, 176, 196)
RED = (235, 47, 66)
GOLD = (247, 183, 49)
TEAL = (45, 196, 182)
BLUE = (92, 156, 255)
GREEN = (96, 199, 110)
PURPLE = (178, 132, 255)
ORANGE = (255, 145, 66)


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
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


def text_block(draw, xy, text, fnt, fill, max_w, leading=1.18, max_lines=None):
    x, y = xy
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    lh = int(fnt.size * leading)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)
M = 26  # margin

# ---------- masthead ----------
d.text((M, 10), "THE WORLD IN ONE DAY", font=F(BLACK, 54), fill=WHITE)
d.rectangle([M, 76, W - M, 80], fill=RED)
d.text((M, 86), "SUNDAY, 22 NOVEMBER 2026", font=F(XBOLD, 24), fill=GOLD)
r = "42 STORIES • EVERY REGION • ONE PAGE"
d.text((W - M - d.textlength(r, font=F(XBOLD, 20)), 88), r, font=F(XBOLD, 20), fill=WHITE)

# ---------- hero row ----------
HY = 122
d.rectangle([M, HY, 640, HY + 218], fill=PANEL2)
d.rectangle([M, HY, 640, HY + 6], fill=RED)
d.text((M + 18, HY + 14), "CLIMATE • ANTALYA, TÜRKIYE", font=F(BOLD, 15), fill=RED)
d.text((M + 18, HY + 36), "COP31", font=F(BLACK, 60), fill=WHITE)
d.text((M + 18, HY + 100), "COLLAPSES", font=F(BLACK, 60), fill=RED)
text_block(d, (M + 18, HY + 172),
           "The climate summit ends with NO DEAL — the first collapse since 2009 — "
           "after the EU, UK and Panama reject a final draft that never once "
           "mentions fossil fuels.",
           F(SEMI, 15), MUTED, 576, max_lines=3)

def hero_card(y, tag, color, head, body):
    d.rectangle([656, y, W - M, y + 105], fill=PANEL)
    d.rectangle([656, y, 660, y + 105], fill=color)
    d.text((672, y + 9), tag, font=F(BOLD, 13), fill=color)
    text_block(d, (672, y + 28), head, F(XBOLD, 21), WHITE, 306, leading=1.1, max_lines=2)
    text_block(d, (672, y + 72), body, F(REG, 12.5), MUTED, 306, leading=1.15, max_lines=2)

hero_card(HY, "WAR • BAHRAIN", RED, "IRAN STRIKES BAHRAIN",
          "Missiles hit US bases and a Sitra plant; 2 hurt. Iran claims 2 Patriot radars destroyed.")
hero_card(HY + 113, "WAR • UKRAINE", GOLD, "FLATS HIT NEAR KYIV",
          "Drone collapses a Dymer block: 2 dead, 14 missing. Barrage: 400+ drones, 110 missiles.")

# ---------- story grid ----------
GRID = [
    ("BALTIC", BLUE, "RUSSIAN SHIP ABLAZE",
     "Cargo ship Sparta II burns in the Gulf of Finland after a drone strike; blast hits a corvette in Libya."),
    ("SHENZHEN", PURPLE, "TRUMP–XI–PUTIN SUMMIT",
     "First-ever trilateral meeting issues a joint declaration on nuclear risks; no Ukraine breakthrough."),
    ("MARKETS", RED, "STOCKS SLIDE 3.7%",
     "S&P 500 falls into correction as the AI sell-off deepens; Nvidia's worst weekly losing run since 2008."),
    ("THE HAGUE", TEAL, "MYANMAR: GENOCIDE",
     "The World Court rules Myanmar committed genocide against the Rohingya people."),
    ("WEST BANK", ORANGE, "SETTLERS TORCH CARS",
     "12 Palestinian vehicles burned in four villages near Ramallah; Israel opens an inquiry."),
    ("SUDAN", RED, "DRONES HIT KHARTOUM",
     "Strikes damage a UN compound in the capital; four people killed."),
    ("GAZA", ORANGE, "STRIKES GO ON",
     "Israeli strikes kill across Gaza; three die in a strike on a food truck near Deir al-Balah."),
    ("MEXICO", GREEN, "'CHAPO ISIDRO' TAKEN",
     "Special forces capture the FBI-listed cartel boss in Sinaloa; 11 killed in clashes."),
    ("SPACE", BLUE, "MERCURY, AT LAST",
     "BepiColombo enters orbit around Mercury after an eight-year journey from Earth."),
    ("INDONESIA", RED, "FACTORY FIRE",
     "Candy factory blaze in Banten kills 3; about 33 workers still missing."),
    ("TRADE", TEAL, "EU–INDONESIA DEAL",
     "Trade pact signed after 10 years of talks; 98.5% of EU tariffs go; 730M people covered."),
    ("GENEVA", PURPLE, "NO KILLER-ROBOT RULES",
     "UN talks on AI weapons end without binding rules; the Red Cross warns time is running out."),
]
GX, GY = M, 352
CW, CH, GAP = 237, 100, 8
for i, (tag, color, head, body) in enumerate(GRID):
    cx = GX + (i % 4) * (CW + GAP)
    cy = GY + (i // 4) * (CH + GAP)
    d.rectangle([cx, cy, cx + CW, cy + CH], fill=PANEL)
    d.rectangle([cx, cy, cx + CW, cy + 4], fill=color)
    d.text((cx + 10, cy + 9), tag, font=F(BOLD, 11), fill=color)
    text_block(d, (cx + 10, cy + 25), head, F(XBOLD, 15.5), WHITE, CW - 20, leading=1.08, max_lines=2)
    text_block(d, (cx + 10, cy + 59), body, F(REG, 11.5), MUTED, CW - 20, leading=1.14, max_lines=3)

# ---------- more of the day ----------
LY = 690
d.text((M, LY), "MORE OF THE DAY", font=F(XBOLD, 19), fill=GOLD)
d.rectangle([M, LY + 28, W - M, LY + 30], fill=GOLD)
MORE_L = [
    "AI 'proves' the Riemann hypothesis — checking begins",
    "One-shot CRISPR therapy cuts bad cholesterol by 52%",
    "Denmark expels Russian attaché over alleged plot",
    "Funeral boat capsizes in Nigeria: 24 dead",
    "Basra power-station fire kills 4, injures 30",
    "Korea's education minister quits in AI cheating row",
    "Fake liquor kills 11 in India's Manipur; 180 treated",
    "Hong Kong holds Election Committee vote",
    "Earth gains a mini-moon: asteroid 2026 QQ8",
    "Whale genome read from breath caught by a drone",
    "Shuri Castle hall restored, 7 years after the fire",
    "BTS win five awards at the MAMA ceremony in Osaka",
]
MORE_R = [
    "Saudi Arabia to triple oil stored in Japan: 24M bbl",
    "Sixth weekend of cost-of-living protests in France",
    "Man convicted of starting 2025 Palisades fire",
    "Argentina approves a $50 billion LNG export project",
    "FBI probes hack of its national crime database",
    "Turkey seizes last big independent TV channel",
    "Princess Kate says she is in remission from cancer",
    "Iran begins rationing power as cold season starts",
    "Belgium strike set to cancel all Monday flights",
    "Cyclone Xavier weakens near the Cook Islands",
    "Mongolia faces a snap presidential vote",
    "200 mascots gather in Saitama, Japan",
]
def more_list(x, items, y0):
    y = y0
    for it in items:
        d.rectangle([x, y + 4, x + 7, y + 11], fill=RED)
        d.text((x + 15, y), it, font=F(SEMI, 12.5), fill=WHITE)
        y += 19
    return y
more_list(M, MORE_L, LY + 40)
more_list(518, MORE_R, LY + 40)

# ---------- footer ----------
FY = 956
d.rectangle([M, FY, W - M, FY + 30], fill=GOLD)
sport = "SPORT — VERSTAPPEN WINS LAS VEGAS BY 0.639s • LEEDS WIN 4-1 AT CHELSEA • INDIA 720/9"
d.text((M + 12, FY + 6), sport, font=F(XBOLD, 14.5), fill=(10, 10, 10))
src = "Sources: Reuters • AP • BBC • Al Jazeera • The Guardian • formula1.com — all stories dated 22 Nov 2026"
d.text((M, FY + 36), src, font=F(REG, 11), fill=MUTED)

img.save("/home/hatch/workspace/makefun/news-image-20261122/news-2026-11-22-v3.png", optimize=True)
import os
p = "/home/hatch/workspace/makefun/news-image-20261122/news-2026-11-22-v3.png"
print("saved", os.path.getsize(p), "bytes")
