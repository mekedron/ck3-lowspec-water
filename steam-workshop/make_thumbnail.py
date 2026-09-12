"""Rebuilds thumbnail.png. Currently a single AFTER frame; for a BEFORE/AFTER pair take a
second screenshot of the same spot with the mod disabled and adapt the Sharp Terrain
generator (two halves, two badges)."""
from PIL import Image, ImageDraw, ImageFont
SRC = "/home/nikita/Pictures/Screenshots/Screenshot_20260913_010758.png"
OUT = "/home/nikita/Projects/ck3-lowspec-water/thumbnail.png"
S = 1024
im = Image.open(SRC).convert("RGB").crop((1300, 120, 2620, 1440)).resize((S, S), Image.LANCZOS)
d = ImageDraw.Draw(im, "RGBA")
big = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 62)
small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
title, sub = "BETTER WATER", "Advanced Shaders off, 6 taps per pixel"
w = int(max(d.textlength(title, font=big), d.textlength(sub, font=small))) + 52
h = 18 * 2 + 62 + 10 + 34
d.rectangle([28, 30, 28 + w, 30 + h], fill=(12, 10, 8, 205))
d.text((54, 48), title, font=big, fill=(245, 238, 225, 255))
d.text((54, 118), sub, font=small, fill=(198, 176, 132, 255))
clean = Image.new("RGB", im.size); clean.putdata(list(im.getdata()))
clean = clean.quantize(colors=256, method=Image.MEDIANCUT, dither=Image.FLOYDSTEINBERG)
clean.save(OUT, "PNG", optimize=True)
