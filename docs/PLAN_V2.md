# Plan v2: from "credible finalist" to a top-3 project

Written 2026-11-14 about 20:30 Baku time. Internal deadline: **Nov 15, 21:30 Baku** (about 25 hours; freeze new features about 5 hours before).
Owners: **Davud + Claude** and **the teammate + his Codex agent**. Task board: `docs/TASKS.md`.

## 1. The challenge (verify against the official text first: task T0.1)

**"Create Health Monitoring Software for Astronauts on Space Missions"** (NASA Space Apps 2026,
<https://www.spaceappschallenge.org/2026/challenges/health-monitoring-software/>).

What we know, from secondary pages that reproduce it (NOT the official page, which we could not open): long missions expose crews to
radiation, isolation and confinement, altered gravity and a closed environment, which can contribute to immune changes, bone loss,
cardiovascular events and behavioural problems. The task is software that **gathers health indicators and lets astronauts evaluate and
act on the status of their own health**. Resources named by teams: NASA's Open Science Data Repository (OSDR) and RadLab.
Unknown until we read the official page: exact deliverables, any required data, and the judging notes. **Do not plan around guesses: T0.1 comes first.**

**Competitive picture (public GitHub repos found in one search):** at least six teams are building astronaut health dashboards, mostly
with physiological sensors, an LLM assistant and risk scores. That field is crowded and loud. **Our difference must be stated plainly:**
a behavioural indicator that needs no wearable, runs fully on board, never leaves the device, says honestly when it does not know, and
puts the astronaut, not Earth, first.

## 2. Where we stand against the challenge (honest)

| Challenge asks | Today | Gap |
|---|---|---|
| Gather health indicators | One passive behavioural indicator (typing timing) plus an optional reaction-time check | Thin. Two indicators, not "health" in the medical sense, and we must never claim it is |
| Astronauts evaluate and act on **their own** status | Reviewer-facing dashboard; the astronaut view is only a proposal on the Privacy page | **Biggest relevance gap.** Our product speaks to a reviewer, the challenge to the astronaut |
| Works on missions (autonomy, isolation) | Runs offline, nothing leaves the device (true, but never demonstrated or argued) | Under-sold |
| Use NASA data / resources | None used | Weak. OSDR and RadLab are not a natural fit for timing data. See W3 for the honest path |
| Evidence | Simulated benchmark only | **Biggest validity gap** |

## 3. Scorecard: now and the target, and the lever for each point

Scores are my own judgement as a reviewer (not NASA's), on the usual criteria; treat them as a compass, not a prediction.

| Criterion | Now | Target | The levers (workstreams) |
|---|---|---|---|
| Creativity | 6 | 7-8 | **W1** the alert cutoff set to a *stated false-alert budget* and checked on held-out real people; an honest negative result (personal "rarity" as an alert rule is calibrated but detects less, see `docs/ML_RESULTS.md`); the baseline-poisoning finding and human re-baselining; **W2** crew-first status. Creativity is the criterion we are least sure of reaching 8 |
| Relevance to space | 4 | 8 | **W2** crew-first view (matches "astronauts evaluate and act on their own status"); the on-board/offline argument made concrete; **W5** exact challenge wording and verified NASA sources (R-2); honest positioning as one indicator inside a crew health monitor |
| Impact | 5 | 8 | W2 (the astronaut gets an actionable, private view); fewer false alarms is the practical benefit under limited crew time and comms delay (W1 numbers); a clear "who uses it, when, what changes" story |
| Validity and honesty | 7 | 8+ | **W3** a small **real** pilot with deliberate perturbations (labelled "pilot, not a validation"); **W1b** calibration check and confidence intervals; **W4** compare real variability with the simulator and fix it; keep every limit on the page |

**What would still hold us below 8, so we say it out loud instead of hiding it:** the pilot is small; no astronaut or spaceflight data;
timing is a behavioural proxy, not a health measurement. The score target assumes judges reward calibrated honesty over bigger claims.

## 4. Strategy: "Crew-first, calibrated, validated"

**W1. Alert-budget calibration (Claude).** *Step 1, done (2026-11-14): the gate experiment.* Ranking today's score among the person's own past
scores (a conformal p-value) is calibrated but, with 8 to 20 sessions of history, detects less than a population threshold at the same
false-alert rate, also when people differ in how erratic they are. **Not used to alert; recorded as a negative result** in `docs/ML_RESULTS.md`.
*Step 2, now:* state the false-alert **budget** the shipped YELLOW cutoff stands for (about 1 normal session in 21 on simulated data), calibrate the
cutoff for a chosen budget on pooled normal sessions, and **check it on held-out people** (leave-one-person-out), first on simulated data and
then on the real pilot (W3). If real people are more variable than the simulator, we recalibrate and report both numbers.

**W1b. Evidence upgrade (Claude).** Add the budget-calibration table (target vs observed false-alert rate on held-out people) and bootstrap
confidence intervals over people to `/evidence`.

**W2. Crew-first "My status" (Claude, accessibility pass by the teammate's agent).** A person-centred page: their own numbers first, rarity in
plain words, what they can do next (check-in, optional reaction test, tell the reviewer), and a clear statement that sharing is their choice
(shown as a proposal, as on the Privacy page; we do not build accounts).

**W3. Real pilot (the teammate runs it; Davud helps; Codex builds the tooling).** 5 to 8 volunteers, one laptop and keyboard, about 12 short
sessions each: 8 normal, then 3 deliberately perturbed (non-dominant hand, or counting backwards while typing), then 1 normal. Pseudonyms only,
consent recorded, aggregate timing numbers only. Reported as "a small pilot with deliberate perturbations", never as validation.

**W4. Realism check (Claude, after pilot data).** Compare real session-to-session variability and pause behaviour with the simulator's
assumptions. If they differ, **fix the simulator and re-run the benchmark**, and say what changed. This directly answers "you graded your own homework".

**W5. Mapping and sources (Davud + teammate).** Put the official challenge wording on the submission; verify 3 to 5 sources a human has opened
(R-2) and say how each informed us; rewrite the submission around the challenge. Time-boxed data feasibility (OSDR) in W6.

**W6 (time-boxed, 90 minutes, Codex): NASA data feasibility.** Is there an openly licensed NASA dataset with repeated behavioural or performance
measures per person (at least 8 sessions each)? If yes and it fits cleanly, run our detector on it and report. If not, document the search
(`docs/DATA_SEARCH.md`) and stop. We do not force a fit.

## 5. Schedule (H0 = now; deadline H+25; freeze H+19)

| Hours | Davud + Claude | Teammate + Codex |
|---|---|---|
| H0-1 | T0.1-T0.3: official text, merge #21, redeploy and smoke the live site, LICENSE and placeholders | Read this plan and `docs/TASKS.md`; branch; start F1 and F4 |
| H1-6 | W1 experiment then product; W1b; start W2 | F1 pilot tooling and protocol, F3/W5 sources draft, W6 data search |
| H6-12 | W2; **pilot sessions run (human time, parallel)** | Run the pilot; F5 accessibility pass |
| H12-17 | W4 analysis; W5 results into Evidence, Privacy and Submission | Submission rewrite; README; verify sources |
| H17-19 | Demo script v2; record backup video | Rehearsal 1 |
| **H19 FREEZE** | Bug fixes only | Bug fixes only |
| H19-25 | Rehearsal 2, voice-over, `smoke.py` on the live URL, submit early | same |

## 6. How we work together

- **One topic per branch, small PRs, merge often.** Branch names: `feat/<ID>-short-name`. Open a PR as soon as the task's "done when" is true.
- **File ownership** (to avoid collisions) is in `docs/TASKS.md`. If you must touch a file you do not own, say so in the PR.
- **Before every PR:** `.venv/bin/python -m pytest -q`; with the app running `node scripts/check_grid.js`; and `python scripts/smoke.py`.
- **Honesty rules** are non-negotiable (`AGENTS.md`): no fatigue, illness or fitness-for-duty claims; nothing "validated on crews"; anything from the
  benchmark is "simulated"; the pilot is "a small pilot". Numbers in docs and pages must come from result files, with tests.
- **Say what you could not verify.** A short PR description with checks and limits, like the previous ones.

## 7. Risks and the cut order

| Risk | Mitigation |
|---|---|
| Rarity does not detect enough | **Happened.** Recorded as a negative result; W1 became budget calibration on held-out people |
| Pilot yields too little or noisy data | Report what we have with its limits; it still checks the simulator (W4) |
| Official challenge needs something we lack | T0.1 first; adapt wording, not claims |
| Live site stale or broken | T0.2 now; `smoke.py` on the live URL before every submission step |
| Scope creep | **Cut in this order:** W6, then the optional self-report check-in, then W2 polish. Never cut: W3 pilot, W1b honesty tables, rehearsals, the submission |

## 8. What we will not claim

That it detects fatigue, illness or fitness for duty; that astronauts use it or it is proven in space; that it is validated on crews; that NASA
approved it; that it replaces a flight surgeon. The pilot is "small and deliberate", the benchmark is "simulated", and we say both every time.
