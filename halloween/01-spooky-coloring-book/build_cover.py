#!/usr/bin/env python3
"""Front cover — built locally with Pillow, no external image generation.

8.5" x 8.5" front cover at 300 DPI = 2550 x 2550 px, no bleed (front-cover-only
preview; full wraparound with spine should be finalized in KDP Cover Creator
once trim/paper/page-count are locked).

Design pass: layered atmospheric gradient sky, soft glow, drop shadows,
ground-integrated character cluster, ribbon badge, vignette + grain finish.
"""
import math
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "generated-art")
OUT = os.path.join(HERE, "Spooky_Fun_Cover_Front.png")

PAGE = 2550
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

random.seed(7)


def font(path, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, path), size)


F_TITLE = font("DejaVuSans-Bold.ttf", 250)
F_SUB = font("DejaVuSans-Bold.ttf", 82)
F_BADGE = font("DejaVuSans-Bold.ttf", 46)
F_BADGE_SM = font("DejaVuSans-Bold.ttf", 52)
F_SEAL = font("DejaVuSans-Bold.ttf", 40)

# palette
SKY_TOP = (33, 18, 56)
SKY_MID = (76, 38, 82)
SKY_HORIZON = (214, 96, 62)
GROUND_NEAR = (198, 84, 40)
GROUND_FAR = (168, 63, 36)
CREAM = (255, 247, 232)
GOLD = (255, 200, 92)
DARK = (35, 18, 14)
MAROON = (110, 34, 30)


def multi_gradient(w, h, stops):
    """stops: list of (fraction, color)."""
    base = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(base)
    for y in range(h):
        t = y / (h - 1)
        for i in range(len(stops) - 1):
            f0, c0 = stops[i]
            f1, c1 = stops[i + 1]
            if f0 <= t <= f1 or i == len(stops) - 2:
                local_t = 0 if f1 == f0 else (t - f0) / (f1 - f0)
                local_t = max(0.0, min(1.0, local_t))
                color = tuple(int(c0[k] + (c1[k] - c0[k]) * local_t) for k in range(3))
                d.line([(0, y), (w, y)], fill=color)
                break
    return base


def radial_glow(size, color, alpha_max=140):
    glow = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(glow)
    cx = cy = size // 2
    steps = 90
    for i in range(steps, 0, -1):
        r = int(size / 2 * i / steps)
        a = int(alpha_max * (1 - i / steps) ** 2)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color, a))
    return glow


