/**
 * Alert-burden calculator on the Evidence page. Pure arithmetic on numbers the page already holds (the simulated benchmark's
 * false-alert rates, embedded from app/results_data.json). It makes no network request.
 */
const $ = (id) => document.getElementById(id);
const data = JSON.parse($("burden-data").textContent);
const sel = $("b-budget");
sel.innerHTML = data.options.map((o, i) => `<option value="${i}">${o.label}</option>`).join("");
sel.value = "1";                       // 1 in 20 by default

const num = (id, lo, hi, fallback) => { const v = Number($(id).value); return Number.isFinite(v) ? Math.min(hi, Math.max(lo, v)) : fallback; };
const fmt = (x) => (x >= 10 ? Math.round(x).toString() : x.toFixed(1));

function render() {
  const crew = num("b-crew", 1, 12, 4), perday = num("b-perday", 1, 6, 1), days = num("b-days", 1, 1000, 180), mins = num("b-minutes", 1, 120, 10);
  const rate = data.options[Number(sel.value)].rate;
  const sessionsPerDay = crew * perday, perDay = sessionsPerDay * rate;
  const mission = perDay * days, hours = (mission * mins) / 60;
  const every = perDay > 0 ? 1 / perDay : Infinity;
  const rows = [
    ["Check-ins in the mission", Math.round(sessionsPerDay * days).toLocaleString()],
    ["Share of normal sessions flagged by chance", `${(rate * 100).toFixed(1)} %`],
    ["False alerts per week, whole crew", fmt(perDay * 7)],
    ["One false alert about every", Number.isFinite(every) ? `${fmt(every)} days` : "never"],
    ["False alerts over the mission", fmt(mission)],
    ["Reviewer time over the mission", `${fmt(hours)} hours`],
  ];
  $("b-out").innerHTML = rows.map(([k, v]) => `<tr><td>${k}</td><td class="num"><strong>${v}</strong></td></tr>`).join("");
}
["b-crew", "b-perday", "b-days", "b-budget", "b-minutes"].forEach((id) => $(id).addEventListener("input", render));
render();
