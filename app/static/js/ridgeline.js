/**
 * "Stacked sessions": the dashboard's signature visual.
 *
 * One line per recent session, oldest at the top, newest at the bottom. A line is flat
 * when that session matched the person's own baseline; it rises where a signal was
 * slower or pausier than their usual. Lines hide the ones behind them (flat background
 * colour fill, no gradients), the way a stacked pulse plot does.
 *
 * Inspiration, honestly credited: stacked pulse plots such as Harold Craft's 1970 plot of
 * pulsar CP 1919. See docs/DESIGN.md. Our version is drawn from our own data.
 *
 * DATA: exactly what GET /api/readiness/<id> returns in `trend[].deviations` (0 = usual
 * or faster, capped at 4). Nothing here is invented. The only non-data movement is a
 * sub-pixel idle "breathing" and the entrance/morph animation.
 *
 * MOTION: entrance (lines settle in, newest draws left to right), morph when the selected
 * person changes, idle breathing. All of it is off under prefers-reduced-motion, and the
 * loop pauses when the canvas is off-screen or the tab is hidden.
 *
 * Owner: Member 3 (Frontend). The data contract it relies on: docs/DATA_CONTRACT.md.
 */

export const FEATURES = [
  { key: "iki_median_ms", label: "Rhythm", short: "Rhythm" },
  { key: "iki_iqr_ms", label: "Variability", short: "Var." },
  { key: "pause_count", label: "Pauses", short: "Pauses" },
  { key: "pause_total_ms", label: "Pause time", short: "Pause t." },
  { key: "checklist_response_median_ms", label: "Response", short: "Resp." },
];

const SLOTS = 14;                 // fixed grid, so a short history is visibly short
const C = { bg: "#090A0F", ink: "#F8FAFC", muted: "#9AA0AA", line: "#1D212C",
            GREEN: "#00F0FF", YELLOW: "#FFB800", RED: "#FF5A6E" };
const xFrac = (k) => 0.1 + (0.8 * k) / (FEATURES.length - 1);

const clamp01 = (v) => Math.min(1, Math.max(0, v));
const easeOut = (t) => 1 - Math.pow(1 - clamp01(t), 3);

