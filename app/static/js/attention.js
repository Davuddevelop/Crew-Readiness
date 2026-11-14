/**
 * Reaction-time attention check: TASK A-1 (Member 4, or Member 3 if we are three).
 *
 * SPEC (agree changes with the team lead first):
 *   - 10 trials.
 *   - Each trial: wait a RANDOM foreperiod of 1500-4000 ms (random so people
 *     can't anticipate the rhythm), then light up #rt-stage.
 *   - Response = click on #rt-stage OR Space key.
 *   - Reaction time = performance.now() at response - performance.now() at stimulus.
 *   - Response BEFORE the stimulus = premature (count it, restart that trial's wait).
 *   - No response within 1500 ms after the stimulus = miss.
 *   - Responses faster than 100 ms after stimulus are physiologically implausible:
 *     treat them as premature. (Think about why!)
 *   - Summary: median RT of valid trials (null if none), premature_count, miss_count.
 *   - POST to /api/attention:
 *       { profile_id, trials: 10, median_rt_ms, premature_count, miss_count }
 *   - Show the summary with the label "Illustrative reaction-time check. Not a medical test."
 *
 * HINTS:
 *   - Model it as a small state machine: idle -> waiting -> stimulus -> (next | done).
 *   - Keep ONE timer handle and clear it on every state change, or you'll get ghost trials.
 *   - Reuse `median` from ./capture.js and `api` from ./common.js.
 *
 * STRETCH: compare the result with the person's own previous attention results.
 */
import { api, esc } from "./common.js";
// import { median } from "./capture.js";

const select = document.getElementById("profile-select");
const startBtn = document.getElementById("rt-start");
const stage = document.getElementById("rt-stage");
const message = document.getElementById("rt-message");

async function loadProfiles() {
  const { profiles } = await api("/api/profiles");
  select.innerHTML = profiles
    .map((p) => `<option value="${esc(p.id)}">${esc(p.display_name)} (${esc(p.mission_role)})</option>`)
    .join("");
  const preselect = new URLSearchParams(location.search).get("crew");
  if (preselect) select.value = preselect;
  startBtn.disabled = false;
}

startBtn.addEventListener("click", () => {
  // TODO(A-1): replace this placeholder with the state machine described above.
  message.textContent = "Not implemented yet. See TODO(A-1) in app/static/js/attention.js.";
  stage.classList.add("rt-todo");
});

loadProfiles().catch((err) => {
  select.innerHTML = `<option>Error: ${esc(err.message)}</option>`;
});
