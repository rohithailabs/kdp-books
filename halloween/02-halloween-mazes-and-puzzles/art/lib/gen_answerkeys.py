import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from page import build_page
from symbols import use
from maze import Maze, render_maze_svg, render_solution_svg, cell_center
from wordsearch import render_wordsearch_answer_svg
from dotdot import render_dots_svg, fit_transform

import gen_mazes as GM
import gen_wordsearch as GW
import gen_dotdot as GD
import gen_countmatch as GC
import gen_spotdiff as GS

OUT = os.path.join(os.path.dirname(__file__), "..")

AREA_X0, AREA_Y0, AREA_X1, AREA_Y1 = 95, 205, 755, 785


def grid_cells(n, cols, rows):
    cw = (AREA_X1 - AREA_X0) / cols
    ch = (AREA_Y1 - AREA_Y0) / rows
    cells = []
    for i in range(n):
        r, c = divmod(i, cols)
        cells.append((AREA_X0 + c * cw, AREA_Y0 + r * ch, cw, ch))
    return cells


def caption(x, y, w, text):
    return (f'<text x="{x+w/2:.1f}" y="{y+18:.1f}" text-anchor="middle" font-family="Poppins" '
            f'font-weight="700" font-size="15" fill="#000">{text}</text>')


def cell_frame(x, y, w, h):
    return (f'<rect x="{x+6:.1f}" y="{y+6:.1f}" width="{w-12:.1f}" height="{h-12:.1f}" rx="8" '
            f'fill="none" stroke="#000" stroke-width="1.4" opacity="0.5"/>')


# ---------- Page 39: Mazes & Dot-to-Dots ----------
def maze_thumb(spec, x, y, w, h):
    pad_top = 30
    size = min(w - 24, h - pad_top - 14)
    ox = x + (w - size) / 2
    oy = y + pad_top
    m = Maze(spec["rows"], spec["cols"], spec["seed"], (0, 0), (spec["rows"] - 1, spec["cols"] - 1),
              spec["dead_ends"], spec["dead_end_depth"])
    walls, cell = render_maze_svg(m, ox, oy, size, wall_w=max(2, size / spec["rows"] * 0.09),
                                   open_edges=[(0, 0, spec["start_side"]), (spec["rows"] - 1, spec["cols"] - 1, spec["end_side"])])
    sol = render_solution_svg(m, ox, oy, size, stroke_w=max(1.6, size / spec["rows"] * 0.06))
    return caption(x, y, w, f'Page {spec["num"]}') + walls + sol


def dotdot_thumb(num, pts, x, y, w, h, closed=True):
    pad_top = 30
    size = min(w - 24, h - pad_top - 14)
    scale, ox, oy = fit_transform(pts, x + (w - size) / 2, y + pad_top, size, size, margin=0.1)
    dots = render_dots_svg(pts, ox, oy, scale, r=2.6, font_size=0, show_lines=True, closed=closed)
    return caption(x, y, w, f"Page {num}") + dots


def page_39():
    items = []
    for spec in GM.PAGES:
        items.append(("maze", spec))
    items.append(("dot", (9, GD.PUMPKIN, True)))
    items.append(("dot", (17, GD.BAT, True)))
    items.append(("dot", (25, GD.JACKOLANTERN, True)))
    items.append(("dot", (32, GD.CAT, False)))

    cells = grid_cells(len(items), 4, 3)
    parts = []
    for (kind, data), (x, y, w, h) in zip(items, cells):
        parts.append(cell_frame(x, y, w, h))
        if kind == "maze":
            parts.append(maze_thumb(data, x, y, w, h))
        else:
            num, pts, closed = data
            parts.append(dotdot_thumb(num, pts, x, y, w, h, closed))
    content = "\n  " + "\n  ".join(parts)
    instr = ["Mazes & Dot-to-Dots", "Pages 4, 7, 9, 12, 16, 17, 22, 25, 26, 30, 32, 37"]
    return build_page("Answer Key A", instr, content, page_num=39, title_size=40, instr_size=16)


# ---------- Page 40: Word Searches ----------
def page_40():
    cells = grid_cells(5, 2, 3)
    parts = []
    for spec, (x, y, w, h) in zip(GW.PAGES, cells):
        parts.append(cell_frame(x, y, w, h))
        grid, placements = GW.generate_wordsearch(spec["words"], spec["n"], spec["seed"], allow_diagonal=spec["diagonal"])
        pad_top = 28
        size = min(w - 20, h - pad_top - 10)
        gsvg = render_wordsearch_answer_svg(grid, placements, x + (w - size) / 2, y + pad_top, size,
                                             font_size=size / spec["n"] * 0.5)
        parts.append(caption(x, y, w, f'Page {spec["num"]}') + gsvg)
    content = "\n  " + "\n  ".join(parts)
    instr = ["Word Searches", "Pages 13, 20, 28, 34, 38"]
    return build_page("Answer Key B", instr, content, page_num=40, title_size=40, instr_size=17)


