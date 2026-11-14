"""
Readiness service: glues storage (store.py) to the math (baseline.py, scoring.py).

The key rule: a session is ALWAYS compared to the sessions that came
BEFORE it. It never takes part in its own baseline, otherwise a strange
session would partly "explain itself away".
"""
from __future__ import annotations

import os

from . import store
from .baseline import compute_baseline, select_baseline_sessions
from .features import FEATURE_NAMES
from .scoring import insufficient_data_view, score_session
from .tasks import DEFAULT_TASK_TYPE

# How many of the most recent sessions the trend carries. The dashboard draws one line
# per session (the "stacked sessions" art), so this is also the number of lines.
TREND_POINTS = 14

# Which scoring model the product uses. "nb" = per-person count model for pauses (benchmark: docs/ML_RESULTS.md);
# "robust" = the original median/MAD z-score for every feature. Env override: CREW_PAUSE_MODEL.
PAUSE_MODEL = os.environ.get("CREW_PAUSE_MODEL", "nb")


def _session_summary(s: dict) -> dict:
    return {
        "id": s["id"],
        "created_at": s["created_at"],
        "source": s["source"],
        "data_quality": s["data_quality"],
        "quality_notes": s["quality_notes"],
        "features": {n: s[n] for n in FEATURE_NAMES},
    }


def _score_at(history: list[dict], index: int, task_type: str):
    """Score history[index] against the sessions before it."""
    session = history[index]
    baseline = compute_baseline(select_baseline_sessions(history[:index]),
                                FEATURE_NAMES, task_type)
    return score_session(session, baseline, session["data_quality"], PAUSE_MODEL), baseline


def readiness_for_profile(db, profile: dict, task_type: str = DEFAULT_TASK_TYPE,
                          with_trend: bool = True) -> dict:
    history = store.list_sessions(db, profile["id"], task_type)
    result: dict = {
        "profile": profile,
        "task_type": task_type,
        "latest_session": None,
        "readiness": insufficient_data_view().to_dict(),
        "baseline": None,
        "trend": [],
        "attention": store.latest_attention_result(db, profile["id"]),
    }
    if not history:
        return result

    view, baseline = _score_at(history, len(history) - 1, task_type)
    result["latest_session"] = _session_summary(history[-1])
    result["readiness"] = view.to_dict()
    result["baseline"] = baseline.to_dict()

    if with_trend:
        start = max(0, len(history) - TREND_POINTS)
        for i in range(start, len(history)):
            v, _ = _score_at(history, i, task_type)
            result["trend"].append({
                "session_id": history[i]["id"],
                "created_at": history[i]["created_at"],
                "source": history[i]["source"],
                "status": v.status,
                "band": v.band,
                "score": None if v.score is None else round(v.score, 2),
                # Per-feature directional deviation that fed the score (0 = usual or faster,
                # capped at 4). None while CALIBRATING, because there is no baseline to
                # deviate from. The dashboard art draws exactly these numbers, nothing else.
                "deviations": (
                    {d.feature: round(d.deviation, 2) for d in v.deviations}
                    if v.status == "SCORED" else None
                ),
            })
    return result


def readiness_for_all(db, task_type: str = DEFAULT_TASK_TYPE) -> list[dict]:
    return [readiness_for_profile(db, p, task_type, with_trend=False)
            for p in store.list_profiles(db)]
