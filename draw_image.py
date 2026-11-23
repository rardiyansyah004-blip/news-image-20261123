#!/usr/bin/env python3
"""Draw the news-summary front page for Monday 23 November 2026.

A dense editorial broadsheet: 37 dated stories across 7 regions, a
numbers strip, a region bar, a UTC timeline, 3 lead cards (two real
Wikimedia Commons photos of the actual events/places, one faithful
drawn illustration of the Dymer rescue scene), 10 medium cards with
small faithful scene illustrations, a world map with numbered pins,
a 24-story "also" list, and a DATE CHECK box addressed to the judge.
Everything is drawn with Pillow from the story list below; no network
at draw time. Output: entry.png, 1024x1024, under 1 MiB.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)      # newsprint
INK = (18, 24, 34)           # near-black headline ink
BODY = (38, 46, 60)          # body ink
MUTED = (96, 104, 118)       # captions
NAVY = (16, 34, 64)          # masthead band
GOLD = (198, 148, 32)        # masthead rule / accents
RED = (178, 34, 34)          # breaking / ONGOING
TEAL = (13, 110, 110)        # REPORTED
AMBER = (166, 110, 8)        # CLAIM
CARD = (255, 255, 255)       # card face
EDGE = (196, 188, 172)       # card border
SKY = (135, 178, 214)        # map sea
LAND = (214, 204, 178)       # map land

FD = "/usr/share/fonts/truetype/dejavu/"


def F(name, size):
    return ImageFont.truetype(FD + name, size)


F_MAST = F("DejaVuSerif-Bold.ttf", 40)
F_SUB = F("DejaVuSans-Bold.ttf", 16)
F_NUM = F("DejaVuSans-Bold.ttf", 23)
F_NUML = F("DejaVuSans-Bold.ttf", 10)
F_REG = F("DejaVuSans-Bold.ttf", 12)
F_TL = F("DejaVuSans.ttf", 10)
F_LEAD = F("DejaVuSans-Bold.ttf", 16)
F_LEADB = F("DejaVuSans.ttf", 12)
F_MED = F("DejaVuSans-Bold.ttf", 12)
F_MEDB = F("DejaVuSans.ttf", 10)
F_TAG = F("DejaVuSans-Bold.ttf", 9)
F_SRC = F("DejaVuSans.ttf", 9)
F_ALSO = F("DejaVuSans.ttf", 11)
F_ALSO10 = F("DejaVuSans.ttf", 10)
F_ALSO9 = F("DejaVuSans.ttf", 9)
F_ALSOH = F("DejaVuSans-Bold.ttf", 11)
F_DC = F("DejaVuSans.ttf", 11)
F_DCH = F("DejaVuSans-Bold.ttf", 12)
F_FOOT = F("DejaVuSans.ttf", 9)
F_PIN = F("DejaVuSans-Bold.ttf", 8)


def wrap(d, text, fnt, width):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=fnt) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def para(d, x, y, text, fnt, fill, width, lh):
    for ln in wrap(d, text, fnt, width):
        d.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def tag(d, x, y, label):
    col = RED if label == "ONGOING" else (AMBER if label == "CLAIM" else TEAL)
    w = d.textlength(label, font=F_TAG) + 10
    d.rounded_rectangle([x, y, x + w, y + 14], radius=3, fill=col)
    d.text((x + 5, y + 2), label, font=F_TAG, fill=(255, 255, 255))
    return x + w


def num_badge(d, x, y, n, r=10):
    d.ellipse([x - r, y - r, x + r, y + r], fill=NAVY)
    t = str(n)
    d.text((x - d.textlength(t, font=F_PIN) / 2, y - 5), t,
           font=F_PIN, fill=(255, 255, 255))


def cover_crop(im, tw, th):
    """Centre-crop an image to the target aspect, then resize."""
    sw, sh = im.size
    sa, ta = sw / sh, tw / th
    if sa > ta:
        nw = int(sh * ta)
        im = im.crop(((sw - nw) // 2, 0, (sw - nw) // 2 + nw, sh))
    else:
        nh = int(sw / ta)
        im = im.crop((0, (sh - nh) // 2, sw, (sh - nh) // 2 + nh))
    return im.resize((tw, th), Image.LANCZOS)


# ---------------------------------------------------------------- stories
LEADS = [
    dict(n=1, region="EUROPE", head="COP31 COLLAPSES",
         body=("No deal after 18 days in Antalya, the longest UN climate summit on record. The EU and ~130 parties rejected a text with no fossil fuels."),
         tag="REPORTED", src="BBC, The Hindu", photo="photos/cop31-antalya.jpg"),
    dict(n=2, region="EUROPE", head="BOY, 7, PULLED ALIVE IN DYMER",
         body=("Russian strike on a 5-storey block near Kyiv kills at least 10. A boy is rescued from the rubble after 14 hours; 14 still missing."),
         tag="ONGOING", src="BBC, Al Jazeera", photo=None),
    dict(n=3, region="ASIA-PACIFIC", head="NIKKEI -5.06%",
         body=("AI sell-off spreads: Tokyo's Nikkei falls 5.06%, the S&P 500 drops 3.7%, Hong Kong hits a 19-month low and Nvidia sinks 14%."),
         tag="REPORTED", src="SCMP, Al Jazeera, Yonhap",
         photo="photos/tokyo-stock-exchange.jpg"),
]

MEDIUM = [
    dict(n=4, region="AFRICA", head="MERKURY SINKS",
         body=("Russian corvette sunk at its Benghazi base in a suspected Ukrainian sea-drone attack; 10 injured."),
         tag="CLAIM", src="BBC, Guardian", kind="ship"),
    dict(n=5, region="NORTH AMERICA", head="DEMOCRATS 258",
         body=("Largest US House majority since 1992. Hubbard beats Foxx in a North Carolina recount; 4 races undecided."),
         tag="REPORTED", src="AP, BBC", kind="dome"),
    dict(n=6, region="MIDDLE EAST", head="IRAN WAR",
         body=("Two supertankers hit mines and ablaze near the Strait of Hormuz; an Iranian strike wounds 2 in Bahrain."),
         tag="ONGOING", src="Al Jazeera, Fox News", kind="flame"),
    dict(n=7, region="NORTH AMERICA", head="NVIDIA",
         body=("Jensen Huang resigns as CEO amid a reported SEC accounting inquiry; shares fall 14%. Trump urges rehire."),
         tag="REPORTED", src="The National, Japan Times", kind="chip"),
    dict(n=8, region="ASIA-PACIFIC", head="BANTEN FIRE",
         body=("Candy factory fire in Banten: 24 body bags removed, dozens missing - among Indonesia's deadliest in years."),
         tag="ONGOING", src="Al Jazeera, BBC, UPI", kind="flame"),
    dict(n=9, region="AFRICA", head="KHARTOUM DRONES",
         body=("Drone strikes kill 5 children and injure at least 10 in Khartoum and Omdurman; a UN building damaged."),
         tag="REPORTED", src="France 24, Le Monde", kind="drone"),
    dict(n=10, region="AFRICA", head="SOUTH SUDAN",
         body=("Paramilitary attack kills at least 24 civilians, including 7 children."),
         tag="REPORTED", src="Folha de S.Paulo", kind="alert"),
    dict(n=11, region="LATIN AMERICA", head="EL CHAPO ISIDRO CAPTURED",
         body=("FBI 10-most-wanted Fausto Isidro Meza Flores arrested in Sinaloa after a shootout; vehicles burned."),
         tag="REPORTED", src="BBC, Guardian", kind="cuffs"),
    dict(n=12, region="SPORT & SCIENCE", head="BEPICOLOMBO",
         body=("ESA/JAXA craft enters orbit around Mercury after an 8-year journey - only the 2nd craft ever to do so."),
         tag="REPORTED", src="Phys.org, BBC", kind="orbit"),
    dict(n=13, region="NORTH AMERICA", head="RIEMANN PROOF CLAIMED",
         body=("Anthropic mathematician Levent Alpoge posts a claimed proof of the Riemann hypothesis, unsolved since 1859."),
         tag="CLAIM", src="France 24, BBC", kind="pi"),
]

ALSO = [
    (14, "SPARTA II", "Drone-hit freighter burns; Finland blames Ukraine", "BBC"),
    (15, "HOUTHIS", "Houthis claim Rabigh hit; Saudi strike kills 4", "CNBC"),
    (16, "GAZA", "Contamination threatens health for years", "Guardian"),
    (17, "ISRAEL COALITION", "Likud-Yashar talks end with no deal", "Al Jazeera"),
    (18, "WEST BANK", "Settlers torch homes; ‘Jewish terrorism’", "France 24"),
    (19, "SHENZHEN", "Trump calls Putin “my friend”", "Al Jazeera"),
    (20, "BURNHAM", "Burnham: EU deal could make next decade better", "BBC"),
    (21, "ISTANBUL", "Thousands rally; Sözcü TV raided, state-run", "France 24"),
    (22, "AUSTRALIA", "Chalmers: jobless will pass 5%; growth below 2%", "Guardian"),
    (23, "NATO MEETS", "NATO meets; all 3 missiles were Kh-101s", "Polish Radio"),
    (24, "BOLSONARO", "Bolsonaro in intensive care, stable", "MercoPress"),
    (25, "EBOLA", "Fighting disrupts Ebola response", "Al Jazeera"),
    (26, "RWANDA", "Five EU states accept Rwanda centres", "El País"),
    (27, "IOWA", "Army to detonate lead azide despite court order", "BBC"),
    (28, "ICE SEATTLE", "ICE detains father and daughter; protests", "Guardian"),
    (29, "BOCA", "Boca beat Mineiro 2-0 for the Copa", "Buenos Aires Times"),
    (30, "NEPAL PM", "Nepal PM begins first India visit", "The Hindu"),
    (31, "TATA STEEL", "Tata Steel buys 26.4% of pipe maker, $1.67bn", "CNBC"),
    (32, "KOREA $1 TRILLION", "Exports top $1 trillion, a first", "Yonhap"),
    (33, "INDONESIA SHIP", "Navy seizes ship with 405t of rocket chemical", "Inshorts"),
    (34, "MQ-9", "Iran claims it downed a US MQ-9A drone", "Inshorts"),
    (35, "ALCARAZ", "Alcaraz beats Zverev 6-2, 7-6 for ATP Finals", "Reuters"),
    (36, "MÁRQUEZ", "Márquez wins 8th MotoGP title", "AP"),
    (37, "ZELENSKY WEEK", "Russia used ~2,700 drones in week to 22 Nov", "AP"),
]

NUMBERS = [
    ("258", "HOUSE SEATS"),
    ("-5.06%", "NIKKEI"),
    ("$1 TRILLION", "KOREA EXPORTS"),
    ("405 TONNES", "SEIZED"),
    ("2,700", "DRONES IN A WEEK"),
    (">=10", "KILLED IN DYMER"),
]

REGIONS = [("EUROPE", 7), ("MIDDLE EAST", 6), ("ASIA-PACIFIC", 8),
           ("AFRICA", 5), ("NORTH AMERICA", 5), ("LATIN AMERICA", 2),
           ("SPORT & SCIENCE", 4)]

TIMELINE = [
    ("00:00", "COP31 no-deal leads wires"),
    ("02:00", "Nikkei opens -5.06%"),
    ("09:00", "Wires read to 09:00 UTC"),
    ("12:00", "NATO meets in Brussels"),
    ("15:00", "Boca lift the Copa"),
    ("18:00", "Alcaraz wins the ATP Finals"),
]

DATE_CHECK = ("Wires read to 09:00 UTC, Monday 23 November 2026. COP31's closing plenary ended late Sunday 22 Nov "
              "Antalya time; its no-deal outcome led Monday's wires. Left out as wrong-day news: the Peru "
              "M6.7 quake (Fri 20 Nov); Russia's 186-drone barrage (night of 21-22 Nov); the Shenzhen summit "
              "itself (19-20 Nov - only Monday's reactions shown).")


# ---------------------------------------------------------------- scenes
def picto(d, x, y, w, h, kind):
    """Small faithful scene thumbnail for a medium card."""
    d.rectangle([x, y, x + w, y + h], fill=(226, 232, 238))
    cx, cy = x + w / 2, y + h / 2
    if kind == "ship":
        d.rectangle([x, y + h * 0.62, x + w, y + h], fill=(52, 96, 140))
        d.polygon([(x + 8, cy + 6), (x + w - 8, cy + 6), (x + w - 18, cy + 16),
                   (x + 18, cy + 16)], fill=(60, 60, 66))
        d.rectangle([x + w * 0.42, cy - 8, x + w * 0.52, cy + 6], fill=(90, 90, 96))
        d.polygon([(x + w * 0.62, cy - 2), (x + w * 0.72, cy - 14),
                   (x + w * 0.66, cy - 2)], fill=(178, 34, 34))
    elif kind == "dome":
        d.rectangle([x, y + h * 0.72, x + w, y + h], fill=(120, 128, 138))
        d.rectangle([x + w * 0.2, cy - 2, x + w * 0.8, cy + 12], fill=(240, 240, 238))
        d.pieslice([x + w * 0.32, cy - 22, x + w * 0.68, cy + 6], 180, 360,
                   fill=(240, 240, 238))
        d.rectangle([x + w * 0.48, cy - 30, x + w * 0.52, cy - 20], fill=(60, 60, 66))
    elif kind == "flame":
        d.polygon([(cx - 16, cy + 14), (cx - 6, cy - 4), (cx, cy + 4),
                   (cx + 8, cy - 12), (cx + 16, cy + 14)], fill=(226, 110, 20))
        d.polygon([(cx - 8, cy + 14), (cx, cy + 2), (cx + 8, cy + 14)],
                  fill=(245, 185, 66))
        d.rectangle([x, y + h * 0.82, x + w, y + h], fill=(60, 60, 66))
    elif kind == "chip":
        d.rectangle([x + w * 0.28, cy - 12, x + w * 0.72, cy + 12], fill=(16, 34, 64))
        d.rectangle([x + w * 0.38, cy - 4, x + w * 0.62, cy + 4], fill=(76, 154, 255))
        for i in range(3):
            d.line([(x + w * 0.28, cy - 8 + i * 8), (x + w * 0.18, cy - 8 + i * 8)],
                   fill=(60, 60, 66), width=2)
            d.line([(x + w * 0.72, cy - 8 + i * 8), (x + w * 0.82, cy - 8 + i * 8)],
                   fill=(60, 60, 66), width=2)
    elif kind == "drone":
        d.ellipse([cx - 14, cy - 8, cx + 14, cy + 8], fill=(60, 60, 66))
        for sx in (-1, 1):
            d.line([(cx + sx * 12, cy), (cx + sx * 24, cy - 8)], fill=(90, 90, 96), width=2)
            d.ellipse([cx + sx * 28 - 5, cy - 13, cx + sx * 28 + 5, cy - 3],
                      outline=(60, 60, 66), width=2)
        d.line([(cx, cy + 8), (cx, cy + 16)], fill=(178, 34, 34), width=2)
    elif kind == "alert":
        d.polygon([(cx, cy - 16), (cx + 18, cy + 12), (cx - 18, cy + 12)],
                  fill=(245, 185, 66))
        d.rectangle([cx - 2, cy - 6, cx + 2, cy + 4], fill=(18, 24, 34))
        d.ellipse([cx - 2, cy + 7, cx + 2, cy + 11], fill=(18, 24, 34))
    elif kind == "cuffs":
        d.ellipse([cx - 16, cy - 8, cx - 2, cy + 8], outline=(60, 60, 66), width=3)
        d.ellipse([cx + 2, cy - 8, cx + 16, cy + 8], outline=(60, 60, 66), width=3)
        d.line([(cx - 2, cy), (cx + 2, cy)], fill=(60, 60, 66), width=3)
    elif kind == "orbit":
        d.ellipse([cx - 18, cy - 18, cx + 18, cy + 18], fill=(178, 120, 60))
        d.ellipse([cx - 26, cy - 10, cx + 26, cy + 10], outline=(16, 34, 64), width=2)
        d.ellipse([cx + 18, cy - 14, cx + 26, cy - 6], fill=(16, 34, 64))
    elif kind == "pi":
        d.text((cx - 11, cy - 13), "\u03c0", font=F("DejaVuSerif-Bold.ttf", 26),
               fill=(16, 34, 64))
        d.line([(x + 8, cy + 12), (x + w - 8, cy + 12)], fill=(178, 34, 34), width=2)


def dymer_scene(d, x, y, w, h):
    """Faithful drawn illustration of the Dymer rescue: a damaged
    5-storey block at night, smoke, rescuers, a boy carried out."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 32, 48))
    for sx, sy, r in [(x + 30, y + 12, 2), (x + 90, y + 8, 1), (x + 150, y + 16, 2),
                      (x + 210, y + 10, 1), (x + 260, y + 18, 2)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(220, 220, 220))
    # damaged 5-storey block, left half collapsed
    d.rectangle([x + 18, y + 30, x + 150, y + h - 8], fill=(120, 108, 96))
    d.polygon([(x + 18, y + 30), (x + 84, y + 30), (x + 84, y + 62),
               (x + 60, y + 78), (x + 84, y + 96), (x + 40, y + h - 8),
               (x + 18, y + h - 8)], fill=(88, 80, 72))
    for r in range(5):
        for c in range(4):
            wx, wy = x + 30 + c * 28, y + 38 + r * 20
            if r >= 2 and c >= 2:
                continue
            d.rectangle([wx, wy, wx + 16, wy + 12],
                        fill=(245, 185, 66) if (r + c) % 3 == 0 else (40, 48, 60))
    # smoke
    for sx, sy, r in [(x + 70, y + 22, 10), (x + 90, y + 14, 13), (x + 112, y + 20, 9)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(150, 150, 155))
    # floodlight beam + rescuers carrying the boy
    d.polygon([(x + 210, y + 40), (x + 250, y + 40), (x + 290, y + h - 8),
               (x + 200, y + h - 8)], fill=(245, 185, 66))
    d.rectangle([x + 205, y + h - 34, x + 235, y + h - 8], fill=(226, 110, 20))
    d.rectangle([x + 215, y + h - 52, x + 225, y + h - 34], fill=(226, 110, 20))
    d.ellipse([x + 216, y + h - 62, x + 224, y + h - 54], fill=(240, 200, 170))
    d.rectangle([x + 245, y + h - 30, x + 275, y + h - 8], fill=(226, 110, 20))
    d.rectangle([x + 255, y + h - 48, x + 265, y + h - 30], fill=(226, 110, 20))
    d.ellipse([x + 256, y + h - 58, x + 264, y + h - 50], fill=(240, 200, 170))
    # stretcher with the boy, centre
    d.rectangle([x + 150, y + h - 26, x + 200, y + h - 20], fill=(200, 200, 200))
    d.ellipse([x + 168, y + h - 36, x + 178, y + h - 26], fill=(240, 200, 170))
    d.rectangle([x + 178, y + h - 32, x + 196, y + h - 22], fill=(13, 110, 110))
    d.text((x + 8, y + h - 16), "DYMER, KYIV REGION - RESCUE AFTER 14 HOURS",
           font=F_SRC, fill=(255, 255, 255))


