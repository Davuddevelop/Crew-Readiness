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

## The walkthrough (3:00)

Timed from a scripted dry run (2026-11-14): the spoken lines below are about 150 words per minute worth, the clicks take
about 10 s in total, and the rest is breathing room. Reading it aloud once should land near 3 minutes.

| Time | Page | Say | Show |
|---|---|---|---|
| 0:00 | `/` landing | "People differ: 220 ms between keys is normal for one person and a big change for another, so one threshold for everyone fits nobody. We compare each person only to themselves, and a human decides." | The poster. Move the mouse toward the gap between the hands: they lean in and never touch. Say: "the system never closes that gap; a person does." |
| 0:20 | `/dashboard` | "Pilot Okafor is YELLOW. This is an illustrative seeded case: it shows what a flag looks like, not how well the model works. It is not a diagnosis, it is a change from *their own* pattern. And the system explains itself in plain words: two pauses against a usual 0.7, which we would expect only about one session in nine (read the number on screen)." | Click the pilot. Read the pause reason aloud. Point at the stacked sessions (flat line = usual) and at "Advisory only". |
| 0:55 | `/replay` | "Here is the idea in motion, on a simulated person. They get 20 % slower for 15 sessions, shaded here. The dashed grey line is the old scoring. It learns the slowdown as normal, so its alerts fade. The white line is the current scoring: flagged sessions stay out of the baseline, so the change keeps showing. Now a different random person. Single runs vary, and sometimes the old scoring does as well. The proof is not one run." | Sustained slowdown. Press **New random person** twice. Point at the table under the chart. |
| 1:50 | `/evidence` | "The proof is 300 simulated people per row. At the level the product uses, false alerts fall from about 13 % to about 5 %. We pay for it: detection also falls, from 0.42 to 0.35 at a 10 % slowdown. At matched false-alert rates the new model is better everywhere. And this box lists what we did not show: simulated data only, no real crews." | The two result tables, then the "What this does not show" box. |
| 2:35 | `/dashboard` | "When a person genuinely changes, say a new keyboard, a human accepts the new normal. We never decide that for them." | Run `python scripts/demo_flag_pilot.py`, refresh: **Review needed**. Click **Accept as new normal**, confirm: status becomes CALIBRATING. Say: "Next: validate on real repeated-session data with a licence we can cite. We have not done that yet, and the page says so." |

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
