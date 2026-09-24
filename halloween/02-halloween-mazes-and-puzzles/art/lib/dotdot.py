import math


def circle_points(cx, cy, r, n, start_deg=-90):
    pts = []
    for i in range(n):
        a = math.radians(start_deg + 360 * i / n)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def fit_transform(pts, area_x0, area_y0, area_w, area_h, margin=0.12, extra_pts=None):
    all_pts = list(pts) + list(extra_pts or [])
    xs = [p[0] for p in all_pts]
    ys = [p[1] for p in all_pts]
    bbox_w = max(xs) - min(xs)
    bbox_h = max(ys) - min(ys)
    scale = min(area_w * (1 - margin) / bbox_w, area_h * (1 - margin) / bbox_h)
    cx = (max(xs) + min(xs)) / 2
    cy = (max(ys) + min(ys)) / 2
    ox = area_x0 + area_w / 2 - cx * scale
    oy = area_y0 + area_h / 2 - cy * scale
    return scale, ox, oy


def render_dots_svg(pts, x0, y0, scale, r=7, font_size=15, show_lines=False, closed=True, color="#000"):
    def T(p):
        return (x0 + p[0] * scale, y0 + p[1] * scale)

    parts = []
    if show_lines:
        tp = [T(p) for p in pts]
        d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in tp)
        if closed:
            d += " Z"
        parts.append(f'<path d="{d}" fill="none" stroke="{color}" stroke-width="3" '
                     f'stroke-linecap="round" stroke-linejoin="round"/>')
    for i, p in enumerate(pts):
        x, y = T(p)
        parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#000"/>')
        # label offset outward from centroid
        cxm = sum(a for a, b in [T(q) for q in pts]) / len(pts)
        cym = sum(b for a, b in [T(q) for q in pts]) / len(pts)
        dx, dy = x - cxm, y - cym
        dist = math.hypot(dx, dy) or 1
        lx, ly = x + dx / dist * 22, y + dy / dist * 22
        parts.append(f'<text x="{lx:.1f}" y="{ly+5:.1f}" text-anchor="middle" font-family="Poppins" '
                     f'font-weight="700" font-size="{font_size}" fill="#000">{i+1}</text>')
    return "\n".join(parts)