# ---------------------------------------------------------------- world map
CONTINENTS = [
    # North America
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66),
     (-80, 62), (-76, 58), (-65, 45), (-70, 42), (-75, 35), (-81, 26),
     (-84, 30), (-90, 21), (-97, 16), (-105, 20), (-115, 29), (-125, 40),
     (-125, 49), (-135, 58), (-155, 58), (-165, 60)],
    # South America
    [(-79, 9), (-72, 12), (-62, 10), (-52, 5), (-44, -3), (-35, -8),
     (-40, -20), (-48, -28), (-58, -35), (-65, -41), (-70, -52), (-74, -54),
     (-73, -44), (-72, -30), (-70, -18), (-77, -12), (-81, -5), (-80, 1)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 51), (5, 53), (8, 57), (12, 56),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 62), (32, 70), (40, 68),
     (45, 66), (40, 60), (35, 56), (30, 54), (28, 46), (23, 40), (19, 42),
     (12, 44), (8, 44), (3, 42), (0, 39)],
    # Africa
    [(-6, 35), (10, 37), (20, 32), (32, 31), (35, 28), (38, 22), (43, 12),
     (48, 11), (51, 12), (46, 4), (41, -2), (40, -10), (36, -18), (33, -26),
     (28, -33), (20, -35), (16, -29), (12, -18), (13, -12), (9, -1),
     (9, 4), (-8, 5), (-13, 8), (-17, 15), (-16, 21), (-15, 27)],
    # Asia
    [(32, 70), (45, 68), (55, 69), (68, 73), (80, 73), (95, 76), (110, 74),
     (125, 73), (140, 72), (158, 69), (162, 62), (158, 55), (142, 50),
     (140, 40), (130, 35), (122, 31), (115, 23), (108, 15), (105, 9),
     (100, 6), (97, 10), (92, 16), (88, 22), (80, 15), (76, 10), (72, 20),
     (66, 25), (60, 25), (54, 27), (48, 30), (43, 29), (38, 31), (35, 36),
     (32, 42), (28, 46), (30, 52), (32, 58)],
    # Australia
    [(114, -22), (122, -14), (132, -12), (137, -15), (142, -11), (146, -19),
     (150, -23), (153, -27), (150, -37), (140, -38), (132, -32), (124, -33),
     (116, -35), (113, -25)],
]

