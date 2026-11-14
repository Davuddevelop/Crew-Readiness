"""
Rebuilds the two landing-page images from their public sources. Nothing here runs in the app.

  app/static/img/hand-human.webp      <- Adam's forearm and hand, Michelangelo, The Creation of Adam (public domain)
  app/static/img/hand-astronaut.webp  <- a spacesuit glove, NASA imagery (two sources supported, see --glove-kind)

Sources are NOT committed (several MB each). URLs, licences and SHA-1 checksums: docs/ASSETS.md.

  python -m venv .assets-venv && .assets-venv/bin/pip install -r scripts/assets/requirements.txt
  .assets-venv/bin/python scripts/assets/make_landing_images.py \\
      --glove PIA26430~orig.jpg --adam "Michelangelo - Creation of Adam (cropped).jpg" \\
      --adam-crop 240,245,600,365 --out app/static/img [--debug DIR] [--glove-kind pia26430|man-and-machine]

--glove-kind pia26430 (default): NASA/JPL-Caltech PIA26430, points right in the source and is mirrored.
--glove-kind man-and-machine: the right-hand glove of NASA's 2012 "Man and Machine" photo (Robonaut 2 and a spacesuit
glove). It already points left, so it is not mirrored. The source is small (1200 x 600), so it is output at 1140 px.

--adam-crop is a box in the coordinates of a 1500px-wide overview of the fresco file. The default only fits
that exact file (3524 x 1599, SHA-1 in docs/ASSETS.md). A different reproduction frames Adam differently:
view an overview of it, re-measure the box, and re-check ADAM_POLY against the result with --debug.

HOW THE CUT-OUT WORKS. A person draws a COARSE outline (the polygons below, in the coordinates of a 1500px-wide
view of the crop). GrabCut then decides the true edge inside a narrow band around it. The polygons are the only
manual input; everything else is deterministic. Each image is padded so its leading fingertip sits on the vertical
centre line at its inner edge, which lets the page place the hands and the gap with plain CSS.
"""
import argparse, os
import cv2
import numpy as np
from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None
VIEW_W = 1500.0

# Coarse outlines, read off a 1500px-wide view of each crop. (x, y)
GLOVE_POLY = [(330,55),(520,100),(650,122),(710,172),(900,205),(1100,252),(1300,282),(1385,315),(1398,365),(1375,408),(1300,432),
              (1345,455),(1415,500),(1415,555),(1375,590),(1300,585),(1280,610),(1300,640),(1312,690),(1270,740),(1210,745),
              (1160,760),(1150,800),(1110,825),(1060,815),(1000,790),(900,730),(800,690),(700,655),(560,715),(420,745),(330,748)]
ADAM_POLY = [(560,240),(640,215),(760,200),(860,180),(930,140),(980,118),(1050,112),(1130,128),(1200,150),(1250,175),(1300,205),
             (1345,250),(1362,282),(1345,296),(1320,326),(1295,342),(1262,338),(1236,326),(1212,338),(1186,346),(1170,322),
             (1130,288),(1085,266),(1052,238),(1010,236),(950,300),(870,355),(790,400),(700,440),(640,456),(560,464)]
GLOVE_CROP_VIEW = (480, 270, 1300, 740)      # region of the 1500px overview of the NASA original

# "Man and Machine" glove: crop box in a 1500px-wide view of the 1200x600 source; outline in a 1500px-wide view of that crop
MM_CROP_VIEW = (760, 120, 1500, 600)
_MM_PX = [(52,570),(60,530),(110,490),(155,480),(250,462),(340,430),(430,385),(480,325),(520,290),(580,268),(650,238),
          (730,222),(765,240),(830,205),(950,150),(1050,110),(1150,95),(1250,80),(1340,55),(1400,70),(1480,80),
          (1480,700),(1380,740),(1280,765),(1190,815),(1150,820),(1130,785),(1050,742),(950,730),(840,668),(760,672),
          (700,690),(692,830),(680,872),(650,886),(620,880),(610,910),(580,926),(540,916),(490,880),(482,820),(476,720),
          (470,760),(466,850),(440,900),(400,916),(360,900),(335,860),(322,780),(322,700),(330,640),(335,592),(290,592),
          (250,616),(180,626),(110,620),(60,600)]
