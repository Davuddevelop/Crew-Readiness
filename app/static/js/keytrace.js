/**
 * Live timing trace for the Monitoring page: motion that explains the product.
 *
 * Every counted key press draws one blip on a scrolling line. Pauses of PAUSE_MS or more
 * (the same threshold capture.js uses) turn the line amber while they happen. A hairline
 * marks the change of checklist step, because time between steps is "response time", not
 * a pause.
 *
 * PRIVACY BY CONSTRUCTION: the only thing this module can receive is a moment in time.
 * pulse() takes a timestamp, never a key or a character, so it cannot draw or store what
 * was typed. That is the point of showing it to the person being monitored.
 *
 * Owner: Member 3 (Frontend). Not scored, not sent to the server: purely a visual mirror.
 */
import { PAUSE_MS } from "./capture.js";

const SPEED = 90;      // px per second the trace scrolls left
const RIGHT_PAD = 28;  // "now" sits this far from the right edge
const COLORS = { ink: "#F8FAFC", muted: "#9AA0AA", line: "#2C3140", amber: "#FFB800" };

export function createKeyTrace(canvas) {
  const ctx = canvas.getContext("2d");
  const reduced = window.matchMedia("(prefers-reduced-motion: reduce)");
  let W = 0, H = 0, dpr = 1, raf = 0, active = false;
  let events = [];   // { t: ms, boundary?: true }, oldest first; timestamps only

  function resize() {
    const r = canvas.getBoundingClientRect();
    dpr = Math.min(2, window.devicePixelRatio || 1);
    W = r.width; H = r.height;
    canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
  }
  const xOf = (t, now) => W - RIGHT_PAD - ((now - t) * SPEED) / 1000;

  function draw(now) {
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, W, H);
    const base = Math.round(H * 0.7) + 0.5;

    // baseline
    ctx.lineWidth = 1; ctx.strokeStyle = COLORS.line; ctx.setLineDash([]);
    ctx.beginPath(); ctx.moveTo(0, base); ctx.lineTo(W, base); ctx.stroke();

    // walk the events: boundaries reset the pause clock, key gaps >= PAUSE_MS are pauses
    let prevKey = null;
    ctx.lineWidth = 1.4;
    for (const e of events) {
      const x = xOf(e.t, now);
      if (e.boundary) {
        prevKey = null;
        if (x > -2) { ctx.strokeStyle = COLORS.line; ctx.beginPath(); ctx.moveTo(x, 6); ctx.lineTo(x, H - 6); ctx.stroke(); }
        continue;
      }
      if (prevKey !== null && e.t - prevKey >= PAUSE_MS) {
        ctx.strokeStyle = COLORS.amber; ctx.lineWidth = 2.4;
        ctx.beginPath(); ctx.moveTo(xOf(prevKey, now) + 6, base); ctx.lineTo(x, base); ctx.stroke();
        ctx.lineWidth = 1.4;
      }
      if (x > -10) {
        ctx.strokeStyle = COLORS.ink;
        ctx.beginPath(); ctx.moveTo(x - 3, base); ctx.lineTo(x, base - H * 0.42); ctx.lineTo(x + 3, base + H * 0.1); ctx.lineTo(x + 6, base); ctx.stroke();
      }
      prevKey = e.t;
    }
    // a pause in progress is shown live, so the person sees what is being counted
    if (prevKey !== null && now - prevKey >= PAUSE_MS) {
      ctx.strokeStyle = COLORS.amber; ctx.lineWidth = 2.4;
      ctx.beginPath(); ctx.moveTo(xOf(prevKey, now) + 6, base); ctx.lineTo(W - RIGHT_PAD, base); ctx.stroke();
    }
    // "now" marker
    ctx.strokeStyle = COLORS.muted; ctx.lineWidth = 1;
    ctx.beginPath(); ctx.moveTo(W - RIGHT_PAD + 0.5, base - 6); ctx.lineTo(W - RIGHT_PAD + 0.5, base + 6); ctx.stroke();
    // forget what has scrolled out of view
    while (events.length && xOf(events[0].t, now) < -40) events.shift();
  }

  function loop(now) { draw(now); raf = active ? requestAnimationFrame(loop) : 0; }
  function redraw() { draw(performance.now()); }

  return {
    start() { resize(); active = true; events = []; if (reduced.matches) redraw(); else raf = requestAnimationFrame(loop); },
    stop() { active = false; cancelAnimationFrame(raf); raf = 0; },
    /** A counted key press happened. Timestamp only. */
    pulse(now = performance.now()) { events.push({ t: now }); if (reduced.matches) redraw(); },
    /** The person moved to the next checklist step. */
    boundary(now = performance.now()) { events.push({ t: now, boundary: true }); if (reduced.matches) redraw(); },
  };
}
