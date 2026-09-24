import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from page import build_page
from wordsearch import generate_wordsearch, render_wordsearch_svg, render_wordlist_svg

OUT = os.path.join(os.path.dirname(__file__), "..")

GRID_X0 = 175
GRID_Y0 = 208
GRID_SIZE = 470

PAGES = [
    dict(num=13, title="Find the Words", words=["BAT", "CAT", "BOO", "OWL", "MOON"],
         n=8, seed=21, diagonal=False, wl_cols=5),
    dict(num=20, title="Find the Words", words=["GHOST", "WITCH", "SPIDER", "CANDY", "PUMPKIN", "TRICK"],
         n=10, seed=22, diagonal=False, wl_cols=3),
    dict(num=28, title="Find the Words", words=["SKELETON", "LANTERN", "BROOM", "VAMPIRE", "MASK", "TREAT", "MOON"],
         n=12, seed=23, diagonal=True, wl_cols=4),
    dict(num=34, title="Find the Words",
         words=["HALLOWEEN", "COSTUME", "CAULDRON", "GRAVEYARD", "SPOOKY", "MIDNIGHT", "CANDY", "WITCH"],
         n=14, seed=24, diagonal=True, wl_cols=4),
    dict(num=38, title="Find the Words",
         words=["OWL", "BAT", "CAT", "WEB", "BOO", "TRICK", "TREAT", "GHOST", "CANDY", "SPOOKY"],
         n=14, seed=25, diagonal=True, wl_cols=5),
]


def wordsearch_page(num, title, words, n, seed, diagonal, wl_cols):
    grid, placements = generate_wordsearch(words, n, seed, allow_diagonal=diagonal)
    gsvg, cell = render_wordsearch_svg(grid, GRID_X0, GRID_Y0, GRID_SIZE)
    wsvg, _ = render_wordlist_svg(words, GRID_X0, GRID_Y0 + GRID_SIZE + 46, GRID_SIZE, cols=wl_cols, font_size=16)
    content = f'''
  {gsvg}
  {wsvg}
'''
    instructions = f"Find these words below! Words go across, down{', and diagonally' if diagonal else ''}."
    return build_page(title, instructions, content, page_num=num, instr_size=19)


if __name__ == "__main__":
    for spec in PAGES:
        svg = wordsearch_page(**spec)
        path = os.path.join(OUT, f"page-{spec['num']:02d}-wordsearch.svg")
        with open(path, "w") as f:
            f.write(svg)
        print("wrote", path)
