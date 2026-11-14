/**
 * Landing page: the real stacked-sessions plot for the person who most needs a human's attention, plus three facts
 * read from the same API response (today's value against their own usual). Fictional crew, synthetic data.
 * Nothing here is invented: if the API is unavailable the section simply stays empty.
 */
import { api, bandChip } from "./common.js";
import { createRidgeline } from "./ridgeline.js";

const $ = (id) => document.getElementById(id);
const ridge = createRidgeline($("pv-canvas"), $("pv-axis"), $("pv-readout"));
const NEED = { RED: 3, YELLOW: 2 };
const n0 = (v) => Math.round(v).toLocaleString("en-US");

function fact(id, value, usual, label) {
  $(id).textContent = value;
  $(`${id}-l`).textContent = `${label}. Their usual: ${usual}.`;
}

(async () => {
  try {
    const { crew } = await api("/api/readiness");
    const pick = [...crew].sort((a, b) => (NEED[b.readiness.band] || 0) - (NEED[a.readiness.band] || 0))[0];
    const data = await api(`/api/readiness/${encodeURIComponent(pick.profile.id)}`);
    const r = data.readiness;
    $("pv-who").textContent = `${data.profile.display_name}, ${data.profile.mission_role}. Fictional crew member, synthetic data.`;
    ridge.setSessions(data.trend, r.band);
    const d = Object.fromEntries(r.deviations.map((x) => [x.feature, x]));
    if (r.status === "SCORED" && d.iki_median_ms && d.pause_count && d.checklist_response_median_ms) {
      fact("f-rhythm", `${n0(d.iki_median_ms.value)} ms`, `${n0(d.iki_median_ms.baseline_median)} ms`, "Time between keys");
      fact("f-pause", `${n0(d.pause_count.value)} pauses`, n0(d.pause_count.baseline_median), "Gaps of 2 seconds or more");
      fact("f-resp", `${n0(d.checklist_response_median_ms.value)} ms`, `${n0(d.checklist_response_median_ms.baseline_median)} ms`, "Time to first key on each checklist item");
      $("pv-chip").innerHTML = bandChip(r);
      $("f-band-l").textContent = r.band === "GREEN" ? "No change worth a check-in." : "A suggested check-in, not a verdict.";
      $("pv-facts").hidden = false;
    }
  } catch {
    /* decorative: leave it empty */
  }
})();
