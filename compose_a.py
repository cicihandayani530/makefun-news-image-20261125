#!/usr/bin/env python3
"""THE TIDEWATER POST - variant A (Layout C: hero band + lead pair row).
One front page for Tuesday 25 November 2026. All figures come from the
locked NI25 pool. Drawn locally with PIL; stdlib + PIL only, no network.
Output: entry_a.png (1024x1024) beside this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
W = H = 1024

# ---- palette: bronze + estuary blue on cream paper -----------------------
PAPER = (246, 239, 219)
CARD = (255, 252, 242)
INK = (32, 34, 38)
MUTE = (96, 92, 78)
BRONZE = (154, 116, 51)
BRONZE_D = (110, 82, 34)
EST = (23, 69, 94)
EST_D = (13, 46, 66)
EST_L = (64, 116, 143)
CREAM_TXT = (250, 244, 224)
CLAIM = (163, 59, 46)
WHITE = (255, 255, 255)

REGION_COLORS = {
    "EUROPE": (58, 92, 140),
    "MIDDLE EAST": (176, 92, 44),
    "WORLD": (110, 82, 34),
    "AFRICA": (146, 108, 32),
    "AMERICAS": (46, 110, 90),
    "ASIA": (150, 62, 74),
    "SOUTH ASIA": (104, 74, 150),
    "ASIA-PACIFIC": (38, 122, 128),
    "OCEANIA": (66, 128, 178),
}

FONT_DIR = "/home/hatch/workspace/tools/bedah-19nov/news-image/fonts"
DEJA = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
DEJA_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
DEJA_O = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf"


def _find_font(names):
    try:
        files = os.listdir(FONT_DIR)
    except OSError:
        return None
    for want in names:
        for f in files:
            if want.lower() in f.lower() and f.lower().endswith((".ttf", ".otf")):
                return os.path.join(FONT_DIR, f)
    return None


DISPLAY = _find_font(["PlayfairDisplay-Black", "Playfair"]) or DEJA_B
SERIF_B = _find_font(["PlayfairDisplay-Bold", "Playfair"]) or DEJA_B


def F(size, kind="sans"):
    path = {"sans": DEJA, "bold": DEJA_B, "obl": DEJA_O,
            "disp": DISPLAY, "serif": SERIF_B}[kind]
    try:
        return ImageFont.truetype(path, size)
    except OSError:
        return ImageFont.load_default()


def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text(d, xy, s, font, fill=INK, anchor="la"):
    d.text(xy, s, font=font, fill=fill, anchor=anchor)


# ---- story data (locked pool, ni25-pool.md) -------------------------------
# num, region, place, headline, deck, source, certainty, chip, scene key
LEAD_HERO = (6, "WORLD", "UKRAINE WAR DATA",
             "700,000 Russian dead, new count finds",
             "A new analysis finds more than 700,000 Russian soldiers killed "
             "in the nearly five-year war on Ukraine - the 700000 toll is "
             "the day's starkest figure.",
             "RFE/RL", "REPORTED", "700,000+ KILLED", "crosses")
LEAD_PAIR = [
    (2, "MIDDLE EAST", "STRAIT OF HORMUZ",
     "Iran says 3 tankers hit by mines",
     "The IRGC Navy claims three oil tankers were hit by naval mines in "
     "the Strait of Hormuz; shipping concerns rise on the claim.",
     "Iranian claim via wires", "CLAIMED", "3 TANKERS HIT - IRAN SAYS",
     "hormuz"),
    (1, "EUROPE", "POLAND",
     "NATO sends early-warning jets to Poland",
     "NATO plans an AWACS deployment in Poland after Russian missiles "
     "landed in Poland; Chancellor Merz vows complete support.",
     "Wire reports", "REPORTED", "AWACS TO POLAND", "awacs"),
]
GRID = [
    (3, "MIDDLE EAST", "IRAQ",
     "Baghdad orders Kurdish oilfields seized",
     "PM al-Zaidi directs federal units to seize oilfields in Kurdish-run "
     "regions; Barzani says Kurdistan will not submit.",
     "Starlit / wires", "REPORTED", "OILFIELDS ORDER", "oil"),
    (4, "MIDDLE EAST", "GAZA",
     "Drone strikes kill Hamas security chief",
     "Israeli drone strikes killed a senior Hamas security official, "
     "three policemen and three siblings, one a child: 7 killed.",
     "Al Jazeera", "REPORTED", "7 KILLED IN STRIKES", "gaza"),
    (5, "EUROPE", "BRUSSELS",
     "EU unveils new Russia sanctions",
     "The European Union announced further restrictive measures - new "
     "sanctions - against Russia amid the war in Ukraine.",
     "Wire roundups", "REPORTED", "NEW EU SANCTIONS", "eu"),
    (7, "EUROPE", "UKRAINE",
     "First German Lynx fighting vehicles arrive",
     "The first 5 German Lynx KF41 infantry fighting vehicles enter "
     "Ukrainian deployment.",
     "Wires", "REPORTED", "5 LYNX KF41 IFVS", "lynx"),
    (10, "ASIA", "CHINA",
     "Xiamen Airlines orders 50 Boeing jets",
     "Xiamen Airlines, a China Southern unit, agreed to acquire 50 "
     "Boeing 737-8 jets.",
     "Wires", "REPORTED", "50 JETS ORDERED", "jet"),
    (11, "EUROPE", "MADRID",
     "Madrid rout PSV 5-1 in comeback",
     "Real Madrid overturned a deficit to beat PSV 5-1; a Bellingham "
     "stunner and an Mbappe brace sealed it.",
     "Wires", "REPORTED", "MADRID 5-1 PSV", "stadium"),
    (13, "OCEANIA", "AUSTRALIA",
     "12 coral species brought back",
     "Great Barrier Reef genetic analysis resurrects 12 Acropora coral "
     "species; reef diversity is wider than known.",
     "Science wires", "REPORTED", "12 SPECIES BACK", "coral"),
    (33, "WORLD", "WASHINGTON",
     "PCE inflation report due today",
     "The US PCE inflation report is due Tuesday 25 November; markets "
     "watch for the Fed's next signal. No figure yet.",
     "Scheduled", "SCHEDULED", "PCE DUE TODAY", "pce"),
    (36, "WORLD", "NVIDIA",
     "Nvidia's $1 trillion Monday",
     "Monday close: shares +31.5%, nearly $1 trillion of value clawed "
     "back as Huang was reinstated as CEO, +$34bn in a day.",
     "Forbes via wires", "REPORTED", "+31.5% MONDAY CLOSE", "chip"),
    (37, "AMERICAS", "USA",
     "Storms target Thanksgiving travel",
     "Inclement weather targeting both US shorelines poses a risk to "
     "Thanksgiving travel for millions.",
     "Wires", "REPORTED", "STORMS BOTH COASTS", "storm"),
]
# briefs: num, region, one-line headline, chip
BRIEFS = [
    (8, "AMERICAS", "Car bomb in Colombia injures at least 23", "23 INJURED"),
    (9, "AMERICAS", "Gunmen hold dozens in a Cartagena supermarket",
     "DOZENS HELD"),
    (12, "WORLD", "England level the T20I series in Australia, chasing 185; "
     "Fraser-McGurk 27 off 13", "ENGLAND BY 8 WICKETS"),
    (14, "OCEANIA", "Fiji declares a disaster amid an El Nino dry spell",
     "DISASTER DECLARED"),
    (15, "MIDDLE EAST", "Iran's pharmacies run dry in a medicine shortage",
     "MEDICINE SHORTAGE"),
    (16, "MIDDLE EAST", "Iran braces for winter gas shortages",
     "WINTER SHORTAGES"),
    (17, "MIDDLE EAST", "Britain sanctions Houthi leaders in London move",
     "UK SANCTIONS"),
    (18, "AFRICA", "Senegal's AFCON title restored by a CAS ruling",
     "TITLE RESTORED"),
    (19, "AFRICA", "Rebels pull back after clashes in DR Congo",
     "REBELS PULL BACK"),
    (20, "AFRICA", "Nigerian emir suspended after an allegation",
     "EMIR SUSPENDED"),
    (21, "AFRICA", "Sudan RSF commander defects in Sudan",
     "COMMANDER DEFECTS"),
    (22, "AFRICA", "Cameroon separatist in a Norway court on war crimes",
     "WAR CRIMES COURT"),
    (23, "SOUTH ASIA", "Old allies reunite in Punjab: BJP and Akali Dal",
     "ALLIANCE AGAIN"),
    (24, "SOUTH ASIA", "Bangladesh opens a China office in Guangzhou",
     "OFFICE OPENS"),
    (25, "ASIA-PACIFIC", "Indonesia's vice-president resigns", "VP RESIGNS"),
    (26, "ASIA-PACIFIC", "Solomon Islands eye an Australia treaty switch",
     "TREATY SWITCH"),
    (27, "ASIA", "North Korea touts China ties at embassy visit",
     "TIES TOUTED"),
    (28, "EUROPE", "Denmark court upholds the ghetto evictions law",
     "COURT UPHOLDS LAW"),
    (29, "EUROPE", "Sarkozy headed for a Libya-case trial in Paris",
     "TRIAL AHEAD"),
    (30, "EUROPE", "Black Sea clash at the UN over shipping attacks",
     "UN CLASH"),
    (31, "WORLD", "Shortwave school returns for Afghan girls",
     "SHORTWAVE RETURNS"),
    (32, "WORLD", "An asteroid eclipses its twin: Dimorphos shadows Didymos",
     "ASTEROID ECLIPSE"),
    (34, "AMERICAS", "US targets 7 firms over chip diversion; one is "
     "Alibaba-owned", "7 FIRMS TARGETED"),
    (35, "EUROPE", "Decoy army: Moscow buys inflatable decoys from China",
     "INFLATABLE DECOYS"),
]
REGION_ORDER = ["EUROPE", "MIDDLE EAST", "WORLD", "AFRICA", "AMERICAS",
                "ASIA", "SOUTH ASIA", "ASIA-PACIFIC", "OCEANIA"]
REGION_COUNTS = {"EUROPE": 8, "MIDDLE EAST": 6, "WORLD": 6, "AFRICA": 5,
                 "AMERICAS": 4, "ASIA": 2, "SOUTH ASIA": 2,
                 "ASIA-PACIFIC": 2, "OCEANIA": 2}
NUMBERS = [("700,000+", "RUSSIAN DEAD - NEW COUNT"),
           ("3", "TANKERS HIT - IRAN SAYS"),
           ("AWACS", "JETS TO POLAND"),
           ("7", "KILLED IN GAZA STRIKES"),
           ("5-1", "MADRID OVER PSV"),
           ("50", "BOEING 737-8 JETS"),
           ("+31.5%", "NVIDIA MONDAY CLOSE"),
           ("12", "CORAL SPECIES BACK")]
TIMELINE = [("EARLY", "NATO AWACS plan for Poland reported"),
            ("MORNING", "Iran says 3 tankers hit mines in Hormuz"),
            ("MIDDAY", "Baghdad orders Kurdish oilfields seized"),
            ("TODAY", "US PCE inflation report due - no figure yet"),
            ("MON CLOSE", "Nvidia +31.5% - Monday close, Forbes"),
            ("TONIGHT", "Storms target Thanksgiving travel, both coasts")]
DATECHECK = ["GTA VI launch hype - a game date, not today's news",
             "COP31 climate talks - earlier this month, not Tuesday",
             "Liverpool 4-0 - a weekend score, not 25 November",
             "Merkury stories filed 23 Nov - two days old, excluded",
             "Black Friday sales - Friday's story, not Tuesday's"]


# ---- layered flat scene illustrations -------------------------------------
def _sky(d, box, top, bot):
    x0, y0, x1, y1 = box
    steps = 24
    for i in range(steps):
        t = i / steps
        c = tuple(int(top[k] + (bot[k] - top[k]) * t) for k in range(3))
        yy = y0 + (y1 - y0) * i // steps
        d.rectangle([x0, yy, x1, y0 + (y1 - y0) * (i + 1) // steps + 1],
                    fill=c)


def scene(d, key, box):
    """Draw one story-specific layered flat scene inside box."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    d.rectangle(box, fill=(238, 231, 205))
    if key == "crosses":  # hero: field of markers, ruined towers, dusk sky
        _sky(d, box, (58, 62, 84), (196, 132, 74))
        d.rectangle([x0, y1 - h * 0.34, x1, y1], fill=(74, 66, 48))
        for tx, th in ((0.06, 0.52), (0.16, 0.38), (0.86, 0.46)):
            bx = x0 + w * tx
            d.rectangle([bx, y0 + h * (0.62 - th), bx + w * 0.055,
                         y1 - h * 0.34], fill=(40, 40, 48))
            d.rectangle([bx + w * 0.012, y0 + h * (0.62 - th) + 4,
                         bx + w * 0.03, y0 + h * (0.62 - th) + 12],
                        fill=(240, 200, 110))
        for r in range(3):
            for i in range(9):
                cx = x0 + w * (0.08 + 0.1 * i) + r * 7
                cy = y1 - h * (0.26 - 0.07 * r)
                s = 5 - r
                d.line([cx, cy - s, cx, cy + s], fill=(238, 232, 210),
                       width=2)
                d.line([cx - s + 2, cy - s + 2, cx + s - 2, cy - s + 2],
                       fill=(238, 232, 210), width=2)
        d.ellipse([x0 + w * 0.68, y0 + h * 0.1, x0 + w * 0.78,
                   y0 + h * 0.1 + w * 0.1], fill=(238, 178, 92))
    elif key == "hormuz":  # strait, two headlands, 3 tankers, mines
        _sky(d, box, (168, 196, 208), (226, 232, 214))
        d.rectangle([x0, y0 + h * 0.52, x1, y1], fill=(38, 92, 118))
        d.polygon([(x0, y0 + h * 0.52), (x0 + w * 0.3, y0 + h * 0.52),
                   (x0 + w * 0.12, y1)], fill=(150, 118, 66))
        d.polygon([(x1, y0 + h * 0.52), (x0 + w * 0.72, y0 + h * 0.52),
                   (x0 + w * 0.9, y1)], fill=(150, 118, 66))
        for i, fx in enumerate((0.36, 0.5, 0.63)):
            tx, ty = x0 + w * fx, y0 + h * (0.56 + 0.1 * (i % 2))
            d.polygon([(tx, ty), (tx + w * 0.13, ty), (tx + w * 0.11,
                        ty + h * 0.09), (tx + w * 0.02, ty + h * 0.09)],
                      fill=(52, 54, 60))
            d.rectangle([tx + w * 0.03, ty - h * 0.07, tx + w * 0.09,
                         ty], fill=(120, 70, 44))
        for fx, fy in ((0.44, 0.82), (0.58, 0.9)):
            mx, my = x0 + w * fx, y0 + h * fy
            d.ellipse([mx - 5, my - 5, mx + 5, my + 5], fill=(30, 30, 34))
            for a in range(0, 360, 60):
                import math
                d.line([mx, my, mx + 8 * math.cos(a * 3.1416 / 180),
                        my + 8 * math.sin(a * 3.1416 / 180)],
                       fill=(30, 30, 34), width=2)
    elif key == "awacs":  # radar jet with disc, rings, second jet
        _sky(d, box, (140, 178, 205), (224, 234, 226))
        cx, cy = x0 + w * 0.46, y0 + h * 0.52
        for r in (0.16, 0.26, 0.36):
            d.ellipse([cx - w * r, cy - w * r * 0.42, cx + w * r,
                       cy + w * r * 0.42], outline=(90, 130, 160), width=2)
        d.polygon([(cx - w * 0.2, cy), (cx + w * 0.16, cy - h * 0.05),
                   (cx + w * 0.22, cy), (cx + w * 0.16, cy + h * 0.05)],
                  fill=(70, 78, 90))
        d.polygon([(cx - w * 0.2, cy), (cx - w * 0.27, cy - h * 0.14),
                   (cx - w * 0.24, cy + h * 0.02)], fill=(52, 60, 72))
        d.rectangle([cx - w * 0.03, cy - h * 0.17, cx + w * 0.05,
                     cy - h * 0.1], fill=(52, 60, 72))
        d.ellipse([cx - w * 0.07, cy - h * 0.22, cx + w * 0.09,
                   cy - h * 0.15], fill=(38, 44, 54))
        d.polygon([(x0 + w * 0.8, y0 + h * 0.3), (x0 + w * 0.9,
                    y0 + h * 0.26), (x0 + w * 0.88, y0 + h * 0.34)],
                  fill=(90, 98, 112))
    elif key == "oil":  # pumpjacks + derrick + pipeline
        _sky(d, box, (214, 178, 120), (240, 226, 190))
        d.rectangle([x0, y1 - h * 0.3, x1, y1], fill=(146, 112, 62))
        for fx in (0.14, 0.52):
            bx, by = x0 + w * fx, y1 - h * 0.3
            d.line([bx, by, bx + w * 0.2, by - h * 0.34], fill=(52, 50, 46),
                   width=4)
            d.line([bx + w * 0.05, by, bx + w * 0.05, by - h * 0.3],
                   fill=(52, 50, 46), width=3)
            d.polygon([(bx + w * 0.17, by - h * 0.4), (bx + w * 0.24,
                        by - h * 0.3), (bx + w * 0.18, by - h * 0.26)],
                      fill=(52, 50, 46))
        dx = x0 + w * 0.82
        d.polygon([(dx, y1 - h * 0.3), (dx + w * 0.05, y0 + h * 0.14),
                   (dx + w * 0.1, y1 - h * 0.3)], outline=(52, 50, 46),
                  width=3)
        d.rectangle([x0, y1 - h * 0.1, x1, y1 - h * 0.05],
                    fill=(90, 88, 82))
    elif key == "gaza":  # rooftops, drone silhouette, smoke (no gore)
        _sky(d, box, (196, 186, 168), (232, 224, 204))
        for i, (fx, fh) in enumerate(((0.04, 0.42), (0.3, 0.55),
                                      (0.56, 0.38), (0.8, 0.5))):
            bx = x0 + w * fx
            d.rectangle([bx, y1 - h * fh, bx + w * 0.2, y1],
                        fill=(120, 108, 92) if i % 2 else (138, 124, 104))
            for wy in range(2):
                d.rectangle([bx + 6, y1 - h * fh + 8 + wy * 14,
                             bx + 14, y1 - h * fh + 15 + wy * 14],
                            fill=(240, 214, 140))
        for fx in (0.36, 0.86):
            sx = x0 + w * fx
            for r in range(3):
                d.ellipse([sx - 5 - r * 3, y0 + h * 0.34 - r * 12,
                           sx + 5 + r * 3, y0 + h * 0.34 - r * 12 + 9],
                          fill=(150, 146, 140))
        dx, dy = x0 + w * 0.6, y0 + h * 0.18
        d.line([dx - 16, dy, dx + 16, dy], fill=(40, 40, 44), width=3)
        d.line([dx, dy - 8, dx, dy + 8], fill=(40, 40, 44), width=3)
        d.rectangle([dx - 6, dy - 4, dx + 6, dy + 4], fill=(40, 40, 44))
    elif key == "eu":  # circle of stars over a document
        _sky(d, box, (52, 78, 140), (96, 122, 178))
        cx, cy, r = x0 + w * 0.3, y0 + h * 0.48, h * 0.3
        import math
        for i in range(12):
            a = 2 * math.pi * i / 12
            sx, sy = cx + r * math.cos(a), cy + r * math.sin(a)
            d.polygon([(sx, sy - 5), (sx + 4, sy + 4), (sx - 4, sy + 4)],
                      fill=(244, 200, 70))
        d.rectangle([x0 + w * 0.58, y0 + h * 0.16, x0 + w * 0.92,
                     y0 + h * 0.84], fill=(246, 242, 228))
        for i in range(4):
            d.line([x0 + w * 0.63, y0 + h * (0.3 + 0.13 * i),
                    x0 + w * 0.87, y0 + h * (0.3 + 0.13 * i)],
                   fill=(120, 116, 104), width=2)
    elif key == "lynx":  # armoured vehicle side profile
        _sky(d, box, (170, 188, 176), (228, 232, 208))
        d.rectangle([x0, y1 - h * 0.26, x1, y1], fill=(104, 110, 84))
        bx, by = x0 + w * 0.12, y1 - h * 0.26
        d.polygon([(bx, by), (bx + w * 0.62, by), (bx + w * 0.7,
                    by - h * 0.2), (bx + w * 0.2, by - h * 0.24),
                   (bx, by - h * 0.14)], fill=(86, 96, 70))
        d.rectangle([bx + w * 0.3, by - h * 0.38, bx + w * 0.52,
                     by - h * 0.22], fill=(74, 84, 60))
        d.line([bx + w * 0.5, by - h * 0.32, bx + w * 0.78,
                by - h * 0.4], fill=(50, 56, 42), width=4)
        for i in range(5):
            wx = bx + w * (0.08 + 0.13 * i)
            d.ellipse([wx, by - h * 0.1, wx + w * 0.09, by - h * 0.01],
                      fill=(44, 48, 38))
    elif key == "jet":  # airliner climbing, tail fin, clouds
        _sky(d, box, (120, 168, 205), (226, 238, 240))
        cx, cy = x0 + w * 0.5, y0 + h * 0.52
        d.polygon([(cx - w * 0.34, cy), (cx + w * 0.26, cy - h * 0.1),
                   (cx + w * 0.36, cy), (cx + w * 0.26, cy + h * 0.08),
                   (cx - w * 0.3, cy + h * 0.05)], fill=(238, 240, 244))
        d.polygon([(cx - w * 0.32, cy), (cx - w * 0.42, cy - h * 0.24),
                   (cx - w * 0.28, cy - h * 0.02)], fill=(38, 92, 140))
        d.polygon([(cx - w * 0.02, cy + h * 0.03), (cx + w * 0.1,
                    cy + h * 0.26), (cx + w * 0.18, cy + h * 0.04)],
                  fill=(200, 206, 214))
        for fx, fy in ((0.16, 0.8), (0.78, 0.2)):
            ex, ey = x0 + w * fx, y0 + h * fy
            d.ellipse([ex, ey, ex + w * 0.16, ey + h * 0.12],
                      fill=(250, 250, 248))
    elif key == "stadium":  # stadium arc, pitch, ball, scoreboard
        _sky(d, box, (70, 110, 80), (150, 190, 140))
        d.rectangle([x0, y1 - h * 0.4, x1, y1], fill=(64, 140, 74))
        d.arc([x0 + w * 0.08, y0 + h * 0.06, x0 + w * 0.66,
               y0 + h * 0.95], 180, 360, fill=(230, 230, 224), width=5)
        d.arc([x0 + w * 0.08, y0 + h * 0.2, x0 + w * 0.66,
               y0 + h * 1.05], 180, 360, fill=(190, 190, 184), width=4)
        d.ellipse([x0 + w * 0.42, y1 - h * 0.3, x0 + w * 0.52,
                   y1 - h * 0.3 + w * 0.1], fill=(250, 250, 250),
                  outline=(60, 60, 60))
        d.rectangle([x0 + w * 0.72, y0 + h * 0.14, x0 + w * 0.96,
                     y0 + h * 0.5], fill=(30, 34, 40))
        text(d, (x0 + w * 0.84, y0 + h * 0.32), "5-1", F(17, "bold"),
             (250, 220, 120), anchor="mm")
    elif key == "coral":  # reef scene: branching coral, fish, rays
        _sky(d, box, (36, 110, 150), (110, 190, 205))
        d.rectangle([x0, y1 - h * 0.18, x1, y1], fill=(214, 196, 150))
        def branch(bx, by, s, col):
            d.line([bx, by, bx, by - s], fill=col, width=4)
            d.line([bx, by - s * 0.5, bx - s * 0.4, by - s * 0.9],
                   fill=col, width=3)
            d.line([bx, by - s * 0.6, bx + s * 0.4, by - s], fill=col,
                   width=3)
        branch(x0 + w * 0.24, y1 - h * 0.16, h * 0.5, (232, 110, 90))
        branch(x0 + w * 0.55, y1 - h * 0.16, h * 0.66, (244, 150, 90))
        branch(x0 + w * 0.82, y1 - h * 0.16, h * 0.42, (226, 92, 120))
        for fx, fy in ((0.4, 0.3), (0.68, 0.2)):
            ex, ey = x0 + w * fx, y0 + h * fy
            d.polygon([(ex, ey), (ex + 14, ey + 5), (ex, ey + 10),
                       (ex - 6, ey + 5)], fill=(250, 210, 90))
    elif key == "pce":  # dashed chart, clock, calendar - NO invented figure
        _sky(d, box, (232, 226, 204), (246, 240, 222))
        for gx in range(1, 5):
            d.line([x0 + w * gx / 5, y0 + 6, x0 + w * gx / 5, y1 - 6],
                   fill=(206, 198, 172), width=1)
        pts = [(0.06, 0.66), (0.28, 0.52), (0.5, 0.58), (0.72, 0.4)]
        for i in range(len(pts) - 1):
            d.line([x0 + w * pts[i][0], y0 + h * pts[i][1],
                    x0 + w * pts[i + 1][0], y0 + h * pts[i + 1][1]],
                   fill=BRONZE_D, width=3)
        cx, cy = x0 + w * 0.85, y0 + h * 0.34
        d.ellipse([cx - 13, cy - 13, cx + 13, cy + 13],
                  outline=INK, width=3)
        d.line([cx, cy, cx, cy - 9], fill=INK, width=2)
        d.line([cx, cy, cx + 7, cy + 3], fill=INK, width=2)
        text(d, (x0 + w * 0.5, y1 - h * 0.14), "DUE TODAY",
             F(13, "bold"), CLAIM, anchor="mm")
    elif key == "chip":  # microchip + rising bars
        _sky(d, box, (30, 44, 58), (58, 84, 104))
        cx, cy, s = x0 + w * 0.3, y0 + h * 0.5, h * 0.44
        d.rectangle([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2],
                    fill=(52, 130, 96), outline=(180, 220, 190), width=2)
        for i in range(3):
            px = cx - s / 2 + (i + 0.5) * s / 3
            d.line([px, cy - s / 2, px, cy - s / 2 - 7],
                   fill=(200, 210, 200), width=2)
            d.line([px, cy + s / 2, px, cy + s / 2 + 7],
                   fill=(200, 210, 200), width=2)
        for i, bh in enumerate((0.2, 0.36, 0.58)):
            bx = x0 + w * (0.56 + 0.13 * i)
            d.rectangle([bx, y1 - h * (0.14 + bh), bx + w * 0.09,
                         y1 - h * 0.14], fill=(240, 190, 80))
    elif key == "storm":  # two coast storm swirls + plane route
        _sky(d, box, (96, 116, 138), (178, 192, 200))
        d.rectangle([x0, y1 - h * 0.3, x1, y1], fill=(52, 92, 118))
        import math
        for cx, cy in ((x0 + w * 0.2, y0 + h * 0.36),
                       (x0 + w * 0.82, y0 + h * 0.3)):
            for r in (5, 10, 15):
                d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300,
                      fill=(240, 244, 246), width=3)
        d.line([x0 + w * 0.2, y0 + h * 0.62, x0 + w * 0.82,
                y0 + h * 0.56], fill=(250, 220, 120), width=2)
        mxp, myp = x0 + w * 0.51, y0 + h * 0.59
        d.polygon([(mxp - 8, myp), (mxp + 8, myp - 3), (mxp + 4, myp + 3)],
                  fill=(250, 250, 250))
    d.rectangle(box, outline=(178, 164, 124), width=1)


