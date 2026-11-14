# ML results: per-person count model for pauses

**Status: measured on SYNTHETIC data only.** Nothing here is evidence about real crews. Every population number and
every event effect is an illustrative assumption (`ml/synth.py`). Reproduce everything with the commands below.

## The question
Today's scoring compares each feature to the person's own median using robust z-scores (median/MAD). We found
that this raises a false alert on roughly 12 % of *normal* sessions at the YELLOW cutoff, and that **78 % of those
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

## Reproduce
```
.venv/bin/python -m ml.report_incumbent        # before: detection and false alerts
.venv/bin/python -m ml.diagnose_false_alerts   # why
.venv/bin/python -m ml.compare 0.5             # fixed-false-alert comparison
.venv/bin/python -m ml.stress_prior            # wrong-prior test
CREW_PAUSE_MODEL=robust python run.py          # run the product with the old scoring
```
