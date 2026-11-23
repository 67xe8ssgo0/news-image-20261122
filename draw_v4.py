#!/usr/bin/env python3
"""Draw v4 of the entry image: a light, classic-newspaper front page with
a different angle from v3 — stories organised by region, a by-the-numbers
strip and an In Brief column set. 45 dated stories from Sunday
22 November 2026, each reported that day (Reuters, AP, BBC, Al Jazeera,
The Guardian, One Turn's day report). Output: news-2026-11-22-v4.png
(1024x1024, <= 1 MiB).
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FD = "/usr/share/fonts/truetype/noto"
S_BLACK = f"{FD}/NotoSerif-Black.ttf"
S_XBOLD = f"{FD}/NotoSerif-ExtraBold.ttf"
S_BOLD = f"{FD}/NotoSerif-Bold.ttf"
BLACK = f"{FD}/NotoSans-Black.ttf"
XBOLD = f"{FD}/NotoSans-ExtraBold.ttf"
BOLD = f"{FD}/NotoSans-Bold.ttf"
SEMI = f"{FD}/NotoSans-SemiBold.ttf"
REG = f"{FD}/NotoSans-Regular.ttf"

PAPER = (247, 243, 233)
CARD = (255, 253, 247)
INK = (16, 17, 22)
MUTED = (88, 90, 98)
RED = (178, 24, 38)
GOLD = (176, 124, 22)
TEAL = (8, 118, 110)
BLUE = (28, 78, 160)
GREEN = (28, 120, 62)
PURPLE = (104, 62, 168)
ORANGE = (196, 92, 16)
DARK = (14, 16, 24)
WHITE = (246, 248, 251)
DMUTED = (168, 178, 198)


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


def text_block(draw, xy, text, fnt, fill, max_w, leading=1.16, max_lines=None):
    x, y = xy
    lines = wrap(draw, text, fnt, max_w)
    if max_lines:
        lines = lines[:max_lines]
    lh = int(fnt.size * leading)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
M = 24

# ---------- masthead ----------
d.text((M, 6), "The World in One Day", font=F(S_BLACK, 56), fill=INK)
d.rectangle([M, 76, W - M, 79], fill=INK)
d.rectangle([M, 82, W - M, 83], fill=INK)
# date band
d.rectangle([M, 90, W - M, 126], fill=INK)
d.text((M + 14, 96), "SUNDAY, 22 NOVEMBER 2026", font=F(XBOLD, 25), fill=(255, 255, 255))
r = "45 STORIES • SIX REGIONS • ONE PAGE"
d.text((W - M - 14 - d.textlength(r, font=F(XBOLD, 17)), 100), r, font=F(XBOLD, 17), fill=(240, 196, 92))

# ---------- lead row ----------
LY = 138
d.rectangle([M, LY, 628, LY + 196], fill=CARD)
d.rectangle([M, LY, 628, LY + 5], fill=RED)
d.text((M + 16, LY + 13), "CLIMATE • ANTALYA, TÜRKIYE", font=F(BOLD, 13.5), fill=RED)
d.text((M + 16, LY + 33), "COP31 collapses:", font=F(S_BLACK, 40), fill=INK)
d.text((M + 16, LY + 79), "no deal on fossil fuels", font=F(S_BLACK, 40), fill=RED)
text_block(d, (M + 16, LY + 130),
           "The UN summit ends with nothing adopted — the first collapse since 2009 — "
           "after the EU, UK and Panama reject a final draft, the 'Antalya Pact', "
           "that never mentions fossil fuels.",
           F(SEMI, 14), (52, 54, 62), 572, max_lines=3)

def dark_card(y, tag, color, head, body):
    d.rectangle([644, y, W - M, y + 94], fill=DARK)
    d.rectangle([644, y, 648, y + 94], fill=color)
    d.text((660, y + 8), tag, font=F(BOLD, 12), fill=color)
    text_block(d, (660, y + 26), head, F(XBOLD, 19.5), WHITE, 322, leading=1.08, max_lines=1)
    text_block(d, (660, y + 54), body, F(REG, 12), DMUTED, 322, leading=1.15, max_lines=2)

dark_card(LY, "WAR • BAHRAIN", (240, 84, 96), "Iran strikes Bahrain",
          "Missiles hit US bases and a Sitra plant; two hurt. Iran claims two Patriot radars destroyed.")
dark_card(LY + 102, "WAR • UKRAINE", (240, 196, 92), "Flats hit near Kyiv",
          "A drone collapses a Dymer block: 2 dead, 14 missing, after a night of 400+ drones.")

# ---------- by the numbers ----------
NY = 346
d.rectangle([M, NY, W - M, NY + 34], fill=(238, 231, 214))
nums = [("400+", "drones fired at Ukraine in one night"),
        ("$50B", "LNG export project approved in Argentina"),
        ("52%", "cholesterol cut by a one-dose gene therapy"),
        ("720/9", "India's declared total vs New Zealand")]
x = M + 14
for big, small in nums:
    d.text((x, NY + 5), big, font=F(S_BLACK, 21), fill=RED)
    bw = d.textlength(big, font=F(S_BLACK, 21))
    text_block(d, (x + bw + 7, NY + 4), small, F(SEMI, 10.5), (52, 54, 62), 150, leading=1.1, max_lines=2)
    x += 244

# ---------- regions ----------
REGIONS = [
    ("EUROPE", BLUE, [
        ("Russian ship ablaze in the Baltic", "Sparta II burns off Finland after a drone strike; a corvette is hit in Libya."),
        ("Myanmar guilty of genocide", "The World Court at The Hague rules on the Rohingya case."),
        ("Denmark expels Russian attaché", "Copenhagen alleges a plot to kill a Ukrainian rapper at a concert."),
        ("France's protests roll on", "Sixth weekend of cost-of-living marches; 144 arrests on Saturday."),
    ]),
    ("MIDDLE EAST", RED, [
        ("Settlers torch West Bank cars", "12 vehicles burned in four villages near Ramallah; Israel opens inquiry."),
        ("Strikes continue across Gaza", "Three killed in a strike on a food truck near Deir al-Balah."),
        ("Houthis claim Saudi refinery hit", "Riyadh says it intercepted a missile over its western region."),
        ("Iran starts rationing power", "Scheduled blackouts begin as the cold season arrives."),
    ]),
    ("ASIA", PURPLE, [
        ("Trump–Xi–Putin summit in Shenzhen", "First trilateral meeting; joint note on nuclear risk, no Ukraine deal."),
        ("Factory fire in Indonesia", "Banten candy plant blaze kills 3; about 33 workers missing."),
        ("Fake liquor kills 11 in Manipur", "Methanol poisoning puts more than 180 in hospital in India."),
        ("Hong Kong's committee votes", "About 5,700 voters pick the electoral college that chooses the leader."),
    ]),
    ("AMERICAS", GREEN, [
        ("Cartel boss 'Chapo Isidro' captured", "Mexican special forces take the FBI-listed boss in Sinaloa; 11 die."),
        ("Palisades fire starter convicted", "A jury finds the man guilty over the 2025 Los Angeles fire that killed 12."),
        ("FBI crime database 'hacked'", "Washington probes a breach of the national crime information system."),
        ("Seattle airport arrests spark outcry", "Masked ICE agents detain two men on a jet bridge; governor protests."),
    ]),
    ("AFRICA & OCEANIA", ORANGE, [
        ("Drones hit Khartoum, UN damaged", "Strikes across Sudan's capital kill four and hit a UN compound."),
        ("Nigeria funeral boat capsizes", "At least 24 mourners die in the south of the country."),
        ("Cyclone Xavier weakens", "The Cook Islands keep an emergency in force; Nassau reports all safe."),
        ("Mlambo-Ngcuka dies at 71", "South Africa's first woman deputy president, ex-head of UN Women."),
    ]),
    ("SCIENCE & SPACE", TEAL, [
        ("BepiColombo reaches Mercury", "Orbit at last, eight years after launch — ESA and JAXA's joint mission."),
        ("AI 'proves' Riemann hypothesis", "An Anthropic researcher publishes the claim; checking may take years."),
        ("CRISPR cuts cholesterol 52%", "A single gene-editing dose holds its effect a year on, in a first trial."),
        ("Earth gains a mini-moon", "Asteroid 2026 QQ8 is briefly in orbit; astronomers say it is harmless."),
    ]),
]
RY = 392
RW, RH, RG = 314, 198, 9
for i, (name, color, stories) in enumerate(REGIONS):
    cx = M + (i % 3) * (RW + RG)
    cy = RY + (i // 3) * (RH + 8)
    d.rectangle([cx, cy, cx + RW, cy + RH], fill=CARD)
    d.rectangle([cx, cy, cx + RW, cy + 22], fill=color)
    d.text((cx + 10, cy + 4), name, font=F(XBOLD, 13), fill=(255, 255, 255))
    sy = cy + 30
    for head, body in stories:
        text_block(d, (cx + 10, sy), head, F(S_BOLD, 13.5), INK, RW - 20, leading=1.05, max_lines=1)
        text_block(d, (cx + 10, sy + 16), body, F(REG, 10.5), MUTED, RW - 20, leading=1.12, max_lines=2)
        sy += 42

# ---------- in brief ----------
BY = 806
d.text((M, BY), "IN BRIEF — ALSO ON 22 NOVEMBER", font=F(XBOLD, 16), fill=INK)
d.rectangle([M, BY + 24, W - M, BY + 26], fill=INK)
BRIEFS = [
    "S&P 500 slides 3.7% into correction",
    "EU–Indonesia trade deal signed after 10 years",
    "Belgium strike set to cancel all Monday flights",
    "Korea's education minister quits over AI cheating",
    "Mongolia faces a snap presidential vote",
    "Basra power-station fire kills 4, injures 30",
    "Saudi oil stored in Japan to triple: 24M barrels",
    "Whale genome sequenced from drone-caught breath",
    "Turkey seizes its last big independent TV channel",
    "Bolsonaro in intensive care in Brasília",
    "Eisenkot invites Likud to coalition talks",
    "UK and EU seal trade and youth-mobility deals",
]
cols = [BRIEFS[0:6], BRIEFS[6:12]]
for ci, col in enumerate(cols):
    x = M + ci * 326
    y = BY + 34
    for it in col:
        d.rectangle([x, y + 4, x + 6, y + 10], fill=RED)
        text_block(d, (x + 12, y), it, F(SEMI, 11), (30, 31, 38), 306, leading=1.1, max_lines=2)
        y += 19

# ---------- reader poll ----------
PX0, PY0, PX1, PY1 = 682, BY - 2, W - M, 946
d.rectangle([PX0, PY0, PX1, PY1], outline=INK, width=2)
d.rectangle([PX0, PY0, PX1, PY0 + 24], fill=RED)
d.text((PX0 + 10, PY0 + 5), "READER POLL", font=F(XBOLD, 13.5), fill=(255, 255, 255))
text_block(d, (PX0 + 10, PY0 + 30), "Which story defined the day?",
           F(S_BOLD, 14.5), INK, PX1 - PX0 - 20, leading=1.1, max_lines=2)
POLL = ["COP31 collapse", "Iran strikes Bahrain", "Kyiv drone attack", "Trump–Xi–Putin summit"]
py = PY0 + 54
for opt in POLL:
    d.rectangle([PX0 + 10, py + 2, PX0 + 22, py + 14], outline=INK, width=1)
    d.text((PX0 + 30, py), opt, font=F(SEMI, 12), fill=(30, 31, 38))
    py += 18
d.text((PX0 + 10, PY1 - 14), "Results in tomorrow's edition", font=F(REG, 10), fill=MUTED)

# ---------- sport band ----------
FY = 952
d.rectangle([M, FY, W - M, FY + 34], fill=INK)
d.text((M + 12, FY + 8), "SPORT", font=F(XBOLD, 15), fill=(240, 196, 92))
sport = "Verstappen wins Las Vegas by 0.639s • Leeds win 4-1 at Chelsea, first since 1999 • Wembanyama scores 50 for the Spurs"
d.text((M + 82, FY + 9), sport, font=F(SEMI, 12.5), fill=(255, 255, 255))
src = "Sources: Reuters • AP • BBC • Al Jazeera • The Guardian • formula1.com — every story dated Sunday 22 November 2026"
d.text((M, FY + 42), src, font=F(REG, 10.5), fill=MUTED)

img.save("/home/hatch/workspace/makefun/work/news-2026-11-22-v4.png", optimize=True)
import os
p = "/home/hatch/workspace/makefun/work/news-2026-11-22-v4.png"
print("saved", os.path.getsize(p), "bytes")
