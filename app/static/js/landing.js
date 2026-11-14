/**
 * Landing motion. Every movement here explains the product or is a quiet idle breath:
 *   - the hands LEAN IN as the pointer nears the gap, but never close it (the system never decides; a person does),
 *     and the empty space between them narrows, never to zero;
 *   - a slow opposite float on the hands and a drift on the ghosted wordmark;
 *   - the three statements fade up as they scroll into view.
 * Transform-only, paused when the stage is off screen or the tab is hidden, and fully off under reduced motion
 * (the page then simply shows everything). Nothing here fetches anything.
 */
const reduce = window.matchMedia("(prefers-reduced-motion: reduce)");

const stage = document.getElementById("land-stage");
const wrapL = document.getElementById("wrap-l");
const wrapR = document.getElementById("wrap-r");
const ghost = stage && stage.querySelector(".ghost");

const MAX_LEAN_VW = 1.8;      // each hand moves at most this far in, so the gap never falls below 60 % of its size
let target = 0, lean = 0, py = 0, tilt = 0, running = false, visible = true, raf = 0;

function frame(now) {
  raf = 0;
  if (!visible || document.hidden) { running = false; return; }
  const vw = window.innerWidth / 100, t = now / 1000;
  lean += (target - lean) * 0.07;
  tilt += (py - tilt) * 0.07;
  const x = lean * MAX_LEAN_VW * vw;
  const bob = Math.sin(t * 0.9) * 5;
  wrapL.style.transform = `translate3d(${x.toFixed(2)}px, ${(bob + tilt * 10).toFixed(2)}px, 0)`;
  wrapR.style.transform = `translate3d(${(-x).toFixed(2)}px, ${(-bob * 0.8 + tilt * 10).toFixed(2)}px, 0)`;
  if (ghost) ghost.style.transform = `translateX(calc(-50% + ${(Math.sin(t * 0.25) * 1.2 * vw).toFixed(2)}px))`;
  raf = requestAnimationFrame(frame);
}
function start() { if (!running && visible && !document.hidden) { running = true; raf = requestAnimationFrame(frame); } }

if (stage && wrapL && wrapR && !reduce.matches) {
  window.addEventListener("pointermove", (e) => {
    if (e.pointerType === "touch") return;
    const r = stage.getBoundingClientRect();
    const near = e.clientY > r.top - r.height * 0.25 && e.clientY < r.bottom + r.height * 0.25;     // only when the pointer is around the hands
    const gapX = window.innerWidth * (0.58 + 0.045);                                                  // the middle of the gap
    const d = Math.abs(e.clientX - gapX) / window.innerWidth;
    target = near ? Math.max(0, 1 - d * 2.4) : 0;
    py = near ? ((e.clientY - (r.top + r.height / 2)) / r.height) : 0;
  }, { passive: true });
  window.addEventListener("pointerleave", () => { target = 0; py = 0; });
  new IntersectionObserver(([en]) => { visible = en.isIntersecting; if (visible) start(); }, { threshold: 0 }).observe(stage);
  document.addEventListener("visibilitychange", start);
  start();
}

if (!reduce.matches && "IntersectionObserver" in window) {
  document.documentElement.classList.add("reveal-on");
  const io = new IntersectionObserver((entries) => entries.forEach((en) => {
    if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
  }), { threshold: 0.2 });
  document.querySelectorAll(".land-three .col").forEach((c) => io.observe(c));
}
