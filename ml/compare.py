"""
Fair comparison: raw thresholds are not comparable across scoring scales, so we compare detection at
EQUAL false-alert rates. Run: python -m ml.compare   (synthetic, illustrative assumptions)
"""
import numpy as np

from .candidates import candidate_nb, candidate_pause_model
from .evaluate import incumbent_detector
import sys

from .synth import Event, PopulationSpec, simulate_person

DETECTORS = {"incumbent": incumbent_detector, "gamma-poisson": candidate_pause_model, "neg-binomial": candidate_nb}
TARGET_FAR = (0.02, 0.05, 0.10)
START, N_SESS, N_PEOPLE = 15, 40, 300
OD = float(sys.argv[1]) if len(sys.argv) > 1 else 0.0   # pause overdispersion of the SIMULATED people


def collect(det, magnitude, seed):
    rng = np.random.default_rng(seed)
    ev = Event("step", START, 5, magnitude)
    normal, event = [], []
    for _ in range(N_PEOPLE):
        s, t = simulate_person(rng, N_SESS, PopulationSpec(pause_overdispersion=OD), events=(ev,))
        for i in range(N_SESS):
            sc = det(s[:i], s[i])
            if sc is None:
                continue
            if t[i] > 0:
                event.append(sc)
            elif i < START:
                normal.append(sc)
    return np.array(normal), np.array(event)


if __name__ == "__main__":
    print(f"detection of event sessions at a FIXED false-alert rate (step event, 5 sessions; simulated pause overdispersion={OD})")
    print(f"{'slowdown':>9} {'false alerts':>13} " + " ".join(f"{n:>14}" for n in DETECTORS))
    for m in (0.03, 0.06, 0.10, 0.15):
        data = {n: collect(d, m, 7) for n, d in DETECTORS.items()}
        for far in TARGET_FAR:
            cells = []
            for n in DETECTORS:
                normal, event = data[n]
                th = np.quantile(normal, 1 - far)          # threshold that gives this FAR on normal sessions
                cells.append(f"{np.mean(event > th):>14.2f}")
            print(f"{m:>8.0%} {far:>13.0%} " + " ".join(cells))