# ---- page assembly (Layout C) ----------------------------------------------
def chip_tag(d, x, y, s, fill):
    f = F(10, "bold")
    tw = d.textlength(s, font=f)
    d.rounded_rectangle([x, y, x + tw + 12, y + 15], 3, fill=fill)
    text(d, (x + 6, y + 2), s, f, WHITE)
    return x + tw + 12


def card_head(d, x, y, maxw, story, hsize, dsize, hmax=2, dmax=3):
    num, region, place, head, deck, src, cert, chip, _ = story
    col = REGION_COLORS[region]
    f = F(10, "bold")
    text(d, (x, y), "%d - %s - %s" % (num, region, place), f, col)
    yy = y + 14
    for ln in wrap(d, head, F(hsize, "bold"), maxw)[:hmax]:
        text(d, (x, yy), ln, F(hsize, "bold"), INK)
        yy += hsize + 3
    for ln in wrap(d, deck, F(dsize), maxw)[:dmax]:
        text(d, (x, yy), ln, F(dsize), (52, 52, 50))
        yy += dsize + 3
    return yy


def tag_row(d, x, y, story, maxw):
    num, region, place, head, deck, src, cert, chip, _ = story
    ccol = CLAIM if cert == "CLAIMED" else EST
    xx = chip_tag(d, x, y, cert, ccol)
    f = F(10)
    text(d, (xx + 6, y + 2), src, f, MUTE)
    chip_tag(d, x, y + 18, chip, BRONZE_D)


