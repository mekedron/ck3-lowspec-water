"""Rebuilds thumbnail.png (Workshop preview) and steam-workshop/thumbnail-200px.png (a
legibility check at Steam's listing size, not uploaded). Layout lives in thumbnail_layout.py.

BEFORE is the flat vanilla low spec ocean: a colour map with no waves, no highlight and no
reflection anywhere on the map, so a crop of open sea (before-flat-water.png) stands in for
the same spot. AFTER is the North Sea with the sun highlight, this mod on. Both windows
are open water only; the AFTER window is zoomed on the highlight, where the difference is
largest, and the labels sit at the bottom of each half to keep it clear."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from thumbnail_layout import make

OLD = os.path.join(os.path.dirname(__file__), "before-flat-water.png")   # flat low spec water, a 420x389 crop of open sea
NEW = "/home/nikita/Pictures/Screenshots/Screenshot_20260913_010758.png"   # waves + highlight (North Sea)
CROP_OLD = (0, 110, 420, 281)   # 2.46:1 band from the middle of that crop
CROP_NEW = (1200, 0, 2240, 423)
OUT = os.path.join(os.path.dirname(__file__), "..", "thumbnail.png")
make(OUT, "BETTER WATER", OLD, NEW, CROP_OLD, CROP_NEW)
