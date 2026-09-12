"""Rebuilds thumbnail.png (Workshop preview) and thumbnail-200px.png (a legibility check
at Steam's listing size, not uploaded). Layout lives in thumbnail_layout.py.

The BEFORE half must be the same spot with the mod off (flat vanilla low spec water);
the crop is chosen around the sun highlight, where the difference is largest."""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from thumbnail_layout import make

OLD = "/home/nikita/Pictures/Screenshots/BEFORE_flat_water.png"            # TODO: same spot, mod off
NEW = "/home/nikita/Pictures/Screenshots/Screenshot_20260913_010758.png"   # waves + highlight, this mod
CROP_OLD = (250, 0, 2370, 853)
CROP_NEW = (250, 0, 2370, 853)   # the North Sea west of Denmark, sun highlight top centre
OUT = os.path.join(os.path.dirname(__file__), "..", "thumbnail.png")
if not os.path.exists(OLD):
    OLD = NEW                     # provisional: both halves from the AFTER shot
make(OUT, "BETTER WATER", OLD, NEW, CROP_OLD, CROP_NEW)
