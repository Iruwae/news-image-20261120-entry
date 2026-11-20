#!/usr/bin/env python3
"""Draw the news-image-20261120 entry: one broadsheet front page, 1024x1024.

All facts verified live 2026-11-21 (see FACTS.md in the brief folder).
Every illustration is drawn here with PIL -- no photos, no downloads.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 242, 231)
INK = (17, 17, 17)
RED = (192, 57, 43)
DARKRED = (140, 30, 20)
NAVY = (20, 38, 74)
BLUE = (43, 108, 176)
TAN = (217, 201, 163)
GREY = (90, 88, 80)

FD = "/usr/share/fonts/truetype/dejavu/"


def F(name, size):
    return ImageFont.truetype(FD + name, size)


SERIF_B = lambda s: F("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: F("DejaVuSerif.ttf", s)
SANS = lambda s: F("DejaVuSans.ttf", s)
SANS_B = lambda s: F("DejaVuSans-Bold.ttf", s)


def wrap(d, text, font, maxw):
    """Greedy word wrap; returns list of lines that fit maxw."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, font, maxw, fill=INK, leading=None):
    """Draw wrapped paragraph; return y below it."""
    lh = leading or int(font.size * 1.28)
    for line in wrap(d, text, font, maxw):
        d.text((x, y), line, font=font, fill=fill)
        y += lh
    return y


def kicker(d, x, y, num, place, topic, color=RED):
    txt = f"{num}  {place} · {topic}" if topic else f"{num}  {place}"
    d.text((x, y), txt, font=SANS_B(10), fill=color)
    return y + 14


img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)
MX = 16  # margin
CW = W - 2 * MX  # 992

# ---------- top line ----------
d.text((MX, 8), "THE WORLD IN ONE DAY", font=SANS_B(13), fill=RED)
right = "35 STORIES · 7 REGIONS · EVERY ONE DATED FRIDAY 20 NOVEMBER 2026"
d.text((W - MX - d.textlength(right, font=SANS_B(11)), 10),
       right, font=SANS_B(11), fill=INK)
d.line([(MX, 30), (W - MX, 30)], fill=INK, width=2)

# ---------- masthead ----------
title = "Friday 20 November 2026"
tw = d.textlength(title, font=SERIF_B(60))
d.text(((W - tw) / 2, 36), title, font=SERIF_B(60), fill=INK)
sub = ("Russian missiles hit Kyiv's bridges · Cyclone Akvan strikes India · "
       "An AI sell-off sinks Asia's markets · UK and EU seal a deal")
sw = d.textlength(sub, font=SERIF(16))
d.text(((W - sw) / 2, 106), sub, font=SERIF(16), fill=INK)
d.line([(MX, 130), (W - MX, 130)], fill=INK, width=2)

# ---------- stat strip: 6 boxes ----------
stats = [
    ("3", "bridges over the Dnipro damaged in Kyiv"),
    ("300,000+", "people moved to shelters before Akvan"),
    ("-6.2%", "Taiwan's share index, Friday's close"),
    ("100,000", "youth visas a year in the UK-EU deal"),
    ("2.3%", "Japan consumer inflation in October"),
    ("118", "runs by Glenn Phillips against India"),
]
sx, sy, swd = MX, 138, CW // 6
for i, (num, lab) in enumerate(stats):
    x = sx + i * swd
    if i:
        d.line([(x, sy + 4), (x, sy + 52)], fill=RED, width=2)
    d.text((x + 8, sy), num, font=SANS_B(28), fill=INK)
    para(d, x + 8, sy + 32, lab, SANS(10), swd - 14, leading=12)
d.line([(MX, 200), (W - MX, 200)], fill=INK, width=1)

# ---------- region bar ----------
regions = [("Europe 8", (43, 108, 176)), ("Asia 8", (192, 57, 43)),
           ("Middle East 3", (150, 110, 40)), ("Africa 5", (39, 120, 70)),
           ("Americas 4", (110, 60, 140)), ("Oceania 3", (30, 130, 140)),
           ("Global 4", (90, 88, 80))]
