"""Common page frame: double-line border, title, instructions, page number.

Canvas is 850x850 units = 8.5in x 8.5in at 100 units/inch.
"""
from symbols import DEFS

W = H = 850
MARGIN_OUTER = 40
MARGIN_INNER = 57
LIVE_X0, LIVE_X1 = 90, 760
CONTENT_TOP = 195
CONTENT_BOTTOM = 780


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def frame_and_chrome(extra_defs=""):
    return f'''<rect x="0" y="0" width="{W}" height="{H}" fill="#fff"/>
  <rect x="{MARGIN_OUTER}" y="{MARGIN_OUTER}" width="{W-2*MARGIN_OUTER}" height="{H-2*MARGIN_OUTER}" rx="34" ry="34"
        fill="none" stroke="#000" stroke-width="5"/>
  <rect x="{MARGIN_INNER}" y="{MARGIN_INNER}" width="{W-2*MARGIN_INNER}" height="{H-2*MARGIN_INNER}" rx="24" ry="24"
        fill="none" stroke="#000" stroke-width="2"/>'''


def title_block(title, instructions=None, title_size=46, instr_size=19, title_y=110, instr_y=None):
    parts = [f'<text x="425" y="{title_y}" text-anchor="middle" font-family="Fredoka" font-weight="700" '
             f'font-size="{title_size}" fill="#000">{esc(title)}</text>']
    if instructions:
        lines = instructions if isinstance(instructions, list) else [instructions]
        y = instr_y if instr_y else title_y + 38
        for i, line in enumerate(lines):
            parts.append(f'<text x="425" y="{y + i*24}" text-anchor="middle" font-family="Poppins" '
                         f'font-weight="400" font-size="{instr_size}" fill="#222">{esc(line)}</text>')
    return "\n  ".join(parts)


def wrap_words(text, max_width_units, font_size, char_w_factor=0.52):
    max_chars = max(4, int(max_width_units / (font_size * char_w_factor)))
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if len(trial) > max_chars and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    if cur:
        lines.append(cur)
    return lines


def paragraph_svg(text, x, y, max_width, font_size=20, line_h=30, weight=400, color="#222",
                   anchor="middle", font_family="Poppins"):
    lines = wrap_words(text, max_width, font_size)
    parts = []
    for i, line in enumerate(lines):
        parts.append(f'<text x="{x}" y="{y + i*line_h}" text-anchor="{anchor}" font-family="{font_family}" '
                     f'font-weight="{weight}" font-size="{font_size}" fill="{color}">{esc(line)}</text>')
    return "\n  ".join(parts), len(lines) * line_h


def page_number(n):
    return (f'<circle cx="425" cy="811" r="15" fill="none" stroke="#000" stroke-width="2"/>'
            f'<text x="425" y="817" text-anchor="middle" font-family="Poppins" font-weight="600" '
            f'font-size="16" fill="#000">{n}</text>')


def build_page(title, instructions, content_svg, page_num=None, title_size=46, instr_size=19,
               title_y=110, instr_y=None, extra_defs="", doc_title="", skip_title=False):
    chrome = frame_and_chrome()
    tb = "" if skip_title else title_block(title, instructions, title_size, instr_size, title_y, instr_y)
    pn = page_number(page_num) if page_num else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
  <title>{esc(doc_title or title)}</title>
  <defs>{DEFS}{extra_defs}</defs>
  {chrome}
  {tb}
  {content_svg}
  {pn}
</svg>
'''
