import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from page import build_page
from dotdot import circle_points, render_dots_svg, fit_transform

OUT = os.path.join(os.path.dirname(__file__), "..")

AREA_X0, AREA_Y0, AREA_W, AREA_H = 100, 205, 650, 555

# ---- Shape definitions (local unit coordinates, later scaled+placed) ----

PUMPKIN = circle_points(300, 340, 210, 8) + [(300, 100), (330, 55)]

BAT = [
    (20, 200), (90, 130), (130, 195), (175, 140), (210, 115),
    (260, 80), (300, 108), (340, 80), (390, 115),
    (425, 140), (470, 195), (510, 130), (580, 200),
    (335, 250), (265, 250),
]

_face_outline = circle_points(300, 300, 210, 15)
JACKOLANTERN = _face_outline  # dots 1-15
JACKOLANTERN_BONUS = [(210, 350), (250, 390), (300, 345), (350, 390), (390, 350)]  # 16-20 (smile)

CAT = [
    (140, 80), (175, 120), (215, 75),              # left ear, dip, right ear
    (250, 130), (230, 190), (200, 230),            # back of head, forehead, chin
    (175, 270), (165, 340), (160, 420),            # chest, front leg, front paw
    (230, 430), (300, 430), (340, 400),            # belly, haunch bottom, back of haunch
    (330, 340), (300, 260), (290, 180),            # back curve up toward shoulders
    (330, 150), (370, 120), (410, 150), (395, 200), (355, 190),  # curled tail spiral
]


def dot_page(num, title, instructions, pts, closed=True):
    scale, ox, oy = fit_transform(pts, AREA_X0, AREA_Y0, AREA_W, AREA_H)
    dots = render_dots_svg(pts, ox, oy, scale, closed=closed)
    content = f"\n  {dots}\n"
    return build_page(title, instructions, content, page_num=num)


def dot_page_bonus(num, title, instructions, pts, bonus_pts):
    scale, ox, oy = fit_transform(pts, AREA_X0, AREA_Y0, AREA_W, AREA_H, extra_pts=bonus_pts)
    main = render_dots_svg(pts, ox, oy, scale, closed=True)
    # bonus dots continue numbering from len(pts)+1
    bonus_labeled = []
    x0, y0 = ox, oy
    import math
    cxm = sum(ox + p[0] * scale for p in bonus_pts) / len(bonus_pts)
    cym = sum(oy + p[1] * scale for p in bonus_pts) / len(bonus_pts)
    for i, (px, py) in enumerate(bonus_pts):
        x, y = ox + px * scale, oy + py * scale
        bonus_labeled.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" fill="#000"/>')
        dx, dy = x - cxm, y - cym
        dist = math.hypot(dx, dy) or 1
        lx, ly = x + dx / dist * 20, y + dy / dist * 20 - 14
        bonus_labeled.append(f'<text x="{lx:.1f}" y="{ly+5:.1f}" text-anchor="middle" font-family="Poppins" '
                             f'font-weight="700" font-size="15" fill="#000">{len(pts)+i+1}</text>')
    content = f"\n  {main}\n  {''.join(bonus_labeled)}\n"
    return build_page(title, instructions, content, page_num=num)


if __name__ == "__main__":
    pages = []

    pages.append((9, dot_page(
        9, "Connect the Dots", "Connect the dots from 1 to 10. Then color your picture!",
        PUMPKIN)))

    pages.append((17, dot_page(
        17, "Connect the Dots", "Connect the dots from 1 to 15. Then color your picture!",
        BAT)))

    pages.append((25, dot_page_bonus(
        25, "Connect the Dots", "Connect the dots from 1 to 20. Then color your picture!",
        JACKOLANTERN, JACKOLANTERN_BONUS)))

    pages.append((32, dot_page(
        32, "Connect the Dots", "Connect the dots from 1 to 20. Then color your picture!",
        CAT, closed=False)))

    for num, svg in pages:
        path = os.path.join(OUT, f"page-{num:02d}-dottodot.svg")
        with open(path, "w") as f:
            f.write(svg)
        print("wrote", path)