# ---------- Page 41: Spot the Difference & Count and Match ----------
SPOTDIFF_MARKS = {
    14: [(134, 378), (96, 226), (158, 280), (345, 290), (253, 50)],
    23: [(68, 208), (120, 275), (150, 370), (52, 442), (235, 101), (150, 440)],
    31: [(230, 284), (160, 280), (43, 98), (117, 82), (242, 102), (40, 168), (217, 70)],
}


def spotdiff_thumb(spec, marks, x, y, w, h):
    pad_top = 28
    inner_w = w - 20
    panel_w = (inner_w - 10) / 2
    scale = min(panel_w / GS.PANEL_W, (h - pad_top - 10) / GS.PANEL_H)
    ox = x + 10
    oy = y + pad_top
    right_x = ox + panel_w + 10
    g = (f'<g transform="translate({ox:.1f},{oy:.1f}) scale({scale:.3f})">{spec["scene_a"]}</g>'
         f'<g transform="translate({right_x:.1f},{oy:.1f}) scale({scale:.3f})">{spec["scene_b"]}'
         + "".join(f'<circle cx="{mx}" cy="{my}" r="16" fill="none" stroke="#e0392b" stroke-width="3"/>' for mx, my in marks)
         + '</g>')
    return caption(x, y, w, f'Page {spec["num"]}') + g


def countmatch_thumb(spec, x, y, w, h):
    import random
    random.seed(spec["seed"])
    counts = spec["counts"]
    shuffled = counts[:]
    while shuffled == counts:
        random.shuffle(shuffled)
    pad_top = 28
    size = min(w - 24, h - pad_top - 10)
    scale = size / 700
    ox = x + (w - size) / 2
    oy = y + pad_top
    parts = [f'<g transform="translate({ox:.1f},{oy:.1f}) scale({scale:.3f})">']
    rows_y = [90, 240, 390]
    for i, c in enumerate(counts):
        parts.append(GC.count_row_svg(spec["symbol"], c, rows_y[i], icon_size=26))
        j = shuffled.index(c)
        x1, y1 = GC.ICON_X0 - 10, rows_y[i]
        # line from row i to the numeral bubble now sitting at row j's slot
        x2, y2 = GC.NUM_X - 45, rows_y[j]
        parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#e0392b" stroke-width="4" stroke-linecap="round"/>')
        parts.append(GC.numeral_bubble(shuffled[i], rows_y[i]))
    parts.append("</g>")
    return caption(x, y, w, f'Page {spec["num"]}') + "".join(parts)


def page_41():
    items = []
    for spec in GS.PAGES:
        items.append(("sd", spec))
    for spec in GC.PAGES:
        items.append(("cm", spec))
    cells = grid_cells(len(items), 3, 3)
    parts = []
    for (kind, spec), (x, y, w, h) in zip(items, cells):
        parts.append(cell_frame(x, y, w, h))
        if kind == "sd":
            parts.append(spotdiff_thumb(spec, SPOTDIFF_MARKS[spec["num"]], x, y, w, h))
        else:
            parts.append(countmatch_thumb(spec, x, y, w, h))
    content = "\n  " + "\n  ".join(parts)
    instr = ["Spot the Difference & Count and Match", "Pages 6, 11, 14, 18, 23, 24, 29, 31, 35"]
    return build_page("Answer Key C", instr, content, page_num=41, title_size=40, instr_size=16)


# ---------- Page 42: Certificate ----------
def page_42():
    content = f'''
  <text x="425" y="190" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="58" fill="#000">Great Job!</text>
  <path d="M230,220 C320,234 530,234 620,220" fill="none" stroke="#000" stroke-width="3" stroke-linecap="round"/>
  <text x="425" y="300" text-anchor="middle" font-family="Poppins" font-weight="400" font-size="22" fill="#222">This certifies that</text>
  <path d="M180,395 L670,395" stroke="#000" stroke-width="3" stroke-linecap="round"/>
  <text x="425" y="460" text-anchor="middle" font-family="Poppins" font-weight="400" font-size="22" fill="#222">solved every maze and puzzle</text>
  <text x="425" y="492" text-anchor="middle" font-family="Poppins" font-weight="400" font-size="22" fill="#222">in this whole book!</text>
  <text x="425" y="580" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="34" fill="#000">Happy Halloween!</text>

  {use("ch-pumpkin", 110, 610, 110, 110)}
  {use("ch-ghost", 630, 615, 100, 108)}
  {use("ic-star", 150, 250, 26, 26)}
  {use("ic-star", 660, 260, 22, 22)}
  {use("ic-bat", 250, 220, 90, 40)}
  {use("ic-bat", 540, 215, 80, 35)}
  {use("ic-puzzle", 90, 430, 60, 60, 'transform="rotate(-10 120 460)"')}
  {use("ic-puzzle", 700, 430, 60, 60, 'transform="rotate(10 730 460)"')}
'''
    return build_page("Great Job!", None, content, page_num=42, skip_title=True)


if __name__ == "__main__":
    for num, fn in [(39, page_39), (40, page_40), (41, page_41), (42, page_42)]:
        svg = fn()
        path = os.path.join(OUT, f"page-{num:02d}-answerkey.svg" if num < 42 else f"page-{num:02d}-certificate.svg")
        with open(path, "w") as f:
            f.write(svg)
        print("wrote", path)
