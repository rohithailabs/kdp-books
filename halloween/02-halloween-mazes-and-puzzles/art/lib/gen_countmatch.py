import os, sys, random
sys.path.insert(0, os.path.dirname(__file__))
from page import build_page
from symbols import use

OUT = os.path.join(os.path.dirname(__file__), "..")

ROW_Y = [300, 460, 620]
ICON_X0 = 140
ICON_ROW_W = 470
NUM_X = 690


def count_row_svg(symbol, count, y, icon_size=46):
    gap = min(58, ICON_ROW_W / max(count, 1))
    parts = []
    for i in range(count):
        x = ICON_X0 + i * gap
        parts.append(use(symbol, x, y - icon_size / 2, icon_size, icon_size))
    return "\n".join(parts)


def numeral_bubble(n, y):
    return (f'<circle cx="{NUM_X}" cy="{y}" r="34" fill="none" stroke="#000" stroke-width="3"/>'
            f'<text x="{NUM_X}" y="{y+14}" text-anchor="middle" font-family="Fredoka" font-weight="700" '
            f'font-size="40" fill="#000">{n}</text>'
            f'<circle cx="{NUM_X-52}" cy="{y}" r="3.5" fill="#000"/>')


def countmatch_page(num, title, symbol, counts, seed):
    random.seed(seed)
    shuffled = counts[:]
    while shuffled == counts:
        random.shuffle(shuffled)
    rows = []
    for i, c in enumerate(counts):
        rows.append(count_row_svg(symbol, c, ROW_Y[i]))
        rows.append(f'<circle cx="{ICON_X0-38}" cy="{ROW_Y[i]}" r="3.5" fill="#000"/>')
    nums = [numeral_bubble(shuffled[i], ROW_Y[i]) for i in range(3)]
    dividers = [f'<line x1="120" y1="{y}" x2="740" y2="{y}" stroke="#000" stroke-width="1" '
                f'stroke-dasharray="1 10" opacity="0.35"/>' for y in [380, 540]]
    content = "\n  " + "\n  ".join(rows + nums + dividers)
    instructions = "Count the items in each row. Draw a line to the matching number."
    return build_page(title, instructions, content, page_num=num)


PAGES = [
    dict(num=6, title="Count the Bats", symbol="ic-bat", counts=[2, 4, 6], seed=1),
    dict(num=11, title="Count the Candy Corn", symbol="ic-candycorn", counts=[1, 3, 5], seed=2),
    dict(num=18, title="Count the Ghosts", symbol="ch-ghost", counts=[3, 5, 7], seed=3),
    dict(num=24, title="Count the Spiders", symbol="ch-spider", counts=[4, 6, 8], seed=4),
    dict(num=29, title="Count the Owls", symbol="ch-owl", counts=[5, 7, 9], seed=5),
    dict(num=35, title="Count the Jack-o-Lanterns", symbol="ch-pumpkin", counts=[6, 8, 10], seed=6),
]

if __name__ == "__main__":
    for spec in PAGES:
        svg = countmatch_page(**spec)
        path = os.path.join(OUT, f"page-{spec['num']:02d}-countmatch.svg")
        with open(path, "w") as f:
            f.write(svg)
        print("wrote", path)
