"""
A SIMULATED six-month mission, scored exactly as the product scores it, to show what a reviewer would actually have to do.
Run: python -m ml.mission_sim      (writes app/mission_sim.json; the Replay page renders that file)

Four simulated crew, one checklist a day for 180 days. ALL of the story below is an illustrative assumption, not a measurement:
  A  from day 60 works with new equipment (30 % slower for good); a human accepts it as the new normal on day 67
  B  a real 25 % slowdown for 10 days from day 120
  C  checks in on 175 of 180 days: no check-in on days 150 to 154 (the missed check-in watchdog's case)
  D  nothing happens
Counts are what the product's own scoring would have flagged (score >= 1.0, YELLOW) and what it would have asked people to do.
"""
import json
from pathlib import Path

import numpy as np

from app.mission import MISSION
from app.readiness import _pending_run, score_history

from .synth import Event, simulate_person

OUT = Path(__file__).resolve().parents[1] / "app" / "mission_sim.json"
DAYS, SEED, ALERT = 180, 11, 1.0
EQUIP_START, EQUIP_ACCEPT, SLOW_START, SLOW_LEN, GAP = 60, 67, 120, 10, range(150, 155)
REVIEW_MINUTES = 10                  # an assumption, as on the alert-burden calculator
INTERVAL_DAYS = MISSION["check_in_interval_hours"] / 24


def _flags(sessions, accept_at=None):
    """Day-by-day YELLOW-or-worse flags for one person's sessions, scored as the product scores them."""
    for i, s in enumerate(sessions):
        s["id"] = i
    if accept_at is not None:
        first = score_history(sessions[:accept_at], "docking_checklist_v1")
        pending = _pending_run(first, sessions[:accept_at])
        sessions = [dict(s, accepted_at="accepted") if s["id"] in pending else s for s in sessions]
    walked = score_history(sessions, "docking_checklist_v1")
    return [bool(v.status == "SCORED" and v.score >= ALERT) for v, _b, _x in walked]


def simulate(seed: int = SEED) -> dict:
    rng = np.random.default_rng(seed)
    a, _ = simulate_person(rng, DAYS, events=(Event("step", EQUIP_START, DAYS - EQUIP_START, 0.30),))
    b, _ = simulate_person(rng, DAYS, events=(Event("step", SLOW_START, SLOW_LEN, 0.25),))
    c, _ = simulate_person(rng, DAYS)
    d, _ = simulate_person(rng, DAYS)
    c_days = [i for i in range(DAYS) if i not in GAP]                      # the days C actually checked in
    c = [c[i] for i in c_days]
    flags = {"A": _flags(a, accept_at=EQUIP_ACCEPT), "B": _flags(b), "C": _flags(c), "D": _flags(d)}
    day_of = {"A": list(range(DAYS)), "B": list(range(DAYS)), "C": c_days, "D": list(range(DAYS))}

    weekly = [0] * ((DAYS + 6) // 7)
    true_flags = false_flags = 0
    for who, fl in flags.items():
        for k, f in enumerate(fl):
            day = day_of[who][k]
            if not f:
                continue
            weekly[day // 7] += 1
            real = (who == "A" and EQUIP_START <= day < EQUIP_ACCEPT) or (who == "B" and SLOW_START <= day < SLOW_START + SLOW_LEN)
            true_flags += real
            false_flags += not real
    a_days = [day_of["A"][k] for k, f in enumerate(flags["A"]) if f]
    b_days = [day_of["B"][k] for k, f in enumerate(flags["B"]) if f]
    checkins = sum(len(v) for v in day_of.values())
    overdue_days = sum(1 for g in GAP if g - (min(GAP) - 1) > INTERVAL_DAYS)           # days past the agreed gap while C is silent
    alerts = true_flags + false_flags
    return {
        "synthetic": True, "seed": seed, "days": DAYS, "crew": 4, "checkins": checkins, "review_minutes": REVIEW_MINUTES,
        "story": {"equipment_start": EQUIP_START + 1, "equipment_accepted": EQUIP_ACCEPT + 1, "slowdown_start": SLOW_START + 1,
                  "slowdown_days": SLOW_LEN, "gap_start": min(GAP) + 1, "gap_days": len(GAP)},
        "weekly_alerts": weekly,
        "alerts": alerts, "flags_during_real_changes": true_flags, "false_alerts": false_flags,
        "equipment_flagged_before_acceptance": sum(EQUIP_START <= d < EQUIP_ACCEPT for d in a_days),
        "equipment_flagged_after_acceptance": sum(d >= EQUIP_ACCEPT for d in a_days),
        "slowdown_days_flagged": sum(SLOW_START <= d < SLOW_START + SLOW_LEN for d in b_days),
        "missed_checkin_overdue_days": overdue_days,
        "reviewer_actions": {"alerts_to_review": alerts, "accept_new_normal": 1, "look_in_after_missed_checkins": 1},
        "reviewer_hours": round(alerts * REVIEW_MINUTES / 60, 1),
        "limits": ["Simulated crew and a story we wrote; every size and timing is an assumption.", "One random run: it illustrates the workload, it is not evidence of accuracy (the 300-person results are above).",
                   "The review time per alert is an assumption.", "Nothing here is about anyone's health."],
    }


if __name__ == "__main__":
    r = simulate()
    OUT.write_text(json.dumps(r, indent=2) + "\n")
    print({k: v for k, v in r.items() if k not in ("weekly_alerts", "limits", "story")})
