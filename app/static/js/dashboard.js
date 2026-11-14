/**
 * Dashboard: crew cards + detail panel (advisory, reasons, trend, evidence).
 * Owner: Member 3 (Frontend & UX).
 *
 * Data comes from GET /api/readiness and GET /api/readiness/<id>
 * (shapes documented in docs/DATA_CONTRACT.md).
 */
import { api, bandChip, esc, timeAgo } from "./common.js";

const grid = document.getElementById("crew-grid");
const detail = document.getElementById("detail");
let chart = null;

function card(entry) {
  const p = entry.profile;
  const r = entry.readiness;
  const score = r.status === "SCORED"
    ? `<div class="score">${r.score.toFixed(2)}<span class="unit"> robust SD</span></div>`
    : `<div class="score muted">${r.baseline_n}/${r.baseline_needed}<span class="unit"> baseline sessions</span></div>`;
  const topReason = r.reasons[0] || r.advisory;
  const synthetic = entry.latest_session?.source === "synthetic"
    ? `<span class="tag">synthetic data</span>` : "";
  return `
    <button class="crew-card band-${esc((r.band || "none").toLowerCase())}" data-id="${esc(p.id)}">
      <div class="card-top">
        <div>
          <div class="name">${esc(p.display_name)}</div>
          <div class="muted small">${esc(p.mission_role)} · ${p.kind === "demo" ? "fictional" : "team test"} ${synthetic}</div>
        </div>
        ${bandChip(r)}
      </div>
      ${score}
      <div class="small">Confidence: <strong>${esc(r.confidence)}</strong> · last task ${esc(timeAgo(entry.latest_session?.created_at))}</div>
      <p class="small card-reason">${esc(topReason)}</p>
    </button>`;
}

async function loadGrid() {
  try {
    const { crew } = await api("/api/readiness");
    grid.innerHTML = crew.map(card).join("");
    grid.querySelectorAll(".crew-card").forEach((el) =>
      el.addEventListener("click", () => loadDetail(el.dataset.id)));
    const wanted = new URLSearchParams(location.search).get("crew");
    if (wanted) loadDetail(wanted);
  } catch (err) {
    grid.innerHTML = `<p class="error">Could not load crew: ${esc(err.message)}</p>`;
  }
}

function renderTrend(trend) {
  // TODO(F-2, Member 3): this is a minimal chart. Ideas: tooltips with the
  // reasons, a marker on the latest session, synthetic vs live styling.
  const ctx = document.getElementById("trend-chart");
  const points = trend.filter((t) => t.score !== null);
  const bandsPlugin = {
    id: "bands",
    beforeDraw(c) {
      const { ctx: g, chartArea: a, scales: { y } } = c;
      if (!a) return;
      const fill = (from, to, color) => {
        const top = y.getPixelForValue(Math.min(to, y.max));
        const bottom = y.getPixelForValue(Math.max(from, y.min));
        g.fillStyle = color;
        g.fillRect(a.left, top, a.right - a.left, bottom - top);
      };
      fill(0, 1, "rgba(34,197,94,0.10)");
      fill(1, 2, "rgba(245,158,11,0.12)");
      fill(2, 4, "rgba(239,68,68,0.12)");
    },
  };
  if (chart) chart.destroy();
  chart = new Chart(ctx, {
    type: "line",
    data: {
      labels: points.map((t) => new Date(t.created_at).toLocaleDateString(undefined, { month: "short", day: "numeric" })),
      datasets: [{
        label: "Deviation score",
        data: points.map((t) => t.score),
        borderColor: "#93c5fd",
        pointBackgroundColor: points.map((t) => ({ GREEN: "#22c55e", YELLOW: "#f59e0b", RED: "#ef4444" }[t.band])),
        pointRadius: 5,
        tension: 0.25,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      scales: {
        y: { min: 0, max: 3, ticks: { color: "#94a3b8" }, grid: { color: "rgba(148,163,184,0.15)" } },
        x: { ticks: { color: "#94a3b8" }, grid: { display: false } },
      },
      plugins: { legend: { display: false } },
    },
    plugins: [bandsPlugin],
  });
}

function fmt(value, unit) {
  return unit === "ms" ? `${Math.round(value)} ms` : `${Math.round(value * 10) / 10}`;
}

async function loadDetail(profileId) {
  try {
    const data = await api(`/api/readiness/${encodeURIComponent(profileId)}`);
    const p = data.profile;
    const r = data.readiness;
    detail.hidden = false;
    document.getElementById("detail-name").textContent = p.display_name;
    document.getElementById("detail-meta").textContent =
      `${p.mission_role} · baseline from ${r.baseline_n} session(s) · confidence ${r.confidence}` +
      (data.latest_session?.data_quality === "low" ? " · latest session flagged LOW quality" : "");
    document.getElementById("detail-chip").innerHTML = bandChip(r);
    document.getElementById("detail-advisory").textContent = r.advisory;
    document.getElementById("detail-disclaimer").textContent = r.disclaimer;
    document.getElementById("detail-reasons").innerHTML = r.reasons.length
      ? r.reasons.map((x) => `<li>${esc(x)}</li>`).join("")
      : `<li class="muted">No signal is notably different from usual.</li>`;
    document.getElementById("detail-evidence").innerHTML = r.deviations.map((d) => `
      <tr>
        <td>${esc(d.label)}</td>
        <td>${fmt(d.value, d.unit)}</td>
        <td>${fmt(d.baseline_median, d.unit)}</td>
        <td>${d.z >= 0 ? "+" : ""}${d.z.toFixed(1)} SD</td>
        <td>${d.deviation.toFixed(2)}</td>
      </tr>`).join("") || `<tr><td colspan="5" class="muted">Not enough baseline sessions yet.</td></tr>`;
    renderTrend(data.trend);
    detail.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (err) {
    detail.hidden = false;
    document.getElementById("detail-advisory").textContent = `Could not load: ${err.message}`;
  }
}

loadGrid();
