/**
 * "Check it yourself": lists what THIS page loaded (the browser's own record of every file it fetched) and whether each came
 * from this device's origin. It makes no request of its own; it only reads performance entries.
 */
import { esc } from "./common.js";

const KINDS = { script: "Scripts", css: "Styles", link: "Styles", img: "Images", font: "Fonts", fetch: "Data (this app's API)",
  xmlhttprequest: "Data (this app's API)", navigation: "The page itself" };

function run() {
  const entries = [...performance.getEntriesByType("navigation"), ...performance.getEntriesByType("resource")];
  const groups = new Map();
  let outside = 0;
  for (const e of entries) {
    const kind = KINDS[e.initiatorType] || "Other";
    const g = groups.get(kind) || { total: 0, local: 0, other: 0 };
    const local = new URL(e.name, location.href).origin === location.origin;
    g.total += 1; g[local ? "local" : "other"] += 1;
    if (!local) outside += 1;
    groups.set(kind, g);
  }
  document.getElementById("netcheck-rows").innerHTML = [...groups].map(([k, g]) =>
    `<tr><td>${esc(k)}</td><td class="num">${g.total}</td><td class="num">${g.local}</td><td class="num">${g.other}</td></tr>`).join("");
  document.getElementById("netcheck-out").hidden = false;
  document.getElementById("netcheck-note").textContent = outside === 0
    ? `${entries.length} files loaded, all from this device (${location.host}). Nothing came from elsewhere.`
    : `${outside} of ${entries.length} files came from elsewhere. That should not happen: please report it.`;
}

document.getElementById("netcheck-run").addEventListener("click", run);
