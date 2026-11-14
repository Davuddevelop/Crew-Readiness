# Demo script (3 minutes) and Q&A

For the NASA Space Apps judges. Everything below is something the product really does today. Numbers are from the
benchmark on **simulated** crews (`/evidence`, `docs/ML_RESULTS.md`); say "simulated" every time you quote one.

## The one-sentence pitch
> Crew Readiness compares how each person works with *their own* usual pattern, and puts a change in front of a human before a critical operation. It never reads what is typed, it never decides, and we show where it is worse as well as better.

## Before you start (5 minutes, do it twice)
1. `python run.py` (local, no internet needed; the app makes no external calls).
2. `flask --app run reset-demo` for a clean demo crew. Open `http://127.0.0.1:5050/`.
3. Open `/replay` once so the chart library is cached (it is local, but it loads faster the second time). Browser zoom 100 %, full screen.
4. Keep a second tab on `/evidence`. Keep a terminal ready with `python scripts/demo_flag_pilot.py`.
5. Hosted copy (`crew-readiness-mu.vercel.app`) works but its database resets itself (decision D-8). Use local for the demo.

## The walkthrough (3:00), version 2

About 150 spoken words per minute; clicks take about 15 s in total. Rehearse it aloud twice; cut a sentence rather than rush.

| Time | Page | Say | Show |
|---|---|---|---|
| 0:00 | `/` landing | "On a long mission the ground may be minutes away, and someone still has to decide who does a critical task. People differ: 220 ms between keys is normal for one person and a big change for another. So we compare each person only with themselves, and a human decides." | The poster. Move toward the gap: the hands lean in and never touch. "The system never closes that gap. A person does." |
| 0:20 | `/me` | "The crew member sees their own status first, on their own device, in plain words, and what they can do next." | The sentence, the actions and the "who sees this" proposal. |
| 0:40 | `/dashboard` | "Pilot Okafor is YELLOW. This is an illustrative seeded case, not a measure of how well it works. It is not a diagnosis: two pauses against a usual 0.7, which we would expect about one session in nine. Read the number on screen." | Click the pilot; read the pause reason; point at "Advisory only". |
| 1:05 | `/mission` then `/brief` | "Before a critical operation the system suggests a check-in and says why. It never assigns or clears anyone. This is the page a reviewer holds: reasons, what it cannot tell you, and a blank record they fill in by hand. Nothing is stored." | Mission advisory, open the brief, point at the "cannot tell you" list and the checkboxes. |
| 1:35 | `/replay` | "Space has its own problem: gloves or a different device make someone slower for good. Both methods flag it. A person accepts it as their new normal, and then repeated alerts fall, and a later real slowdown is still caught. It only stops because a human accepted." | Choose **New equipment**. Point at the band, the "accepted" line, the later band, then the table. Press **New random person** once: "one person is an illustration." |
| 2:10 | `/evidence` | "The proof is 300 simulated people per row. False alerts fall from about 13 % to about 5 %. We pay for it: detection also falls, from 0.42 to 0.35 at a 10 % slowdown. **[If the pilot ran, add one line from `docs/pilot/pilot_report.json`: 'In a pilot with N volunteers on one laptop, X of Y deliberate changes were flagged and Z of W normal sessions. That is a feasibility check, not validation.']** And this box lists what we did not show." | Operating-point table, then the pilot section if it is there, then "What this does not show". |
| 2:40 | `/about` | "It runs with no network: this button lists every file the page loaded and none came from elsewhere. Turn off Wi-Fi and it still works." | Press **List what this page loaded**. |
| 2:50 | close | "A prototype for on-board decision support, tested only on simulated data and a small volunteer check. Next: real repeated-session data. It detects changes, never fatigue, and a human decides." | Back to the landing poster. |

Spoken numbers must be read off the screen on the day (they come from `app/results_data.json` and the pilot report), not from this table.

