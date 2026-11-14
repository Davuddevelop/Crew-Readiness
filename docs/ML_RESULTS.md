# ML results: per-person count model for pauses

**Status: measured on SYNTHETIC data only.** Nothing here is evidence about real crews. Every population number and
every event effect is an illustrative assumption (`ml/synth.py`). Reproduce everything with the commands below.

## The question
Today's scoring compares each feature to the person's own median using robust z-scores (median/MAD). We found
that this raises a false alert on about 12-13 % of *normal* sessions (it varies a little with the simulated people) at the YELLOW cutoff, and that **78 % of those
alerts come from `pause_total_ms`**: pauses are small counts (usually 0 or 1), the MAD is often 0, and one ordinary
pause then looks huge. See `python -m ml.diagnose_false_alerts`.

## The change (`app/pause_model.py`)
Score **pause count** with a per-person negative binomial: mean from their own history (shrunk toward a prior),
burstiness estimated from their own history (shrunk, then widened for uncertainty in the mean). Report how
surprising today's count is as a tail probability, turned into the same deviation scale as other features.
**Known loss:** pause *time* (one very long pause) is shown as context but is no longer scored.

## Results (`python -m ml.compare 0.0|0.5|1.5`)
Detection of event sessions at a **fixed 5 % false-alert rate**, 5-session step event, 300 simulated people per cell.

| Slowdown | Pause burstiness | Median/MAD (before) | Gamma-Poisson | Negative binomial (now) |
|---|---|---|---|---|
| 6 % | none | 0.14 | 0.17 | 0.18 |
| 10 % | none | 0.24 | 0.34 | 0.36 |
| 15 % | none | 0.42 | 0.57 | 0.59 |
| 10 % | high (od 1.5) | 0.22 | 0.26 | 0.29 |
| 15 % | high (od 1.5) | 0.39 | 0.47 | 0.53 |

## At the shipped alert level (YELLOW at score >= 1.0, no matching)
`python -m ml.export_results`, 300 simulated people per row, 5-session step event, synthetic.

| Slowdown | Detected before | Detected now | False alerts before | False alerts now |
|---|---|---|---|---|
| 6 % | 0.26 | 0.18 | 11.9 % | 4.7 % |
| 10 % | 0.42 | 0.35 | 13.0 % | 4.7 % |
| 15 % | 0.62 | 0.58 | 12.7 % | 4.8 % |

**This is a trade-off, not a free win.** False alerts fall by about 60 %, and detection also falls (by 0.04 to 0.08).
The fixed-false-alert table above is the fair comparison (the new model is better at every matched rate). The product's
cutoff of 1.0 now sits at a more conservative point on the curve; whether that is the right point is a decision for
the team (decision 3 in `docs/ML_PLAN.md`: what false-alert rate is acceptable to a crew). Lowering the cutoff trades the
false-alert reduction back for detection. After the change, the remaining false alerts are spread evenly across
features (checklist 35 %, typing rhythm 26 %, pauses 20 %, typing variability 19 %), so no single feature dominates.

## Robustness to a wrong assumption (`python -m ml.stress_prior`)
Assumed burstiness prior 0.05 / 0.5 / 2.0, against simulated people whose true burstiness is 0 / 0.5 / 1.5
(10 % slowdown, 5 % false alerts): detection stays 0.35-0.38 / 0.36-0.38 / 0.29 against 0.24 / 0.29 / 0.22 for
median/MAD. The prior washes out because burstiness is learned per person.

## Limits (say these out loud)
1. **Synthetic.** The simulator draws pauses from a Poisson-type process. Real pausing may differ. A public
   dataset check is still open (`docs/ML_PLAN.md`).
2. **Our own benchmark.** We wrote both the generator and the model. The overdispersion and prior tests reduce but do
   not remove that risk.
3. **Modest gains.** Roughly +0.1 detection at equal false alerts in the favourable case, +0.03 to +0.14 when pauses are
   very bursty. Not a breakthrough; a real, reproducible improvement with a stated mechanism.
4. **Not scored any more:** pause time. Long single pauses go unflagged by this model.
5. **Calibration of "1 session in N"** assumes the count model is right; it is an explanation aid, not a guarantee.
6. Detects changes in interaction timing against a person's own history. **Not** fatigue, illness or fitness for duty.

## Public dataset search (2026-11-14): no usable fit, dropped
The plan asked for one public dataset with repeated per-person task timings and a citable licence. What we found,
so nobody repeats it:
- **Sandbox network:** only Hugging Face and a few media hosts are reachable. Zenodo, OSF, PhysioNet, figshare, UCI,
  Kaggle and the CMU keystroke-dynamics page were not.
- **Hugging Face keystroke sets** (e.g. Aalto 136M features): one session per person, so there is no personal history,
  and most carry no licence tag, which means we cannot use them.
- **Closest candidate:** `Emulated-Inc/drowsy-driving-reaction-time-eeg`, a mirror of Cao et al. 2019 (*Scientific Data*
  6:19, doi:10.1038/s41597-019-0027-4), tagged CC BY 4.0. Lane-drift reaction times, 62 sessions. **At most 5 sessions per
  person (most have 2 or 3)**, below our 5-session minimum baseline; 20 sessions are EEG files without a trial table;
  the task is driving, and its framing is drowsiness, which is the claim this project avoids. Not used.
- **Consequence:** every number in this repository is synthetic. If a typing or reaction-time dataset with 10+ sessions
  per person and a licence appears (the CMU keystroke-dynamics benchmark is a plausible candidate; its terms are
  **unverified**), the first use is the false-alert rate on real people with no injected events.

## Reproduce
```
.venv/bin/python -m ml.report_incumbent        # before: detection and false alerts
.venv/bin/python -m ml.diagnose_false_alerts   # why
.venv/bin/python -m ml.compare 0.5             # fixed-false-alert comparison
.venv/bin/python -m ml.stress_prior            # wrong-prior test
CREW_PAUSE_MODEL=robust python run.py          # run the product with the old scoring
```
