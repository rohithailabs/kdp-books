"""Word search grid generator + SVG renderer."""
import random

DIRS_HV = [(0, 1), (1, 0)]
DIRS_ALL = [(0, 1), (1, 0), (1, 1), (-1, 1)]


def generate_wordsearch(words, size, seed, allow_diagonal=False, allow_reverse=False):
    random.seed(seed)
    words = [w.upper() for w in words]
    dirs = DIRS_ALL if allow_diagonal else DIRS_HV
    grid = [[None] * size for _ in range(size)]
    placements = {}

    def fits(word, r, c, dr, dc):
        for i, ch in enumerate(word):
            rr, cc = r + dr * i, c + dc * i
            if not (0 <= rr < size and 0 <= cc < size):
                return False
            if grid[rr][cc] not in (None, ch):
                return False
        return True

    def place(word, r, c, dr, dc):
        for i, ch in enumerate(word):
            grid[r + dr * i][c + dc * i] = ch

    for word in sorted(words, key=len, reverse=True):
        candidates = []
        for dr, dc in dirs:
            for r in range(size):
                for c in range(size):
                    w = word[::-1] if (allow_reverse and random.random() < 0.5) else word
                    if fits(w, r, c, dr, dc):
                        candidates.append((r, c, dr, dc, w))
        if not candidates:
            raise ValueError(f"could not place word {word} in {size}x{size} grid")
        r, c, dr, dc, w = random.choice(candidates)
        place(w, r, c, dr, dc)
        placements[word] = (r, c, dr, dc, len(word))

    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for r in range(size):
        for c in range(size):
            if grid[r][c] is None:
                grid[r][c] = random.choice(letters)

    return grid, placements


def render_wordsearch_svg(grid, x0, y0, size_px, font_size=None):
    n = len(grid)
    cell = size_px / n
    fs = font_size or cell * 0.62
    parts = [f'<rect x="{x0:.1f}" y="{y0:.1f}" width="{size_px:.1f}" height="{size_px:.1f}" '
              f'fill="none" stroke="#000" stroke-width="3"/>']
    for i in range(1, n):
        x = x0 + i * cell
        parts.append(f'<line x1="{x:.1f}" y1="{y0:.1f}" x2="{x:.1f}" y2="{y0+size_px:.1f}" stroke="#000" stroke-width="1.1"/>')
        y = y0 + i * cell
        parts.append(f'<line x1="{x0:.1f}" y1="{y:.1f}" x2="{x0+size_px:.1f}" y2="{y:.1f}" stroke="#000" stroke-width="1.1"/>')
    for r in range(n):
        for c in range(n):
            cx = x0 + c * cell + cell / 2
            cy = y0 + r * cell + cell / 2 + fs * 0.34
            parts.append(f'<text x="{cx:.1f}" y="{cy:.1f}" text-anchor="middle" '
                         f'font-family="Poppins" font-weight="600" font-size="{fs:.1f}" fill="#000">{grid[r][c]}</text>')
    return "\n".join(parts), cell


def render_wordlist_svg(words, x0, y0, avail_w, y_line_h=34, cols=None, font_size=17):
    words = [w.upper() for w in words]
    cols = cols or min(len(words), 5)
    rows = -(-len(words) // cols)
    col_w = avail_w / cols
    parts = []
    for i, w in enumerate(words):
        r, c = divmod(i, cols)
        cx = x0 + c * col_w + col_w / 2
        cy = y0 + r * y_line_h
        box_w = max(64, len(w) * font_size * 0.62 + 20)
        parts.append(f'<rect x="{cx-box_w/2:.1f}" y="{cy-22:.1f}" width="{box_w:.1f}" height="30" rx="14" '
                     f'fill="none" stroke="#000" stroke-width="2.2"/>')
        parts.append(f'<text x="{cx:.1f}" y="{cy:.1f}" text-anchor="middle" font-family="Poppins" '
                     f'font-weight="600" font-size="{font_size}" fill="#000">{w}</text>')
    return "\n".join(parts), rows * y_line_h


def render_wordsearch_answer_svg(grid, placements, x0, y0, size_px, font_size=None):
    """Small thumbnail: grid + circled found words, for the answer key."""
    svg, cell = render_wordsearch_svg(grid, x0, y0, size_px, font_size)
    parts = [svg]
    for word, (r, c, dr, dc, length) in placements.items():
        x1 = x0 + c * cell + cell / 2
        y1 = y0 + r * cell + cell / 2
        x2 = x0 + (c + dc * (length - 1)) * cell + cell / 2
        y2 = y0 + (r + dr * (length - 1)) * cell + cell / 2
        rx = abs(x2 - x1) / 2 + cell * 0.55
        ry = abs(y2 - y1) / 2 + cell * 0.55
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        angle = 0
        import math
        if dr != 0 and dc != 0:
            angle = 45 if dr == dc else -45
        parts.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" '
                     f'transform="rotate({angle} {cx:.1f} {cy:.1f})" fill="none" stroke="#e0392b" stroke-width="2.6"/>')
    return "\n".join(parts)
