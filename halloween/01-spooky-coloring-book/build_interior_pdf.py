#!/usr/bin/env python3
"""Assemble the Spooky Fun interior PDF from generated art + text, entirely locally.

Canvas: 8.5" x 8.5" at 300 DPI = 2550 x 2550 px per page.
"""
import os
import textwrap
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.join(HERE, "generated-art")
OUT = os.path.join(HERE, "Spooky_Fun_Interior.pdf")

PAGE = 2550  # 8.5in @ 300dpi
MARGIN = 225  # 0.75in
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

def font(path, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, path), size)

F_TITLE_XL = font("DejaVuSans-Bold.ttf", 150)
F_TITLE_L = font("DejaVuSans-Bold.ttf", 100)
F_TITLE_M = font("DejaVuSans-Bold.ttf", 70)
F_PAGE_TITLE = font("DejaVuSans-Bold.ttf", 64)
F_BODY = font("DejaVuSans.ttf", 40)
F_BODY_BOLD = font("DejaVuSans-Bold.ttf", 40)
F_SMALL = font("DejaVuSans.ttf", 32)
F_SCRIPT = font("DejaVuSerif-Bold.ttf", 120)

BLACK = (20, 20, 20)
GRAY = (90, 90, 90)

# manuscript titles for coloring pages 4-43
TITLES = {
    4: "Boo!", 5: "Smiley Pumpkin", 6: "Witch in the Sky", 7: "Black Cat",
    8: "Haunted House on the Hill", 9: "Roar! Trick-or-Treat!", 10: "Candy Corn Trio",
    11: "Upside-Down Bat", 12: "Itsy Bitsy Spider", 13: "Night Owl",
    14: "Scarecrow's Pumpkin Patch", 15: "Ghost Family Trick-or-Treating",
    16: "Pick a Pumpkin", 17: "Bubble, Bubble", 18: "Knock, Knock!",
    19: "Bat Family Flying Home", 20: "Web Between the Pumpkins",
    21: "Jack-o-Lantern Porch", 22: "Little Ghost Says Hi", 23: "Full Candy Bucket",
    24: "Witch's Hat and Broom", 25: "Friendly Mummy", 26: "Silly Vampire Bat",
    27: "Pumpkin Parade", 28: "Wise Old Owl", 29: "Bobbing for Apples",
    30: "Cat on a Pumpkin", 31: "Peek-a-Boo Ghost", 32: "Scarecrow in the Wind",
    33: "Brave Little Lion", 34: "Spooky Tree", 35: "Witch and the Castle",
    36: "Party Pumpkin", 37: "Moonlight Parade", 38: "Spider with a Bow",
    39: "Bats Around the House", 40: "Cauldron Friends", 41: "Starry Halloween Night",
    42: "Trick-or-Treat Sign", 43: "Happy Halloween!",
}


def new_page():
    return Image.new("RGB", (PAGE, PAGE), "white")


def draw_center_text(draw, text, y, fnt, fill=BLACK, max_width=None):
    if max_width:
        avg_char = fnt.getlength("M")
        wrap_width = max(10, int(max_width / max(avg_char * 0.55, 1)))
        lines = textwrap.wrap(text, width=wrap_width)
    else:
        lines = [text]
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=fnt)
        w = bbox[2] - bbox[0]
        draw.text(((PAGE - w) / 2, y), line, font=fnt, fill=fill)
        y += (bbox[3] - bbox[1]) + 20
    return y


def draw_page_number(draw, n):
    text = str(n)
    bbox = draw.textbbox((0, 0), text, font=F_SMALL)
    w = bbox[2] - bbox[0]
    draw.text(((PAGE - w) / 2, PAGE - MARGIN + 40), text, font=F_SMALL, fill=GRAY)


def place_art(page_img, art_path, box_size, box_top):
    art = Image.open(art_path).convert("RGB")
    aw, ah = art.size
    scale = min(box_size / aw, box_size / ah)
    nw, nh = int(aw * scale), int(ah * scale)
    art = art.resize((nw, nh), Image.LANCZOS)
    x = (PAGE - nw) // 2
    y = box_top + (box_size - nh) // 2
    page_img.paste(art, (x, y))


def rounded_border(draw, inset, radius=60, width=6, color=(60, 60, 60)):
    draw.rounded_rectangle(
        [inset, inset, PAGE - inset, PAGE - inset], radius=radius, outline=color, width=width
    )


def small_icon(page_img, src_path, box, center_xy, rotate=0):
    icon = Image.open(src_path).convert("RGBA")
    icon.thumbnail((box, box), Image.LANCZOS)
    if rotate:
        icon = icon.rotate(rotate, expand=True)
    x = center_xy[0] - icon.width // 2
    y = center_xy[1] - icon.height // 2
    page_img.paste(icon, (x, y), icon)


