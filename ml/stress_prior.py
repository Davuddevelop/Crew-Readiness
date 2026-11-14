"""
Is the negative-binomial win robust to a WRONG dispersion prior? Run: python -m ml.stress_prior
Rows: the prior we ASSUME. Columns: how bursty the simulated people REALLY are.
Cell: detection of event sessions at 5% false alerts (10% slowdown, 5-session step). Synthetic, illustrative.
"""
import numpy as np

from . import candidates
from .compare import collect
from .evaluate import incumbent_detector

TRUE_OD = (0.0, 0.5, 1.5)
PRIORS = (0.05, 0.5, 2.0)
FAR, MAG = 0.05, 0.10


def det_at_far(det, od, seed=7):
    normal, event = collect(det, MAG, seed, od)
    return float(np.mean(event > np.quantile(normal, 1 - FAR)))


if __name__ == "__main__":
    print(f"{'assumed prior':>14} | " + " ".join(f"true od={od:<4}" for od in TRUE_OD))
    print(f"{'incumbent':>14} | " + " ".join(f"{det_at_far(incumbent_detector, od):>11.2f}" for od in TRUE_OD))
    for p in PRIORS:
        candidates.pause_model.PRIOR_DISPERSION = p
        print(f"{'nb prior ' + str(p):>14} | " + " ".join(f"{det_at_far(candidates.candidate_nb, od):>11.2f}" for od in TRUE_OD))
