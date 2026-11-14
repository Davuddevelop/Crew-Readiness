/**
 * Two hands reaching toward each other, drawn as stacked contour lines.
 *
 * A person's hand (left) and an astronaut's gloved hand (right) almost touch. The gap is the
 * point: in this product the system never decides, a human closes the gap.
 *
 * HOW IT IS MADE (no photographs, no AI imagery, no assets: all of it is code)
 *   1. A hand is a skeleton: a palm ellipse plus finger chains (joint angles, tapering radii).
 *      The glove is the same skeleton with fatter radii, puffed joints and a cuff.
 *   2. The skeleton is rasterised to a low-resolution mask, blurred into a smooth height field
 *      (a dome: high in the middle of a finger, low at its edge).
 *   3. Horizontal lines are drawn only where the mask is, displaced upward by the height field,
 *      top to bottom, each one erasing what it hides: the same stacked-line technique as the
 *      dashboard's session art, and the pulsar plots it descends from (docs/DESIGN.md).
 *
 * The art is drawn once per size (not per frame), so it costs nothing while the page is idle.
 * Motion is CSS only (the hands approach on load) and is off under prefers-reduced-motion.
 *
 * Tune a pose by editing the numbers in HUMAN / GLOVE below and reloading. Units are "hand
 * pixels"; the whole hand scales to fit its canvas.
 */
import { tokens } from "./tokens.js";

// ---------- skeletons (wrist at the origin, hand pointing right, y grows downward) ----------
const HUMAN = {
  wrist: { x0: -80, x1: 40, y0: -32, y1: 32 },
  palm: { cx: 115, cy: 0, rx: 102, ry: 60 },
  fingers: [
    { base: [190, -42], len: [84, 52, 38], ang: [-0.05, -0.03, -0.02], r: [17, 11] },   // index, extended
    { base: [198, -14], len: [92, 58, 40], ang: [0.12, 0.42, 0.45], r: [18, 11.5] },    // middle, relaxed
    { base: [194, 14], len: [84, 54, 38], ang: [0.22, 0.55, 0.55], r: [17, 11] },       // ring
    { base: [182, 40], len: [64, 42, 30], ang: [0.32, 0.62, 0.6], r: [14, 9.5] },       // little
  ],
  thumb: { base: [66, 44], len: [66, 52], ang: [0.95, -0.45], r: [21, 13] },
  ink: { alpha: 0.7, width: 1.1, ring: 0 },
  detail: {                                          // interior anatomy: raised in the relief, not in the outline
    knuckles: [[182, -42, 14], [190, -14, 15], [186, 14, 14], [174, 40, 12]],   // [x, y, radius]
    tendons: [[182, -42], [190, -14], [186, 14], [174, 40]],                     // run from each knuckle toward the wrist
    pads: [[104, 46, 44, 26]],                                                   // thumb base: [x, y, rx, ry]
  },
};

const GLOVE = {
  wrist: { x0: -120, x1: 60, y0: -54, y1: 54 },
  cuffs: [{ x0: 4, x1: 40, y0: -92, y1: 92 }, { x0: 48, x1: 58, y0: -76, y1: 76 }],   // the metal wrist ring
  palm: { cx: 112, cy: 0, rx: 106, ry: 70 },
  fingers: [
    { base: [192, -44], len: [80, 50, 36], ang: [-0.02, -0.02, 0.0], r: [24, 18] },
    { base: [200, -14], len: [84, 52, 36], ang: [0.15, 0.4, 0.45], r: [26, 19] },
    { base: [196, 20], len: [78, 50, 34], ang: [0.26, 0.5, 0.52], r: [25, 18] },
    { base: [184, 52], len: [60, 40, 28], ang: [0.38, 0.58, 0.55], r: [21, 15] },
  ],
  thumb: { base: [66, 56], len: [64, 48], ang: [0.95, -0.45], r: [29, 20] },
  ink: { alpha: 0.92, width: 1.3, ring: 1.26, bellows: 1.14 },   // ring: puffed joints; bellows: ridges mid-segment (the segmented glove look)
  detail: {
    knuckles: [[186, -44, 20], [196, -12, 22], [190, 22, 21], [178, 52, 17]],
    plates: [[110, -58, 70, 118], [64, -66, 22, 132]],                           // back-of-hand plate and a wrist band: [x, y, w, h]
    pads: [[104, 58, 50, 32]],
  },
};

