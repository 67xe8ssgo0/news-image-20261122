#!/usr/bin/env python3
"""Sum up 22 November 2026's world news in one image.

Draws a single 1024x1024 newspaper-style front page with Pillow.
Output: news-2026-11-22.png (must stay <= 1024x1024 and <= 1 MiB).
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FONT_DIR = "/usr/share/fonts/truetype/noto"
BLACK = f"{FONT_DIR}/NotoSans-Black.ttf"
XBOLD = f"{FONT_DIR}/NotoSans-ExtraBold.ttf"
BOLD = f"{FONT_DIR}/NotoSans-Bold.ttf"
SEMI = f"{FONT_DIR}/NotoSans-SemiBold.ttf"
REG = f"{FONT_DIR}/NotoSans-Regular.ttf"

BG = (10, 16, 30)
PANEL = (19, 28, 48)
PANEL2 = (24, 36, 62)
WHITE = (245, 247, 250)
MUTED = (168, 180, 200)
RED = (232, 55, 74)
GOLD = (245, 183, 49)
TEAL = (45, 196, 182)
BLUE = (84, 150, 255)
GREEN = (96, 199, 110)
PURPLE = (178, 132, 255)


def font(path, size):
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


def draw_text_block(draw, xy, text, fnt, fill, max_w, leading):
    x, y = xy
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rounded(draw, box, radius, fill):
    draw.rounded_rectangle(box, radius=radius, fill=fill)


def tag(draw, x, y, text, color):
    f = font(BOLD, 21)
    w = draw.textlength(text, font=f) + 26
    rounded(draw, (x, y, x + w, y + 34), 17, fill=color)
    draw.text((x + 13, y + 4), text, font=f, fill=(8, 12, 22))
    return x + w


def main():
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # ---- header ------------------------------------------------------
    d.rectangle((0, 0, W, 10), fill=RED)
    d.text((48, 34), "THE WORLD IN ONE IMAGE", font=font(BLACK, 55), fill=WHITE)
    d.text((48, 102), "Sunday, 22 November 2026  ·  The day's top stories, on one page",
           font=font(SEMI, 25), fill=MUTED)
    d.line((48, 148, W - 48, 148), fill=(52, 66, 96), width=2)

    # ---- lead story --------------------------------------------------
    y = 168
    rounded(d, (40, y, W - 40, y + 232), 22, fill=PANEL2)
    d.rectangle((40, y, 52, y + 232), fill=RED)
    tag(d, 76, y + 20, "LEAD STORY · CLIMATE", RED)
    tag(d, 76 + 320, y + 20, "ANTALYA, TÜRKIYE", GOLD)
    yy = draw_text_block(d, (76, y + 62), "COP31 climate talks collapse",
                         font(XBOLD, 47), WHITE, W - 160, 52)
    draw_text_block(
        d, (76, yy + 6),
        "The UN climate summit ends with no adopted deal for the first time since 2009, "
        "after the EU rejected a final draft that never directly mentioned fossil fuels.",
        font(REG, 25), MUTED, W - 160, 34)

    # ---- five more stories ------------------------------------------
    stories = [
        ("WAR · KYIV", BLUE,
         "Russian strikes kill 6 in Kyiv region",
         "Ukraine reports another deadly wave of Russian attacks around the capital."),
        ("SUMMIT · SHENZHEN", PURPLE,
         "Xi, Trump & Putin meet for first trilateral talks",
         "A historic three-way meeting at APEC, where Xi held talks with 14 national leaders."),
        ("MARKETS · NEW YORK", GOLD,
         "US stocks slide into correction territory",
         "A tech sell-off drags the S&P 500 and the Dow down from their highs."),
        ("TECH · UNITED NATIONS", TEAL,
         "UN pledges 'killer robot' rules by 2028",
         "Autonomous-weapons talks edge toward draft rules after Russian pushback stalls a treaty."),
        ("AMERICAS · MEXICO", GREEN,
         "Mexico captures FBI most-wanted drug kingpin",
         "'Chapo Isidro', a Sinaloa-linked trafficker, is seized in a deadly firefight."),
    ]
    y += 232 + 12
    card_h = 88
    for label, color, head, body in stories:
        rounded(d, (40, y, W - 40, y + card_h), 16, fill=PANEL)
        d.rectangle((40, y, 48, y + card_h), fill=color)
        d.text((68, y + 10), label, font=font(BOLD, 19), fill=color)
        d.text((68, y + 34), head, font=font(BOLD, 26), fill=WHITE)
        d.text((68, y + 63), body, font=font(REG, 19), fill=MUTED)
        y += card_h + 10

    # ---- ticker + footer ---------------------------------------------
    ticker = ("ALSO TODAY:  EU–Indonesia trade deal signed  ·  Houthis strike Riyadh  ·  "
              "Leeds stun Chelsea 4–1, first win at Stamford Bridge since 1999  ·  EU eyes a Big Tech tax")
    yy = draw_text_block(d, (48, y + 2), ticker, font(SEMI, 20), (210, 218, 232), W - 96, 27)
    d.line((48, yy + 8, W - 48, yy + 8), fill=(52, 66, 96), width=2)
    d.text((48, yy + 18), "Sources: Reuters · SCMP · Sankei · World in Summary — compiled 23 Nov 2026",
           font=font(REG, 19), fill=MUTED)

    img.save("news-2026-11-22.png", optimize=True)
    print("saved news-2026-11-22.png")


if __name__ == "__main__":
    main()