rx, ry, rh = MX, 206, 20
seg = CW // 7
for i, (lab, col) in enumerate(regions):
    x = rx + i * seg
    wdt = seg - 2 if i < 6 else CW - 6 * seg
    d.rectangle([x, ry, x + wdt, ry + rh], fill=col)
    tw2 = d.textlength(lab, font=SANS_B(11))
    d.text((x + (wdt - tw2) / 2, ry + 4), lab, font=SANS_B(11), fill=(255, 255, 255))

# ---------- LEADS ----------
LY, LH_IMG = 234, 148
COLW = (CW - 16) // 3


def lead_panel(x, y, w, draw_fn):
    draw_fn(x, y, w, LH_IMG)
    d.rectangle([x, y, x + w, y + LH_IMG], outline=INK, width=1)


def kyiv(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    # stars
    for sx_, sy_ in [(20, 12), (60, 26), (110, 10), (180, 20), (240, 14),
                     (290, 30), (150, 34), (90, 40), (210, 44)]:
        d.ellipse([x + sx_, y + sy_, x + sx_ + 2, y + sy_ + 2], fill=(255, 255, 255))
    # skyline
    for bx, bw, bh in [(0, 34, 52), (36, 26, 70), (64, 40, 46), (106, 30, 64),
                       (138, 36, 50), (176, 28, 74), (206, 42, 54),
                       (250, 30, 66), (282, 36, 48)]:
        d.rectangle([x + bx, y + h - bh - 26, x + bx + bw, y + h - 26], fill=(8, 14, 30))
    # river + bridge
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(28, 68, 120))
    d.line([(x, y + h - 26), (x + w, y + h - 26)], fill=(10, 10, 10), width=3)
    for px in (70, 160, 250):
        d.line([(x + px, y + h - 26), (x + px, y + h - 8)], fill=(10, 10, 10), width=3)
    # fires on the bridge
    for fx in (76, 166, 256):
        d.ellipse([x + fx - 6, y + h - 40, x + fx + 6, y + h - 26], fill=(255, 140, 0))
        d.polygon([(x + fx - 4, y + h - 28), (x + fx, y + h - 44),
                   (x + fx + 4, y + h - 28)], fill=(255, 200, 0))
    # dotted missile trails arcing down
    for (x0, y0, x1, y1) in [(30, 8, 120, 78), (150, 4, 230, 84), (240, 10, 300, 70)]:
        for t in range(0, 11):
            tt = t / 10
            px = x + x0 + (x1 - x0) * tt
            py = y + y0 + (y1 - y0) * tt * tt
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 220, 130))
    d.rectangle([x + 8, y + 8, x + 62, y + 30], fill=RED)
    d.text((x + 13, y + 12), "KYIV", font=SANS_B(15), fill=(255, 255, 255))
    d.rectangle([x + 8, y + 34, x + 118, y + 52], fill=(255, 255, 255))
    d.text((x + 12, y + 37), "3 bridges hit", font=SANS_B(12), fill=INK)
    d.rectangle([x + 8, y + h - 20, x + 108, y + h - 4], fill=(0, 0, 0))
    d.text((x + 12, y + h - 18), "Officials' count", font=SANS_B(10), fill=(255, 255, 255))