MM_POLY = [(x * 1500 / 1480, y * 1500 / 1480) for x, y in _MM_PX]    # the outline was read off a 1480px-wide render
MM_W = 1140

ADAM_W, GLOVE_W = 1500, 1260                 # output pixel widths (about 2x the CSS widths)
FADE = 0.10                                  # outer 10% of the width fades out (transparency only)


def crop_view(im, box):
    k = im.size[0] / VIEW_W
    return im.crop(tuple(round(v * k) for v in box))


def kern(r):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


def cut(pil_rgb, poly, band_frac, work_w=1800.0, keep_holes_below=0.02):
    """Return a float32 alpha (0..255) at the crop's full resolution."""
    img = cv2.cvtColor(np.asarray(pil_rgb.convert("RGB")), cv2.COLOR_RGB2BGR)
    h0, w0 = img.shape[:2]
    work = min(1.0, work_w / w0)
    small = cv2.resize(img, None, fx=work, fy=work, interpolation=cv2.INTER_AREA)
    h, w = small.shape[:2]
    k = w / VIEW_W
    pts = np.array([(x * k, y * k) for x, y in poly], np.int32)
    P = np.zeros((h, w), np.uint8); cv2.fillPoly(P, [pts], 255)
    r = max(3, int(band_frac * w))
    core, outer = cv2.erode(P, kern(r)), cv2.dilate(P, kern(r))
    mask = np.full((h, w), cv2.GC_BGD, np.uint8)
    mask[outer > 0] = cv2.GC_PR_BGD
    mask[P > 0] = cv2.GC_PR_FGD
    mask[core > 0] = cv2.GC_FGD
    cv2.grabCut(small, mask, None, np.zeros((1, 65)), np.zeros((1, 65)), 8, cv2.GC_INIT_WITH_MASK)
    fg = np.where((mask == cv2.GC_FGD) | (mask == cv2.GC_PR_FGD), 255, 0).astype(np.uint8)
    fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, kern(3)); fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, kern(4))
    n, lab, st, _ = cv2.connectedComponentsWithStats(fg)
    fg = np.where(lab == 1 + np.argmax(st[1:, cv2.CC_STAT_AREA]), 255, 0).astype(np.uint8)
    inv = cv2.bitwise_not(fg); n2, lab2, st2, _ = cv2.connectedComponentsWithStats(inv)
    for i in range(1, n2):                      # fill small interior holes, never the gaps between fingers
        x, y, ww, hh, a = st2[i]
        if x > 0 and y > 0 and x + ww < w and y + hh < h and a < keep_holes_below * w * h:
            fg[lab2 == i] = 255
    alpha = cv2.resize(fg, (w0, h0), interpolation=cv2.INTER_LINEAR)
    alpha = cv2.GaussianBlur(alpha, (0, 0), max(1.0, w0 / 1500.0))
    alpha = np.clip((alpha.astype(np.float32) - 128) * 3.0 + 128, 0, 255)
    return cv2.erode(alpha.astype(np.uint8), kern(1))


def to_rgba_gray(pil_rgb, alpha, black=0.0, gain=1.0):
    rgb = np.asarray(pil_rgb.convert("RGB")).astype(np.float32)
    g = np.clip((0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2] - black) * gain, 0, 255)
    return Image.fromarray(np.dstack([g, g, g, alpha.astype(np.float32)]).astype(np.uint8), "RGBA")


def grade(im, gamma, gain):
    a = np.asarray(im.convert("RGBA")).astype(np.float32)
    g = np.clip(((a[..., 0] / 255.0) ** gamma) * 255.0 * gain, 0, 255)
    a[..., 0] = a[..., 1] = a[..., 2] = g
    return Image.fromarray(a.astype(np.uint8), "RGBA")


