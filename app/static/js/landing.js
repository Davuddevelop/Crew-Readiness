/**
 * Landing page: the hands, and a live preview of the real dashboard.
 * The preview reuses the dashboard's own stacked-sessions renderer and the same API, so it
 * can never drift from the product. If the API is unavailable the card simply stays empty.
 */
import { api, bandChip } from "./common.js";
import { createRidgeline } from "./ridgeline.js";
import { createHands } from "./hands.js";

const $ = (id) => document.getElementById(id);

createHands({ left: $("hand-l"), right: $("hand-r"), stage: $("land-stage"), spark: $("land-spark") });

const ridge = createRidgeline($("pv-canvas"), $("pv-axis"), $("pv-readout"));
const NEED = { RED: 3, YELLOW: 2 };

(async () => {
  try {
    const { crew } = await api("/api/readiness");
    // show whoever most needs a human's attention, same rule as the dashboard
    const pick = [...crew].sort((a, b) => (NEED[b.readiness.band] || 0) - (NEED[a.readiness.band] || 0))[0];
    const data = await api(`/api/readiness/${encodeURIComponent(pick.profile.id)}`);
    $("pv-name").textContent = data.profile.display_name;
    $("pv-chip").innerHTML = bandChip(data.readiness);
    ridge.setSessions(data.trend, data.readiness.band);
  } catch {
    /* decorative: leave it empty */
  }
})();