def page_title_page():
    img = new_page()
    d = ImageDraw.Draw(img)
    rounded_border(d, 90, radius=80, width=8, color=(40, 40, 40))
    y = draw_center_text(d, "Spooky Fun", 420, F_TITLE_XL)
    y = draw_center_text(d, "My First Halloween Coloring Book", y + 40, F_TITLE_M)

    icons = [
        (os.path.join(ART, "page-04.png"), -700),
        (os.path.join(ART, "page-05.png"), -230),
        (os.path.join(ART, "page-11.png"), 230),
        (os.path.join(ART, "page-07.png"), 700),
    ]
    cy = 1750
    for src, dx in icons:
        small_icon(img, src, 420, (PAGE // 2 + dx, cy))
    return img


def page_belongs_to():
    img = new_page()
    d = ImageDraw.Draw(img)
    rounded_border(d, 90)
    small_icon(img, os.path.join(ART, "page-05.png"), 260, (300, 300))
    small_icon(img, os.path.join(ART, "page-05.png"), 260, (PAGE - 300, 300))
    small_icon(img, os.path.join(ART, "page-05.png"), 260, (300, PAGE - 300))
    small_icon(img, os.path.join(ART, "page-05.png"), 260, (PAGE - 300, PAGE - 300))

    y = draw_center_text(d, "This Book", 560, F_TITLE_L)
    y = draw_center_text(d, "Belongs To:", y + 10, F_TITLE_L)
    y += 100
    line_w = 1400
    x0 = (PAGE - line_w) // 2
    d.line([(x0, y), (x0 + line_w, y)], fill=BLACK, width=5)
    y += 160
    y = draw_center_text(d, "My favorite Halloween costume is:", y, F_BODY_BOLD)
    y += 100
    d.line([(x0, y), (x0 + line_w, y)], fill=BLACK, width=5)
    return img


def page_parent_note():
    img = new_page()
    d = ImageDraw.Draw(img)
    small_icon(img, os.path.join(ART, "page-10.png"), 300, (PAGE - 320, 320))
    y = draw_center_text(d, "A Note for Grown-Ups", 300, F_TITLE_M)
    y += 100
    note = (
        "Welcome to Spooky Fun! Inside you'll find 40 friendly Halloween "
        "pictures for your child to color — ghosts, pumpkins, witches, "
        "black cats, and more. There is no wrong way to color. Let your "
        "child pick any colors they like, color outside the lines, or "
        "skip around the book. Grab your crayons, markers, or colored "
        "pencils, and have a happy (not scary) Halloween!"
    )
    draw_center_text(d, note, y, F_BODY, max_width=1900)
    return img


TITLE_BAKED_IN = {42, 43}  # these pages already render their heading as part of the art


def coloring_page(n):
    img = new_page()
    d = ImageDraw.Draw(img)
    art_path = os.path.join(ART, f"page-{n:02d}.png")
    if n in TITLE_BAKED_IN:
        box_top = 130
        box_size = PAGE - box_top - MARGIN - 60
    else:
        title = TITLES[n]
        bbox = d.textbbox((0, 0), title, font=F_PAGE_TITLE)
        w = bbox[2] - bbox[0]
        d.text(((PAGE - w) / 2, 130), title, font=F_PAGE_TITLE, fill=BLACK)
        box_top = 320
        box_size = PAGE - box_top - MARGIN - 60
    place_art(img, art_path, box_size, box_top)
    draw_page_number(d, n)
    return img


def page_certificate():
    border = Image.open(os.path.join(ART, "page-44.png")).convert("RGB")
    img = border.resize((PAGE, PAGE), Image.LANCZOS)
    d = ImageDraw.Draw(img)
    y = draw_center_text(d, "Great Job!", 420, F_TITLE_XL)
    y += 80
    y = draw_center_text(d, "This certifies that", y, F_BODY, )
    y += 60
    line_w = 1500
    x0 = (PAGE - line_w) // 2
    d.line([(x0, y), (x0 + line_w, y)], fill=BLACK, width=5)
    y += 100
    y = draw_center_text(
        d, "colored their way through this whole Spooky Fun book!", y, F_BODY, max_width=1900
    )
    y += 60
    draw_center_text(d, "Happy Halloween!", y, F_TITLE_M)
    return img


def main():
    pages = []
    pages.append(page_title_page())
    pages.append(page_belongs_to())
    pages.append(page_parent_note())
    for n in range(4, 44):
        pages.append(coloring_page(n))
    pages.append(page_certificate())

    assert len(pages) == 44, len(pages)
    first, rest = pages[0], pages[1:]
    first.save(OUT, save_all=True, append_images=rest, resolution=300.0)
    print("Wrote", OUT, "pages:", len(pages))


if __name__ == "__main__":
    main()
