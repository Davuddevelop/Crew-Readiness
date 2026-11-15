/**
 * Replay: one simulated person, scored two ways. All numbers come from /api/simulate (the real scoring code
 * on synthetic data); this file only draws them.
 */
import { api, esc } from "./common.js";
import { tokens } from "./tokens.js";

const $ = (id) => document.getElementById(id);
let chart;

function params() {
  return new URLSearchParams({
    scenario: $("scenario").value,
    magnitude: ($("size").value / 100).toString(),
    length: $("length").value,
    seed: $("seed").value,
  });
}

function sync() {
  const sc = $("scenario").value;
  $("size-out").textContent = `${$("size").value} %`;
  $("length-out").textContent = $("length").value;
  $("size-wrap").hidden = sc === "steady";
  $("length-wrap").hidden = sc === "steady" || sc === "spike" || sc === "equipment";
}

function draw(d) {
  const T = tokens();
  const rows = d.sessions;
  const shade = {
    id: "shade",
    beforeDatasetsDraw(c) {
      const { ctx, chartArea: a, scales: { x, y } } = c;
      const idx = rows.map((r, i) => (r.event ? i : -1)).filter((i) => i >= 0);
      ctx.save();
      const half = (x.getPixelForValue(1) - x.getPixelForValue(0)) / 2;
      if (d.bands) {
        ctx.fillStyle = "rgba(248,250,252,0.07)";
        for (const b of d.bands) ctx.fillRect(x.getPixelForValue(b.from - 1) - half, a.top, x.getPixelForValue(b.to - 1) - x.getPixelForValue(b.from - 1) + 2 * half, a.bottom - a.top);
        ctx.font = "11px " + T.font; ctx.fillStyle = T.muted; ctx.textAlign = "left";
        for (const b of d.bands) ctx.fillText(b.label, x.getPixelForValue(b.from - 1) - half + 4, a.top + 12);
        ctx.strokeStyle = T.ink; ctx.setLineDash([]); ctx.lineWidth = 1;
        for (const m of d.markers || []) {
          const px = x.getPixelForValue(m.at - 1) - half;
          ctx.beginPath(); ctx.moveTo(px, a.top + 18); ctx.lineTo(px, a.bottom); ctx.stroke();
          ctx.textAlign = "left"; ctx.fillStyle = T.ink; ctx.fillText(m.label, px + 4, a.top + 30);
        }
      } else if (idx.length) {
        ctx.fillStyle = "rgba(248,250,252,0.07)";
        ctx.fillRect(x.getPixelForValue(idx[0]) - half, a.top, x.getPixelForValue(idx[idx.length - 1]) - x.getPixelForValue(idx[0]) + 2 * half, a.bottom - a.top);
      }
      ctx.strokeStyle = T.muted; ctx.setLineDash([2, 4]); ctx.lineWidth = 1;
      const py = y.getPixelForValue(d.alert_threshold);
      ctx.beginPath(); ctx.moveTo(a.left, py); ctx.lineTo(a.right, py); ctx.stroke();
      ctx.restore();
    },
  };
  if (chart) chart.destroy();
  Chart.defaults.font.family = T.font;
  Chart.defaults.color = T.muted;
  chart = new Chart($("replay-chart"), {
    type: "line",
    data: {
      labels: rows.map((r) => r.i),
      datasets: [
        { label: "Old scoring", data: rows.map((r) => r.before), borderColor: T.muted, borderWidth: 1.5, borderDash: [5, 4],
          pointRadius: 0, tension: 0, spanGaps: false },
        { label: "Current scoring", data: rows.map((r) => r.now), borderColor: T.ink, borderWidth: 2, tension: 0, spanGaps: false,
          pointRadius: 4, pointBorderWidth: 1.5, pointBorderColor: rows.map((r) => (r.now !== null && r.now >= d.alert_threshold ? T.signal : T.ink)),
          pointBackgroundColor: rows.map((r) => (r.excluded ? T.bg : r.now !== null && r.now >= d.alert_threshold ? T.signal : T.ink)) },
      ],
    },
    options: {
      responsive: true, maintainAspectRatio: false, animation: false,
      scales: {
        y: { min: 0, suggestedMax: 3, ticks: { stepSize: 1, font: { size: 11 } }, grid: { display: false }, border: { display: false },
             title: { display: true, text: "Score (0 = usual)", font: { size: 11 } } },
        x: { ticks: { font: { size: 11 }, maxRotation: 0, autoSkip: true, maxTicksLimit: 14 }, grid: { display: false }, border: { color: T.line },
             title: { display: true, text: "Session", font: { size: 11 } } },
      },
      plugins: {
        legend: { display: true, labels: { boxWidth: 18, boxHeight: 2, font: { size: 12 } } },
        tooltip: { displayColors: false, backgroundColor: T.surface, borderColor: T.line, borderWidth: 1 },
      },
    },
    plugins: [shade],
  });
}

function summarise(d) {
  if (d.table) {
    $("replay-head").innerHTML = `<tr>${d.table.headers.map((h) => `<th>${esc(h)}</th>`).join("")}</tr>`;
    $("replay-summary").innerHTML = d.table.rows.map((r) => `<tr><td>${esc(r[0])}</td>${r.slice(1).map((c) => `<td class="num">${esc(c)}</td>`).join("")}</tr>`).join("");
    $("replay-note").textContent = "Same simulated person and sessions for both. The current scoring only stops alerting because a person accepted the change; it never decides that itself. One simulated person is an illustration, not evidence. The 300-person figures are on the Evidence page.";
    return;
  }
  $("replay-head").innerHTML = "<tr><th><span class="sr-only">Scoring method</span></th><th>Affected sessions flagged</th><th>False alerts in normal sessions</th></tr>";
  const row = (name, s) => `<tr><td>${esc(name)}</td>
    <td class="num">${s.event_sessions ? `${s.flagged_in_event} of ${s.event_sessions}` : "no change to find"}</td>
    <td class="num">${s.false_alerts} of ${s.normal_sessions}</td></tr>`;
  $("replay-summary").innerHTML = row("Old scoring", d.summary.before) + row("Current scoring", d.summary.now);
  const b = d.summary.before, n = d.summary.now;
  let note = "";
  if (d.scenario === "steady") {
    note = "Nothing changed, so every alert here is a false alarm. A good system raises few.";
  } else if (n.flagged_in_event > b.flagged_in_event) {
    note = "In this run the current scoring kept flagging the change for longer, because flagged sessions did not become the person's new normal.";
  } else if (n.flagged_in_event < b.flagged_in_event) {
    note = "In this run the current scoring flagged fewer of the affected sessions. It is more cautious, and that costs sensitivity. Try other people.";
  } else {
    note = "In this run both flagged the same number of affected sessions. Try a longer slowdown or other random people.";
  }
  $("replay-note").textContent = note + " One simulated person is an illustration, not evidence.";
}

let pending;
async function load() {
  sync();
  const my = (pending = Symbol());
  try {
    const d = await api(`/api/simulate?${params()}`);
    if (my !== pending) return;
    draw(d); summarise(d);
  } catch (err) {
    $("replay-note").textContent = `Could not run the scenario: ${err.message}`;
  }
}

$("scenario").addEventListener("input", () => { $("size").value = $("scenario").value === "equipment" ? 40 : 20; });
["scenario", "size", "length", "seed"].forEach((id) => $(id).addEventListener("input", load));
$("reroll").addEventListener("click", () => { $("seed").value = Math.floor(Math.random() * 10000); load(); });
load();
