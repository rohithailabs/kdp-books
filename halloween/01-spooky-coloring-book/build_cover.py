#!/usr/bin/env python3
"""Build the front cover entirely locally (no external image generation).

8.5" x 8.5" front cover at 300 DPI = 2550 x 2550 px, no bleed (front-cover-only
preview; full wraparound with spine should be finalized in KDP Cover Creator
once trim/paper/page-count are locked).
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "generated-art")
OUT = os.path.join(HERE, "Spooky_Fun_Cover_Front.png")

PAGE = 2550
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(path, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, path), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 260)
F_SUB = font("DejaVuSans-Bold.ttf", 90)
F_BADGE = font("DejaVuSans-Bold.ttf", 52)

ORANGE_TOP = (255, 178, 92)
ORANGE_BOT = (247, 127, 58)
PURPLE_DEEP = (74, 41, 92)
CREAM = (255, 248, 235)
DARK = (40, 22, 15)


def vertical_gradient(w, h, top, bottom):
    base = Image.new("RGB", (w, h), top)
    top_arr = top
    bot_arr = bottom
    for y in range(h):
        t = y / (h - 1)
        row_color = tuple(int(top_arr[i] + (bot_arr[i] - top_arr[i]) * t) for i in range(3))
        ImageDraw.Draw(base).line([(0, y), (w, y)], fill=row_color)
    return base


def draw_moon(draw, cx, cy, r, color):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    # crescent bite
    bite_r = r * 0.92
    bx = cx + r * 0.55
    draw.ellipse([bx - bite_r, cy - bite_r, bx + bite_r, cy + bite_r], fill=ORANGE_TOP)


def draw_star(draw, cx, cy, r, color):
    pts = []
    for i in range(4):
        ang = math.pi / 2 * i
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
        ang2 = ang + math.pi / 4
        pts.append((cx + r * 0.35 * math.cos(ang2), cy + r * 0.35 * math.sin(ang2)))
    draw.polygon(pts, fill=color)


def draw_hill(img, y_base, color, amplitude=60, seed_offset=0):
    w, h = img.size
    d = ImageDraw.Draw(img)
    pts = [(0, h)]
    for x in range(0, w + 1, 40):
        y = y_base + amplitude * math.sin((x + seed_offset) / 260.0)
        pts.append((x, y))
    pts.append((w, h))
    d.polygon(pts, fill=color)


def load_transparent(art_path, threshold=245):
    art = Image.open(art_path).convert("RGBA")
    pixels = art.load()
    w, h = art.size
    for yy in range(h):
        for xx in range(w):
            r, g, b, a = pixels[xx, yy]
            if r >= threshold and g >= threshold and b >= threshold:
                pixels[xx, yy] = (r, g, b, 0)
    return art


def paste_centered(base, art_path, box_size, center):
    art = load_transparent(art_path)
    aw, ah = art.size
    scale = min(box_size / aw, box_size / ah)
    art = art.resize((int(aw * scale), int(ah * scale)), Image.LANCZOS)
    x = center[0] - art.width // 2
    y = center[1] - art.height // 2
    base.paste(art, (x, y), art)


def text_with_outline(draw, xy, text, font_, fill, outline, outline_w=8, anchor="mm"):
    x, y = xy
    for dx in range(-outline_w, outline_w + 1, 2):
        for dy in range(-outline_w, outline_w + 1, 2):
            if dx * dx + dy * dy <= outline_w * outline_w:
                draw.text((x + dx, y + dy), text, font=font_, fill=outline, anchor=anchor)
    draw.text((x, y), text, font=font_, fill=fill, anchor=anchor)


def main():
    img = vertical_gradient(PAGE, PAGE, ORANGE_TOP, ORANGE_BOT)

    # night sky band at top
    sky = Image.new("RGB", (PAGE, 820), PURPLE_DEEP)
    img.paste(sky, (0, 0))
    # soften the seam between sky and gradient
    seam = vertical_gradient(PAGE, 200, PURPLE_DEEP, ORANGE_TOP)
    img.paste(seam, (0, 720))

    d = ImageDraw.Draw(img)
    draw_moon(d, PAGE - 480, 380, 200, CREAM)
    for sx, sy, sr in [(260, 200, 20), (430, 340, 14), (650, 160, 16), (900, 300, 12),
                        (1150, 210, 18), (1500, 150, 14), (1750, 320, 16), (330, 550, 12)]:
        draw_star(d, sx, sy, sr, CREAM)

    # rolling hill silhouette between sky and ground
    draw_hill(img, 900, (191, 87, 46), amplitude=50, seed_offset=0)
    draw_hill(img, 960, (166, 68, 38), amplitude=40, seed_offset=300)

    d = ImageDraw.Draw(img)

    # title banner
    text_with_outline(d, (PAGE // 2, 980), "SPOOKY FUN", F_TITLE, CREAM, DARK, outline_w=14)
    text_with_outline(
        d, (PAGE // 2, 1150), "MY FIRST HALLOWEEN COLORING BOOK", F_SUB, CREAM, DARK, outline_w=8
    )
    d.text(
        (PAGE // 2, 1250),
        "40 Cute (Not Scary!) Pictures to Color • Ages 4-8",
        font=F_BADGE,
        fill=DARK,
        anchor="mm",
    )

    # character cluster on a cream "ground" panel
    panel_top = 1320
    panel_bottom = PAGE - 160
    d.rounded_rectangle([140, panel_top, PAGE - 140, panel_bottom], radius=70, fill=CREAM)
    d.rounded_rectangle(
        [140, panel_top, PAGE - 140, panel_bottom], radius=70, outline=DARK, width=10
    )

    bat_cy = panel_top + 190
    paste_centered(img, os.path.join(ART, "page-11.png"), 220, (PAGE // 2 - 330, bat_cy))
    paste_centered(img, os.path.join(ART, "page-11.png"), 220, (PAGE // 2 + 330, bat_cy))

    trio_cy = panel_top + 660
    paste_centered(img, os.path.join(ART, "page-05.png"), 600, (PAGE // 2, trio_cy))
    paste_centered(img, os.path.join(ART, "page-04.png"), 420, (PAGE // 2 - 620, trio_cy + 40))
    paste_centered(img, os.path.join(ART, "page-07.png"), 420, (PAGE // 2 + 620, trio_cy + 40))

    img = img.convert("RGB")
    img.save(OUT, dpi=(300, 300))
    print("Wrote", OUT, img.size)


if __name__ == "__main__":
    main()
