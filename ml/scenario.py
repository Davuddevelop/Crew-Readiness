"""
One simulated person, scored two ways, for the Replay page.

  before: the original scoring (median/MAD for every feature, every OK session joins the baseline)
  now:    the product's scoring (per-person count model for pauses, flagged sessions kept out of the baseline)

Both see the same simulated sessions. SYNTHETIC and illustrative: one random person proves nothing; the 300-person
results are on the Evidence page. The dependency points one way: the app imports this lazily, this imports the app.
"""
from __future__ import annotations

import numpy as np

from app.readiness import score_history

from .evaluate import incumbent_detector
from .synth import Event, simulate_person

SCENARIOS = ("steady", "step", "spike", "ramp")
START, N_SESSIONS, ALERT = 15, 40, 1.0
LIMITS = {"magnitude": (0.0, 0.5), "length": (1, 25), "seed": (0, 9999)}


def run_scenario(scenario: str, magnitude: float, length: int, seed: int) -> dict:
    if scenario not in SCENARIOS:
        raise ValueError(f"scenario must be one of {SCENARIOS}")
    events = () if scenario == "steady" else (Event(scenario, START, 1 if scenario == "spike" else length, magnitude),)
    sessions, truth = simulate_person(np.random.default_rng(seed), N_SESSIONS, events=events)
    walked = score_history(sessions, "docking_checklist_v1")

    rows = []
    for i, s in enumerate(sessions):
        before = incumbent_detector(sessions[:i], s)
        view, _b, excluded = walked[i]
        rows.append({"i": i + 1, "event": truth[i] > 0,
                     "before": None if before is None else round(before, 2),
                     "now": None if view.score is None else round(view.score, 2),
                     "excluded": bool(excluded)})

    def summary(key: str) -> dict:
        scored = [r for r in rows if r[key] is not None]
        ev = [r for r in scored if r["event"]]
        normal = [r for r in scored if not r["event"] and r["i"] <= START]      # before the event, so contamination is not counted
        return {"event_sessions": len(ev), "flagged_in_event": sum(r[key] >= ALERT for r in ev),
                "normal_sessions": len(normal), "false_alerts": sum(r[key] >= ALERT for r in normal)}

    return {"synthetic": True, "scenario": scenario, "magnitude": magnitude, "length": length, "seed": seed,
            "alert_threshold": ALERT, "sessions": rows, "summary": {"before": summary("before"), "now": summary("now")}}
