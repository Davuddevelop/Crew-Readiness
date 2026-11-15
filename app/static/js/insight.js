/**
 * "Your sleep and your reaction time, on this device" (plan v4, W2). It joins the person's PRIVATE notes (read from this browser's
 * localStorage) to their own reaction checks (one read-only GET of their own aggregates) and compares the two IN THE BROWSER.
 * Nothing about the notes is ever sent: the only request is GET /api/attention/<id>, which carries no note data.
 */
import { api } from "./common.js";

const $ = (id) => document.getElementById(id);
const MIN_EACH = 3;                      // paired days needed on each side before we say anything
const SHORT_HOURS = 6;
const day = (iso) => new Date(iso).toLocaleDateString("en-CA");
const med = (a) => { const s = [...a].sort((x, y) => x - y), m = s.length >> 1; return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2; };

export function compare(pairs) {
  const short = pairs.filter((p) => p.sleep < SHORT_HOURS).map((p) => p.rt), long = pairs.filter((p) => p.sleep >= SHORT_HOURS).map((p) => p.rt);
  if (short.length < MIN_EACH || long.length < MIN_EACH) {
    return `Not enough paired days yet. You have ${short.length} day${short.length === 1 ? "" : "s"} with under ${SHORT_HOURS} hours of sleep and ${long.length} with ${SHORT_HOURS} or more that also have a reaction check; ${MIN_EACH} of each are needed before this says anything.`;
  }
  const d = Math.round(med(short) - med(long)), word = d > 0 ? "slower" : d < 0 ? "faster" : "the same";
  return `On the ${short.length} days you noted under ${SHORT_HOURS} hours of sleep, your reaction time was ${d === 0 ? "the same as" : `about ${Math.abs(d)} ms ${word} than`} on the ${long.length} days you noted ${SHORT_HOURS} or more (medians ${Math.round(med(short))} ms and ${Math.round(med(long))} ms).`;
}

function pairsFor(id, checks) {
  let notes = [];
  try { notes = JSON.parse(localStorage.getItem(`crew-readiness-notes-v1:${id}`) || "[]"); } catch { notes = []; }
  const byDay = new Map();
  for (const c of checks) if (c.median_rt_ms != null) { const k = day(c.created_at); (byDay.get(k) || byDay.set(k, []).get(k)).push(c.median_rt_ms); }
  const out = [];
  for (const n of notes) if (typeof n.sleep === "number") { const rts = byDay.get(day(n.t)); if (rts) out.push({ sleep: n.sleep, rt: med(rts) }); }
  return out;
}

let current = null;
async function refresh() {
  const id = current || ($("me-select") && $("me-select").value);
  if (!id) return;
  try {
    const { checks } = await api(`/api/attention/${encodeURIComponent(id)}`);
    $("insight-text").textContent = compare(pairsFor(id, checks));
  } catch (err) { $("insight-text").textContent = `Could not load your reaction checks: ${err.message}`; }
}
document.addEventListener("me:shown", (e) => { current = e.detail.id; refresh(); });
document.addEventListener("notes:changed", () => { refresh(); });
$("insight-example").addEventListener("click", () => {
  // EXAMPLE numbers, made up for illustration only: they are not anyone's data
  const ex = [[5, 331], [5.5, 322], [4.5, 340], [7, 296], [8, 301], [7.5, 290]].map(([sleep, rt]) => ({ sleep, rt }));
  $("insight-text").textContent = "EXAMPLE (made-up numbers): " + compare(ex);
});
