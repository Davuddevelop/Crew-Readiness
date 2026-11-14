/**
 * Gives every table cell its column name (data-label), so that on a phone CSS can show each row as a labelled card
 * instead of a clipped, horizontally scrolling table. Some tables are filled by JavaScript after load, so it re-applies
 * whenever a table body changes. It only adds attributes; it never reads or changes the data.
 */
function label(table) {
  const heads = [...table.querySelectorAll("thead th")].map((th) => th.textContent.trim());
  table.querySelectorAll("tbody tr").forEach((tr) => {
    [...tr.children].forEach((td, i) => { if (heads[i] && td.getAttribute("data-label") !== heads[i]) td.setAttribute("data-label", heads[i]); });
  });
}
document.querySelectorAll("table.evidence").forEach((table) => {
  label(table);
  const body = table.querySelector("tbody");
  if (body) new MutationObserver(() => label(table)).observe(body, { childList: true });
});
