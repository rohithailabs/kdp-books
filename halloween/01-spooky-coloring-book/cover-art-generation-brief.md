# Spooky Fun — External Cover Art Generation Brief

Use this with an external AI image generator (Midjourney, DALL-E, Ideogram, Leonardo, etc.) to produce a colorful, professional-looking cover illustration. This replaces the local line-art cover background with real color art, which is the single biggest lever for making the cover convert on Amazon.

## Prompt

```
Children's book cover illustration, Halloween theme, vibrant flat
vector art style like a bestselling kids' coloring book cover.
A cheerful group of Halloween characters in the foreground: a round
smiling ghost, a grinning jack-o-lantern, a fluffy black cat with a
bow, and a small bat — all rendered in bright saturated candy colors
(orange, purple, teal, cream), thick clean black outlines, big
friendly cartoon eyes, no scary or dark elements. Simple whimsical
background: a purple-to-orange gradient night sky, a smiling
crescent moon, a few stars, gentle rolling hills. Bold, punchy,
high-contrast composition that reads clearly as a small thumbnail.
Empty open space in the upper third of the image for large title
text to be added later. Square 1:1 composition, centered, flat
digital illustration, vector art, children's picture book style,
NOT photorealistic, no text, no watermark, no signature.
```

## Negative prompt (if the tool supports one)

```
photorealistic, scary, dark, muted colors, gore, blood, weapons,
realistic proportions, text, watermark, signature, cluttered
background, low contrast, sepia, grayscale, extra limbs, deformed
hands, blurry, low quality, jpeg artifacts
```

## Specs

| Setting | Value |
|---|---|
| Aspect ratio | 1:1 (square) |
| Target resolution | 2550 x 2550 px minimum (8.5" x 8.5" @ 300 DPI — KDP's front cover trim size) |
| Style keywords to try | "flat vector illustration", "children's book illustration", "Canva coloring book cover style", "2D flat design", "kawaii cute style" |
| Color mood | Saturated, candy-bright — orange, purple, teal/cream accents. Avoid anything muted, sepia, or photoreal. |
| Composition | Characters centered/lower two-thirds; keep the upper third visually clear (sky/background only) so title text can be overlaid without collision |
| Format to save | PNG, no background compression artifacts |

## What to do with the result

1. Generate at the highest resolution the tool allows (most cap well below 2550px — that's fine, upscale afterward with the tool's own upscaler or Real-ESRGAN/similar).
2. Send the raw PNG back here.
3. I'll composite the title ("Spooky Fun"), subtitle, ribbon badge, and age seal on top locally (already have a working script for this), so you don't need the generator to render any text.

## Why this matters (context from the design review)

The current locally-built cover is technically clean but shows blank black-and-white line art and uses a generic system font — both likely to underperform at Amazon's small thumbnail size against competitors that show *colored* sample art in a bold, saturated, characterful style. Swapping in real color art here is the highest-leverage single fix.