### Extended version (3:45): add the live-capture step
Insert after the dashboard: `/monitor`, choose a crew member (not the pilot), **Start task**, type the checklist (about 25 s at
normal speed), stop at the review step. Say: "Only timing numbers leave the browser. Never what you type." Show the payload
preview: nine numbers, a profile id and a task type, and no text. Click **Discard**. The dry run confirmed that neither the
preview nor the data actually sent contains any typed phrase.

## Backup video and a pre-flight check
- **Backup video** (if the live demo fails): `scripts/record_demo.js` drives the real app through this walkthrough and burns in captions
  made from the "Say" lines; numbers in them are read from the live page and from `app/results_data.json`. It records against a
  throwaway database so the pilot starts in the real demo state. Usage is in the file header. It has no voice-over: add your own
  or present over it.
- **Pre-flight / pre-submission check:** `python scripts/smoke.py [URL]` visits every page of a running copy (local or deployed),
  checks the API contract, confirms typed text is rejected, and scans the page text for claims we ruled out. Exit code 1 means
  something is wrong. Run it against the deployed URL the night before.

## What we claim, and what we do not
**We claim:** it detects changes in interaction timing against a person's own history, privately, and puts them in front of a human. On simulated data the count model for pauses cuts false alerts by about 60 % at the shipped level, and keeping flagged sessions out of the baseline stops a sustained change from being absorbed.

**We do not claim:** fatigue, illness, cognitive state or fitness for duty detection; validation on real crews or astronauts; NASA approval or endorsement; that the thresholds are clinical (they are illustrative).

## Hard questions, honest answers
- **"How is this different from a health dashboard or a wearable?"** It uses no sensors and no health data. It compares a person's own task-interaction timing with their own earlier sessions, entirely on the device, and leaves meaning to a human. That is also why it makes no health claim.
- **"Why gloves?"** It is an illustrative equipment change, not a measurement. The point is that a change in timing is not always about the person, so a human can accept it as the new normal. The size and timing in the simulation are our assumptions.
- **"Is this actually for astronauts?"** Not yet. It is a prototype for on-board decision support on computer-based procedure work, using a typed checklist as a stand-in task, tested only on simulated data. Real conditions (tablets, gloves, shared devices, microgravity, a different keyboard or time of day) are untested, and real use would need crew consent and clear rules on who sees what. One property that does suit space: it runs fully offline and sends nothing off the device.
- **"Is this validated on astronauts?"** No. Everything is synthetic or a fictional crew. We looked for a licensed public dataset with enough repeated sessions per person and found none we could use (`docs/ML_RESULTS.md`). The next step is real validation.
- **"You wrote the simulator and the model. Isn't that circular?"** Partly, yes. We reduced it: pauses are tested at several burstiness levels, and the model still wins when its assumption is wrong. It remains a simulation.
- **"Detection went down."** Yes, at the shipped alert level. We trade some sensitivity for far fewer false alarms, because a crew learns to ignore a system that cries wolf. The fair comparison (matched false alerts) favours the new model. The cut-off is a team decision, not a law.
- **"Why not detect fatigue?"** We cannot validate it, and a wrong claim about fitness for duty is worse than none. We detect *change* and leave interpretation to a human.
- **"What about privacy?"** Typed text, key identities and raw timelines never leave the browser; the server rejects them and the database has no column for them. Tested.
- **"Why do flagged sessions stay out of the baseline?"** Otherwise a sustained slowdown becomes the new normal and the alerts fade (0.88 to 0.07 by the 15th affected session in simulation; 0.40 with the fix). A person can accept a genuine new normal.
- **"Pause time is no longer scored."** Correct, a known loss: one very long pause can go unflagged. It is shown as context.
- **"Where do NASA data or APIs come in?"** The method does not need any. The glove image is NASA's (credit on the page). Real validation could use NASA human-research data if we can get access; we have not requested any.

## If something breaks
- Page blank or chart missing: reload; the app needs no network. Check the terminal for the server.
- Wrong crew states: `flask --app run reset-demo`, reload.
- Replay shows an error: the page says so; use `/evidence` instead and describe the same result.
- Never improvise a claim. If asked something not covered here, say what we measured and what we did not.
