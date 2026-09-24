# KDP Books — Project Notes & Learnings

Operational learnings from producing Book 1 (Halloween "Spooky Fun" coloring book), captured so books 2-8 don't hit the same walls.

## Publisher / legal info

- **Publisher / copyright holder:** Rohith AI Labs
- Every book's interior needs a **copyright page** (right after the title page, unnumbered) with: title, `Copyright © 2026 Rohith AI Labs. All rights reserved.`, a standard reproduction-rights notice, a disclosure that illustrations were AI-generated, "Published by Rohith AI Labs. First Edition, 2026."
- **KDP also requires AI-content disclosure in the publishing dashboard itself** (separate from the in-book notice) when uploading — don't forget this at actual publish time, it's not something this repo's files can satisfy on their own.
- Decide author/publisher name **before** generating any book's copyright page — retrofitting it after art/layout is done costs a full page-numbering pass (see below).

## Interior art generation (Canva `generate-image`)

- `mcp__Canva__generate-image` reliably produces correct, on-brief line art (and colorful art) from a good prompt. Content quality has not been the bottleneck — **downloading it at usable resolution has been.**
- `mcp__Canva__get-assets` on a generated media ID only returns a **signature-locked 200x200 thumbnail**. Not usable for print. Don't bother trying to resize the URL — the signature is bound to the exact params.
- **The reliable download method:** `create-design` (format `"Poster (Square)"`, brief "blank square canvas, no text, no decoration") → poll `get-create-design-async-job` → `edit-design` with an `insert_fill` operation placing the **exact existing media ID** onto the page → commit the transaction → `get-export-formats` → `export-design` (`type: "png", lossless: true`) → curl the result.
  - This is far more reliable than asking `create-design`'s brief to "use this existing asset by ID" in prose — that's a **soft match**, and it sometimes silently substitutes unrelated art or a blank page. Always visually verify (Read tool) the downloaded PNG against the illustration brief before accepting it.
- **Canva's design-generation quota gets exceeded often and unpredictably**, independent of how much you've actually used. When it hits:
  - Don't hammer it in a tight loop or in parallel across many pages at once — that seems to make it worse.
  - Retry **sequentially, one page at a time**, with real 30-60s waits between attempts, up to ~5-6 tries per page.
  - If it's still failing after that, stop and move on — it sometimes clears itself after tens of minutes for no obvious reason. Don't burn excessive agent-turns spinning on it.
- **Background agents' self-reported failures are not fully trustworthy.** Twice in this project, an agent reported pages as failed/not-downloaded when the files actually existed on disk and were correct. Before accepting a "failed" or "mismatch" report, or before writing it off, do a quick `ls -la` / visual check yourself.
- Downloaded art comes back at **inconsistent resolutions and aspect ratios** across pages (seen: 894x1264, 1587x1587, 1587x1588, 1587x2245, 2380x2380, 3175x3174, 4760x4760). Any layout script must use a "contain, don't crop" fit (scale to max size that fits within a target box, centered) rather than assuming square input.
- This environment's network egress to `media.canva.com` may appear blocked at first — don't trust a stale "blocked" note in an old manifest. If network access was recently broadened, re-verify directly rather than assuming the old block still holds.

## Cover art

- **Do not rely on Canva for cover backgrounds/compositions.** The `create-design` design-generation pipeline is the same one hitting quota limits above, and it's overkill for what's needed.
- **What actually worked well:** ask the user to generate a single colorful illustration with an **external** image tool (they used one directly in chat), using a carefully written prompt (saturated colors, flat vector children's-book style, empty space reserved for title text, square 1:1). See `halloween/01-spooky-coloring-book/cover-art-generation-brief.md` for the exact prompt/negative-prompt/specs template — reuse this pattern (swap theme/characters) for the other 7 books.
- Composite the title, subtitle, ribbon badge, and age-range seal **locally with Pillow** on top of whatever background art comes in. This is fully reliable and gives pixel-perfect control — see `build_cover.py`.
- **Design lessons from review** (don't repeat these mistakes):
  - Showing **blank black-and-white line art** on the cover reads as "homework," not "fun" — it hurts conversion. Use colorful/saturated art on the cover even though the interior stays black-and-white.
  - Muted, atmospheric, "artsy" gradients underperform at Amazon's tiny thumbnail size. Bold, high-contrast, saturated colors read better at a glance.
  - A generic system font (DejaVu Sans Bold) looks like a placeholder, not a professional children's book. **Use `fonts-comic-neue`** (installed via `apt-get install -y fonts-comic-neue`, lives at `/usr/share/fonts/opentype/comic-neue/`) for titles and body text — it's free, rounded, kid-friendly, and Google Fonts downloads are blocked in this environment so don't bother trying to fetch a webfont.
  - When compositing line-art characters over a colored background, their **transparent interiors let the background bleed straight through**, which can make them nearly invisible against a same-hued background. Either put them on a contrasting backdrop shape, or (better, as it turned out) just use full-color art for anything shown at cover scale.

## PDF assembly

- Build the full interior PDF **locally with Pillow**, not through Canva. `PIL.Image.save(path, save_all=True, append_images=[...], resolution=300.0)` produces a clean multi-page PDF directly from a list of page images — no external dependency, no quota risk, fully deterministic.
- Canvas: 8.5"x8.5" square trim = 2550x2550px @ 300 DPI per page (adjust if a future book uses a different trim size).
- No PDF-preview tool (`pdftoppm`/`poppler`) is installed in this environment — to spot-check pages, call the page-building functions directly in a Python one-liner and save individual PNGs, then view with the Read tool.
- **When inserting a new front-matter page after art/pages already exist** (e.g. adding the copyright page after coloring-page art was already generated and named `page-04.png`...`page-43.png`): don't rename 40 art files. Instead keep the art filenames as the "content" index and add a fixed offset to the **printed** page number so it matches the new physical position in the PDF. Document the offset clearly in `manuscript.md` so it's not confusing later.

## Process / repo conventions

- This repo has a `main` branch (kept as a clean base) and per-feature work happens on `claude/dazzling-edison-4eoys9`; merge in when asked.
- A stop-hook requires committing/pushing whenever there are uncommitted changes — commit incrementally as background agents' work lands (per-batch commits are fine and expected), rather than trying to batch everything into one big commit at the end.
- When running multiple background agents in parallel over adjacent page ranges (e.g. pages 4-23 vs 24-33), expect some file churn/flicker (a page briefly "deleted" while an agent retries it) — don't panic-commit mid-flicker; check `ls` for a stable state first.
- Per-book folder structure: `manuscript.md`, `illustration-briefs.md`, `kdp-metadata.md`, `generated-art/` (raw downloaded art + manifest), `external-art/` (user-supplied cover background), `build_interior_pdf.py`, `build_cover.py`, `Spooky_Fun_Interior.pdf`, `Spooky_Fun_Cover_Front.png`. Reuse this same structure and these same two build scripts (parameterized per book) for books 2-8 rather than reinventing the layout approach each time.
