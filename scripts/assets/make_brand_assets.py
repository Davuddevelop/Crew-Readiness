"""
Prepares the brand images from the team's logo. Nothing here runs in the app.

  app/static/img/logo.webp       <- the logo cropped to its drawing, background transparent, recoloured to our palette
  app/static/img/logo-mark.webp  <- small version for the nav: bolder strokes so it survives at about 28 px
  app/static/img/favicon.png     <- 64 x 64 for the browser tab

The source is an AI-generated 1024 x 550 raster supplied by the team lead (see docs/ASSETS.md). Its background is almost,
but not exactly, our page colour, so it is keyed to transparent rather than left as a faintly different rectangle.

  .assets-venv/bin/python scripts/assets/make_brand_assets.py --logo logo-source.png --out app/static/img
"""
import argparse
import os

import cv2
import numpy as np
from PIL import Image

KEY_LOW, KEY_SPAN = 6, 14      # background-distance below KEY_LOW is fully transparent; opaque by KEY_LOW + KEY_SPAN
# Our palette (app/static/css/style.css :root): the disc becomes --line, the strokes become --ink.
DISC, INK = np.array([0x2A, 0x2A, 0x2E], np.float32), np.array([0xF8, 0xFA, 0xFC], np.float32)
SRC_DISC_LUM, SRC_INK_LUM = 43.0, 235.0
MARK_H, MARK_BOLD = 56, 3     # nav mark height in pixels (2x of 28 CSS px); stroke thickening in source pixels


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--logo", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    rgb = np.asarray(Image.open(a.logo).convert("RGB")).astype(np.int16)
    bg = rgb[5, 5]
    dist = np.abs(rgb - bg).sum(axis=2)
    box = np.where(dist > 40)
    x0, x1, y0, y1 = box[1].min(), box[1].max() + 1, box[0].min(), box[0].max() + 1
    alpha = np.clip((dist - KEY_LOW) / KEY_SPAN, 0, 1)
    lum = rgb.mean(axis=2)
    t = np.clip((lum - SRC_DISC_LUM) / (SRC_INK_LUM - SRC_DISC_LUM), 0, 1)[..., None]
    col = DISC * (1 - t) + INK * t                                   # recolour: disc -> --line, strokes -> --ink
    rgba = np.dstack([col, alpha * 255]).astype(np.uint8)[y0:y1, x0:x1]
    logo = Image.fromarray(rgba, "RGBA")
    logo.save(os.path.join(a.out, "logo.webp"), "WEBP", lossless=True, method=6)
    print(f"logo.webp  {logo.width}x{logo.height}")

    # nav mark: thicken the strokes, then shrink
    tt = (t[..., 0] > 0.5).astype(np.uint8)[y0:y1, x0:x1] * 255
    thick = cv2.dilate(tt, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * MARK_BOLD + 1,) * 2))
    base = np.asarray(logo).astype(np.float32)
    w = (cv2.GaussianBlur(thick, (0, 0), 1.0).astype(np.float32) / 255.0)[..., None]
    bold = base.copy()
    bold[..., :3] = base[..., :3] * (1 - w) + INK * w
    bold[..., 3] = np.maximum(base[..., 3], w[..., 0] * 255)
    mark = Image.fromarray(bold.astype(np.uint8), "RGBA")
    mark = mark.resize((round(mark.width * MARK_H / mark.height), MARK_H), Image.LANCZOS)
    mark.save(os.path.join(a.out, "logo-mark.webp"), "WEBP", lossless=True, method=6)
    print(f"logo-mark.webp  {mark.width}x{mark.height}")

    side = max(logo.size)
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    sq.alpha_composite(logo, ((side - logo.width) // 2, (side - logo.height) // 2))
    fav = sq.resize((64, 64), Image.LANCZOS)
    fav.save(os.path.join(a.out, "favicon.png"), optimize=True)
    print("favicon.png  64x64")


if __name__ == "__main__":
    main()