const TIP_X = 358;        // index-fingertip centre, in hand pixels (human; the glove is within 2%)
const TIP_Y = -46;
const REACH_LOCAL = 372;  // wrist origin to the very end of the index finger, incl. its radius
const WRIST_BLEED = -50;  // negative: the wrist origin sits this far INSIDE the canvas, so the cuff is fully visible
const REACH_FRAC = 0.94;  // fingertips end this far across the canvas; the rest is the gap between the hands

// ---------- geometry ----------
function chain(base, len, ang, r) {
  const pts = [{ x: base[0], y: base[1], r: r[0] }];
  let a = 0, x = base[0], y = base[1];
  len.forEach((L, i) => {
    a += ang[i]; x += Math.cos(a) * L; y += Math.sin(a) * L;
    pts.push({ x, y, r: r[0] + (r[1] - r[0]) * ((i + 1) / len.length) });
  });
  return pts;
}

function capsule(ctx, p, q) {
  const dx = q.x - p.x, dy = q.y - p.y, d = Math.hypot(dx, dy) || 1;
  const nx = -dy / d, ny = dx / d;
  ctx.beginPath();
  ctx.moveTo(p.x + nx * p.r, p.y + ny * p.r);
  ctx.lineTo(q.x + nx * q.r, q.y + ny * q.r);
  ctx.lineTo(q.x - nx * q.r, q.y - ny * q.r);
  ctx.lineTo(p.x - nx * p.r, p.y - ny * p.r);
  ctx.closePath(); ctx.fill();
  for (const c of [p, q]) { ctx.beginPath(); ctx.arc(c.x, c.y, c.r, 0, Math.PI * 2); ctx.fill(); }
}

function paintDetail(ctx, spec) {
  const d = spec.detail || {};
  ctx.fillStyle = "rgba(255,255,255,0.8)";
  for (const [x, y, r] of d.knuckles || []) { ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.fill(); }
  ctx.strokeStyle = "rgba(255,255,255,0.5)"; ctx.lineWidth = 9; ctx.lineCap = "round";
  for (const [x, y] of d.tendons || []) { ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(10, y * 0.55); ctx.stroke(); }
  ctx.fillStyle = "rgba(255,255,255,0.55)";
  for (const [x, y, rx, ry] of d.pads || []) { ctx.beginPath(); ctx.ellipse(x, y, rx, ry, 0, 0, Math.PI * 2); ctx.fill(); }
  ctx.fillStyle = "rgba(255,255,255,0.6)";
  for (const [x, y, w, h] of d.plates || []) ctx.fillRect(x, y, w, h);
}

function paintSkeleton(ctx, spec) {
  ctx.fillStyle = "#fff";
  const w = spec.wrist;
  ctx.fillRect(w.x0, w.y0, w.x1 - w.x0, w.y1 - w.y0);
  for (const c of spec.cuffs || []) ctx.fillRect(c.x0, c.y0, c.x1 - c.x0, c.y1 - c.y0);
  ctx.beginPath(); ctx.ellipse(spec.palm.cx, spec.palm.cy, spec.palm.rx, spec.palm.ry, 0, 0, Math.PI * 2); ctx.fill();
  const chains = spec.fingers.map((f) => chain(f.base, f.len, f.ang, f.r));
  chains.push(chain(spec.thumb.base, spec.thumb.len, spec.thumb.ang, spec.thumb.r));
  for (const pts of chains) {
    for (let i = 0; i < pts.length - 1; i++) capsule(ctx, pts[i], pts[i + 1]);
    if (spec.ink.ring) {
      for (let i = 1; i < pts.length - 1; i++) {
        ctx.beginPath(); ctx.arc(pts[i].x, pts[i].y, pts[i].r * spec.ink.ring, 0, Math.PI * 2); ctx.fill();
      }
    }
    if (spec.ink.bellows) {
      for (let i = 0; i < pts.length - 1; i++) {
        const m = { x: (pts[i].x + pts[i + 1].x) / 2, y: (pts[i].y + pts[i + 1].y) / 2, r: (pts[i].r + pts[i + 1].r) / 2 };
        ctx.beginPath(); ctx.arc(m.x, m.y, m.r * spec.ink.bellows, 0, Math.PI * 2); ctx.fill();
      }
    }
  }
}

