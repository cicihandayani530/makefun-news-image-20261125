#!/usr/bin/env python3
"""THE TIDEWATER POST - variant B (Layout C alt: three equal lead columns,
estuary-blue dominant masthead). Tuesday 25 November 2026, one page.
Figures only from the locked NI25 pool. Local PIL drawing, no network.
Output: entry_b.png (1024x1024) beside this file.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024
PAPER = (243, 236, 216)
CARD = (253, 250, 238)
INK = (30, 32, 36)
MUTE = (94, 90, 76)
BRONZE = (154, 116, 51)
BRONZE_D = (110, 82, 34)
EST = (23, 69, 94)
EST_D = (11, 42, 60)
EST_L = (64, 116, 143)
CREAM_TXT = (250, 244, 224)
CLAIM = (163, 59, 46)
WHITE = (255, 255, 255)
RCOL = {"EUROPE": (58, 92, 140), "MIDDLE EAST": (176, 92, 44),
        "WORLD": (110, 82, 34), "AFRICA": (146, 108, 32),
        "AMERICAS": (46, 110, 90), "ASIA": (150, 62, 74),
        "SOUTH ASIA": (104, 74, 150), "ASIA-PACIFIC": (38, 122, 128),
        "OCEANIA": (66, 128, 178)}
FONT_DIR = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts"
DEJA = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DEJA_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def _find(names):
    try:
        files = os.listdir(FONT_DIR)
    except OSError:
        return None
    for want in names:
        for f in files:
            if want.lower() in f.lower() and f.lower().endswith((".ttf", ".otf")):
                return os.path.join(FONT_DIR, f)
    return None


DISP = _find(["PlayfairDisplay-Black", "Playfair"]) or DEJA_B


def F(size, bold=False, disp=False):
    p = DISP if disp else (DEJA_B if bold else DEJA)
    try:
        return ImageFont.truetype(p, size)
    except OSError:
        return ImageFont.load_default()


def wrap(d, text_, font, maxw):
    out, cur = [], ""
    for wd in text_.split():
        t = (cur + " " + wd).strip()
        if d.textlength(t, font=font) <= maxw or not cur:
            cur = t
        else:
            out.append(cur)
            cur = wd
    if cur:
        out.append(cur)
    return out


def T(d, xy, s, font, fill=INK, anchor="la"):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)


# num, region, place, headline, deck, source, cert, chip, scene
LEADS = [
    (6, "WORLD", "UKRAINE WAR DATA", "700,000 Russian dead, new count finds",
     "New analysis: more than 700,000 Russian soldiers killed in the "
     "nearly five-year war - the 700000 toll leads the day.",
     "RFE/RL", "REPORTED", "700,000+ KILLED", "crosses"),
    (2, "MIDDLE EAST", "STRAIT OF HORMUZ", "Iran says 3 tankers hit by mines",
     "The IRGC Navy claims three oil tankers were hit by naval mines in "
     "the Strait of Hormuz; shipping concerns rise.",
     "Iranian claim via wires", "CLAIMED", "3 TANKERS HIT - IRAN SAYS",
     "hormuz"),
    (1, "EUROPE", "POLAND", "NATO sends early-warning jets to Poland",
     "NATO plans an AWACS deployment in Poland after Russian missiles "
     "landed in Poland; Merz vows complete support.",
     "Wire reports", "REPORTED", "AWACS TO POLAND", "awacs"),
]
GRID = [
    (3, "MIDDLE EAST", "IRAQ", "Baghdad orders Kurdish oilfields seized",
     "PM al-Zaidi orders federal units to seize oilfields; Barzani: "
     "Kurdistan will not submit.", "Starlit / wires", "REPORTED",
     "OILFIELDS ORDER", "oil"),
    (4, "MIDDLE EAST", "GAZA", "Drone strikes kill Hamas security chief",
     "Strikes killed a senior Hamas security official, three policemen "
     "and three siblings, one a child.", "Al Jazeera", "REPORTED",
     "7 KILLED IN STRIKES", "gaza"),
    (5, "EUROPE", "BRUSSELS", "EU unveils new Russia sanctions",
     "The EU announced further restrictive measures - new sanctions - "
     "against Russia.", "Wire roundups", "REPORTED", "NEW EU SANCTIONS",
     "eu"),
    (7, "EUROPE", "UKRAINE", "First German Lynx fighting vehicles arrive",
     "The first 5 German Lynx KF41 infantry fighting vehicles enter "
     "Ukrainian service.", "Wires", "REPORTED", "5 LYNX KF41 IFVS", "lynx"),
    (10, "ASIA", "CHINA", "Xiamen Airlines orders 50 Boeing jets",
     "Xiamen Airlines, a China Southern unit, agreed to acquire 50 "
     "Boeing 737-8 jets.", "Wires", "REPORTED", "50 JETS ORDERED", "jet"),
    (11, "EUROPE", "MADRID", "Madrid rout PSV 5-1 in comeback",
     "Madrid overturned a deficit to beat PSV 5-1; Bellingham stunner, "
     "Mbappe brace.", "Wires", "REPORTED", "MADRID 5-1 PSV", "stadium"),
    (13, "OCEANIA", "AUSTRALIA", "12 coral species brought back",
     "Genetic analysis resurrects 12 Acropora coral species on the "
     "Great Barrier Reef.", "Science wires", "REPORTED",
     "12 SPECIES BACK", "coral"),
    (33, "WORLD", "WASHINGTON", "PCE inflation report due today",
     "The US PCE inflation report is due Tuesday 25 November; no figure "
     "has been published yet.", "Scheduled", "SCHEDULED", "PCE DUE TODAY",
     "pce"),
    (36, "WORLD", "NVIDIA", "Nvidia's $1 trillion Monday",
     "Monday close: +31.5%, nearly $1 trillion clawed back as Huang "
     "returned as CEO, +$34bn a day.", "Forbes via wires", "REPORTED",
     "+31.5% MONDAY CLOSE", "chip"),
    (37, "AMERICAS", "USA", "Storms target Thanksgiving travel",
     "Weather targeting both US shorelines risks Thanksgiving travel "
     "for millions.", "Wires", "REPORTED", "STORMS BOTH COASTS", "storm"),
]
BRIEFS = [
    (8, "AMERICAS", "Car bomb in Colombia injures at least 23", "23 INJURED"),
    (9, "AMERICAS", "Gunmen hold dozens in a Cartagena supermarket",
     "DOZENS HELD"),
    (12, "WORLD", "England level the T20I series; Fraser-McGurk 27 off 13",
     "ENGLAND BY 8 WICKETS"),
    (14, "OCEANIA", "Fiji declares a disaster in an El Nino dry spell",
     "DISASTER DECLARED"),
    (15, "MIDDLE EAST", "Iran's pharmacies run dry amid shortages",
     "MEDICINE SHORTAGE"),
    (16, "MIDDLE EAST", "Iran braces for winter gas shortages",
     "WINTER SHORTAGES"),
    (17, "MIDDLE EAST", "Britain sanctions Houthi leaders", "UK SANCTIONS"),
    (18, "AFRICA", "Senegal's AFCON title restored by CAS ruling",
     "TITLE RESTORED"),
    (19, "AFRICA", "Rebels pull back after clashes in DR Congo",
     "REBELS PULL BACK"),
    (20, "AFRICA", "Nigerian emir suspended after allegation",
     "EMIR SUSPENDED"),
    (21, "AFRICA", "Sudan RSF commander defects in Sudan",
     "COMMANDER DEFECTS"),
    (22, "AFRICA", "Cameroon separatist in Norway court, war crimes",
     "WAR CRIMES COURT"),
    (23, "SOUTH ASIA", "Punjab: BJP and Akali Dal reunite as allies",
     "ALLIANCE AGAIN"),
    (24, "SOUTH ASIA", "Bangladesh opens a China office in Guangzhou",
     "OFFICE OPENS"),
    (25, "ASIA-PACIFIC", "Indonesia's vice-president resigns", "VP RESIGNS"),
    (26, "ASIA-PACIFIC", "Solomon Islands eye Australia treaty switch",
     "TREATY SWITCH"),
    (27, "ASIA", "North Korea touts China ties at embassy visit",
     "TIES TOUTED"),
    (28, "EUROPE", "Denmark court upholds ghetto evictions law",
     "COURT UPHOLDS LAW"),
    (29, "EUROPE", "Sarkozy headed for Libya-case trial in Paris",
     "TRIAL AHEAD"),
    (30, "EUROPE", "Black Sea clash at the UN over shipping", "UN CLASH"),
    (31, "WORLD", "Shortwave school returns for Afghan girls",
     "SHORTWAVE RETURNS"),
    (32, "WORLD", "Dimorphos shadows Didymos in an asteroid eclipse",
     "ASTEROID ECLIPSE"),
    (34, "AMERICAS", "US targets 7 firms over chips; one Alibaba-owned",
     "7 FIRMS TARGETED"),
    (35, "EUROPE", "Moscow buys inflatable decoys from China",
     "INFLATABLE DECOYS"),
]
REGIONS = [("EUROPE", 8), ("MIDDLE EAST", 6), ("WORLD", 6), ("AFRICA", 5),
           ("AMERICAS", 4), ("ASIA", 2), ("SOUTH ASIA", 2),
           ("ASIA-PACIFIC", 2), ("OCEANIA", 2)]
NUMBERS = [("700,000+", "RUSSIAN DEAD"), ("3", "TANKERS - IRAN SAYS"),
           ("AWACS", "TO POLAND"), ("7", "DEAD IN GAZA"),
           ("5-1", "MADRID-PSV"), ("50", "BOEING JETS"),
           ("+31.5%", "NVIDIA MON"), ("12", "CORAL BACK")]
TIMELINE = [("EARLY", "NATO AWACS plan for Poland reported"),
            ("MORNING", "Iran says 3 tankers hit mines in Hormuz"),
            ("MIDDAY", "Baghdad orders Kurdish oilfields seized"),
            ("TODAY", "US PCE inflation report due - no figure yet"),
            ("MON CLOSE", "Nvidia +31.5% - Monday close, Forbes"),
            ("TONIGHT", "Storms target Thanksgiving travel")]
DATECHECK = ["GTA VI launch hype - not today's news",
             "COP31 talks - earlier this month, not Tuesday",
             "Liverpool 4-0 - a weekend score, not 25 Nov",
             "Merkury stories of 23 Nov - two days old",
             "Black Friday sales - Friday, not Tuesday"]


# ---- compact layered scenes (variant B drawing hand) -----------------------
def scene(d, key, box):
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle(box, fill=(233, 226, 200))
    if key == "crosses":
        d.rectangle([x0, y0, x1, y0 + h * 0.55], fill=(84, 84, 104))
        d.rectangle([x0, y0 + h * 0.55, x1, y1], fill=(96, 86, 58))
        for i in range(10):
            cx = x0 + w * (0.08 + 0.09 * i)
            cy = y0 + h * (0.68 + 0.1 * (i % 3))
            d.line([cx, cy - 6, cx, cy + 6], fill=(240, 236, 214), width=2)
            d.line([cx - 4, cy - 3, cx + 4, cy - 3], fill=(240, 236, 214),
                   width=2)
        d.rectangle([x0 + w * 0.8, y0 + h * 0.2, x0 + w * 0.88,
                     y0 + h * 0.55], fill=(44, 44, 52))
    elif key == "hormuz":
        d.rectangle([x0, y0 + h * 0.45, x1, y1], fill=(38, 92, 118))
        d.polygon([(x0, y0 + h * 0.45), (x0 + w * 0.34, y0 + h * 0.45),
                   (x0 + w * 0.14, y1)], fill=(150, 118, 66))
        d.polygon([(x1, y0 + h * 0.45), (x0 + w * 0.68, y0 + h * 0.45),
                   (x0 + w * 0.88, y1)], fill=(150, 118, 66))
        for fx in (0.38, 0.56):
            tx, ty = x0 + w * fx, y0 + h * 0.6
            d.polygon([(tx, ty), (tx + w * 0.14, ty), (tx + w * 0.11,
                        ty + h * 0.1), (tx + w * 0.03, ty + h * 0.1)],
                      fill=(52, 54, 60))
            d.rectangle([tx + w * 0.04, ty - h * 0.08, tx + w * 0.1, ty],
                        fill=(120, 70, 44))
        mx, my = x0 + w * 0.5, y0 + h * 0.86
        d.ellipse([mx - 5, my - 5, mx + 5, my + 5], fill=(26, 26, 30))
        for a in range(0, 360, 60):
            d.line([mx, my, mx + 8 * math.cos(math.radians(a)),
                    my + 8 * math.sin(math.radians(a))],
                   fill=(26, 26, 30), width=2)
    elif key == "awacs":
        d.rectangle([x0, y0, x1, y0 + h * 0.7], fill=(140, 178, 205))
        cx, cy = x0 + w * 0.5, y0 + h * 0.42
        for r in (0.14, 0.24):
            d.ellipse([cx - w * r, cy - w * r * 0.4, cx + w * r,
                       cy + w * r * 0.4], outline=(90, 130, 160), width=2)
        d.polygon([(cx - w * 0.22, cy), (cx + w * 0.2, cy - h * 0.05),
                   (cx + w * 0.24, cy), (cx + w * 0.18, cy + h * 0.05)],
                  fill=(70, 78, 90))
        d.ellipse([cx - w * 0.07, cy - h * 0.2, cx + w * 0.09,
                   cy - h * 0.13], fill=(38, 44, 54))
        d.rectangle([x0, y1 - h * 0.3, x1, y1], fill=(120, 140, 110))
    elif key == "oil":
        d.rectangle([x0, y0, x1, y0 + h * 0.62], fill=(222, 186, 128))
        d.rectangle([x0, y0 + h * 0.62, x1, y1], fill=(146, 112, 62))
        for fx in (0.16, 0.55):
            bx, by = x0 + w * fx, y0 + h * 0.62
            d.line([bx, by, bx + w * 0.22, by - h * 0.3],
                   fill=(52, 50, 46), width=4)
            d.line([bx + w * 0.06, by, bx + w * 0.06, by - h * 0.26],
                   fill=(52, 50, 46), width=3)
    elif key == "gaza":
        d.rectangle([x0, y0, x1, y0 + h * 0.5], fill=(204, 194, 176))
        for i, fx in enumerate((0.05, 0.32, 0.6, 0.84)):
            bx = x0 + w * fx
            d.rectangle([bx, y0 + h * (0.5 + 0.08 * (i % 2)), bx + w * 0.15,
                         y1], fill=(128, 116, 98))
        dx, dy = x0 + w * 0.5, y0 + h * 0.2
        d.line([dx - 15, dy, dx + 15, dy], fill=(40, 40, 44), width=3)
        d.rectangle([dx - 5, dy - 4, dx + 5, dy + 4], fill=(40, 40, 44))
        for r in range(2):
            d.ellipse([x0 + w * 0.66 - r * 4, y0 + h * 0.4 - r * 10,
                       x0 + w * 0.66 + 9 + r * 4, y0 + h * 0.4 - r * 10 + 8],
                      fill=(152, 148, 142))
    elif key == "eu":
        d.rectangle([x0, y0, x1, y1], fill=(52, 78, 140))
        cx, cy, r = x0 + w * 0.5, y0 + h * 0.5, h * 0.32
        for i in range(12):
            a = 2 * math.pi * i / 12
            sx, sy = cx + r * math.cos(a), cy + r * math.sin(a)
            d.polygon([(sx, sy - 5), (sx + 4, sy + 4), (sx - 4, sy + 4)],
                      fill=(244, 200, 70))
    elif key == "lynx":
        d.rectangle([x0, y0 + h * 0.66, x1, y1], fill=(104, 110, 84))
        bx, by = x0 + w * 0.14, y0 + h * 0.66
        d.polygon([(bx, by), (bx + w * 0.6, by), (bx + w * 0.66,
                    by - h * 0.18), (bx + w * 0.16, by - h * 0.2)],
                  fill=(86, 96, 70))
        d.line([bx + w * 0.42, by - h * 0.26, bx + w * 0.74,
                by - h * 0.34], fill=(50, 56, 42), width=4)
        for i in range(4):
            wx = bx + w * (0.08 + 0.15 * i)
            d.ellipse([wx, by - h * 0.09, wx + w * 0.09, by],
                      fill=(44, 48, 38))
    elif key == "jet":
        d.rectangle([x0, y0, x1, y0 + h * 0.7], fill=(120, 168, 205))
        cx, cy = x0 + w * 0.5, y0 + h * 0.4
        d.polygon([(cx - w * 0.34, cy), (cx + w * 0.3, cy - h * 0.08),
                   (cx + w * 0.36, cy), (cx - w * 0.3, cy + h * 0.05)],
                  fill=(238, 240, 244))
        d.polygon([(cx - w * 0.32, cy), (cx - w * 0.42, cy - h * 0.22),
                   (cx - w * 0.28, cy)], fill=(38, 92, 140))
    elif key == "stadium":
        d.rectangle([x0, y0 + h * 0.55, x1, y1], fill=(64, 140, 74))
        d.arc([x0 + w * 0.1, y0 + h * 0.05, x0 + w * 0.7, y0 + h * 0.9],
              180, 360, fill=(230, 230, 224), width=5)
        d.rectangle([x0 + w * 0.76, y0 + h * 0.12, x0 + w * 0.97,
                     y0 + h * 0.44], fill=(30, 34, 40))
        T(d, (x0 + w * 0.865, y0 + h * 0.28), "5-1", F(15, True),
          (250, 220, 120), anchor="mm")
    elif key == "coral":
        d.rectangle([x0, y0, x1, y1], fill=(52, 128, 165))
        for bx, s, col in ((0.26, 0.4, (232, 110, 90)),
                           (0.58, 0.55, (244, 150, 90)),
                           (0.84, 0.34, (226, 92, 120))):
            px, py = x0 + w * bx, y1 - 4
            d.line([px, py, px, py - h * s], fill=col, width=4)
            d.line([px, py - h * s * 0.5, px - w * 0.08,
                    py - h * s * 0.85], fill=col, width=3)
            d.line([px, py - h * s * 0.6, px + w * 0.08, py - h * s],
                   fill=col, width=3)
    elif key == "pce":
        d.rectangle([x0, y0, x1, y1], fill=(240, 234, 214))
        pts = [(0.08, 0.62), (0.3, 0.48), (0.52, 0.55), (0.74, 0.36)]
        for i in range(3):
            d.line([x0 + w * pts[i][0], y0 + h * pts[i][1],
                    x0 + w * pts[i + 1][0], y0 + h * pts[i + 1][1]],
                   fill=BRONZE_D, width=3)
        T(d, (x0 + w * 0.5, y1 - h * 0.16), "DUE TODAY", F(12, True),
          CLAIM, anchor="mm")
    elif key == "chip":
        d.rectangle([x0, y0, x1, y1], fill=(36, 52, 66))
        cx, cy, s = x0 + w * 0.3, y0 + h * 0.5, h * 0.4
        d.rectangle([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2],
                    fill=(52, 130, 96), outline=(180, 220, 190), width=2)
        for i, bh in enumerate((0.2, 0.36, 0.56)):
            bx = x0 + w * (0.58 + 0.13 * i)
            d.rectangle([bx, y1 - h * (0.16 + bh), bx + w * 0.09,
                         y1 - h * 0.16], fill=(240, 190, 80))
    elif key == "storm":
        d.rectangle([x0, y0, x1, y0 + h * 0.62], fill=(110, 128, 148))
        d.rectangle([x0, y0 + h * 0.62, x1, y1], fill=(52, 92, 118))
        for cx, cy in ((x0 + w * 0.22, y0 + h * 0.3),
                       (x0 + w * 0.8, y0 + h * 0.26)):
            for r in (5, 10, 15):
                d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300,
                      fill=(240, 244, 246), width=3)
    d.rectangle(box, outline=(178, 164, 124), width=1)


def chip_tag(d, x, y, s, fill):
    f = F(10, True)
    tw = d.textlength(s, font=f)
    d.rounded_rectangle([x, y, x + tw + 12, y + 15], 3, fill=fill)
    T(d, (x + 6, y + 2), s, f, WHITE)
    return x + tw + 12


def head_block(d, x, y, maxw, st, hs, ds, dmax=3):
    num, reg, place, head, deck, src, cert, chip, _ = st
    T(d, (x, y), "%d - %s - %s" % (num, reg, place), F(10, True), RCOL[reg])
    yy = y + 14
    for ln in wrap(d, head, F(hs, True), maxw)[:2]:
        T(d, (x, yy), ln, F(hs, True), INK)
        yy += hs + 3
    for ln in wrap(d, deck, F(ds), maxw)[:dmax]:
        T(d, (x, yy), ln, F(ds), (52, 52, 50))
        yy += ds + 3
    return yy


def tags(d, x, y, st):
    num, reg, place, head, deck, src, cert, chip, _ = st
    xx = chip_tag(d, x, y, cert, CLAIM if cert == "CLAIMED" else EST)
    T(d, (xx + 6, y + 2), src, F(10), MUTE)
    chip_tag(d, x, y + 18, chip, BRONZE_D)


WORLD = [
    "        oooo        ooo   ooooooo                               ",
    "      ooooooooo   ooooooooooooooooo  oooo                       ",
    "     oooooooooo  ooooooooooooooooooooooooo  oo                  ",
    "      oooooooo    oooooooooooooooooooooooo                      ",
    "       ooooo      ooooo  ooooooooooooo  ooo                     ",
    "       oooo        oo     oooooooooo      o                     ",
    "      ooooo               oooooooo                              ",
    "      oooo                 ooooo            o                   ",
    "     oooo                   ooo                                 ",
    "     ooo                                                        ",
    "     oo                              oooo                       ",
]
PINS = [(1, 0.47, 0.16), (2, 0.56, 0.34), (3, 0.55, 0.3), (4, 0.545, 0.33),
        (5, 0.455, 0.2), (6, 0.52, 0.14), (7, 0.525, 0.17),
        (10, 0.78, 0.32), (11, 0.44, 0.24), (13, 0.88, 0.78),
        (33, 0.13, 0.26), (36, 0.07, 0.3), (37, 0.16, 0.22)]


def draw_map(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(226, 233, 226))
    rows, cols = len(WORLD), max(len(r) for r in WORLD)
    for ri, row in enumerate(WORLD):
        for ci, ch in enumerate(row):
            if ch == "o":
                px = x0 + (ci + 0.5) * (x1 - x0) / cols
                py = y0 + (ri + 0.5) * (y1 - y0) / rows
                d.ellipse([px - 1.6, py - 1.6, px + 1.6, py + 1.6],
                          fill=(120, 140, 118))
    for num, fx, fy in PINS:
        px, py = x0 + fx * (x1 - x0), y0 + fy * (y1 - y0)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=BRONZE_D)
        T(d, (px, py - 5), str(num), F(9, True), WHITE, anchor="ma")
    T(d, (x0 + 4, y1 - 13), "Pins = card numbers on this page", F(9), MUTE)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 12
    T(d, (MX, 10), "ONE DAY - ONE PAGE - EVERY STORY DATED AND SOURCED",
      F(13, True), EST)
    T(d, (W - MX, 10), "37 STORIES - 9 REGIONS", F(13, True), BRONZE_D,
      anchor="ra")
    # inverted masthead: bronze band, cream serif, blue date block at right
    d.rectangle([MX, 34, W - MX, 104], fill=BRONZE_D)
    d.rectangle([MX, 34, W - MX, 38], fill=EST_D)
    d.rectangle([MX, 100, W - MX, 104], fill=EST_D)
    T(d, (MX + 16, 42), "THE TIDEWATER POST", F(38, disp=True), CREAM_TXT)
    T(d, (MX + 18, 84), "ESTUARY EDITION - BRONZE & BLUE", F(10, True),
      (238, 220, 170))
    d.rectangle([W - MX - 218, 42, W - MX - 8, 96], fill=EST_D)
    T(d, (W - MX - 113, 48), "TUESDAY", F(19, True), CREAM_TXT, anchor="ma")
    T(d, (W - MX - 113, 70), "25 NOVEMBER 2026", F(19, True), CREAM_TXT,
      anchor="ma")
    # number strip
    y = 112
    cw = (W - 2 * MX) / 8
    for i, (big, lab) in enumerate(NUMBERS):
        x = MX + i * cw
        if i:
            d.line([x, y + 2, x, y + 34], fill=(196, 182, 140), width=1)
        T(d, (x + cw / 2, y), big, F(20, True), EST_D, anchor="ma")
        T(d, (x + cw / 2, y + 25), lab, F(8, True), MUTE, anchor="ma")
    # region strip
    y = 154
    x = MX
    T(d, (x, y + 2), "REGIONS:", F(11, True), INK)
    x += d.textlength("REGIONS: ", font=F(11, True))
    for reg, n in REGIONS:
        lab = "%s %d" % (reg, n)
        tw = d.textlength(lab, font=F(10, True))
        d.rounded_rectangle([x, y, x + tw + 10, y + 16], 3, fill=RCOL[reg])
        T(d, (x + 5, y + 2), lab, F(10, True), WHITE)
        x += tw + 15
    # leads: three equal columns
    y = 178
    lw = (W - 2 * MX - 2 * 8) / 3
    lh = 252
    for i, st in enumerate(LEADS):
        x = MX + i * (lw + 8)
        d.rectangle([x, y, x + lw, y + lh], fill=CARD)
        d.rectangle([x, y, x + lw, y + lh], outline=BRONZE, width=2)
        scene(d, st[8], (x + 6, y + 6, x + lw - 6, y + 104))
        head_block(d, x + 8, y + 112, lw - 16, st, 18, 11.5, dmax=4)
        tags(d, x + 8, y + lh - 38, st)
    # grid 5 x 2
    y += lh + 8
    gw = (W - 2 * MX - 4 * 8) / 5
    gh = 138
    for idx, st in enumerate(GRID):
        r, c = divmod(idx, 5)
        x = MX + c * (gw + 8)
        yy0 = y + r * (gh + 8)
        d.rectangle([x, yy0, x + gw, yy0 + gh], fill=CARD)
        d.rectangle([x, yy0, x + gw, yy0 + gh],
                    outline=(196, 182, 140), width=1)
        scene(d, st[8], (x + 5, yy0 + 5, x + gw - 5, yy0 + 47))
        head_block(d, x + 6, yy0 + 51, gw - 12, st, 14, 10, dmax=2)
        tags(d, x + 6, yy0 + gh - 36, st)
    # briefs: 4 columns x 6
    y += 2 * gh + 16
    T(d, (MX, y), "ALSO ON THE PAGE - 24 MORE DATED STORIES, NUMBERED",
      F(13, True), BRONZE_D)
    y += 18
    colw = (W - 2 * MX - 3 * 12) / 4
    for idx, (num, reg, head, chip) in enumerate(BRIEFS):
        c, r = divmod(idx, 6)
        x = MX + c * (colw + 12)
        yy0 = y + r * 15
        T(d, (x, yy0), "%d." % num, F(10, True), RCOL[reg])
        s = head + " - " + chip
        f = F(10)
        while d.textlength(s, font=f) > colw - 20 and len(s) > 10:
            s = s[:-2]
        T(d, (x + 20, yy0), s, f, (52, 52, 50))
    # bottom band: timeline | map | date check
    y += 6 * 15 + 10
    d.line([MX, y - 4, W - MX, y - 4], fill=BRONZE, width=2)
    T(d, (MX, y), "THE DAY IN ORDER", F(12, True), EST_D)
    for i, (when, what) in enumerate(TIMELINE):
        yy0 = y + 20 + i * 15
        T(d, (MX, yy0), when, F(10, True), BRONZE_D)
        s = what
        f = F(10)
        while d.textlength(s, font=f) > 218 and len(s) > 10:
            s = s[:-2]
        T(d, (MX + 74, yy0), s, f, (52, 52, 50))
    mx0 = MX + 330
    T(d, (mx0, y), "WHERE IT HAPPENED - 13 PINS", F(12, True), EST_D)
    draw_map(d, (mx0, y + 18, mx0 + 330, y + 104))
    dx = MX + 690
    T(d, (dx, y), "DATE CHECK - NOT TODAY", F(12, True), CLAIM)
    for i, s in enumerate(DATECHECK):
        yy0 = y + 20 + i * 15
        T(d, (dx, yy0), "x", F(11, True), CLAIM)
        f = F(10)
        t = s
        while d.textlength(t, font=f) > W - MX - dx - 16 and len(t) > 10:
            t = t[:-2]
        T(d, (dx + 14, yy0), t, f, (52, 52, 50))
    fy = H - 26
    d.line([MX, fy - 4, W - MX, fy - 4], fill=BRONZE, width=2)
    T(d, (MX, fy), "Sources: RFE/RL - Al Jazeera - DW - Forbes - Starlit - "
      "wire roundups. Claims labelled as claims.", F(10), MUTE)
    T(d, (W - MX, fy), "Original drawings - drawn for this page",
      F(10, True), BRONZE_D, anchor="ra")
    img.save(os.path.join(HERE, "entry_b.png"), optimize=True)
    print("entry_b.png", os.path.getsize(os.path.join(HERE, "entry_b.png")))


if __name__ == "__main__":
    build()
