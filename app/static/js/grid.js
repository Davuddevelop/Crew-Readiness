/**
 * Dev aid for the Swiss grid: open any page with ?grid to overlay the 12 columns
 * (4 on narrow screens). Everything on the page should start and end on a column edge.
 * Nothing else depends on this file.
 */
if (new URLSearchParams(location.search).has("grid")) {
  const wrap = document.createElement("div");
  wrap.className = "gridviz";
  wrap.innerHTML = `<div class="page" style="height:100%"><div class="grid">${"<i></i>".repeat(12)}</div></div>`;
  document.body.appendChild(wrap);
}
