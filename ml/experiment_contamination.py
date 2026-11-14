"""
Does a flagged session poison the person's baseline? EXPERIMENT, not shipped behaviour.
Run: python -m ml.experiment_contamination   (synthetic, illustrative assumptions)

Policies for which past sessions form the baseline:
  keep-all        today's behaviour: every OK session counts, flagged or not
  exclude-flagged sessions scored >= EXCLUDE (while a baseline existed) are left out of future baselines
Event: a SUSTAINED step slowdown (15 sessions). Metric: share of event sessions flagged, by position in the event.
"""
import numpy as np

from app.baseline import compute_baseline, select_baseline_sessions
from app.features import FEATURE_NAMES
from app.pause_model import pause_deviation_nb
from app.scoring import GROUP_WEIGHTS, score_session
from app.tasks import DEFAULT_TASK_TYPE

from .synth import Event, simulate_person

EXCLUDE, ALERT = 1.5, 1.0


def nb_score(pool, today):
    base = compute_baseline(select_baseline_sessions(pool), FEATURE_NAMES, DEFAULT_TASK_TYPE)
    v = score_session({n: today[n] for n in FEATURE_NAMES}, base, today["data_quality"], "nb")
    return v.score if v.status == "SCORED" else None


def run(policy, magnitude, n_people=300, start=15, length=15, n=40, seed=7):
    rng = np.random.default_rng(seed)
    hits = np.zeros(length); cnt = np.zeros(length); fa = tot = 0
    for _ in range(n_people):
        s, t = simulate_person(rng, n, events=(Event("step", start, length, magnitude),))
        pool = []
        for i, sess in enumerate(s):
            sc = nb_score(pool, sess)
            if sc is not None:
                if t[i] > 0:
                    hits[i - start] += sc >= ALERT; cnt[i - start] += 1
                elif i < start:
                    fa += sc >= ALERT; tot += 1
            if policy == "keep-all" or sc is None or sc < EXCLUDE:
                pool.append(sess)
    return hits / np.maximum(cnt, 1), fa / max(tot, 1)


if __name__ == "__main__":
    print("detection by session number inside a 15-session sustained slowdown (alert at 1.0)")
    for mag in (0.10, 0.20):
        for pol in ("keep-all", "exclude-flagged"):
            d, fa = run(pol, mag)
            print(f"{mag:>4.0%} {pol:<16} " + " ".join(f"{d[k]:.2f}" for k in (0, 2, 4, 7, 10, 14)) + f"   false alerts {fa:.3f}")
    print("columns: event session 1, 3, 5, 8, 11, 15")
