"""Why does the incumbent false-alarm? Event-free people only. Run: python -m ml.diagnose_false_alerts"""
import numpy as np

from app.baseline import compute_baseline, select_baseline_sessions
from app.features import FEATURE_NAMES
from app.scoring import SCORED_FEATURES, score_session
from app.tasks import DEFAULT_TASK_TYPE

from .evaluate import incumbent_detector
from .synth import simulate_person

rng = np.random.default_rng(11)
rows = []   # (history_len, score, top_feature)
for _ in range(400):
    s, _t = simulate_person(rng, 40)
    for i in range(5, 40):
        hist = s[:i]
        base = compute_baseline(select_baseline_sessions(hist), FEATURE_NAMES, DEFAULT_TASK_TYPE)
        v = score_session({n: s[i][n] for n in FEATURE_NAMES}, base, "ok")
        top = max(v.deviations, key=lambda d: d.deviation).feature if v.deviations else None
        rows.append((i, v.score, top))

sc = np.array([r[1] for r in rows]); n = np.array([r[0] for r in rows])
print("A) false-alert rate vs alert threshold (all event-free sessions)")
for th in (0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5):
    print(f"   score >= {th:<4}: {np.mean(sc >= th):.3f}")
print("\nB) false-alert rate at 1.0 vs sessions of history")
for lo, hi in ((5, 8), (8, 12), (12, 20), (20, 40)):
    m = (n >= lo) & (n < hi); print(f"   history {lo:>2}-{hi-1:<2}: {np.mean(sc[m] >= 1.0):.3f}  (n={m.sum()})")
print("\nC) which feature drives the alerts at >= 1.0")
from collections import Counter
c = Counter(r[2] for r in rows if r[1] >= 1.0); tot = sum(c.values())
for f, k in c.most_common(): print(f"   {f:<30} {k/tot:.2f}")