def akvan(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(178, 214, 235))
    # land (left, tan-green) and sea
    d.polygon([(x, y), (x + 120, y), (x + 150, y + 50), (x + 120, y + 100),
               (x + 130, y + h), (x, y + h)], fill=(198, 214, 170))
    d.polygon([(x + 120, y), (x + w, y), (x + w, y + h), (x + 130, y + h),
               (x + 120, y + 100), (x + 150, y + 50)], fill=(43, 108, 176))
    # cyclone spiral: white concentric arcs
    cx, cy = x + w - 95, y + 78
    for r in (52, 40, 28, 16):
        d.arc([cx - r, cy - r, cx + r, cy + r], start=20, end=300,
              fill=(255, 255, 255), width=5)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(255, 255, 255))
    # Gopalpur red dot + dashed track
    gx, gy = x + 138, y + 62
    d.ellipse([gx - 5, gy - 5, gx + 5, gy + 5], fill=RED)
    for t in range(0, 8):
        tt = t / 7
        px = gx + (cx - gx) * tt
        py = gy + (cy - gy) * tt
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
    d.text((x + 10, y + 10), "GOPALPUR", font=SANS_B(11), fill=INK)
    d.text((x + 10, y + 26), "Odisha, India", font=SANS(10), fill=INK)
    d.rectangle([x + w - 150, y + 8, x + w - 8, y + 30], fill=RED)
    d.text((x + w - 145, y + 12), "LANDFALL · 8 am", font=SANS_B(12), fill=(255, 255, 255))
    d.rectangle([x + 8, y + h - 20, x + 100, y + h - 4], fill=(0, 0, 0))
    d.text((x + 12, y + h - 18), "Weather office", font=SANS_B(10), fill=(255, 255, 255))


def selloff(x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(26, 26, 40))
    # falling chart, left half
    pts = [(x + 14, y + 30), (x + 44, y + 44), (x + 70, y + 38), (x + 96, y + 66),
           (x + 122, y + 84), (x + 148, y + 78), (x + 168, y + 112)]
    for i in range(len(pts) - 1):
        d.line([pts[i], pts[i + 1]], fill=(230, 60, 50), width=3)
    for gy in (y + 40, y + 70, y + 100):
        d.line([(x + 10, gy), (x + 175, gy)], fill=(70, 70, 95), width=1)
    d.text((x + 12, y + 118), "", font=SANS_B(12), fill=(255, 255, 255))
    # market rows, right half
    rows = [("Taipei", "-6.2%"), ("Seoul", "-5.2%"), ("Tokyo", "-5.1%"),
            ("Hong Kong", "-2.2%")]
    for i, (m, v) in enumerate(rows):
        ry2 = y + 14 + i * 30
        d.text((x + 185, ry2), m, font=SANS_B(13), fill=(255, 255, 255))
        vw = d.textlength(v, font=SANS_B(14))
        d.text((x + w - 8 - vw, ry2), v, font=SANS_B(14), fill=(255, 90, 80))
        d.line([(x + 185, ry2 + 24), (x + w - 8, ry2 + 24)], fill=(70, 70, 95), width=1)
    d.rectangle([x + 8, y + h - 20, x + 108, y + h - 4], fill=(0, 0, 0))
    d.text((x + 12, y + h - 18), "Closing prices", font=SANS_B(10), fill=(255, 255, 255))


leads = [
    ("1", "KYIV, UKRAINE · WAR", "Russian missiles hit three Kyiv bridges",
     "An overnight barrage of 110+ missiles, 27 of them ballistic, and 400+ "
     "drones killed at least 8 across Ukraine — 6 in Kyiv, including "
     "3 water workers, and 2 in Lviv — and cut power and water in the capital. "
     "(Reuters, Kyiv Independent)", kyiv),
    ("2", "ODISHA, INDIA · CYCLONE", "Cyclone Akvan comes ashore in eastern India",
     "The storm crossed the coast near Gopalpur from about 8 am with winds of "
     "70-80 km/h, gusting to 90, after more than 300,000 people were moved to "
     "shelters. 423 rescue teams deployed; no deaths reported. (IMD, PTI)", akvan),
    ("3", "TAIPEI · SEOUL · TOKYO · MARKETS", "AI sell-off sinks Asia's stock markets",
     "Taiwan's index fell 6.2% to end its worst week since 1991. Seoul lost "
     "5.2% and Tokyo 5.1% as chipmakers led the slide; SoftBank fell 14.6%. "
     "(Reuters, Al Jazeera)", selloff),
]
for i, (num, place, head, body, fn) in enumerate(leads):
    x = MX + i * (COLW + 8)
    lead_panel(x, LY, COLW, fn)
    ty = LY + LH_IMG + 8
    kicker(d, x, ty, num, place, "")
    # headline (bold, up to 3 lines)
    hy = ty + 16
    hy = para(d, x, hy, head, SANS_B(18), COLW, leading=21)
    para(d, x, hy + 2, body, SANS(11), COLW, leading=14)

