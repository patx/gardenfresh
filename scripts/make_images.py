#!/usr/bin/env python3
"""Generate responsive webp variants for every source image.

Usage: python3 scripts/make_images.py

- Picks the largest source per base name in assets/images/ (the old -1200/-1920
  suffixed files are size-suffixed duplicates; several are byte-identical).
- Writes assets/images/r/{name}-{width}.webp for widths in WIDTHS that do not
  exceed the source width (always at least the source width itself, capped).
- Records the variant manifest in build/data/images_generated.json.
- Compresses the client logos in assets/logos/ in place if oversized.

Idempotent: skips outputs that are newer than their source.
"""

import json
import re
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "assets" / "images"
OUT = SRC / "r"
MANIFEST = ROOT / "build" / "data" / "images_generated.json"

WIDTHS = (480, 800, 1200, 1600, 1920)


def quality(width):
    # Large hero variants tolerate more compression at display density.
    return 80 if width <= 800 else 74 if width <= 1200 else 66
LOGO_MAX_H = 112  # 2x the 56px display height
SKIP = {"south-florida-produce-social-1200x630.jpeg"}  # OG image stays as-is


NO_CROP = {"usda-organic-logo"}


def sources():
    """Map base name -> largest source file for that name."""
    best = {}
    for f in sorted(SRC.iterdir()):
        if not f.is_file() or f.name in SKIP:
            continue
        base = re.sub(r"-\d+(x\d+)?$", "", f.stem)
        with Image.open(f) as im:
            w, h = im.size
        if base not in best or w > best[base][1]:
            best[base] = (f, w, h)
    return best


def crop_box(w, h, base):
    """Portrait/square sources are hero-cropped to 3:2 landscape."""
    if base in NO_CROP or h <= 0.9 * w:
        return None, w, h
    th = round(w * 2 / 3)
    top = (h - th) // 2
    return (0, top, w, top + th), w, th


def main():
    OUT.mkdir(exist_ok=True)
    manifest = {}
    made = skipped = 0
    for base, (src, sw, sh) in sorted(sources().items()):
        box, w, h = crop_box(sw, sh, base)
        widths = [x for x in WIDTHS if x <= w]
        if not widths:  # source narrower than the smallest step
            widths = [w]
        elif w < WIDTHS[-1] and w >= widths[-1] * 1.2:
            widths.append(w)  # keep the native width when it adds real detail
        manifest[base] = {"widths": widths, "w": w, "h": h}
        for tw in widths:
            dest = OUT / f"{base}-{tw}.webp"
            if dest.exists() and dest.stat().st_mtime >= src.stat().st_mtime:
                skipped += 1
                continue
            with Image.open(src) as im:
                if im.mode not in ("RGB", "RGBA"):
                    im = im.convert("RGBA")
                if im.mode == "RGBA" and base != "usda-organic-logo":
                    bg = Image.new("RGB", im.size, (255, 255, 255))
                    bg.paste(im, mask=im.split()[-1])
                    im = bg
                if box:
                    im = im.crop(box)
                th = round(tw * h / w)
                im.resize((tw, th), Image.LANCZOS).save(
                    dest, "WEBP", quality=quality(tw), method=6)
            made += 1

    MANIFEST.write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n")

    for logo in sorted((ROOT / "assets" / "logos").glob("*.png")):
        with Image.open(logo) as im:
            if im.height <= LOGO_MAX_H and logo.stat().st_size <= 25_000:
                continue
            ratio = LOGO_MAX_H / im.height
            im = im.resize((round(im.width * ratio), LOGO_MAX_H), Image.LANCZOS)
            im.save(logo, "PNG", optimize=True)
        print(f"  compressed logo {logo.name} -> {logo.stat().st_size // 1024}KB")

    total = sum(f.stat().st_size for f in OUT.iterdir()) // 1024
    print(f"variants: {made} written, {skipped} up-to-date; "
          f"{len(manifest)} images, servable total {total}KB")


if __name__ == "__main__":
    main()
