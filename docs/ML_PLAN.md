# ML plan: from "median and MAD" to a model we can defend

Scope (decided with the team lead): **personal-baseline model**, evaluated on **synthetic crews with injected drift plus one public dataset**, crew health / human factors challenge. Deadline: internal Nov 15 21:30.

## The claim we are allowed to make
"Given a person's own history, the system flags sessions whose interaction timing departs from *their* pattern, with calibrated uncertainty, for a human to review." We never claim fatigue, illness or fitness for duty. No astronaut data exists for us, so every number below comes from synthetic or public data and is labelled that way.

## Rule 0: evaluation before modelling
A model nobody can score is a demo. Build the benchmark first; every candidate (including today's median/MAD) is judged on it.

**Synthetic crews (ground truth we control).** For each simulated person: a personal baseline for the 9 features, session-to-session noise, a slow drift (learning effect), and *injected events* with known start, size and shape (step change, ramp, single spike, interruption). Because we inject the events, we know the truth.

**Metrics** (report all, on held-out simulated crews, several random seeds):
- detection rate by event size (a curve, not one number)
- false-alert rate per 100 normal sessions (alert fatigue is the real cost)
- detection delay in sessions
- calibration: when the system says 80% likely, is it right about 80% of the time?
- behaviour with 3 to 5 sessions of history (the cold start we already handle with CALIBRATING)

**Baselines to beat:** (a) today's median/MAD score, (b) a fixed threshold on raw typing speed. If a fancier model does not beat (a), we say so and keep (a). That is a legitimate, credible result.

## Candidate models (you choose and defend one, two at most)
Each is per person, small, explainable, and trainable on tens of sessions:
1. **Robust z with shrinkage:** shrink a new person's baseline toward the crew's, so 4 sessions of history are less noisy.
2. **Change-point detection** (CUSUM / Bayesian online change-point): flags *when* a shift began, not only that today is odd.
3. **Probabilistic baseline** (e.g. per-feature Student-t or a small Gaussian-process / state-space model with drift): gives a predictive distribution, so "how surprising is today" is a probability with an interval.

## Public dataset (searched 2026-11-14: none usable, dropped; see docs/ML_RESULTS.md)
Find one with repeated reaction-time or task-performance measures per person over days, **with a licence we can cite**. Candidates to *verify*, not assume: published psychomotor-vigilance (PVT) datasets, NASA's MATB-II task environment (NASA-developed; check redistribution terms), NASA Life Sciences Data Archive (access is request-based, so probably too slow). Record source, licence and checksum in `docs/ASSETS.md`-style provenance. If nothing clean turns up by hour ~8, we drop it and say synthetic only. Do not use data we cannot license.

## NASA APIs: where they honestly fit
The feature set does not need any. Optional context that is real and low risk: a mission timeline view fed by public NASA data (e.g. ISS position / crew schedule context) as *display context only*. Not needed for the ML claim; add only if time remains.

## Schedule (about 35 h)
| When | Output | Owner |
|---|---|---|
| H0-6 | Synthetic generator + metrics harness + score of today's baseline | Member 2 with review |
| H6-8 | Public dataset found and licensed, or dropped | Member 4 |
| H8-20 | One candidate model, run through the harness, results table | Member 2 |
| H20-26 | Wire the winner into `readiness.py`; show uncertainty and "why" in the UI | Member 1 / 3 |
| H26-35 | Honest results page, limits, demo script, rehearsal | all |

## Decisions that are yours (write the answer in this file)
1. Which candidate model, and why does it suit 5-20 sessions of data?
2. What event shapes and sizes are *realistic* for the injected drift? Justify from literature, not from what makes the demo look good.
3. What false-alert rate is acceptable to a crew, and why?
4. ~~Should flagged sessions be excluded from future baselines?~~ **Decided (team lead): yes, and a human accepts a genuine new normal.** Implemented; evidence in `docs/ML_RESULTS.md`.
