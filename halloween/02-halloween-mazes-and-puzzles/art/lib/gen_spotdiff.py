import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from page import build_page, wrap_words
from symbols import use

OUT = os.path.join(os.path.dirname(__file__), "..")

PANEL_W = 300
PANEL_H = 480
GAP = 40
LEFT_X = 95
RIGHT_X = LEFT_X + PANEL_W + GAP


def panel_frame(x):
    return f'<rect x="{x}" y="200" width="{PANEL_W}" height="{PANEL_H}" fill="none" stroke="#000" stroke-width="2.4" rx="10"/>'


def house_scene(door="arch", window_left=True, bats=1, pumpkin_face="zigzag", branch=True):
    parts = []
    parts.append('<path d="M40,180 L150,70 L260,180" fill="none" stroke="#000" stroke-width="6" '
                  'stroke-linecap="round" stroke-linejoin="round"/>')
    parts.append('<rect x="60" y="175" width="180" height="150" fill="#fff" stroke="#000" stroke-width="6"/>')
    if door == "arch":
        parts.append('<path d="M130,325 L130,255 C130,238 145,228 158,228 C171,228 186,238 186,255 L186,325" '
                     'fill="#fff" stroke="#000" stroke-width="4"/>')
    else:
        parts.append('<rect x="130" y="250" width="56" height="75" fill="#fff" stroke="#000" stroke-width="4"/>')
    if window_left:
        parts.append('<rect x="80" y="210" width="32" height="32" rx="3" fill="#fff" stroke="#000" stroke-width="3.2"/>')
    parts.append('<rect x="205" y="210" width="32" height="32" rx="3" fill="#fff" stroke="#000" stroke-width="3.2"/>')
    # tree
    tbranch = '<path d="M330,300 C345,290 358,292 372,280" fill="none" stroke="#000" stroke-width="4" stroke-linecap="round"/>' if branch else ""
    parts.append(f'''<path d="M320,340 L320,260" stroke="#000" stroke-width="5" stroke-linecap="round"/>
      <path d="M320,290 C305,280 296,282 284,270 M320,270 C332,260 342,262 356,250" fill="none" stroke="#000" stroke-width="4" stroke-linecap="round"/>
      {tbranch}''')
    # pumpkin
    if pumpkin_face == "zigzag":
        mouth = '<path d="M118,392 Q124,400 130,392 Q134,402 140,392 Q144,400 150,392" fill="none" stroke="#000" stroke-width="2.4" stroke-linecap="round"/>'
    else:
        mouth = '<circle cx="134" cy="396" r="8" fill="none" stroke="#000" stroke-width="2.4"/>'
    parts.append(f'''<circle cx="134" cy="378" r="36" fill="#fff" stroke="#000" stroke-width="4.4"/>
      <path d="M118,368 L128,368 L123,380 Z" fill="#000"/>
      <path d="M150,368 L140,368 L145,380 Z" fill="#000"/>
      {mouth}''')
    # bats
    bat_positions = [(20, 50), (230, 40), (255, 110)]
    for i in range(bats):
        bx, by = bat_positions[i]
        parts.append(use("ic-bat", bx, by, 46, 20))
    return "\n".join(parts)


def kid_walk_scene(costume3="pumpkin", extra_pumpkin=False, bat=True, door="arch", window="box",
                    fence=True):
    parts = []
    parts.append('<path d="M20,170 L120,80 L220,170" fill="none" stroke="#000" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>')
    parts.append('<rect x="35" y="165" width="170" height="140" fill="#fff" stroke="#000" stroke-width="5"/>')
    if door == "arch":
        parts.append('<path d="M100,305 L100,245 C100,232 110,224 120,224 C130,224 140,232 140,245 L140,305" fill="#fff" stroke="#000" stroke-width="3.6"/>')
    else:
        parts.append('<rect x="100" y="250" width="40" height="55" fill="#fff" stroke="#000" stroke-width="3.6"/>')
    if window == "box":
        parts.append('<rect x="55" y="195" width="26" height="26" rx="2" fill="#fff" stroke="#000" stroke-width="2.6"/>')
    else:
        parts.append('<circle cx="68" cy="208" r="13" fill="#fff" stroke="#000" stroke-width="2.6"/>')
    parts.append(use("ch-kid-ghost", 20, 320, 78, 108))
    if costume3 == "pumpkin":
        parts.append(use("ch-kid-pumpkin", 110, 330, 78, 108))
    else:
        parts.append(use("ch-witch-full", 118, 322, 62, 100))
    parts.append(use("ch-kid-pumpkin", 205, 335, 74, 102))
    if extra_pumpkin:
        parts.append(use("ch-pumpkin", 30, 420, 44, 44))
    if bat:
        parts.append(use("ic-bat", 210, 90, 50, 22))
    if fence:
        parts.append('<path d="M15,440 L285,440" stroke="#000" stroke-width="3" stroke-linecap="round"/>')
    return "\n".join(parts)


