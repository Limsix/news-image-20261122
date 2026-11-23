"""Draw a newspaper front page summing up Sunday 22 November 2026.

1024x1024, PIL only, fully deterministic. All fonts are bundled in the
fonts/ directory next to this file and loaded relative to it.

Stories (all reported on Sunday 22 November 2026):
  Lead      COP31 climate talks collapse in Antalya, Turkey (AP / Reuters).
  Gulf      Iran strikes hit an industrial site in Bahrain (Reuters / AFP).
  Mexico    Cartel boss 'El Chapo Isidro' captured in Sinaloa (AP).
  Ukraine   Russian drone hits a flat block in Dymer, near Kyiv (AP).
  Indonesia Candy factory fire in Cikande; 3 dead, 36 missing (AP / Reuters).
  Markets   US stocks fall into correction on an AI sell-off (AP).
  Space     BepiColombo enters orbit around Mercury (One Turn).
"""

import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 36
INK = (18, 18, 18)
PAPER = (247, 243, 232)
PAPER_DARK = (238, 232, 214)
RED = (158, 32, 28)
BLUE = (28, 68, 128)
TEAL = (18, 96, 92)
GREY = (96, 92, 84)
LIGHT_GREY = (214, 208, 192)

_FONT_DIR = Path(__file__).resolve().parent / "fonts"


def _font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(_FONT_DIR / name), size)


SERIF_B = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
SANS = "DejaVuSans.ttf"