// ---------- fields ----------
function boxBlur(src, w, h, r) {
  const tmp = new Float32Array(w * h), out = new Float32Array(w * h), n = 2 * r + 1;
  for (let y = 0; y < h; y++) {                       // horizontal pass
    let acc = 0;
    for (let x = -r; x <= r; x++) acc += src[y * w + Math.min(w - 1, Math.max(0, x))];
    for (let x = 0; x < w; x++) {
      tmp[y * w + x] = acc / n;
      acc += src[y * w + Math.min(w - 1, x + r + 1)] - src[y * w + Math.max(0, x - r)];
    }
  }
  for (let x = 0; x < w; x++) {                       // vertical pass
    let acc = 0;
    for (let y = -r; y <= r; y++) acc += tmp[Math.min(h - 1, Math.max(0, y)) * w + x];
    for (let y = 0; y < h; y++) {
      out[y * w + x] = acc / n;
      acc += tmp[Math.min(h - 1, y + r + 1) * w + x] - tmp[Math.max(0, y - r) * w + x];
    }
  }
  return out;
}

function buildFields(spec, W, H, S, ox, oy, cell) {
  const gw = Math.ceil(W / cell), gh = Math.ceil(H / cell);
  const c = document.createElement("canvas");
  c.width = gw; c.height = gh;
  const g = c.getContext("2d", { willReadFrequently: true });
  g.setTransform(1 / cell, 0, 0, 1 / cell, 0, 0);
  g.translate(ox, oy); g.scale(S, S);
  paintSkeleton(g, spec);
  const px = g.getImageData(0, 0, gw, gh).data;
  let mask = new Float32Array(gw * gh);
  for (let i = 0; i < mask.length; i++) mask[i] = px[i * 4 + 3] / 255;
  const blurOf = (src, r) => { let f = src; for (let pass = 0; pass < 3; pass++) f = boxBlur(f, gw, gh, r); return f; };
  const fine = blurOf(mask, 4), wide = blurOf(mask, 26);   // fingers are shaped by `fine`, the palm by `wide`
  // interior anatomy, painted on its own canvas so it can raise the relief without changing the outline
  const dc = document.createElement("canvas"); dc.width = gw; dc.height = gh;
  const dg = dc.getContext("2d", { willReadFrequently: true });
  dg.setTransform(1 / cell, 0, 0, 1 / cell, 0, 0); dg.translate(ox, oy); dg.scale(S, S);
  paintDetail(dg, spec);
  const dpx = dg.getImageData(0, 0, gw, gh).data;
  let detail = new Float32Array(gw * gh);
  for (let i = 0; i < detail.length; i++) detail[i] = dpx[i * 4 + 3] / 255;
  detail = blurOf(detail, 2);
  const relief = fine.map((v, i) => Math.min(1.25, 0.34 * v + 0.46 * wide[i] + 0.55 * detail[i] * (mask[i] > 0.5 ? 1 : 0)));
  return { gw, gh, mask, relief, cell };
}

const sample = (field, gw, gh, cell, x, y) => {
  const fx = Math.min(gw - 1, Math.max(0, x / cell)), fy = Math.min(gh - 1, Math.max(0, y / cell));
  const x0 = Math.floor(fx), y0 = Math.floor(fy), x1 = Math.min(gw - 1, x0 + 1), y1 = Math.min(gh - 1, y0 + 1);
  const tx = fx - x0, ty = fy - y0;
  const a = field[y0 * gw + x0] * (1 - tx) + field[y0 * gw + x1] * tx;
  const b = field[y1 * gw + x0] * (1 - tx) + field[y1 * gw + x1] * tx;
  return a * (1 - ty) + b * ty;
};

