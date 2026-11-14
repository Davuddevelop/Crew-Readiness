# Task board

Plan and reasoning: `docs/PLAN_V2.md`. H0 = 2026-11-14 about 20:30 Baku. Deadline H+25 (Nov 15, 21:30). **Feature freeze at H+19.**
Status: `[ ]` open, `[~]` in progress, `[x]` done. Update this file in your PR when you finish a task.

## Phase 0: unblock (first hour)

| ID | Owner | Task | Est. | Done when |
|---|---|---|---|---|
| T0.1 | Davud | Open the official challenge page and paste its text (title, description, any required deliverables, listed resources, judging notes) into `docs/CHALLENGE.md`. Our plan so far rests on secondary sources | 15 min | `docs/CHALLENGE.md` exists, with the URL and the date read |
| T0.2 | Davud | Merge PR #21 (Mission advisory). Production has not rebuilt since the Privacy page: in the Vercel dashboard redeploy `main` and check the project's production branch and Git settings. Then run `python scripts/smoke.py <live URL>` | 30 min | Live Mission page shows a real advisory; smoke passes on the live URL |
| T0.3 | Davud | Add a `LICENSE` file (your choice; MIT is usual). Fill the `[PLACEHOLDERS]` in `docs/SUBMISSION.md` (team name, challenge title from T0.1, repo URL, AI tool name). Name the logo's AI tool in `docs/ASSETS.md` | 30 min | No `[...]` or "NOT STATED" left in those two files |
| T0.4 | Teammate | Read `docs/PLAN_V2.md`, `docs/TASKS.md`, `AGENTS.md`; pull `main`; confirm you can run the app and the tests | 15 min | Tests pass locally |

## Workstreams, owner: Davud + Claude

| ID | Task | Est. | Depends | Done when |
|---|---|---|---|---|
| C1 | **Calibrated personal rarity.** Experiment first: is the conformal p-value of today's score vs the person's own past scores calibrated on simulated crews? If yes, add "a score this high happened in 1 of your last N sessions" to the readiness payload and UI; if no, record that finding and stop | 4 h | none | `ml/calibration.py` with a result; if calibrated, the payload, UI text, tests and docs |
| C2 | **Evidence upgrade.** Calibration table and bootstrap confidence intervals in `ml/export_results.py`, rendered on `/evidence`, with tests tying the numbers to the file | 2.5 h | C1 | `/evidence` shows calibration and intervals; tests pass |
| C3 | **Crew-first "My status" page** (`/me`): own numbers first, rarity in plain words, what you can do next, sharing shown as the person's choice (a proposal) | 3 h | C1 | Page works on desktop and phone; claims test passes |
| C4 | **Pilot analysis and realism check.** `ml/pilot_report.py`; compare real variability with the simulator; fix the simulator if they differ and re-run the benchmark | 2 h | F2 data | A report and, if needed, an updated simulator and results |
| C5 | **Results into the story.** Evidence, Privacy ("what we validated"), Submission, DEMO.md updated with the pilot and calibration numbers; every number from a file, with tests | 2 h | C2, C4, F2 | Pages and docs match the result files |

## Workstreams, owner: teammate + Codex

| ID | Task | Est. | Depends | Done when |
|---|---|---|---|---|
| F1 | **Pilot tooling and protocol.** `docs/PILOT.md` (protocol, consent text, session-order sheet), `scripts/export_pilot.py` (reads `team_test` profiles, exports **aggregate timing numbers only**, pseudonymous, to CSV), a test that the export contains no typed text or names | 2 h | T0.4 | A volunteer can follow `PILOT.md`; the export script runs; tests pass |
| F2 | **Run the pilot (people, not Codex).** 5-8 volunteers, one laptop and keyboard: 8 normal sessions, then 3 perturbed (non-dominant hand, or counting backwards while typing), then 1 normal. Record each volunteer's session order and consent in the sheet. Pseudonyms only | 3 h (parallel with other work) | F1 | Export CSV with at least 5 people x 12 sessions, and the filled sheet, in `docs/pilot/` |
| F3 | **Verified sources (R-2).** `docs/SOURCES.md`: 3-5 sources on behavioural health and performance monitoring in spaceflight and on keystroke or reaction-time monitoring. **A human opens every link and checks every claim before it goes in.** One line each: what they found, how it informed us. Separate their findings from ours | 2 h | T0.1 | Each source verified by a person; nothing cited from memory or from an AI summary |
| F4 | **NASA data feasibility, time-boxed to 90 minutes.** Is there an openly licensed NASA dataset (OSDR and others) with repeated behavioural or performance measures per person (at least 8 sessions each)? Write `docs/DATA_SEARCH.md`. If a clean fit exists, run our detector on it and report; if not, stop and document | 1.5 h | none | `docs/DATA_SEARCH.md` with what was searched, what was found, licence, and a go/no-go |
| F5 | **Accessibility and phone pass** on `/me` and the new Evidence tables (keyboard, focus, 390 px width), with a script like `scripts/check_keyboard.js` | 1.5 h | C2, C3 | The checks pass; fixes merged |
| F6 | **Submission and README rewrite** against the official challenge wording (T0.1). Davud owns the placeholders; you draft the text from the result files | 1.5 h | T0.1, C5 | `docs/SUBMISSION.md` and `README.md` match the challenge and every claim passes `tests/test_claims.py` |

## Together

| ID | Task | Est. | Done when |
|---|---|---|---|
| I1 | Demo script v2 (`docs/DEMO.md`), backup video re-recorded, voice-over | 2 h | Two timed rehearsals under 3:00 |
| I2 | Final pass: `smoke.py` on the live URL, `check_grid.js`, all tests; submit **early** | 1 h | Submitted |

## File ownership (to avoid collisions)

| Area | Owner |
|---|---|
| `app/scoring.py`, `app/readiness.py`, `app/pause_model.py`, `ml/*`, `app/results_data.json`, `/evidence`, new `/me` page and its template/JS | Davud + Claude |
| `docs/PILOT.md`, `docs/pilot/*`, `scripts/export_pilot.py`, `docs/SOURCES.md`, `docs/DATA_SEARCH.md`, `tests/test_pilot_export.py`, `tests/test_sources.py` (if any) | Teammate + Codex |
| `docs/SUBMISSION.md`, `README.md` | Teammate drafts (F6); Davud owns the placeholders |
| `app/templates/about.html` | Teammate (R-1 owner); numbers there are tied to result files by `tests/test_about.py`, so tell Davud when results change |
| `docs/DEMO.md`, `scripts/record_demo.js`, `scripts/smoke.py` | Davud + Claude |
| `app/static/css/style.css`, `app/templates/base.html` | **Shared, careful:** small PRs, pull `main` first |

## Rules for everyone

Read `AGENTS.md`. Small PRs. Tests and `check_grid.js` before each one. Never write that astronauts use it or that it is validated on crews. The pilot is
"a small pilot with deliberate perturbations", the benchmark is "simulated". Say what you could not verify.
