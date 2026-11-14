"""
Prepares the brand images from the team's logo. Nothing here runs in the app.

  app/static/img/logo.webp    <- the logo cropped to its drawing, background made transparent (lossless)
  app/static/img/favicon.png  <- 64 x 64 for the browser tab

The source is an AI-generated 1024 x 550 raster supplied by the team lead (see docs/ASSETS.md). Its background is almost,
but not exactly, our page colour, so it is keyed to transparent rather than left as a faintly different rectangle.

  .assets-venv/bin/python scripts/assets/make_brand_assets.py --logo logo-source.png --out app/static/img
"""
import argparse
import os

import numpy as np
from PIL import Image

KEY_LOW, KEY_SPAN = 6, 14      # background-distance below KEY_LOW is fully transparent; opaque by KEY_LOW + KEY_SPAN


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
    rgba = np.dstack([rgb, (alpha * 255)]).astype(np.uint8)[y0:y1, x0:x1]
    logo = Image.fromarray(rgba, "RGBA")
    logo.save(os.path.join(a.out, "logo.webp"), "WEBP", lossless=True, method=6)
    print(f"logo.webp  {logo.width}x{logo.height}")

    side = max(logo.size)
    sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    sq.alpha_composite(logo, ((side - logo.width) // 2, (side - logo.height) // 2))
    fav = sq.resize((64, 64), Image.LANCZOS)
    fav.save(os.path.join(a.out, "favicon.png"), optimize=True)
    print("favicon.png  64x64")


if __name__ == "__main__":
    main()