// ---------- one hand onto one canvas ----------
function renderHand(canvas, spec, { mirror, ink }) {
  const rect = canvas.getBoundingClientRect();
  const W = rect.width, H = rect.height;
  if (!W || !H) return null;
  const dpr = Math.min(2, window.devicePixelRatio || 1);
  canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);

  const S = (REACH_FRAC * W) / (REACH_LOCAL - WRIST_BLEED);   // origin sits at -WRIST_BLEED*S, so the tip lands at REACH_FRAC*W
  const ox = -WRIST_BLEED * S, oy = H * 0.38;
  const F = buildFields(spec, W, H, S, ox, oy, 3);
  const amp = S * 15;
  const spacing = Math.max(3.2, S * 2.4);

  const ctx = canvas.getContext("2d");
  ctx.setTransform(mirror ? -dpr : dpr, 0, 0, dpr, mirror ? W * dpr : 0, 0);
  ctx.clearRect(-2, -2, W + 4, H + 4);
  ctx.lineJoin = "round"; ctx.lineCap = "round";
  ctx.strokeStyle = ink; ctx.lineWidth = spec.ink.width; ctx.globalAlpha = spec.ink.alpha;

  const inside = (x, y) => sample(F.mask, F.gw, F.gh, F.cell, x, y) > 0.5;
  for (let y0 = spacing; y0 < H - 4; y0 += spacing) {
    let x = 0;
    while (x < W) {
      while (x < W && !inside(x, y0)) x += 2;
      if (x >= W) break;
      const xa = x;
      while (x < W && inside(x, y0)) x += 2;
      const xb = x;
      if (xb - xa < 4) continue;
      const pts = [];
      for (let xx = xa; xx <= xb; xx += 2) {
        pts.push([xx, y0 - amp * Math.min(1, sample(F.relief, F.gw, F.gh, F.cell, xx, y0) / 0.75)]);
      }
      // hide whatever this line stands in front of, then draw it
      ctx.save();
      ctx.globalCompositeOperation = "destination-out"; ctx.globalAlpha = 1;
      ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]);
      for (const p of pts) ctx.lineTo(p[0], p[1]);
      ctx.lineTo(xb, H); ctx.lineTo(xa, H); ctx.closePath(); ctx.fill();
      ctx.restore();
      ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]);
      for (const p of pts) ctx.lineTo(p[0], p[1]);
      ctx.stroke();
    }
  }
  // where the index fingertip ends, in canvas CSS pixels (so the spark can sit in the gap)
  const tipX = ox + S * TIP_X, tipY = oy + S * TIP_Y - amp * 0.6;
  return { tipX: mirror ? W - tipX : tipX, tipY, S };
}

/** Draw both hands and place the "spark" between the fingertips. */
export function createHands({ left, right, stage, spark }) {
  const t = tokens();
  let timer = 0;
  function render() {
    const l = renderHand(left, HUMAN, { mirror: false, ink: t.ink });
    const r = renderHand(right, GLOVE, { mirror: true, ink: t.ink });
    if (!l || !r || !spark) return;
    const sr = stage.getBoundingClientRect();
    const lr = left.getBoundingClientRect(), rr = right.getBoundingClientRect();
    const x0 = lr.left - sr.left + l.tipX, x1 = rr.left - sr.left + r.tipX;
    const y = lr.top - sr.top + (l.tipY + r.tipY) / 2;
    spark.style.left = `${x0}px`;
    spark.style.width = `${Math.max(0, x1 - x0)}px`;
    spark.style.top = `${y}px`;
  }
  const ro = new ResizeObserver(() => { clearTimeout(timer); timer = setTimeout(render, 80); });
  ro.observe(stage);
  render();
  return { render, destroy() { ro.disconnect(); } };
}