def draw_moon(img, cx, cy, r, color, sky_snapshot):
    glow = radial_glow(int(r * 3.2), color, alpha_max=55)
    img.paste(glow, (cx - glow.width // 2, cy - glow.height // 2), glow)
    d = ImageDraw.Draw(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    bite_r = r * 0.96
    bx = cx + r * 0.62
    # sample the ORIGINAL sky gradient (pre-glow) so the crescent bite matches the sky exactly
    mask = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(mask)
    md.ellipse([bx - bite_r, cy - bite_r, bx + bite_r, cy + bite_r], fill=255)
    img.paste(sky_snapshot, (0, 0), mask)


def draw_star(draw, cx, cy, r, color, alpha=255):
    layer = Image.new("RGBA", (int(r * 4), int(r * 4)), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    lc = r * 2
    pts = []
    for i in range(4):
        ang = math.pi / 2 * i
        pts.append((lc + r * math.cos(ang), lc + r * math.sin(ang)))
        ang2 = ang + math.pi / 4
        pts.append((lc + r * 0.32 * math.cos(ang2), lc + r * 0.32 * math.sin(ang2)))
    ld.polygon(pts, fill=(*color, alpha))
    return layer, (int(cx - lc), int(cy - lc))


def draw_bat_silhouette(size, color=(20, 10, 18)):
    w = h = size
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = w / 2, h / 2
    body_r = w * 0.09
    d.ellipse([cx - body_r, cy - body_r, cx + body_r, cy + body_r], fill=color)
    for side in (-1, 1):
        wing = [
            (cx, cy),
            (cx + side * w * 0.5, cy - h * 0.28),
            (cx + side * w * 0.38, cy - h * 0.05),
            (cx + side * w * 0.46, cy + h * 0.05),
            (cx + side * w * 0.28, cy + h * 0.02),
            (cx + side * w * 0.14, cy + h * 0.16),
            (cx, cy + h * 0.06),
        ]
        d.polygon(wing, fill=color)
    return layer


def draw_hill(img, y_base, color, amplitude=60, seed_offset=0, texture=False):
    w, h = img.size
    d = ImageDraw.Draw(img)
    pts = [(0, h)]
    for x in range(0, w + 1, 30):
        y = y_base + amplitude * math.sin((x + seed_offset) / 300.0) + amplitude * 0.3 * math.sin(
            (x + seed_offset) / 90.0
        )
        pts.append((x, y))
    pts.append((w, h))
    d.polygon(pts, fill=color)
    if texture:
        rnd = random.Random(seed_offset)
        for _ in range(140):
            x = rnd.uniform(0, w)
            base_y = y_base + amplitude * math.sin((x + seed_offset) / 300.0)
            y = base_y + rnd.uniform(10, h - base_y - 10)
            if y >= h:
                continue
            tuft_h = rnd.uniform(8, 20)
            shade = tuple(max(0, c - rnd.randint(0, 18)) for c in color)
            d.line([(x, y), (x - 5, y - tuft_h)], fill=shade, width=3)
            d.line([(x, y), (x + 5, y - tuft_h)], fill=shade, width=3)


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


def drop_shadow_for(art_rgba, blur=18, offset=(0, 14), alpha=110, tint=(20, 10, 8)):
    alpha_ch = art_rgba.split()[3]
    shadow = Image.new("RGBA", art_rgba.size, (0, 0, 0, 0))
    solid = Image.new("RGBA", art_rgba.size, (*tint, alpha))
    shadow = Image.composite(solid, shadow, alpha_ch)
    shadow = shadow.filter(ImageFilter.GaussianBlur(blur))
    return shadow, offset


def paste_with_shadow(base, art_path, box_size, center, shadow_alpha=110, blur=20,
                       backdrop=True, backdrop_color=CREAM, backdrop_scale=1.14):
    art = load_transparent(art_path)
    aw, ah = art.size
    scale = min(box_size / aw, box_size / ah)
    art = art.resize((int(aw * scale), int(ah * scale)), Image.LANCZOS)
    x = center[0] - art.width // 2
    y = center[1] - art.height // 2

    # soft contact shadow ellipse beneath (drawn first, furthest back)
    ell_w, ell_h = int(art.width * 0.62), int(art.height * 0.10)
    ell_y = y + art.height - ell_h // 2
    ellipse_layer = Image.new("RGBA", base.size, (0, 0, 0, 0))
    ed = ImageDraw.Draw(ellipse_layer)
    ed.ellipse(
        [center[0] - ell_w // 2, ell_y, center[0] + ell_w // 2, ell_y + ell_h],
        fill=(20, 10, 8, 90),
    )
    ellipse_layer = ellipse_layer.filter(ImageFilter.GaussianBlur(14))
    base.alpha_composite(ellipse_layer)

    # contrasting cream disc behind the character so its transparent interior
    # (which would otherwise show the same-hued ground straight through) pops
    if backdrop:
        disc_r = int(max(art.width, art.height) * backdrop_scale / 2)
        disc = Image.new("RGBA", (disc_r * 2, disc_r * 2), (0, 0, 0, 0))
        dd = ImageDraw.Draw(disc)
        dd.ellipse([0, 0, disc_r * 2, disc_r * 2], fill=(*backdrop_color, 255))
        disc_shadow, (sdx, sdy) = drop_shadow_for(disc, blur=blur, alpha=shadow_alpha)
        base.paste(disc_shadow, (center[0] - disc_r + sdx, center[1] - disc_r + sdy), disc_shadow)
        base.paste(disc, (center[0] - disc_r, center[1] - disc_r), disc)
    else:
        shadow, (sdx, sdy) = drop_shadow_for(art, blur=blur, alpha=shadow_alpha)
        base.paste(shadow, (x + sdx, y + sdy), shadow)

    base.paste(art, (x, y), art)


def text_soft_shadow(base_rgba, xy, text, font_, fill, anchor="mm",
                      shadow_color=(20, 10, 8), shadow_alpha=150, blur=10, offset=(0, 10),
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
    draw.polygon(body, fill=fill, outline=outline)
    tail_w = w * 0.09
    for side, x0 in ((-1, left), (1, right - tail_w)):
        tail = [
            (x0, top), (x0 + tail_w, top), (x0 + tail_w, bottom),
            (x0 + tail_w / 2, bottom - notch * 0.6), (x0, bottom),
        ]
        shade = tuple(max(0, c - 35) for c in fill)
        draw.polygon(tail, fill=shade, outline=outline)


def add_grain(img, amount=10):
    w, h = img.size
    rnd = random.Random(42)
    noise = Image.new("L", (w // 2, h // 2))
    noise.putdata([rnd.randint(128 - amount, 128 + amount) for _ in range(w // 2 * h // 2)])
    noise = noise.resize((w, h))
    noise_rgb = Image.merge("RGB", (noise, noise, noise))
    return Image.blend(img, noise_rgb, 0.035)


def vignette(img, strength=90):
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    d.ellipse([-w * 0.25, -h * 0.25, w * 1.25, h * 1.25], fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(220))
    dark = Image.new("RGB", (w, h), (0, 0, 0))
    dark.putalpha(Image.eval(mask, lambda v: strength * (255 - v) // 255))
    img = img.convert("RGBA")
    img.alpha_composite(dark)
    return img.convert("RGB")


def main():
    img = multi_gradient(
        PAGE, PAGE,
        [(0.0, SKY_TOP), (0.28, SKY_MID), (0.42, SKY_HORIZON), (0.48, GOLD),
         (0.55, GROUND_FAR), (1.0, GROUND_NEAR)],
    ).convert("RGBA")

    sky_snapshot = img.copy()
    draw_moon(img, PAGE - 470, 360, 195, CREAM, sky_snapshot)

    d = ImageDraw.Draw(img)
    star_spots = [(230, 190, 16), (420, 330, 11), (640, 150, 13), (880, 290, 10),
                  (1120, 200, 15), (1480, 140, 11), (1720, 300, 13), (300, 520, 9),
                  (990, 430, 8), (150, 380, 8)]
    for sx, sy, sr in star_spots:
        layer, pos = draw_star(d, sx, sy, sr, GOLD, alpha=230)
        img.paste(layer, pos, layer)

    for bx, by, bs, rot in [(560, 520, 90, 8), (1980, 460, 70, -12), (1780, 640, 55, 5)]:
        bat = draw_bat_silhouette(bs).rotate(rot, expand=True, resample=Image.BICUBIC)
        img.paste(bat, (bx - bat.width // 2, by - bat.height // 2), bat)

    draw_hill(img, 1240, GROUND_FAR, amplitude=55, seed_offset=0)
    draw_hill(img, 1330, GROUND_NEAR, amplitude=42, seed_offset=340, texture=True)

    d = ImageDraw.Draw(img)

    # title with soft shadow + crisp stroke
    text_soft_shadow(img, (PAGE // 2, 1000), "SPOOKY FUN", F_TITLE, CREAM,
                      shadow_alpha=170, blur=16, offset=(0, 16),
                      stroke_width=10, stroke_fill=DARK)
    text_soft_shadow(img, (PAGE // 2, 1175), "MY FIRST HALLOWEEN COLORING BOOK", F_SUB, GOLD,
                      shadow_alpha=140, blur=8, offset=(0, 8),
                      stroke_width=6, stroke_fill=DARK)

    # ribbon badge
    d = ImageDraw.Draw(img)
    ribbon(d, PAGE // 2, 1310, 1720, 130, MAROON, DARK)
    d.text((PAGE // 2, 1310), "40 CUTE (NOT SCARY) PICTURES TO COLOR", font=F_BADGE_SM,
           fill=CREAM, anchor="mm")

    # foreground character cluster, ground-integrated with shadows
    ground_y = 2000
    paste_with_shadow(img, os.path.join(ART, "page-11.png"), 190, (PAGE // 2 - 470, ground_y - 560),
                       blur=12, shadow_alpha=80, backdrop=False)
    paste_with_shadow(img, os.path.join(ART, "page-11.png"), 190, (PAGE // 2 + 470, ground_y - 600),
                       blur=12, shadow_alpha=80, backdrop=False)

    paste_with_shadow(img, os.path.join(ART, "page-04.png"), 480, (PAGE // 2 - 660, ground_y))
    paste_with_shadow(img, os.path.join(ART, "page-05.png"), 700, (PAGE // 2, ground_y + 30))
    paste_with_shadow(img, os.path.join(ART, "page-07.png"), 480, (PAGE // 2 + 660, ground_y))

    # age seal, bottom-left
    seal_c = (260, PAGE - 260)
    d = ImageDraw.Draw(img)
    d.ellipse([seal_c[0] - 150, seal_c[1] - 150, seal_c[0] + 150, seal_c[1] + 150],
              fill=GOLD, outline=DARK, width=8)
    d.ellipse([seal_c[0] - 118, seal_c[1] - 118, seal_c[0] + 118, seal_c[1] + 118],
              outline=DARK, width=4)
    d.text((seal_c[0], seal_c[1] - 28), "AGES", font=F_SEAL, fill=DARK, anchor="mm")
    d.text((seal_c[0], seal_c[1] + 30), "4-8", font=font("DejaVuSans-Bold.ttf", 66), fill=DARK,
           anchor="mm")

    img = vignette(img.convert("RGB"), strength=55)
    img = add_grain(img, amount=5)

    img.save(OUT, dpi=(300, 300))
    print("Wrote", OUT, img.size)


if __name__ == "__main__":
    main()
