"""Score the shipped median/MAD detector. Run: python -m ml.report_incumbent   (synthetic, illustrative assumptions)"""
from .evaluate import evaluate, incumbent_detector

if __name__ == "__main__":
    print("incumbent median/MAD, step event of 5 sessions, 300 simulated people per row, alert at score >= 1.0")
    print(f"{'slowdown':>9} {'detect/sess':>12} {'caught ppl':>11} {'delay':>6} {'false alerts':>13}")
    for m in (0.0, 0.03, 0.06, 0.10, 0.15, 0.30):
        r = evaluate(incumbent_detector, shape="step", magnitude=m, length=5, n_people=300, seed=7)
        d = "-" if r.median_delay is None else f"{r.median_delay:.0f}"
        print(f"{m:>8.0%} {r.detection_rate:>12.2f} {r.first_alert_rate:>11.2f} {d:>6} {r.false_alert_rate:>13.3f}")
