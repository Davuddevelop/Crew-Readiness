/**
 * "Prepare a summary for the ground" (plan v4, W3): store and forward. It builds a plain-text summary ON THIS DEVICE from what the Mission page
 * already shows, and offers it to copy or save. It makes NO network request and stores nothing; a person decides what to send, when, and how.
 */
const $ = (id) => document.getElementById(id);
const lines = (el) => [...el.querySelectorAll("li")].map((li) => `- ${li.textContent.trim()}`);

function build() {
  const level = ($("advisory").querySelector(".chip") || {}).textContent || "unknown";
  const watch = ($("watchdog-body").querySelector(".chip") || {}).textContent || "unknown";
  const out = [
    "CREW READINESS: SUMMARY FOR THE GROUND",
    "Prepared on board by a person from the Mission page; the software did not send it.",
    `Prepared: ${new Date().toLocaleString()}`,
    `${$("mission-name").textContent.trim()} (${$("tminus").textContent.trim()}); ${$("mission-op").textContent.trim()}`,
    "",
    `SUGGESTION: ${level.trim()}`, ...lines($("advisory")),
    "",
    `CHECK-INS: ${watch.trim()}`, ...lines($("watchdog-body")),
    "",
    "WHAT THIS IS: advisory only. It compares each person's task-interaction timing with their own earlier sessions. It is not a medical assessment and says nothing about fatigue, illness or fitness for duty.",
    "It is a prototype tested on simulated data and a very small volunteer check; the crew in this demonstration is fictional.",
  ];
  return out.join("\n");
}

function say(msg) { $("ground-status").textContent = msg; }

$("ground-make").addEventListener("click", () => {
  $("ground-text").value = build();
  $("ground-out").hidden = false;
  say("Built on this device. Nothing was sent.");
});
$("ground-copy").addEventListener("click", async () => {
  try { await navigator.clipboard.writeText($("ground-text").value); say("Copied. Send it when a link window opens."); }
  catch { $("ground-text").select(); say("Could not copy automatically. The text is selected: copy it yourself."); }
});
$("ground-save").addEventListener("click", () => {
  const url = URL.createObjectURL(new Blob([$("ground-text").value], { type: "text/plain" }));
  const a = Object.assign(document.createElement("a"), { href: url, download: "crew-readiness-summary-for-the-ground.txt" });
  document.body.appendChild(a); a.click(); a.remove(); URL.revokeObjectURL(url);
  say("Saved as a text file on this device. Nothing was sent.");
});
