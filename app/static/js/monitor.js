/**
 * Monitoring page: runs the fixed checklist, captures timing, shows the exact
 * payload, then POSTs it to /api/sessions.
 * Owner: Member 3 (Frontend & UX).
 */
import { api, bandChip, esc } from "./common.js";
import { createCapture } from "./capture.js";

const task = JSON.parse(document.getElementById("task-data").textContent);
const taskType = JSON.parse(document.getElementById("task-type").textContent);

const $ = (id) => document.getElementById(id);
const select = $("profile-select");
const input = $("task-input");

let capture = null;
let index = 0;
let features = null;

const normalise = (s) => s.trim().replace(/\s+/g, " ").toLowerCase();

async function loadProfiles() {
  const { profiles } = await api("/api/profiles");
  select.innerHTML = profiles
    .map((p) => `<option value="${esc(p.id)}">${esc(p.display_name)} (${esc(p.mission_role)})${p.kind === "demo" ? " · fictional" : ""}</option>`)
    .join("");
  const preselect = new URLSearchParams(location.search).get("crew");
  if (preselect) select.value = preselect;
  $("start-btn").disabled = false;
}

function showItem() {
  const item = task.items[index];
  $("step-counter").textContent = `Step ${index + 1} of ${task.items.length}`;
  $("step-text").textContent = item.step;
  $("confirm-hint").textContent = item.confirm;
  $("progress-bar").style.width = `${(index / task.items.length) * 100}%`;
  $("task-feedback").textContent = "";
  input.value = "";
  input.focus();
  capture.startItem();
}

function start() {
  capture = createCapture();
  index = 0;
  $("step-setup").hidden = true;
  $("step-task").hidden = false;
  $("monitor-pill").hidden = false;
  select.disabled = true;
  capture.startTask();
  showItem();
}

function finish() {
  features = capture.summarize();
  capture = null; // stop capturing immediately
  input.value = "";
  $("monitor-pill").hidden = true;
  $("step-task").hidden = true;
  $("step-review").hidden = false;
  $("payload-preview").textContent = JSON.stringify(
    { profile_id: select.value, task_type: taskType, features }, null, 2);
}

input.addEventListener("paste", (e) => e.preventDefault()); // keep sessions comparable

input.addEventListener("keydown", (e) => {
  if (!capture) return;
  if (e.key === "Enter") {
    e.preventDefault();
    const expected = task.items[index].confirm;
    if (normalise(input.value) === normalise(expected)) {
      capture.endItem();
      index += 1;
      if (index < task.items.length) showItem();
      else finish();
    } else {
      capture.recordRetry();
      $("task-feedback").textContent = "Phrase doesn't match. Check it and try again.";
      input.classList.remove("shake");
      void input.offsetWidth; // restart animation
      input.classList.add("shake");
    }
    return;
  }
  capture.onKeyDown(e);
});

$("start-btn").addEventListener("click", start);

$("discard-btn").addEventListener("click", () => location.reload());

$("submit-btn").addEventListener("click", async () => {
  $("submit-btn").disabled = true;
  try {
    const data = await api("/api/sessions", {
      method: "POST",
      body: JSON.stringify({ profile_id: select.value, task_type: taskType, features }),
    });
    const r = data.readiness;
    $("step-review").hidden = true;
    $("step-result").hidden = false;
    $("result-body").innerHTML = `
      <p>${bandChip(r)} <span class="muted">Session #${data.session_id} stored as aggregate features only.</span></p>
      <p class="advisory">${esc(r.advisory)}</p>
      ${r.reasons.length ? `<ul class="reasons">${r.reasons.map((x) => `<li>${esc(x)}</li>`).join("")}</ul>` : ""}
      ${data.latest_session.data_quality === "low"
        ? `<p class="warn">Flagged LOW quality: ${esc(data.latest_session.quality_notes)}</p>` : ""}
      <p><a class="btn" href="/?crew=${encodeURIComponent(select.value)}">Open on dashboard →</a>
         <a class="btn btn-ghost" href="/monitor?crew=${encodeURIComponent(select.value)}">Run again</a></p>`;
  } catch (err) {
    $("submit-btn").disabled = false;
    alert(`Could not submit: ${err.message}`);
  }
});

loadProfiles().catch((err) => {
  select.innerHTML = `<option>Error: ${esc(err.message)}</option>`;
});
