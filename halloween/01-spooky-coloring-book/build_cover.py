#!/usr/bin/env python3
"""Front cover — composites title/badge/seal onto externally-generated color art.

8.5" x 8.5" front cover at 300 DPI = 2550 x 2550 px, no bleed (front-cover-only
preview; full wraparound with spine should be finalized in KDP Cover Creator
once trim/paper/page-count are locked).
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
BG = os.path.join(HERE, "external-art", "cover-background-external.jpg")
OUT = os.path.join(HERE, "Spooky_Fun_Cover_Front.png")

PAGE = 2550
FONT_DIR = "/usr/share/fonts/opentype/comic-neue"


def font(path, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, path), size)


F_TITLE = font("ComicNeue-Bold.otf", 320)
F_SUB = font("ComicNeue-Bold.otf", 100)
F_BADGE_SM = font("ComicNeue-Bold.otf", 60)
F_SEAL_LABEL = font("ComicNeue-Bold.otf", 44)
F_SEAL_NUM = font("ComicNeue-Bold.otf", 74)

CREAM = (255, 247, 232)
GOLD = (255, 200, 92)
DARK = (28, 14, 10)
MAROON = (110, 34, 30)


def text_soft_shadow(base_rgba, xy, text, font_, fill, anchor="mm",
                      shadow_color=(20, 10, 8), shadow_alpha=160, blur=12, offset=(0, 12),
                      stroke_width=0, stroke_fill=None):
    layer = Image.new("RGBA", base_rgba.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = xy
    d.text((x + offset[0], y + offset[1]), text, font=font_, fill=(*shadow_color, shadow_alpha),
           anchor=anchor)
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    base_rgba.alpha_composite(layer)
    d2 = ImageDraw.Draw(base_rgba)
    if stroke_width:
        d2.text((x, y), text, font=font_, fill=fill, anchor=anchor,
                 stroke_width=stroke_width, stroke_fill=stroke_fill)
    else:
        d2.text((x, y), text, font=font_, fill=fill, anchor=anchor)


def ribbon(draw, cx, cy, w, h, fill, outline):
    notch = h * 0.5
    left = cx - w / 2
    right = cx + w / 2
    top = cy - h / 2
    bottom = cy + h / 2
    body = [
        (left, top), (right, top), (right, bottom), (cx, bottom - notch * 0.5), (left, bottom),
    ]
    draw.polygon(body, fill=fill, outline=outline, width=6)
    tail_w = w * 0.09
    for side, x0 in ((-1, left), (1, right - tail_w)):
        tail = [
            (x0, top), (x0 + tail_w, top), (x0 + tail_w, bottom),
            (x0 + tail_w / 2, bottom - notch * 0.6), (x0, bottom),
        ]
        shade = tuple(max(0, c - 35) for c in fill)
        draw.polygon(tail, fill=shade, outline=outline, width=4)


def main():
    bg = Image.open(BG).convert("RGB").resize((PAGE, PAGE), Image.LANCZOS)
    img = bg.convert("RGBA")

    # gentle darken band behind the title so cream/white text stays legible
    # over whatever sky color sits there, without hiding the art
    band = Image.new("RGBA", (PAGE, 760), (0, 0, 0, 0))
    bd = ImageDraw.Draw(band)
    for y in range(760):
        a = int(70 * (1 - abs(y - 380) / 380))
        bd.line([(0, y), (PAGE, y)], fill=(10, 5, 15, max(0, a)))
    img.alpha_composite(band, (0, 120))

    text_soft_shadow(img, (PAGE // 2, 330), "SPOOKY FUN", F_TITLE, CREAM,
                      shadow_alpha=190, blur=18, offset=(0, 18),
                      stroke_width=11, stroke_fill=DARK)
    text_soft_shadow(img, (PAGE // 2, 505), "MY FIRST HALLOWEEN COLORING BOOK", F_SUB, GOLD,
                      shadow_alpha=160, blur=9, offset=(0, 9),
                      stroke_width=6, stroke_fill=DARK)

    d = ImageDraw.Draw(img)
    ribbon(d, PAGE // 2, 630, 1720, 130, MAROON, DARK)
    d.text((PAGE // 2, 630), "40 CUTE (NOT SCARY) PICTURES TO COLOR", font=F_BADGE_SM,
           fill=CREAM, anchor="mm")

    # age seal, bottom-left, over the sandy ground area
    seal_c = (270, PAGE - 250)
    seal_shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(seal_shadow)
    sd.ellipse([seal_c[0] - 150, seal_c[1] - 140, seal_c[0] + 150, seal_c[1] + 160],
               fill=(20, 10, 8, 110))
    seal_shadow = seal_shadow.filter(ImageFilter.GaussianBlur(16))
    img.alpha_composite(seal_shadow)

    d = ImageDraw.Draw(img)
    d.ellipse([seal_c[0] - 150, seal_c[1] - 150, seal_c[0] + 150, seal_c[1] + 150],
              fill=GOLD, outline=DARK, width=8)
    d.ellipse([seal_c[0] - 116, seal_c[1] - 116, seal_c[0] + 116, seal_c[1] + 116],
              outline=DARK, width=4)
    d.text((seal_c[0], seal_c[1] - 28), "AGES", font=F_SEAL_LABEL, fill=DARK, anchor="mm")
    d.text((seal_c[0], seal_c[1] + 32), "4-8", font=F_SEAL_NUM, fill=DARK, anchor="mm")

    img.convert("RGB").save(OUT, dpi=(300, 300))
    print("Wrote", OUT, img.size)


if __name__ == "__main__":
    main()