def wrap(draw: ImageDraw.ImageDraw, text: str, font, width: int):
    """Greedy word wrap returning a list of lines that fit `width`."""
    lines, current = [], ""
    for word in text.split():
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def text_block(draw, x, y, text, font, width, leading, fill=INK):
    lines = wrap(draw, text, font, width)
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def hline(draw, y, x0, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def draw_lead_art(draw, x0, y0, x1, y1):
    """COP31 art: a cracked Earth under a smokestack sky, Antalya label."""
    rng = random.Random(20261122)
    draw.rectangle([x0, y0, x1, y1], fill=(214, 228, 240), outline=INK, width=3)
    # sky gradient bands
    for i in range(5):
        yy0 = y0 + i * (y1 - y0) // 5
        yy1 = y0 + (i + 1) * (y1 - y0) // 5
        shade = 214 - i * 6
        draw.rectangle([x0 + 2, yy0, x1 - 2, yy1], fill=(shade, 228 - i * 4, 240))
    # pale sun, top left, clear of the globe
    cx, cy, r = x0 + 52, y0 + 42, 26
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(240, 214, 120),
                 outline=(200, 160, 60), width=3)
    # smokestacks on the horizon
    base = y1 - 88
    for sx, sw, sh in [(x0 + 330, 26, 84), (x0 + 372, 22, 66), (x0 + 408, 26, 92)]:
        draw.rectangle([sx, base - sh, sx + sw, base], fill=(90, 88, 84),
                       outline=INK, width=2)
        for k in range(3):
            px = sx + sw // 2 + (k - 1) * 10 + rng.randint(-3, 3)
            py = base - sh - 14 - k * 16
            pr = 12 - k * 2
            draw.ellipse([px - pr, py - pr, px + pr, py + pr],
                         fill=(180, 178, 170), outline=(140, 138, 130), width=1)
    # Earth, sitting on the ground line (fully visible, not clipped)
    ecx, ecy, er = x0 + 150, base - 62, 64
    draw.ellipse([ecx - er, ecy - er, ecx + er, ecy + er],
                 fill=(52, 110, 190), outline=INK, width=4)
    # land masses (simple blobs)
    for lx, ly, lr in [(ecx - 30, ecy - 22, 18), (ecx + 20, ecy - 32, 14),
                       (ecx + 32, ecy + 18, 17), (ecx - 22, ecy + 28, 13)]:
        draw.ellipse([lx - lr, ly - lr // 2, lx + lr, ly + lr // 2],
                     fill=(74, 148, 84))
    # crack across the globe
    crack = [(ecx - 54, ecy - 36), (ecx - 28, ecy - 12), (ecx - 40, ecy + 6),
             (ecx - 8, ecy + 24), (ecx + 12, ecy + 8), (ecx + 36, ecy + 30),
             (ecx + 54, ecy + 20)]
    draw.line(crack, fill=RED, width=6, joint="curve")
    # ground line
    draw.line([(x0, base), (x1, base)], fill=INK, width=3)
    draw.rectangle([x0, base, x1, y1], fill=(196, 188, 164))
    for gx in range(x0 + 12, x1 - 10, 26):
        draw.line([(gx, base + 8), (gx + 12, base + 8)], fill=(150, 142, 120),
                  width=3)
    # caption strip
    cap_h = 30
    draw.rectangle([x0, y1 - cap_h, x1, y1], fill=INK)
    draw.text((x0 + 12, y1 - cap_h + 5),
              "THE EARTH WAITS: NO DEAL IN ANTALYA",
              font=_font(SANS_B, 16), fill=(247, 243, 232))


def draw_icon(draw, kind, x0, y0, x1, y1):
    """Small pictogram inside a secondary-story box."""
    cx = (x0 + x1) // 2
    cy = (y0 + y1) // 2
    if kind == "missile":
        draw.arc([x0 + 8, y0 + 6, x1 - 8, y1 + 26], 200, 340, fill=RED, width=5)
        draw.polygon([(x1 - 26, y0 + 22), (x1 - 8, y0 + 30), (x1 - 26, y0 + 40)],
                     fill=RED)
        for wx in range(x0 + 6, x1 - 6, 18):
            draw.arc([wx, y1 - 12, wx + 16, y1 + 2], 180, 360, fill=BLUE, width=3)
    elif kind == "badge":
        pts = []
        import math
        for i in range(10):
            ang = math.pi / 2 + i * math.pi / 5
            rr = 30 if i % 2 == 0 else 16
            pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
        draw.polygon(pts, fill=(240, 200, 60), outline=INK, width=2)
        draw.text((cx - 7, cy - 11), "★", font=_font(SANS_B, 22), fill=INK)
    elif kind == "building":
        draw.rectangle([x0 + 14, y0 + 22, x1 - 14, y1 - 6], fill=(168, 160, 144),
                       outline=INK, width=2)
        draw.polygon([(x0 + 14, y0 + 22), (x0 + 34, y0 + 6), (x0 + 52, y0 + 22)],
                     fill=(120, 112, 96), outline=INK)
        for wy in (y0 + 38, y0 + 58):
            for wx in (x0 + 24, x0 + 48, x0 + 72):
                draw.rectangle([wx, wy, wx + 12, wy + 12], fill=(247, 243, 232),
                               outline=INK, width=1)
        draw.ellipse([x1 - 34, y0 + 2, x1 - 8, y0 + 28], fill=(180, 178, 170),
                     outline=(140, 138, 130), width=1)
    elif kind == "flame":
        draw.rectangle([x0 + 16, y0 + 34, x1 - 16, y1 - 6], fill=(120, 112, 96),
                       outline=INK, width=2)
        draw.polygon([(cx - 16, y0 + 34), (cx, y0 + 4), (cx + 16, y0 + 34)],
                     fill=(226, 110, 30), outline=RED, width=2)
        draw.ellipse([cx - 8, y0 + 20, cx + 8, y0 + 36], fill=(240, 200, 60))
    elif kind == "chart":
        draw.line([(x0 + 6, y0 + 12), (x0 + 26, y0 + 26), (x0 + 46, y0 + 22),
                   (x0 + 66, y0 + 46), (x0 + 80, y0 + 50)], fill=RED, width=5,
                  joint="curve")
        draw.polygon([(x0 + 80, y0 + 50), (x0 + 92, y0 + 38), (x0 + 92, y0 + 56)],
                     fill=RED)
        draw.line([(x0 + 6, y1 - 8), (x1 - 6, y1 - 8)], fill=INK, width=2)
    elif kind == "planet":
        draw.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=(150, 140, 130),
                     outline=INK, width=2)
        draw.ellipse([cx - 44, cy - 10, cx + 44, cy + 10], outline=TEAL, width=3)
        draw.ellipse([cx + 40, cy - 34, cx + 48, cy - 26], fill=(240, 200, 60),
                     outline=INK, width=1)


def secondary_box(draw, x0, y0, x1, y1, tag, tag_color, headline, detail, icon):
    draw.rectangle([x0, y0, x1, y1], fill=PAPER, outline=INK, width=2)
    # tag ribbon
    tag_font = _font(SANS_B, 15)
    tw = draw.textlength(tag, font=tag_font)
    draw.rectangle([x0, y0, x0 + tw + 18, y0 + 26], fill=tag_color)
    draw.text((x0 + 9, y0 + 4), tag, font=tag_font, fill=(255, 255, 255))
    # headline (max 2 lines at 19pt in this width)
    hy = y0 + 34
    hy = text_block(draw, x0 + 10, hy, headline, _font(SANS_B, 19),
                    x1 - x0 - 20, 23)
    # icon strip at the bottom left, detail text to its right; the zone
    # below the headline is tall enough for 4 detail lines
    icon_y0 = y0 + 108
    draw_icon(draw, icon, x0 + 8, icon_y0, x0 + 100, y1 - 8)
    text_block(draw, x0 + 108, icon_y0 + 4, detail, _font(SANS, 14),
               x1 - x0 - 118, 18, fill=(40, 38, 34))