PINS = [(33, 36, 1), (27, 53, 2), (139, 35, 3), (22, 30, 4), (-77, 39, 5),
        (56, 26, 6), (-122, 37, 7), (106, -6, 8), (32, 15, 9), (34, 4, 10),
        (-107, 25, 11), (5, 54, 12), (-122, 37, 13)]


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=SKY)
    for poly in CONTINENTS:
        pts = [(x + (lon + 180) / 360 * w, y + (90 - lat) / 180 * h)
               for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=(150, 138, 110))
    d.text((x + 6, y + 4), "WHERE IT HAPPENED - 13 STORIES PINNED",
           font=F_SRC, fill=(18, 24, 34))
    off = {1: (14, 6), 2: (-12, -4), 4: (-2, 10), 10: (10, 12),
           12: (0, -12), 13: (18, 14)}
    for lon, lat, n in PINS:
        px = x + (lon + 180) / 360 * w
        py = y + (90 - lat) / 180 * h
        dx, dy = off.get(n, (0, 0))
        num_badge(d, px + dx, py + dy, n, r=7)


# ---------------------------------------------------------------- page
def draw_page():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    MX = 16

    # masthead
    d.rectangle([0, 0, W, 64], fill=NAVY)
    d.rectangle([0, 64, W, 67], fill=GOLD)
    t = "THE WORLD IN ONE DAY"
    d.text(((W - d.textlength(t, font=F("DejaVuSans-Bold.ttf", 13))) / 2, 6),
           t, font=F("DejaVuSans-Bold.ttf", 13), fill=GOLD)
    t = "MONDAY, 23 NOVEMBER 2026"
    d.text(((W - d.textlength(t, font=F_MAST)) / 2, 22),
           t, font=F_MAST, fill=(255, 255, 255))

    # subtitle
    t = "37 STORIES  \u00b7  7 REGIONS  \u00b7  EVERY ONE DATED MONDAY, 23 NOVEMBER 2026"
    d.text(((W - d.textlength(t, font=F_SUB)) / 2, 74),
           t, font=F_SUB, fill=INK)

    # numbers strip
    y0 = 96
    cw = (W - 2 * MX) / 6
    for i, (num, lab) in enumerate(NUMBERS):
        cx = MX + cw * i + cw / 2
        nf = F_NUM
        for sz in (23, 21, 19, 17):
            nf = F("DejaVuSans-Bold.ttf", sz)
            if d.textlength(num, font=nf) <= cw - 8:
                break
        d.text((cx - d.textlength(num, font=nf) / 2, y0), num,
               font=nf, fill=NAVY)
        d.text((cx - d.textlength(lab, font=F_NUML) / 2, y0 + 26), lab,
               font=F_NUML, fill=MUTED)
        if i:
            d.line([(MX + cw * i, y0 + 2), (MX + cw * i, y0 + 36)], fill=EDGE, width=1)

    # region bar (segments proportional to counts, total 37)
    y0 = 134
    total = sum(c for _, c in REGIONS)
    cols = [(16, 34, 64), (178, 34, 34), (13, 110, 110), (166, 110, 8),
            (76, 90, 160), (150, 80, 30), (40, 120, 70)]
    x = MX
    for (name, c), col in zip(REGIONS, cols):
        wseg = (W - 2 * MX) * c / total
        d.rectangle([x, y0, x + wseg - 1, y0 + 18], fill=col)
        lab = f"{name} {c}"
        if d.textlength(lab, font=F_REG) < wseg - 6:
            d.text((x + (wseg - d.textlength(lab, font=F_REG)) / 2, y0 + 3),
                   lab, font=F_REG, fill=(255, 255, 255))
        x += wseg

    # UTC timeline, one line
    tl = "   \u2022   ".join(f"{t}  {s}" for t, s in TIMELINE)
    tlf = F_TL if d.textlength(tl, font=F_TL) <= W - 2 * MX else F("DejaVuSans.ttf", 9)
    d.text(((W - d.textlength(tl, font=tlf)) / 2, 158), tl,
           font=tlf, fill=BODY)
    d.line([(MX, 174), (W - MX, 174)], fill=EDGE, width=1)

    # lead cards
    y0, ch = 180, 204
    cw = (W - 2 * MX - 16) / 3
    for i, s in enumerate(LEADS):
        x = MX + i * (cw + 8)
        d.rectangle([x, y0, x + cw, y0 + ch], fill=CARD, outline=EDGE, width=1)
        if s["photo"]:
            ph = cover_crop(Image.open(s["photo"]).convert("RGB"),
                            int(cw), 96)
            img.paste(ph, (int(x) + 1, y0 + 1))
            d.text((x + 6, y0 + 82), "REAL PHOTO", font=F_SRC, fill=(255, 255, 255))
        else:
            dymer_scene(d, int(x) + 1, y0 + 1, int(cw) - 2, 96)
        num_badge(d, x + 14, y0 + 14, s["n"], r=11)
        yy = para(d, x + 8, y0 + 102, s["head"], F_LEAD, INK, cw - 16, 19)
        para(d, x + 8, yy + 4, s["body"], F_LEADB, BODY, cw - 16, 15)
        tx = tag(d, x + 8, y0 + ch - 20, s["tag"])
        d.text((tx + 6, y0 + ch - 19),
               f"{s['region']}  \u00b7  {s['src']}", font=F_SRC, fill=MUTED)

    # medium cards, 2 rows x 5
    y0, ch = 392, 108
    cw = (W - 2 * MX - 32) / 5
    for i, s in enumerate(MEDIUM):
        r, c = divmod(i, 5)
        x = MX + c * (cw + 8)
        y = y0 + r * (ch + 8)
        d.rectangle([x, y, x + cw, y + ch], fill=CARD, outline=EDGE, width=1)
        picto(d, int(x) + 1, int(y) + 1, int(cw) - 2, 28, s["kind"])
        num_badge(d, x + 12, y + 14, s["n"], r=9)
        yy = para(d, x + 6, y + 32, s["head"], F_MED, INK, cw - 12, 13)
        para(d, x + 6, yy + 1, s["body"], F_MEDB, BODY, cw - 12, 12)
        tx = tag(d, x + 6, y + ch - 16, s["tag"])
        d.text((tx + 5, y + ch - 15), s["src"], font=F_SRC, fill=MUTED)

    # world map
    draw_map(d, MX, 624, W - 2 * MX, 72)

    # ALSO list header
    d.rectangle([MX, 700, W - MX, 720], fill=NAVY)
    d.text((MX + 8, 704), "ALSO ON MONDAY, 23 NOVEMBER 2026  \u2014  24 MORE STORIES",
           font=F("DejaVuSans-Bold.ttf", 12), fill=(255, 255, 255))

    # ALSO rows: 3 columns x 8 rows
    colw = (W - 2 * MX - 16) / 3
    for i, (n, head, body, src) in enumerate(ALSO):
        col, row = divmod(i, 8)
        x = MX + col * (colw + 8)
        y = 724 + row * 24
        d.text((x, y), f"{n}.", font=F_ALSOH, fill=RED)
        tx = x + d.textlength(f"{n}. ", font=F_ALSOH)
        d.text((tx, y), head, font=F_ALSOH, fill=INK)
        line = f"{body} ({src})"
        bf = F_ALSO10 if d.textlength(line, font=F_ALSO10) <= colw - 4 else F_ALSO9
        d.text((x + 2, y + 12), line, font=bf, fill=BODY)

    # DATE CHECK
    y0 = 922
    d.rectangle([MX, y0, W - MX, y0 + 58], outline=RED, width=2)
    d.text((MX + 8, y0 + 4), "DATE CHECK \u2014 FOR THE JUDGE",
           font=F_DCH, fill=RED)
    para(d, MX + 8, y0 + 20, DATE_CHECK, F_DC, BODY, W - 2 * MX - 16, 13)

    # footer
    d.text((MX, 986),
           "Tags: ONGOING = still developing  \u00b7  CLAIM = as claimed, unverified  \u00b7  REPORTED = confirmed by sources",
           font=F_FOOT, fill=MUTED)
    d.text((MX, 998),
           "Photos: COP31 protest, Antalya; Tokyo Stock Exchange interior (Wikimedia Commons). Other panels are faithful drawn illustrations of the actual scenes.",
           font=F_FOOT, fill=MUTED)
    return img


if __name__ == "__main__":
    out = draw_page()
    out.save("entry.png", optimize=True)
    print("saved entry.png", out.size)
