"""
One simulated person, scored two ways, for the Replay page.

  before: the original scoring (median/MAD for every feature, every OK session joins the baseline)
  now:    the product's scoring (per-person count model for pauses, flagged sessions kept out of the baseline)

Both see the same simulated sessions. SYNTHETIC and illustrative: one random person proves nothing; the 300-person
results are on the Evidence page. The dependency points one way: the app imports this lazily, this imports the app.
"""
from __future__ import annotations

import numpy as np

from app.readiness import _pending_run, score_history

from .evaluate import incumbent_detector
from .synth import Event, simulate_person

SCENARIOS = ("steady", "step", "spike", "ramp", "equipment")
START, N_SESSIONS, ALERT = 15, 40, 1.0
LIMITS = {"magnitude": (0.0, 0.5), "length": (1, 25), "seed": (0, 9999)}


# "Equipment change": from session 16 the person works with something new (gloves, a shared tablet) and is slower for good.
# A human accepts the new normal after ACCEPT_AFTER affected sessions. Later a real, separate slowdown begins.
# ALL of these numbers are illustrative assumptions, not measurements.
EQUIP_N, EQUIP_ACCEPT_AFTER = 45, 7
LATER_START, LATER_LENGTH, LATER_MAGNITUDE = 35, 8, 0.2


def equipment_change(magnitude: float, seed: int) -> dict:
    """One simulated person through an equipment change, a human accepting it, then a real slowdown. Both scorings see the same sessions."""
    accept_at = START + EQUIP_ACCEPT_AFTER                    # index of the first session scored AFTER the acceptance
    events = (Event("step", START, EQUIP_N - START, magnitude), Event("step", LATER_START, LATER_LENGTH, LATER_MAGNITUDE))
    sessions, _truth = simulate_person(np.random.default_rng(seed), EQUIP_N, events=events)
    for i, s in enumerate(sessions):
        s["id"] = i
    first = score_history(sessions[:accept_at], "docking_checklist_v1")
    pending = _pending_run(first, sessions[:accept_at])      # the flagged run the person is asked to accept; may be empty
    accepted = [dict(s, accepted_at="accepted") if s["id"] in pending else s for s in sessions]
    after = score_history(accepted, "docking_checklist_v1")
    rows = []
    for i, s in enumerate(sessions):
        view, _b, excluded = (first if i < accept_at else after)[i]
        before = incumbent_detector(sessions[:i], s)
        phase = "later" if LATER_START <= i < LATER_START + LATER_LENGTH else "equipment" if START <= i < accept_at else "after" if i >= accept_at else "normal"
        rows.append({"i": i + 1, "phase": phase, "event": phase == "later",
                     "before": None if before is None else round(before, 2),
                     "now": None if view.score is None else round(view.score, 2),
                     "excluded": bool(excluded) and i < accept_at})

    def share(key, phase):
        r = [x[key] for x in rows if x["phase"] == phase and x[key] is not None]
        return f"{sum(v >= ALERT for v in r)} of {len(r)}"

    return {"synthetic": True, "scenario": "equipment", "magnitude": magnitude, "seed": seed, "alert_threshold": ALERT,
            "sessions": rows, "accepted_sessions": len(pending),
            "bands": [{"from": START + 1, "to": accept_at, "label": "New equipment"},
                      {"from": LATER_START + 1, "to": LATER_START + LATER_LENGTH, "label": "A real slowdown"}],
            "markers": [{"at": accept_at, "label": "A person accepts the new normal" if pending else "Nothing was flagged strongly enough to accept"}],
            "table": {"headers": ["", "Flagged while the equipment was new", "Flagged after it was accepted, with nothing else changing", "Flagged during a later real slowdown"],
                      "rows": [[name, share(k, "equipment"), _after(rows, k), share(k, "later")]
                               for name, k in (("Old scoring", "before"), ("Current scoring", "now"))]}}


def _after(rows, key):
    r = [x[key] for x in rows if x["phase"] == "after" and x["i"] <= LATER_START and x[key] is not None]
    return f"{sum(v >= ALERT for v in r)} of {len(r)}"


def run_scenario(scenario: str, magnitude: float, length: int, seed: int) -> dict:
    if scenario not in SCENARIOS:
        raise ValueError(f"scenario must be one of {SCENARIOS}")
    if scenario == "equipment":
        return equipment_change(magnitude, seed)
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


def equipment_benchmark(n_people: int = 300, magnitude: float = 0.4, seed: int = 0, n_boot: int = 1000) -> dict:
    """The equipment-change scenario over many simulated people (each a different random person), for the Evidence page.
    Shares are pooled over people; the 95 % interval comes from resampling people. Illustrative assumptions throughout."""
    phases = (("equipment", "while the equipment was new"), ("after", "after it was accepted"), ("later", "during a later real slowdown"))
    counts = {k: {ph: [] for ph, _ in phases} for k in ("before", "now")}
    accepted = []
    for i in range(n_people):
        d = equipment_change(magnitude, seed * 100000 + i)
        accepted.append(d["accepted_sessions"] > 0)
        for k in counts:
            for ph, _ in phases:
                r = [x[k] for x in d["sessions"] if x["phase"] == ph and x[k] is not None and (ph != "after" or x["i"] <= LATER_START)]
                counts[k][ph].append((sum(v >= ALERT for v in r), len(r)))
    rng = np.random.default_rng(seed + 1)
    out = {"people": n_people, "magnitude": magnitude, "accepted_share": round(float(np.mean(accepted)), 3),
           "assumptions": {"start_session": START + 1, "accepted_after_sessions": EQUIP_ACCEPT_AFTER, "later_slowdown": LATER_MAGNITUDE,
                           "later_start_session": LATER_START + 1, "later_length": LATER_LENGTH},
           "rows": []}
    for k, name in (("before", "Old scoring"), ("now", "Current scoring")):
        row = {"scoring": name}
        for ph, _ in phases:
            a = np.array(counts[k][ph], dtype=float)
            rate = a[:, 0].sum() / a[:, 1].sum()
            boots = [a[j, 0].sum() / a[j, 1].sum() for j in (rng.integers(0, len(a), len(a)) for _ in range(n_boot))]
            row[ph] = {"rate": round(float(rate), 3), "ci95": [round(float(np.quantile(boots, .025)), 3), round(float(np.quantile(boots, .975)), 3)]}
        out["rows"].append(row)
    return out


if __name__ == "__main__":
    import json
    print(json.dumps(equipment_benchmark(), indent=2))      # synthetic, illustrative assumptions