def render_front_page() -> Image.Image:
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # --- masthead ---
    hline(draw, 14, MARGIN, W - MARGIN, 3)
    mast = _font(SERIF_B, 74)
    title = "THE WORLD TODAY"
    tw = draw.textlength(title, font=mast)
    draw.text(((W - tw) / 2, 24), title, font=mast, fill=INK)
    hline(draw, 112, MARGIN, W - MARGIN, 2)

    # --- date bar ---
    date_font = _font(SANS_B, 30)
    date = "SUNDAY, 22 NOVEMBER 2026"
    dw = draw.textlength(date, font=date_font)
    draw.text(((W - dw) / 2, 122), date, font=date_font, fill=RED)
    small = _font(SANS, 15)
    draw.text((MARGIN, 132), "WORLD EDITION", font=small, fill=GREY)
    right = "ONE DAY IN THE WORLD"
    draw.text((W - MARGIN - draw.textlength(right, font=small), 132),
              right, font=small, fill=GREY)
    hline(draw, 164, MARGIN, W - MARGIN, 5)

    # --- lead story ---
    y = 180
    kicker = _font(SANS_B, 17)
    draw.text((MARGIN, y), "CLIMATE SUMMIT  •  ANTALYA, TURKEY",
              font=kicker, fill=TEAL)
    y += 30
    head = _font(SERIF_B, 56)
    headline = "CLIMATE TALKS COLLAPSE"
    draw.text((MARGIN, y), headline, font=head, fill=INK)
    y += 70
    sub = "COP31 ends with no deal as the EU rejects a draft that never mentions fossil fuels"
    y = text_block(draw, MARGIN, y, sub, _font(SERIF, 24), W - 2 * MARGIN, 30,
                   fill=(40, 38, 34))
    y += 12

    # lead art left, body text right (shortened so it fits the art height)
    art_x0, art_y0 = MARGIN, y
    art_x1, art_y1 = 540, y + 210
    draw_lead_art(draw, art_x0, art_y0, art_x1, art_y1)
    body_x = 560
    body_w = W - MARGIN - body_x
    by = art_y0
    by = text_block(
        draw, body_x, by,
        "The UN climate summit ended on Sunday with no agreement, after "
        "the EU and its allies rejected a final draft that made no mention "
        "of fossil fuels.",
        _font(SERIF, 19), body_w, 25)
    by += 10
    by = text_block(
        draw, body_x, by,
        "Negotiators left Antalya without a text \u2014 the first collapse "
        "of a UN climate summit in years.",
        _font(SERIF, 19), body_w, 25)
    by += 10
    draw.text((body_x, by), "— AP / Reuters", font=_font(SANS, 15), fill=GREY)

    y = art_y1 + 16
    hline(draw, y, MARGIN, W - MARGIN, 3)
    y += 14

    # --- secondary stories: 2 rows x 3 ---
    stories = [
        ("GULF", RED, "IRAN STRIKES HIT BAHRAIN SITE",
         "Missiles and drones hit an industrial site; two people injured. "
         "Gulf states condemn the attack.", "missile"),
        ("MEXICO", TEAL, "CARTEL BOSS CAPTURED IN MEXICO",
         "\u2018El Chapo Isidro\u2019 seized in Sinaloa; 11 killed in the raid, "
         "including four soldiers.", "badge"),
        ("UKRAINE", BLUE, "DRONE HITS FLATS NEAR KYIV",
         "A Russian drone strikes a five-storey block in Dymer; 14 people "
         "missing.", "building"),
        ("INDONESIA", RED, "FACTORY FIRE IN INDONESIA",
         "Blaze at a candy plant in Cikande kills 3; 36 workers still "
         "missing.", "flame"),
        ("MARKETS", BLUE, "STOCKS TUMBLE ON AI FEARS",
         "The S&P 500 falls 3.7% on Friday into correction; the Nasdaq "
         "drops 5.3%.", "chart"),
        ("SPACE", TEAL, "PROBE REACHES MERCURY",
         "BepiColombo enters orbit around Mercury after an eight-year "
         "journey from Earth.", "planet"),
    ]
    gap = 12
    box_w = (W - 2 * MARGIN - 2 * gap) // 3
    box_h = 190
    for row in range(2):
        for col in range(3):
            i = row * 3 + col
            x0 = MARGIN + col * (box_w + gap)
            y0 = y + row * (box_h + gap)
            tag, color, head, detail, icon = stories[i]
            secondary_box(draw, x0, y0, x0 + box_w, y0 + box_h,
                          tag, color, head, detail, icon)

    # --- footer ---
    fy = y + 2 * box_h + gap + 12
    hline(draw, fy, MARGIN, W - MARGIN, 2)
    foot = ("All stories reported Sunday 22 November 2026  •  Sources: AP, "
            "Reuters, AFP, Al Jazeera")
    ff = _font(SANS, 15)
    fw = draw.textlength(foot, font=ff)
    draw.text(((W - fw) / 2, fy + 8), foot, font=ff, fill=GREY)

    return img