# ---------- SMALL STORIES (2 rows x 5) ----------
SY = 516
SCW = (CW - 4 * 8) // 5  # 192
SH_IMG = 52


def icon_panel(x, y, w, h, kind):
    d.rectangle([x, y, x + w, y + h], fill=(232, 226, 208))
    d.rectangle([x, y, x + w, y + h], outline=INK, width=1)
    cx, cy = x + w // 2, y + h // 2
    if kind == "ukeu":  # two flags
        d.rectangle([x + 18, y + 12, x + 82, y + h - 12], fill=(0, 51, 153))
        for k in range(8):
            import math
            a = math.pi * 2 * k / 8
            d.ellipse([x + 50 + 16 * math.cos(a) - 2, y + h // 2 + 11 * math.sin(a) - 2,
                       x + 50 + 16 * math.cos(a) + 2, y + h // 2 + 11 * math.sin(a) + 2],
                      fill=(255, 204, 0))
        d.rectangle([x + 96, y + 12, x + w - 18, y + h - 12], fill=(255, 255, 255))
        d.rectangle([x + 96, y + h // 2 - 4, x + w - 18, y + h // 2 + 4], fill=(200, 16, 46))
        d.rectangle([x + 128, y + 12, x + 136, y + h - 12], fill=(200, 16, 46))
    elif kind == "cop":  # globe + thermometer
        d.ellipse([x + 14, cy - 18, x + 50, cy + 18], fill=(43, 108, 176))
        d.ellipse([x + 22, cy - 10, x + 34, cy + 2], fill=(80, 180, 90))
        d.ellipse([x + 34, cy + 4, x + 46, cy + 14], fill=(80, 180, 90))
        d.rectangle([x + 120, cy - 20, x + 128, cy + 12], fill=(255, 255, 255))
        d.ellipse([x + 114, cy + 8, x + 134, cy + 24], fill=RED)
        d.rectangle([x + 122, cy - 16, x + 126, cy + 10], fill=RED)
        d.text((x + 62, cy - 8), "NO DEAL", font=SANS_B(13), fill=RED)
        d.text((x + 62, cy + 8), "YET", font=SANS_B(13), fill=INK)
    elif kind == "pol":  # missile over field
        d.rectangle([x, y + h - 16, x + w, y + h], fill=(90, 160, 80))
        d.line([(x + 30, y + 18), (x + 150, y + 34)], fill=(120, 120, 120), width=6)
        d.polygon([(x + 150, y + 28), (x + 168, y + 37), (x + 150, y + 44)], fill=RED)
        d.polygon([(x + 30, y + 18), (x + 14, y + 12), (x + 14, y + 24)], fill=(255, 140, 0))
    elif kind == "irq":  # convoy trucks
        d.rectangle([x, y + h - 18, x + w, y + h], fill=(210, 190, 140))
        for tx in (20, 80, 140):
            d.rectangle([x + tx, cy - 8, x + tx + 36, cy + 8], fill=(60, 90, 50))
            d.rectangle([x + tx + 36, cy - 2, x + tx + 48, cy + 8], fill=(60, 90, 50))
            for wx in (tx + 8, tx + 28, tx + 42):
                d.ellipse([x + wx - 4, cy + 8, x + wx + 4, cy + 16], fill=(20, 20, 20))
        d.text((x + 10, y + 6), "TROOPS IN", font=SANS_B(12), fill=INK)
    elif kind == "ita":  # marchers + placards
        for px, col in [(30, RED), (80, INK), (130, RED)]:
            d.ellipse([x + px - 6, y + 8, x + px + 6, y + 20], fill=col)
            d.rectangle([x + px - 7, y + 22, x + px + 7, y + h - 8], fill=col)
        d.rectangle([x + 140, y + 4, x + w - 8, y + 22], fill=(255, 255, 255))
        d.text((x + 144, y + 8), "SCIOPERO", font=SANS_B(10), fill=RED)
    elif kind == "jpn":  # red sun + rising bars
        d.ellipse([x + 14, y + 8, x + 46, y + 40], fill=RED)
        for i, bh in enumerate((14, 22, 30, 38)):
            bx = x + 70 + i * 26
            d.rectangle([bx, y + h - 8 - bh, bx + 18, y + h - 8], fill=INK)
        d.line([(x + 66, y + h - 12), (x + 170, y + 12)], fill=RED, width=3)
    elif kind == "kor":  # courthouse columns
        d.polygon([(x + 20, y + 10), (cx, y + 2), (x + w - 20, y + 10)], fill=INK)
        for i in range(4):
            bx = x + 34 + i * 40
            d.rectangle([bx, y + 14, bx + 14, y + h - 10], fill=(120, 110, 90))
        d.rectangle([x + 20, y + h - 10, x + w - 20, y + h - 4], fill=INK)
    elif kind == "ken":  # oil derrick + sun
        d.ellipse([x + w - 44, y + 6, x + w - 16, y + 34], fill=(255, 170, 0))
        d.line([(x + 40, y + 6), (x + 30, y + h - 6)], fill=INK, width=3)
        d.line([(x + 80, y + 6), (x + 90, y + h - 6)], fill=INK, width=3)
        for yy in (16, 28, 40):
            d.line([(x + 37, y + yy), (x + 83, y + yy + 6)], fill=INK, width=2)
        d.rectangle([x + 120, y + h - 16, x + w - 10, y + h - 6], fill=(60, 60, 60))
    elif kind == "buk":  # ballot box
        d.rectangle([x + 60, cy - 8, x + 130, cy + 18], fill=(30, 80, 160))
        d.rectangle([x + 78, cy - 12, x + 112, cy - 8], fill=INK)
        d.polygon([(x + 86, cy - 30), (x + 104, cy - 30), (x + 100, cy - 12),
                   (x + 90, cy - 12)], fill=(255, 255, 255))
        d.text((x + 140, cy - 6), "2027", font=SANS_B(13), fill=INK)
        d.text((x + 12, y + 6), "3RD TERM", font=SANS_B(12), fill=RED)
    elif kind == "cri":  # cricket bat + ball
        d.rectangle([x, y + h - 14, x + w, y + h], fill=(70, 150, 70))
        d.rectangle([x + 30, y + 8, x + 52, y + 20], fill=(200, 170, 120))
        d.line([(x + 42, y + 20), (x + 30, y + 44)], fill=(200, 170, 120), width=8)
        d.ellipse([x + 120, y + 10, x + 140, y + 30], fill=RED)
        for sx_ in (150, 158, 166):
            d.rectangle([x + sx_, y + 30, x + sx_ + 3, y + 52], fill=(220, 190, 130))
        d.text((x + 10, y + h - 13), "118 · first in all formats", font=SANS_B(8),
               fill=(255, 255, 255))


smalls = [
    ("4", "BRUSSELS · DIPLOMACY", "UK and EU seal a “reset” deal",
     "Food trade, youth visas, carbon link; tuition fees still open. (Reuters, CNN)", "ukeu"),
    ("5", "ANTALYA · CLIMATE", "COP31 reaches its last day with no deal",
     "No fossil fuels in draft; Panama vows to block it. [FORECAST] "
     "Talks may run on. (UN News)", "cop"),
    ("6", "E. POLAND · SECURITY", "Russian missiles cross into Poland",
     "A Kh-101 cruise missile and a drone fell in the south-east; NATO jets "
     "scrambled, no one hurt. (Reuters)", "pol"),
    ("7", "C. IRAQ · SECURITY", "Iraqi army enters a militia stronghold",
     "Troops deploy to Jurf al-Sakhar after an oil-smuggling probe. (Reuters)", "irq"),
    ("8", "ITALY · LABOUR", "General strike over Italy's budget",
     "Workers and students march in 100+ cities; rail stops at 9 pm. (Reuters)", "ita"),
    ("9", "TOKYO · ECONOMY", "Japan's inflation picks up to 2.3%",
     "Headline CPI 2.3%, core 2.2% in October; a December rate rise stays in "
     "view. (Reuters)", "jpn"),
    ("10", "SEOUL · POLITICS", "Korea's ruling party to impeach top judge",
     "The move follows the court sending Han Duck-soo's case back for retrial. "
     "(Korea JoongAng Daily)", "kor"),
    ("11", "TURKANA, KENYA · ENERGY", "Kenya starts drilling its first oil well",
     "Spudding at Amosing; first crude due 1 December, 20,000 barrels a day. "
     "(Capital FM)", "ken"),
    ("12", "SAN SALVADOR · POLITICS", "Bukele files to run for a third term",
     "Registered Thu night; the vote is 28 February 2027. (Reuters, AP)", "buk"),
    ("13", "WELLINGTON · CRICKET", "Phillips hits 118 against India",
     "First player with centuries in all formats vs India in one year. "
     "(ICC, Reuters)", "cri"),
]
for idx, (num, place, head, body, kind) in enumerate(smalls):
    row, col = divmod(idx, 5)
    x = MX + col * (SCW + 8)
    y = SY + row * 144
    icon_panel(x, y, SCW, SH_IMG, kind)
    ty = y + SH_IMG + 5
    kicker(d, x, ty, num, place, "")
    hy = ty + 14
    hy = para(d, x, hy, head, SANS_B(13), SCW, leading=15)
    para(d, x, hy + 1, body, SANS(10), SCW, leading=12)

# ---------- BOTTOM: map + briefs ----------
BY = 806
d.text((MX, BY), "WHERE IT HAPPENED", font=SANS_B(12), fill=INK)
d.text((MX + 312, BY), "ALSO ON FRIDAY 20 NOVEMBER — 22 MORE STORIES",
       font=SANS_B(12), fill=INK)
d.line([(MX, BY + 17), (W - MX, BY + 17)], fill=INK, width=1)

# simplified world map
mx0, my0, mw, mh = MX, BY + 22, 296, 118
d.rectangle([mx0, my0, mx0 + mw, my0 + mh], fill=(214, 228, 235))
d.rectangle([mx0, my0, mx0 + mw, my0 + mh], outline=INK, width=1)
# continents (rough polygons, tan)
d.polygon([(mx0 + 8, my0 + 28), (mx0 + 70, my0 + 14), (mx0 + 96, my0 + 26),
           (mx0 + 80, my0 + 48), (mx0 + 44, my0 + 52), (mx0 + 16, my0 + 44)], fill=TAN)  # N America
d.polygon([(mx0 + 66, my0 + 62), (mx0 + 96, my0 + 58), (mx0 + 104, my0 + 82),
           (mx0 + 88, my0 + 106), (mx0 + 72, my0 + 88)], fill=TAN)  # S America
d.polygon([(mx0 + 128, my0 + 22), (mx0 + 168, my0 + 14), (mx0 + 186, my0 + 30),
           (mx0 + 172, my0 + 52), (mx0 + 146, my0 + 48)], fill=TAN)  # Europe
d.polygon([(mx0 + 150, my0 + 56), (mx0 + 190, my0 + 52), (mx0 + 200, my0 + 80),
           (mx0 + 182, my0 + 104), (mx0 + 160, my0 + 88)], fill=TAN)  # Africa
d.polygon([(mx0 + 190, my0 + 18), (mx0 + 268, my0 + 10), (mx0 + 288, my0 + 34),
           (mx0 + 272, my0 + 62), (mx0 + 226, my0 + 66), (mx0 + 200, my0 + 44)], fill=TAN)  # Asia
d.polygon([(mx0 + 252, my0 + 88), (mx0 + 284, my0 + 84), (mx0 + 288, my0 + 102),
           (mx0 + 258, my0 + 106)], fill=TAN)  # Oceania
pins = {1: (156, 36), 2: (222, 58), 3: (250, 50), 4: (132, 20), 5: (172, 48),
        6: (164, 22), 7: (188, 54), 8: (142, 44), 9: (264, 28), 10: (246, 28),
        11: (170, 74), 12: (52, 56), 13: (272, 94)}
for n, (px, py) in pins.items():
    d.ellipse([mx0 + px - 7, my0 + py - 7, mx0 + px + 7, my0 + py + 7],
              fill=RED, outline=(255, 255, 255), width=1)
    tw3 = d.textlength(str(n), font=SANS_B(8))
    d.text((mx0 + px - tw3 / 2, my0 + py - 5), str(n), font=SANS_B(8),
           fill=(255, 255, 255))
d.text((mx0 + 4, my0 + mh - 12), "Pins 1–13 mark the drawn stories",
       font=SANS(8), fill=GREY)

# briefs 14-35: 22 items, numbered straight through, no duplicates.
# (FACTS.md's tail is off by one between its list and its note; resolved here
# as 32/33 Antalya, 34 Turin ATP pay, 35 Turin ATP Finals.)
briefs = [
    "14 Lviv — Strike on a railway station kills two (BBC)",
    "15 Moscow — Russia declares Estonia's border closed (Reuters)",
    "16 Berlin — Pupils strike over military service (Al Jazeera)",
    "17 London — General says UK runs cyber attacks abroad (Sky News)",
    "18 Beijing — China holds loan rates for an 18th month (Xinhua)",
    "19 Tokyo — SoftBank shares fall more than 14% in a day (Al Jazeera)",
    "20 Seoul — Kospi ends the week 7.9% lower (Anadolu)",
    "21 Ganjam — 209 mm of rain as Akvan crosses Odisha (PTI)",
    "22 Lebanon — Israeli air strikes hit south and east (Anadolu)",
    "23 Yemen — Gunmen fire on a cargo ship off the coast (UKMTO)",
    "24 Abuja — Court bars new evidence against Tinubu (Channels TV)",
    "25 Kampala — Police told to enforce Ebola ban on rallies (allAfrica)",
    "26 Malawi — Fuel crisis brings night-long petrol queues (Al Jazeera)",
    "27 Africa — AfDB: 22 countries in debt distress (allAfrica)",
    "28 Las Vegas — Russell fastest in wet Grand Prix practice (Autosport)",
    "29 New York — Nasdaq futures fall 1.6% before the bell (24/7 Wall St)",
    "30 Washington — Democrats query law firm's free work (Al Jazeera)",
    "31 Sydney — Australian shares fall 1.8% in the sell-off (Reuters)",
    "32 Antalya — Panama asks COP31 to cap world oil output (Anadolu)",
    "33 Antalya — EU official calls climate draft unacceptable (RTE)",
    "34 Turin — ATP backs plan to lift player pay past $350m (Anadolu)",
    "35 Turin — ATP Finals group stage ends; semis Saturday (ATP)",
]
assert len(briefs) == 22, len(briefs)
bx0, by0 = MX + 312, BY + 24
bcolw = (W - MX - bx0 - 8) // 2
for i, b in enumerate(briefs):
    col, row = divmod(i, 11)
    x = bx0 + col * (bcolw + 8)
    y = by0 + row * 11
    d.text((x, y), b, font=SANS(9), fill=INK)

# ---------- DATE CHECK ----------
dy = 952
d.rectangle([MX, dy, W - MX, dy + 40], outline=RED, width=2)
dc = ("DATE CHECK  Left out as Thursday 19 November's news: the World Court's "
      "ruling on Myanmar, the three-leader declaration in Shenzhen, Tonga's "
      "drought emergency and the migrant boat lost off Senegal. Not yet shown: "
      "BepiColombo's entry into orbit round Mercury (Sat 21 Nov) and any final "
      "COP31 text.")
para(d, MX + 6, dy + 4, dc, SANS(10), CW - 12, leading=13)

# ---------- footer ----------
d.text((MX, 998), "Every story here happened, or was first reported, on Friday "
       "20 November 2026. Officials' counts are attributed.",
       font=SANS(9), fill=INK)
ft = "Sources named beside each story · original drawings"
d.text((W - MX - d.textlength(ft, font=SANS(9)), 998), ft, font=SANS(9), fill=GREY)

img.save("entry.png", optimize=True)
print("saved entry.png", img.size)