def fade_outer(im, side):
    a = np.asarray(im).copy(); w = a.shape[1]; n = max(2, int(w * FADE))
    ramp = np.linspace(0, 1, n, dtype=np.float32)
    if side == "left":
        a[:, :n, 3] = (a[:, :n, 3] * ramp).astype(np.uint8)
    else:
        a[:, w - n:, 3] = (a[:, w - n:, 3] * ramp[::-1]).astype(np.uint8)
    return Image.fromarray(a, "RGBA")


def tip(im, side):
    al = np.asarray(im)[..., 3] > 40
    cols = np.where(al.any(axis=0))[0]
    x = cols.max() if side == "right" else cols.min()
    span = range(x - 5, x + 1) if side == "right" else range(x, x + 6)
    ys = np.concatenate([np.where(al[:, c])[0] for c in span if 0 <= c < al.shape[1]])
    return int(x), int(ys.mean())


def centre_tip(im, side):
    im = im.crop(im.getchannel("A").point(lambda v: 255 if v > 10 else 0).getbbox())
    _, y = tip(im, side)
    half = max(y, im.height - y) + 8
    canvas = Image.new("RGBA", (im.width, 2 * half), (0, 0, 0, 0))
    canvas.alpha_composite(im, (0, half - y))
    return canvas


def trim(im):
    return im.crop(im.getchannel("A").point(lambda v: 255 if v > 10 else 0).getbbox())


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--glove", required=True, help="NASA PIA26430~orig.jpg")
    ap.add_argument("--adam", required=True, help="fresco reproduction (see docs/ASSETS.md)")
    ap.add_argument("--adam-crop", default="240,245,600,365", help="x0,y0,x1,y1 of Adam's arm in a 1500px-wide overview of --adam")
    ap.add_argument("--glove-kind", choices=("pia26430", "man-and-machine"), default="pia26430")
    ap.add_argument("--out", required=True)
    ap.add_argument("--debug", help="write cut-out previews here")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    if a.debug: os.makedirs(a.debug, exist_ok=True)

    # --- astronaut glove (points right in the source; mirrored later) ---
    mm = a.glove_kind == "man-and-machine"
    g_src = crop_view(Image.open(a.glove).convert("RGB"), MM_CROP_VIEW if mm else GLOVE_CROP_VIEW)
    g_alpha = cut(g_src, MM_POLY if mm else GLOVE_POLY, band_frac=0.016)
    glove = trim(to_rgba_gray(g_src, g_alpha, black=18, gain=1.08))
    # --- Adam's hand (points right) ---
    box = tuple(float(v) for v in a.adam_crop.split(","))
    h_src = crop_view(Image.open(a.adam).convert("RGB"), box)
    h_alpha = cut(h_src, ADAM_POLY, band_frac=0.012)
    human = trim(to_rgba_gray(h_src, h_alpha))
    if a.debug:
        for name, im in (("glove", glove), ("adam", human)):
            for bg_name, bg in (("black", (0, 0, 0)), ("gray", (70, 70, 74))):
                base = Image.new("RGBA", im.size, bg + (255,)); base.alpha_composite(im)
                base.convert("RGB").resize((1500, round(1500 * im.height / im.width))).save(f"{a.debug}/{name}-{bg_name}.jpg", quality=92)

    human = fade_outer(centre_tip(grade(human, 1.35, 1.12), "right"), "left")
    human = human.resize((ADAM_W, round(human.height * ADAM_W / human.width)), Image.LANCZOS)
    graded = grade(glove, 1.18, 1.0)
    glove = fade_outer(centre_tip(graded if mm else ImageOps.mirror(graded), "left"), "right")
    gw = MM_W if mm else GLOVE_W
    glove = glove.resize((gw, round(glove.height * gw / glove.width)), Image.LANCZOS)
    for name, im in (("hand-human", human), ("hand-astronaut", glove)):
        im.save(os.path.join(a.out, f"{name}.webp"), "WEBP", quality=84, method=6)
        print(f"{name}.webp  {im.width}x{im.height}")


if __name__ == "__main__":
    main()
