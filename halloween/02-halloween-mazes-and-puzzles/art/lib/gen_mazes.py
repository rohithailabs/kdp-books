import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from page import build_page, CONTENT_TOP
from maze import Maze, render_maze_svg
from symbols import use

OUT = os.path.join(os.path.dirname(__file__), "..")

AREA_SIZE = 520
LIVE_X0, LIVE_X1 = 90, 760
LIVE_Y0, LIVE_Y1 = 195, 793
AREA_X0 = LIVE_X0 + ((LIVE_X1 - LIVE_X0) - AREA_SIZE) / 2
AREA_Y0 = LIVE_Y0 + ((LIVE_Y1 - LIVE_Y0) - AREA_SIZE) / 2

EDGE_POINT = {
    'top': lambda x0, y0, cell, r, c: (x0 + c * cell + cell / 2, y0 + r * cell),
    'bottom': lambda x0, y0, cell, r, c: (x0 + c * cell + cell / 2, y0 + (r + 1) * cell),
    'left': lambda x0, y0, cell, r, c: (x0 + c * cell, y0 + r * cell + cell / 2),
    'right': lambda x0, y0, cell, r, c: (x0 + (c + 1) * cell, y0 + r * cell + cell / 2),
}
OUTWARD = {'top': (0, -1), 'bottom': (0, 1), 'left': (-1, 0), 'right': (1, 0)}


def arrow_marker(px, py, side, half_extent):
    dx, dy = OUTWARD[side]
    x1, y1 = px + dx * (half_extent + 24), py + dy * (half_extent + 24)
    x2, y2 = px + dx * (half_extent + 6), py + dy * (half_extent + 6)
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#000" stroke-width="5" '
            f'stroke-linecap="round" marker-end="url(#mz-arrow)"/>')


def maze_page(num, title, instructions, rows, cols, seed, dead_ends, dead_end_depth,
              start_symbol, start_dim, end_symbol, end_dim, start_side='left', end_side='right',
              decorations=""):
    start_rc = (0, 0)
    end_rc = (rows - 1, cols - 1)
    m = Maze(rows, cols, seed, start_rc, end_rc, dead_ends, dead_end_depth)
    cell = AREA_SIZE / max(rows, cols)
    wall_w = max(5, cell * 0.11)
    walls, cell = render_maze_svg(m, AREA_X0, AREA_Y0, AREA_SIZE, wall_w=wall_w,
                                   open_edges=[(0, 0, start_side), (rows - 1, cols - 1, end_side)])

    sx, sy = EDGE_POINT[start_side](AREA_X0, AREA_Y0, cell, 0, 0)
    ex, ey = EDGE_POINT[end_side](AREA_X0, AREA_Y0, cell, rows - 1, cols - 1)

    sw, sh = start_dim
    ew, eh = end_dim
    start_use = use(start_symbol, sx - sw / 2, sy - sh / 2, sw, sh)
    end_use = use(end_symbol, ex - ew / 2, ey - eh / 2, ew, eh)
    arrow = arrow_marker(sx, sy, start_side, max(sw, sh) / 2)

    defs = '''<marker id="mz-arrow" viewBox="0 0 20 20" refX="14" refY="10" markerWidth="9" markerHeight="9" orient="auto">
      <path d="M2,2 L18,10 L2,18 C6,14 6,6 2,2 Z" fill="#000"/>
    </marker>'''

    content = f'''
  {walls}
  {arrow}
  {start_use}
  {end_use}
  {decorations}
'''
    return build_page(title, instructions, content, page_num=num, extra_defs=defs)


PAGES = [
    dict(num=4, title="Candy Trail",
         instructions="Help the trick-or-treater get to the candy! Start at the arrow.",
         rows=4, cols=4, seed=111, dead_ends=0, dead_end_depth=2,
         start_symbol="ch-pumpkin", start_dim=(70, 70), end_symbol="ic-candybucket", end_dim=(66, 66),
         start_side='left', end_side='right'),
    dict(num=7, title="Home Sweet Home",
         instructions="Help the little ghost find its way home! Start at the ghost.",
         rows=4, cols=4, seed=212, dead_ends=0, dead_end_depth=2,
         start_symbol="ch-ghost", start_dim=(62, 68), end_symbol="ch-house", end_dim=(68, 68),
         start_side='top', end_side='bottom'),
    dict(num=12, title="Yarn... I Mean, Pumpkin!",
         instructions="Help the black cat get to the pumpkin! Start at the cat.",
         rows=5, cols=5, seed=313, dead_ends=1, dead_end_depth=2,
         start_symbol="ch-cat", start_dim=(64, 64), end_symbol="ch-pumpkin", end_dim=(66, 66),
         start_side='left', end_side='right'),
    dict(num=16, title="To the Cauldron!",
         instructions="Help the witch get back to her cauldron! Watch out for dead ends!",
         rows=6, cols=6, seed=414, dead_ends=3, dead_end_depth=2,
         start_symbol="ch-witch-full", start_dim=(52, 66), end_symbol="ch-cauldron", end_dim=(66, 60),
         start_side='top', end_side='bottom'),
    dict(num=22, title="Web It Up",
         instructions="Help the spider get to its web! Watch out for dead ends!",
         rows=7, cols=7, seed=515, dead_ends=3, dead_end_depth=2,
         start_symbol="ch-spider", start_dim=(60, 54), end_symbol="ch-web", end_dim=(64, 64),
         start_side='left', end_side='top'),
    dict(num=26, title="Treasure Hunt",
         instructions="Help the mummy find the hidden treasure! Watch out for dead ends!",
         rows=7, cols=7, seed=616, dead_ends=4, dead_end_depth=2,
         start_symbol="ch-mummy", start_dim=(50, 60), end_symbol="ic-chest", end_dim=(64, 52),
         start_side='top', end_side='bottom'),
    dict(num=30, title="Fly Home, Little Bat",
         instructions="Help the vampire bat get back to its cave! Watch out for dead ends!",
         rows=8, cols=8, seed=717, dead_ends=5, dead_end_depth=2,
         start_symbol="ch-bat", start_dim=(66, 44), end_symbol="ic-cave", end_dim=(66, 60),
         start_side='left', end_side='right'),
    dict(num=37, title="Graveyard Party",
         instructions="Help all three ghosts find their way through the graveyard to the party!",
         rows=9, cols=9, seed=818, dead_ends=6, dead_end_depth=2,
         start_symbol="ch-ghost", start_dim=(52, 57), end_symbol="ic-party", end_dim=(58, 52),
         start_side='left', end_side='right'),
]


if __name__ == "__main__":
    for spec in PAGES:
        svg = maze_page(**spec)
        path = os.path.join(OUT, f"page-{spec['num']:02d}-maze.svg")
        with open(path, "w") as f:
            f.write(svg)
        print("wrote", path)
