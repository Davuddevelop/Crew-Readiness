# Pilot results (task F2/C4): two volunteers, one laptop

**What this is:** a feasibility check, not validation. Two volunteers (`pilot-01`, `pilot-02`), one laptop and keyboard, 12 recorded
sessions each of the typed checklist. Files: `docs/pilot/pilot_sessions.csv` (the export, aggregate timing numbers only) and
`docs/pilot/session_sheet.csv` (the labels). Analysis: `python -m ml.pilot_report` writes `docs/pilot/pilot_report.json`, which the
Evidence page renders. Nothing below was edited by hand.

## What happened (deviations from `docs/PILOT.md`, recorded as they occurred)
- `pilot-01` did the changed sessions as **8, 9, 10** (the plan said 9 to 11), so had 7 normal sessions before them, and the sheet marks
  session 12 with issue `other` (no detail recorded).
- `pilot-02` did the changed sessions as 9, 10, 11 as planned.
- Labels were kept exactly as written on the sheet. We did not relabel anything after seeing the data.

## Results (the shipped YELLOW cutoff, 1.0)
| | Flagged | Note |
|---|---|---|
| Normal sessions scored (sessions 6 onward) | 0 of 8 | the first five sessions per person are CALIBRATING |
| Sessions recorded as changed | 5 of 6 | non-dominant hand 3 of 3; counting backwards 2 of 3 |

- All five flagged changed sessions scored about 1.8 to 1.9: YELLOW, never RED.
- **The miss:** `pilot-02` session 9 is labelled "counting backwards" but its timing is indistinguishable from normal
  (median 98.5 ms between keys, against about 100 ms usually, and a normal duration). Either counting did not affect typing in that
  session or it was not done; we cannot tell. It is counted as a miss.
- Typing slowed by about 2.4 times in the flagged sessions, far larger than the 6 to 15 % slowdowns in the simulated benchmark. This
  pilot therefore says nothing about how small a change the tool can find.

## Is the simulator realistic? Partly not
- Each volunteer's typical time between keys was about 99 ms (single sessions 86 to 116 ms) against 145 to 230 ms assumed; real people paused (gaps of 2 s or more) about
  0.0 to 0.1 times per session against 0.4 to 1.2 assumed. With pauses almost always zero for these typists, the pause part of the
  score (30 % of the weight) contributed nothing here.
- Session-to-session variability of checklist response time came out 2.4 times the assumed value, but that is driven by one first
  session (`pilot-01` session 1, 1885 ms against about 700 ms usually; the practice run did not fully remove the first-session
  effect). Leaving first sessions out (an exploratory, after-the-fact choice) gives values below the assumed ones instead. With
  two people we do not re-tune the simulator; we report the gap and keep the benchmark as it was.

## Limits
Two volunteers, one laptop, a typed checklist, deliberate and large changes, labels not blinded to the volunteer, 8 normal and 6
changed scored sessions. Intervals are wide (the report shows them). Not astronauts or crew; nothing about fatigue, illness or fitness
for duty. Not enough people for the held-out alert-budget calibration (it needs 5).

## What we would do next
More volunteers; smaller, graded changes; check whether a different weighting helps typists who rarely pause.