def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 12
    # kicker
    text(d, (MX, 10), "37 DATED STORIES - 9 REGIONS - 13 FULL-SCENE CARDS",
         F(13, "bold"), BRONZE_D)
    text(d, (W - MX, 10), "ESTUARY EDITION - ONE DAY, ONE PAGE",
         F(13, "bold"), EST, anchor="ra")
    # masthead
    d.rectangle([MX, 34, W - MX, 102], fill=EST_D)
    d.rectangle([MX, 34, W - MX, 38], fill=BRONZE)
    d.rectangle([MX, 98, W - MX, 102], fill=BRONZE)
    text(d, (W // 2, 44), "THE TIDEWATER POST", F(52, "disp"), CREAM_TXT,
         anchor="ma")
    text(d, (MX + 10, 82), "BRONZE & ESTUARY", F(10, "bold"), (198, 178, 128))
    text(d, (W - MX - 10, 82), "No. 25-11", F(10, "bold"), (198, 178, 128),
         anchor="ra")
    # date band
    d.rectangle([MX, 108, W - MX, 146], fill=(238, 229, 200))
    text(d, (W // 2, 114), "TUESDAY 25 NOVEMBER 2026", F(30, "bold"), INK,
         anchor="ma")
    # number strip (8 cells)
    y = 152
    cw = (W - 2 * MX) / 8
    for i, (big, lab) in enumerate(NUMBERS):
        x = MX + i * cw
        if i:
            d.line([x, y + 2, x, y + 34], fill=(196, 182, 140), width=1)
        text(d, (x + cw / 2, y), big, F(21, "bold"), EST_D, anchor="ma")
        for j, ln in enumerate(wrap(d, lab, F(8, "bold"), cw - 6)[:2]):
            text(d, (x + cw / 2, y + 25 + j * 9), ln, F(8, "bold"), MUTE,
                 anchor="ma")
    # region strip (9 chips with honest counts)
    y = 196
    x = MX
    text(d, (x, y + 2), "REGIONS:", F(11, "bold"), INK)
    x += d.textlength("REGIONS: ", font=F(11, "bold"))
    for reg in REGION_ORDER:
        lab = "%s %d" % (reg, REGION_COUNTS[reg])
        tw = d.textlength(lab, font=F(10, "bold"))
        d.rounded_rectangle([x, y, x + tw + 10, y + 16], 3,
                            fill=REGION_COLORS[reg])
        text(d, (x + 5, y + 2), lab, F(10, "bold"), WHITE)
        x += tw + 15
    # leads: hero band (#6) then pair row (#2, #1)
    y = 220
    d.rectangle([MX, y, W - MX, y + 148], fill=CARD)
    d.rectangle([MX, y, W - MX, y + 148], outline=BRONZE, width=2)
    scene(d, LEAD_HERO[8], (MX + 8, y + 8, MX + 368, y + 140))
    yy = card_head(d, MX + 384, y + 10, W - MX - 384 - 10, LEAD_HERO,
                   26, 14, hmax=2, dmax=4)
    tag_row(d, MX + 384, y + 148 - 40, LEAD_HERO, 0)
    y += 156
    half = (W - 2 * MX - 8) / 2
    for i, st in enumerate(LEAD_PAIR):
        x = MX + i * (half + 8)
        d.rectangle([x, y, x + half, y + 92], fill=CARD)
        d.rectangle([x, y, x + half, y + 92], outline=EST_L, width=1)
        scene(d, st[8], (x + 6, y + 6, x + 150, y + 86))
        card_head(d, x + 160, y + 6, half - 168, st, 16, 11, hmax=2,
                  dmax=3)
        tag_row(d, x + 160, y + 92 - 38, st, 0)
    # grid: 10 cards, 5 x 2
    y += 100
    gw = (W - 2 * MX - 4 * 8) / 5
    gh = 138
    for idx, st in enumerate(GRID):
        r, c = divmod(idx, 5)
        x = MX + c * (gw + 8)
        yy0 = y + r * (gh + 8)
        d.rectangle([x, yy0, x + gw, yy0 + gh], fill=CARD)
        d.rectangle([x, yy0, x + gw, yy0 + gh], outline=(196, 182, 140),
                    width=1)
        scene(d, st[8], (x + 5, yy0 + 5, x + gw - 5, yy0 + 47))
        cy = card_head(d, x + 6, yy0 + 51, gw - 12, st, 14, 10, hmax=2,
                       dmax=2)
        tag_row(d, x + 6, yy0 + gh - 36, st, 0)
    # briefs band: 24 more stories, 3 columns x 8
    y += 2 * gh + 16
    text(d, (MX, y), "ALSO ON THE PAGE - 24 MORE DATED STORIES, NUMBERED",
         F(13, "bold"), BRONZE_D)
    y += 18
    colw = (W - 2 * MX - 2 * 16) / 3
    for idx, (num, reg, head, chip) in enumerate(BRIEFS):
        c, r = divmod(idx, 8)
        x = MX + c * (colw + 16)
        yy0 = y + r * 14
        text(d, (x, yy0), "%d." % num, F(10, "bold"),
             REGION_COLORS[reg])
        s = head + " - " + chip
        f = F(10)
        while d.textlength(s, font=f) > colw - 22 and len(s) > 10:
            s = s[:-2]
        text(d, (x + 20, yy0), s, f, (52, 52, 50))
    # bottom band: map | timeline | date check
    y += 8 * 14 + 8
    d.line([MX, y - 4, W - MX, y - 4], fill=BRONZE, width=2)
    # map panel
    text(d, (MX, y), "WHERE IT HAPPENED - 13 CARD PINS", F(12, "bold"),
         EST_D)
    map_box = (MX, y + 18, MX + 380, y + 104)
    draw_map(d, map_box)
    # timeline panel
    tx = MX + 396
    text(d, (tx, y), "THE DAY IN ORDER", F(12, "bold"), EST_D)
    for i, (when, what) in enumerate(TIMELINE):
        yy0 = y + 20 + i * 15
        text(d, (tx, yy0), when, F(10, "bold"), BRONZE_D)
        s = what
        f = F(10)
        while d.textlength(s, font=f) > 268 and len(s) > 10:
            s = s[:-2]
        text(d, (tx + 74, yy0), s, f, (52, 52, 50))
    # date check panel
    dx = MX + 700
    text(d, (dx, y), "DATE CHECK - NOT TODAY'S NEWS", F(12, "bold"),
         CLAIM)
    for i, s in enumerate(DATECHECK):
        yy0 = y + 20 + i * 15
        text(d, (dx, yy0), "x", F(11, "bold"), CLAIM)
        f = F(10)
        t = s
        while d.textlength(t, font=f) > W - MX - dx - 16 and len(t) > 10:
            t = t[:-2]
        text(d, (dx + 14, yy0), t, f, (52, 52, 50))
    # footer
    fy = H - 26
    d.line([MX, fy - 4, W - MX, fy - 4], fill=BRONZE, width=2)
    text(d, (MX, fy), "Sources: RFE/RL - Al Jazeera - DW - Forbes - Starlit "
         "- wire roundups. Claims are labelled as claims.",
         F(10), MUTE)
    text(d, (W - MX, fy), "Original drawings - drawn for this page",
         F(10, "bold"), BRONZE_D, anchor="ra")
    img.save(os.path.join(HERE, "entry_a.png"), optimize=True)
    print("entry_a.png", os.path.getsize(os.path.join(HERE, "entry_a.png")))


# schematic dotted world + numbered pins for the 13 full-scene cards
WORLD = [
    "                                                                ",
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
    "                                                                ",
]
PINS = [(1, 0.47, 0.16), (2, 0.56, 0.34), (3, 0.55, 0.3), (4, 0.545, 0.33),
        (5, 0.455, 0.2), (6, 0.52, 0.14), (7, 0.525, 0.17),
        (10, 0.78, 0.32), (11, 0.44, 0.24), (13, 0.88, 0.78),
        (33, 0.13, 0.26), (36, 0.07, 0.3), (37, 0.16, 0.22)]


def draw_map(d, box):
    x0, y0, x1, y1 = box
    d.rectangle(box, fill=(226, 233, 226))
    rows = len(WORLD)
    cols = max(len(r) for r in WORLD)
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
        text(d, (px, py - 5), str(num), F(9, "bold"), WHITE, anchor="ma")
    text(d, (x0 + 4, y1 - 13), "Pins = card numbers on this page",
         F(9), MUTE)


if __name__ == "__main__":
    build()
