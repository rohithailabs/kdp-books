import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from page import build_page
from symbols import use

OUT = os.path.join(os.path.dirname(__file__), "..")


def page_05():
    content = use("ch-pumpkin-plain", 215, 240, 420, 420)
    return build_page("Pretty Pumpkin", "Color this pumpkin any way you like!", content, page_num=5)


def page_10():
    content = use("ch-witch-bust", 215, 240, 420, 420)
    return build_page("Friendly Witch", "Color the witch and her hat!", content, page_num=10)


def page_15():
    content = f'''
  {use("ic-moon", 590, 230, 90, 90)}
  {use("ic-star", 540, 340, 26, 26)}
  {use("ch-owl", 225, 255, 400, 400)}
  <path d="M120,660 C300,630 550,630 730,660" fill="none" stroke="#000" stroke-width="8" stroke-linecap="round"/>
  <path d="M200,660 L170,620 M600,660 L640,615" fill="none" stroke="#000" stroke-width="5" stroke-linecap="round"/>
'''
    return build_page("Wise Owl", "Color the owl sitting on its branch.", content, page_num=15)


def page_21():
    content = f'''
  {use("ic-moon", 610, 225, 80, 80)}
  {use("ic-star", 555, 320, 22, 22)}
  {use("ch-tree-bare", 105, 300, 190, 250)}
  {use("ch-house", 330, 260, 380, 380)}
  <path d="M90,640 L770,640" stroke="#000" stroke-width="5" stroke-linecap="round"/>
  {use("ch-pumpkin", 400, 590, 80, 80)}
  {use("ch-pumpkin", 500, 585, 90, 90)}
'''
    return build_page("Haunted House", "Color the haunted house and everything around it.", content, page_num=21)


def page_27():
    content = f'''
  {use("ic-star", 600, 230, 24, 24)}
  {use("ic-moon", 640, 300, 60, 60)}
  {use("ch-scarecrow", 275, 220, 300, 420)}
  <path d="M90,650 L770,650" stroke="#000" stroke-width="5" stroke-linecap="round"/>
  {use("ch-pumpkin", 120, 580, 100, 100)}
  {use("ch-pumpkin", 230, 610, 80, 80)}
  {use("ch-pumpkin-plain", 590, 600, 95, 95)}
  {use("ch-pumpkin-plain", 690, 610, 75, 75)}
'''
    return build_page("Scarecrow in the Field", "Color the scarecrow and the pumpkin patch around him.",
                       content, page_num=27)


def page_36():
    content = f'''
  {use("ic-star", 140, 220, 22, 22)}
  {use("ic-star", 700, 210, 26, 26)}
  {use("ic-moon", 640, 230, 60, 60)}
  {use("ch-kid-ghost", 130, 330, 190, 266)}
  {use("ch-kid-pumpkin", 335, 350, 190, 266)}
  {use("ch-witch-full", 555, 320, 175, 280)}
  <path d="M90,680 L770,680" stroke="#000" stroke-width="5" stroke-linecap="round"/>
'''
    return build_page("Trick-or-Treat Friends", "Color the group of trick-or-treaters in their costumes.",
                       content, page_num=36)


if __name__ == "__main__":
    for num, fn in [(5, page_05), (10, page_10), (15, page_15), (21, page_21), (27, page_27), (36, page_36)]:
        svg = fn()
        path = os.path.join(OUT, f"page-{num:02d}-coloring.svg")
        with open(path, "w") as f:
            f.write(svg)
        print("wrote", path)