def candy_table_scene(buckets=3, candycorn=True, spider=False, web=False, star=True, bat2=False, moon=False):
    parts = []
    parts.append('<path d="M20,340 L280,340" stroke="#000" stroke-width="5" stroke-linecap="round"/>')
    parts.append('<path d="M20,340 L20,420 M280,340 L280,420" stroke="#000" stroke-width="4" stroke-linecap="round"/>')
    bx = [60, 150, 230]
    for i in range(buckets):
        parts.append(use("ic-candybucket", bx[i] - 34, 250, 68, 68))
    if candycorn:
        parts.append(use("ic-candycorn", 105, 260, 34, 40))
        parts.append(use("ic-candycorn", 190, 265, 30, 36))
    if web:
        parts.append(use("ch-web", 15, 70, 56, 56))
    if moon:
        parts.append(use("ic-moon", 95, 60, 44, 44))
    if star:
        parts.append(use("ic-star", 230, 90, 24, 24))
    if spider:
        parts.append(use("ch-spider", 20, 150, 40, 36))
    if bat2:
        parts.append(use("ic-bat", 195, 60, 44, 19))
    return "\n".join(parts)


def spotdiff_page(num, title, instructions, scene_a, scene_b):
    a = f'<g transform="translate({LEFT_X},210)">{scene_a}</g>'
    b = f'<g transform="translate({RIGHT_X},210)">{scene_b}</g>'
    content = f'''
  {panel_frame(LEFT_X)}
  {panel_frame(RIGHT_X)}
  {a}
  {b}
'''
    lines = wrap_words(instructions, 620, 19)
    return build_page(title, lines, content, page_num=num, instr_size=19)


PAGES = []


def build_all():
    a = house_scene(door="arch", window_left=True, bats=1, pumpkin_face="zigzag", branch=True)
    b = house_scene(door="box", window_left=False, bats=2, pumpkin_face="o", branch=False)
    PAGES.append(dict(num=14, title="What's Different?",
                       instructions="These two haunted houses look the same, but 5 things are different! Find them all.",
                       scene_a=a, scene_b=b))

    a = kid_walk_scene(costume3="witch", extra_pumpkin=False, bat=False, door="arch", window="box", fence=False)
    b = kid_walk_scene(costume3="pumpkin", extra_pumpkin=True, bat=True, door="box", window="round", fence=True)
    PAGES.append(dict(num=23, title="What's Different?",
                       instructions="These two trick-or-treating scenes look the same, but 6 things are different! Find them all.",
                       scene_a=a, scene_b=b))

    a = candy_table_scene(buckets=2, candycorn=False, spider=False, web=False, star=False, bat2=False, moon=False)
    b = candy_table_scene(buckets=3, candycorn=True, spider=True, web=True, star=True, bat2=True, moon=True)
    PAGES.append(dict(num=31, title="What's Different?",
                       instructions="These two candy bucket pictures look the same, but 7 things are different! Find them all.",
                       scene_a=a, scene_b=b))


build_all()

if __name__ == "__main__":
    for spec in PAGES:
        svg = spotdiff_page(**spec)
        path = os.path.join(OUT, f"page-{spec['num']:02d}-spotdiff.svg")
        with open(path, "w") as f:
            f.write(svg)
        print("wrote", path)
