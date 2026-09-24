import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from page import build_page, paragraph_svg, esc
from symbols import use

OUT = os.path.join(os.path.dirname(__file__), "..")


def page_02():
    content = f'''
  <text x="425" y="200" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="44" fill="#000">This Book Belongs To:</text>
  <path d="M150,330 L700,330" stroke="#000" stroke-width="3" stroke-linecap="round"/>
  <text x="330" y="410" text-anchor="end" font-family="Fredoka" font-weight="600" font-size="30" fill="#000">I am</text>
  <path d="M350,395 L470,395" stroke="#000" stroke-width="3" stroke-linecap="round"/>
  <text x="490" y="410" text-anchor="start" font-family="Fredoka" font-weight="600" font-size="30" fill="#000">years old.</text>

  {use("ch-pumpkin", 110, 470, 110, 110)}
  {use("ch-ghost", 640, 480, 100, 108)}
  {use("ic-bat", 300, 500, 110, 46)}
  {use("ic-bat", 470, 555, 90, 38, 'transform="rotate(-8 515 574)"')}
  {use("ic-star", 250, 600, 26, 26)}
  {use("ic-star", 560, 470, 22, 22)}

  <g>
    {use("ic-candycorn", 140, 680, 34, 40)}
    {use("ch-cat", 210, 665, 70, 70)}
    {use("ic-puzzle", 300, 672, 60, 60)}
    {use("ic-candycorn", 390, 680, 34, 40)}
    {use("ch-owl", 450, 665, 68, 68)}
    {use("ic-puzzle", 540, 672, 60, 60)}
    {use("ch-bat", 610, 668, 90, 58)}
  </g>
  <path d="M105,745 L745,745" stroke="#000" stroke-width="2" stroke-dasharray="1 10" stroke-linecap="round"/>
'''
    return build_page("This Book Belongs To", None, content, page_num=2, skip_title=True)


def page_03():
    note = ("Welcome to Halloween Mazes & Puzzles! This book starts with easy activities and gets a "
            "little trickier as you go, so it grows with your child. Feel free to help trace mazes "
            "with a finger first, read instructions aloud, or work through pages together. An answer "
            "key for every puzzle is in the back of the book if you need it. Grab a pencil or crayon "
            "and have a spooky-fun time!")
    para, h = paragraph_svg(note, 425, 290, 560, font_size=22, line_h=34)
    content = f'''
  <text x="425" y="180" text-anchor="middle" font-family="Fredoka" font-weight="700" font-size="42" fill="#000">A Note for Grown-Ups</text>
  <path d="M230,210 C300,222 550,222 620,210" fill="none" stroke="#000" stroke-width="3" stroke-linecap="round"/>
  {para}

  <g transform="translate(370,600)">
    <path d="M0,60 L70,-10 C76,-16 86,-16 92,-10 C98,-4 98,6 92,12 L22,82 L-6,90 Z"
          fill="#fff" stroke="#000" stroke-width="4" stroke-linejoin="round"/>
    <path d="M0,60 L22,82" stroke="#000" stroke-width="4" stroke-linecap="round"/>
    <path d="M64,-4 L84,16" stroke="#000" stroke-width="3" stroke-linecap="round"/>
    <path d="M-6,90 L-16,104 L-2,96 Z" fill="#000"/>
  </g>
  {use("ic-star", 150, 630, 24, 24)}
  {use("ic-star", 660, 600, 20, 20)}
  {use("ch-pumpkin-plain", 640, 660, 80, 80)}
  {use("ch-ghost", 120, 655, 78, 86)}
'''
    return build_page("A Note for Grown-Ups", None, content, page_num=3, skip_title=True)


if __name__ == "__main__":
    with open(os.path.join(OUT, "page-02-belongs-to.svg"), "w") as f:
        f.write(page_02())
    with open(os.path.join(OUT, "page-03-parent-note.svg"), "w") as f:
        f.write(page_03())
    print("wrote pages 2-3")