export function createRidgeline(canvas, axisEl, readoutEl) {
  const ctx = canvas.getContext("2d");
  const motionQuery = window.matchMedia("(prefers-reduced-motion: reduce)");
  const slots = Array.from({ length: SLOTS }, () => ({
    present: 0, a: 0, tgt: FEATURES.map(() => 0), cur: FEATURES.map(() => 0),
    dashed: false, session: null,
  }));
  let W = 0, H = 0, dpr = 1;
  // The entrance starts the first time the canvas is actually visible, so it is never
  // "used up" while the art is off-screen.
  let introStart = null, introPending = true, latestBand = null, hover = null;
  let raf = 0, last = 0, onScreen = true;

  // ---- axis labels (HTML, so they stay crisp and selectable) ----
  axisEl.innerHTML = FEATURES.map((f, k) =>
    `<span style="left:${(xFrac(k) * 100).toFixed(1)}%"><b class="l" style="font-weight:inherit">${f.label}</b><b class="s" style="font-weight:inherit">${f.short}</b></span>`).join("");

  function resize() {
    const r = canvas.getBoundingClientRect();
    dpr = Math.min(2, window.devicePixelRatio || 1);
    W = r.width; H = r.height;
    canvas.width = Math.round(W * dpr);
    canvas.height = Math.round(H * dpr);
    if (!raf) draw(performance.now());
  }

  // ---- geometry shared by drawing and hover hit-testing ----
  function geometry() {
    const top = H * 0.19, bottom = H - 40;
    const gap = (bottom - top) / (SLOTS - 1);
    // peak height per SD: tied to line spacing, but a 4-SD peak on the top line must still fit
    return { top, gap, scale: Math.min(gap * 0.85, top / 4.2), sigma: Math.min(60, Math.max(14, W * 0.04)) };
  }

  function yAt(slot, j, x, g, now) {
    let bump = 0;
    for (let k = 0; k < FEATURES.length; k++) {
      const d = (x - W * xFrac(k)) / g.sigma;
      bump += slot.cur[k] * Math.exp(-0.5 * d * d);
    }
    const breathe = motionQuery.matches ? 1 : 1 + 0.03 * Math.sin(now / 3100 + j * 0.9);
    const drift = motionQuery.matches ? 0 : Math.sin(now / 2200 + j * 0.55) * 0.8;
    return g.top + j * g.gap + drift - bump * g.scale * breathe;
  }

  function introProgress(j, now) {
    if (introStart === null || motionQuery.matches) return 1;
    return easeOut((now - introStart - j * 55) / 650);
  }

  // ---- drawing ----
  function draw(now) {
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.fillStyle = C.bg;
    ctx.fillRect(0, 0, W, H);

    ctx.strokeStyle = C.line; ctx.lineWidth = 1; ctx.setLineDash([]);
    for (let k = 0; k < FEATURES.length; k++) {
      const x = Math.round(W * xFrac(k)) + 0.5;
      ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H - 34); ctx.stroke();
    }

    const g = geometry();
    for (let j = 0; j < SLOTS; j++) {
      const s = slots[j];
      if (s.a < 0.01) continue;
      const p = introProgress(j, now);
      const isLatest = j === SLOTS - 1 && s.present;
      const yShift = (1 - p) * -12;
      let reveal = W;
      if (isLatest && introStart !== null && !motionQuery.matches) {
        reveal = W * easeOut((now - introStart - SLOTS * 55 - 100) / 1100);
      }

      ctx.save();
      ctx.beginPath();
      ctx.rect(0, 0, Math.max(0, reveal), H);
      ctx.clip();

      ctx.beginPath();
      for (let x = 0; x <= W + 3; x += 3) {
        const y = yAt(s, j, Math.min(x, W), g, now) + yShift;
        x === 0 ? ctx.moveTo(0, y) : ctx.lineTo(Math.min(x, W), y);
      }
      ctx.save();                       // flat fill below the line hides lines behind it
      ctx.lineTo(W, H); ctx.lineTo(0, H); ctx.closePath();
      ctx.fillStyle = C.bg; ctx.fill();
      ctx.restore();

      const recency = 0.22 + 0.5 * (j / (SLOTS - 1));
      if (isLatest) {
        ctx.strokeStyle = C[latestBand] || C.ink; ctx.lineWidth = 2.2; ctx.globalAlpha = p;
        ctx.setLineDash(s.dashed ? [3, 5] : []);
      } else if (hover === j) {
        ctx.strokeStyle = C.ink; ctx.lineWidth = 1.8; ctx.globalAlpha = s.a;
        ctx.setLineDash(s.dashed ? [3, 5] : []);
      } else if (s.dashed) {
        ctx.strokeStyle = C.muted; ctx.lineWidth = 1.1; ctx.globalAlpha = 0.5 * s.a * p;
        ctx.setLineDash([3, 5]);
      } else {
        ctx.strokeStyle = C.ink; ctx.lineWidth = 1.2; ctx.globalAlpha = recency * s.a * p;
        ctx.setLineDash([]);
      }
      // stroke only the curve: redraw the path without the closing edges
      ctx.beginPath();
      for (let x = 0; x <= W + 3; x += 3) {
        const y = yAt(s, j, Math.min(x, W), g, now) + yShift;
        x === 0 ? ctx.moveTo(0, y) : ctx.lineTo(Math.min(x, W), y);
      }
      ctx.stroke();
      ctx.restore();
    }
  }

  // ---- animation loop ----
  function step(now) {
    const dt = Math.min(48, now - (last || now)); last = now;
    const k = 1 - Math.exp(-dt / 170);
    for (const s of slots) {
      s.a += (s.present - s.a) * k;
      for (let i = 0; i < s.cur.length; i++) s.cur[i] += (s.tgt[i] - s.cur[i]) * k;
    }
    draw(now);
    raf = requestAnimationFrame(step);
  }
  function startLoop() {
    if (raf || motionQuery.matches || !onScreen || document.hidden) return;
    if (introPending && slots.some((s) => s.present)) { introPending = false; introStart = performance.now(); }
    last = 0; raf = requestAnimationFrame(step);
  }
  function stopLoop() { cancelAnimationFrame(raf); raf = 0; }

  // ---- public: feed it the trend from the API ----
  function setSessions(trend, band) {
    latestBand = band;
    const sessions = trend.slice(-SLOTS);
    const offset = SLOTS - sessions.length;
    const first = introStart === null;
    slots.forEach((s, j) => {
      const sess = sessions[j - offset] || null;
      s.session = sess;
      s.present = sess ? 1 : 0;
      s.dashed = !!sess && !sess.deviations;
      s.tgt = FEATURES.map((f) => (sess && sess.deviations ? sess.deviations[f.key] || 0 : 0));
      if (first || motionQuery.matches) { s.cur = s.tgt.slice(); s.a = s.present; }
    });
    updateReadout();
    // Always paint a frame: an off-screen canvas must not be left blank.
    if (motionQuery.matches || !onScreen) draw(performance.now()); else startLoop();
  }

  // ---- hover: which session is this line? ----
  function updateReadout() {
    const j = hover !== null ? hover : SLOTS - 1;
    const s = slots[j].session;
    if (!s) { readoutEl.innerHTML = ""; return; }
    const when = new Date(s.created_at).toLocaleString(undefined,
      { month: "short", day: "numeric", hour: "2-digit", minute: "2-digit" });
    const status = s.band || "calibrating";
    const score = s.score === null ? "no score yet" : s.score.toFixed(2);
    readoutEl.innerHTML =
      `${hover !== null ? "Session" : "Latest session"}<br><strong>${when}</strong><br>${score} · ${status}`;
  }
  canvas.addEventListener("pointermove", (e) => {
    const r = canvas.getBoundingClientRect();
    const x = e.clientX - r.left, y = e.clientY - r.top;
    const g = geometry(), now = performance.now();
    let best = null, bestD = 14;
    slots.forEach((s, j) => {
      if (!s.present) return;
      const d = Math.abs(yAt(s, j, x, g, now) - y);
      if (d < bestD) { bestD = d; best = j; }
    });
    if (best !== hover) { hover = best; updateReadout(); if (!raf) draw(now); }
  });
  canvas.addEventListener("pointerleave", () => {
    hover = null; updateReadout(); if (!raf) draw(performance.now());
  });

  // ---- lifecycle ----
  const ro = new ResizeObserver(resize); ro.observe(canvas);
  const io = new IntersectionObserver(([e]) => {
    onScreen = e.isIntersecting; onScreen ? startLoop() : stopLoop();
  }); io.observe(canvas);
  document.addEventListener("visibilitychange", () => (document.hidden ? stopLoop() : startLoop()));
  motionQuery.addEventListener("change", () => { stopLoop(); setSessionsAgain(); });
  let lastArgs = null;
  const setSessionsAgain = () => lastArgs && setSessions(...lastArgs);

  resize();
  return {
    setSessions(trend, band) { lastArgs = [trend, band]; setSessions(trend, band); },
    destroy() { stopLoop(); ro.disconnect(); io.disconnect(); },
  };
}
