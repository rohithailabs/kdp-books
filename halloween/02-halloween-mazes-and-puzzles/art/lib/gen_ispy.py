import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from page import build_page, paragraph_svg, wrap_words
from symbols import use

OUT = os.path.join(os.path.dirname(__file__), "..")


def page_08():
    bg = f'''
  {use("ic-moon", 640, 210, 70, 70)}
  {use("ic-star", 580, 300, 20, 20)}
  {use("ch-tree", 95, 260, 190, 250)}
  {use("ch-house", 420, 235, 330, 330)}
  <path d="M90,690 L760,690" stroke="#000" stroke-width="4" stroke-linecap="round"/>
  {use("ic-fence", 130, 610, 220, 90)}
  <path d="M420,690 C460,640 470,600 480,565" fill="none" stroke="#000" stroke-width="3" stroke-dasharray="2 10" stroke-linecap="round"/>
'''
    finds = f'''
  {use("ch-cat", 210, 600, 90, 90)}
  {use("ic-bat", 250, 260, 90, 40)}
  {use("ic-bat", 470, 200, 78, 34)}
  {use("ch-pumpkin", 500, 610, 78, 78)}
  {use("ch-pumpkin", 575, 625, 62, 62)}
  {use("ch-pumpkin", 630, 600, 92, 92)}
  {use("ch-web", 168, 585, 62, 62)}
  {use("ch-spider", 178, 605, 42, 38)}
'''
    content = bg + finds
    instr = "Look at the picture. Can you find: 1 black cat, 2 bats, 3 pumpkins, and 1 spider? Circle each one you find."
    return build_page("I Spy Halloween!", wrap_words(instr, 620, 19), content, page_num=8, instr_size=19)


def page_19():
    bg = f'''
  {use("ch-tree-bare", 85, 235, 170, 260)}
  {use("ch-tree-bare", 330, 200, 190, 290)}
  {use("ch-tree-bare", 610, 250, 160, 250)}
  <path d="M90,700 L760,700" stroke="#000" stroke-width="4" stroke-linecap="round"/>
  {use("ic-star", 250, 230, 20, 20)}
  {use("ic-moon", 700, 215, 60, 60)}
'''
    finds = f'''
  {use("ch-owl", 130, 300, 90, 90)}
  {use("ch-owl", 560, 340, 75, 75)}
  {use("ic-bat", 300, 240, 80, 34)}
  {use("ic-bat", 460, 260, 70, 30)}
  {use("ic-bat", 660, 320, 76, 32)}
  {use("ch-cat", 355, 610, 80, 80)}
  {use("ic-mushroom", 175, 640, 60, 60)}
  {use("ic-mushroom", 470, 655, 46, 46)}
  {use("ic-mushroom", 555, 630, 66, 66)}
  {use("ic-mushroom", 650, 650, 50, 50)}
'''
    content = bg + finds
    instr = "Look at the picture. Can you find: 2 owls, 3 bats, 1 black cat, and 4 mushrooms? Circle each one you find."
    return build_page("I Spy in the Spooky Forest!", wrap_words(instr, 620, 19), content, page_num=19, instr_size=19)


def page_33():
    bg = f'''
  {use("ch-house", 100, 260, 260, 260)}
  {use("ch-house", 520, 250, 250, 250)}
  <path d="M90,700 L760,700" stroke="#000" stroke-width="4" stroke-linecap="round"/>
  {use("ic-moon", 470, 210, 55, 55)}
  {use("ic-star", 420, 300, 18, 18)}
'''
    finds = f'''
  {use("ch-pumpkin", 150, 610, 66, 66)}
  {use("ch-pumpkin", 470, 615, 58, 58)}
  {use("ch-pumpkin", 660, 605, 70, 70)}
  {use("ic-bat", 200, 210, 70, 30)}
  {use("ic-bat", 380, 180, 62, 27)}
  {use("ic-bat", 520, 230, 66, 28)}
  {use("ic-bat", 700, 190, 58, 25)}
  {use("ch-witch-full", 245, 480, 78, 125)}
  {use("ch-witch-full", 610, 490, 72, 115)}
  {use("ch-cat", 400, 630, 68, 68)}
  {use("ch-kid-ghost", 130, 500, 82, 115)}
  {use("ch-kid-pumpkin", 330, 520, 82, 115)}
  {use("ch-kid-ghost", 460, 505, 74, 104)}
  {use("ch-kid-pumpkin", 545, 525, 74, 104)}
  {use("ch-ghost", 660, 540, 66, 72)}
'''
    content = bg + finds
    instr = "Look at the busy picture. Find: 3 pumpkins, 4 bats, 2 witches, 1 black cat, and 5 trick-or-treaters!"
    return build_page("I Spy on Trick-or-Treat Street!", wrap_words(instr, 600, 18), content, page_num=33, instr_size=18)


if __name__ == "__main__":
    for num, fn in [(8, page_08), (19, page_19), (33, page_33)]:
        svg = fn()
        path = os.path.join(OUT, f"page-{num:02d}-ispy.svg")
        with open(path, "w") as f:
            f.write(svg)
        print("wrote", path)
