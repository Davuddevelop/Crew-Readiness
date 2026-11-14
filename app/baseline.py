"""
Personal baseline: "what is normal for THIS person on THIS task?"

We use the MEDIAN as the centre and the MAD (median absolute deviation)
as the spread, not mean and standard deviation.

Why robust statistics? With 5-20 sessions, one weird session (someone
got interrupted, sneezed, switched keyboards) would drag a mean and blow
up a standard deviation. The median and MAD barely move. Multiplying the
MAD by 1.4826 makes it comparable to a standard deviation for normally
distributed data, so "2 robust SD" still reads naturally.

Owner: Member 2 (Data & ML). Pure functions — no database access here.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

# Illustrative prototype choices. Document any change in docs/DATA_CONTRACT.md.
MIN_BASELINE_SESSIONS = 5    # below this we show CALIBRATING, never a score
MAX_BASELINE_SESSIONS = 20   # rolling window of the most recent comparable sessions
MAD_TO_SD = 1.4826


@dataclass(frozen=True)
class FeatureBaseline:
    median: float
    spread: float   # robust SD = 1.4826 * MAD (may be 0 for very consistent people)


@dataclass(frozen=True)
class Baseline:
    task_type: str
    n: int                                   # how many sessions it was built from
    features: dict[str, FeatureBaseline]
    pause_counts: tuple = ()                 # the person's recent pause counts (for the count model)

    @property
    def ready(self) -> bool:
        return self.n >= MIN_BASELINE_SESSIONS

    def to_dict(self) -> dict:
        return {
            "task_type": self.task_type,
            "n": self.n,
            "ready": self.ready,
            "min_required": MIN_BASELINE_SESSIONS,
            "features": {k: {"median": round(v.median, 1), "spread": round(v.spread, 1)}
                         for k, v in self.features.items()},
        }


def select_baseline_sessions(history: list[dict]) -> list[dict]:
    """Choose which past sessions count as 'normal' for this person.

    `history` is oldest-first and must NOT include the session being scored.
    Rules (prototype):
      * only data_quality == 'ok' sessions
      * most recent MAX_BASELINE_SESSIONS of those
    Known limitation (Member 2 — discuss!): a deviating session, once stored,
    becomes part of the future baseline. Should RED sessions be excluded?
    """
    ok = [s for s in history if s["data_quality"] == "ok"]
    return ok[-MAX_BASELINE_SESSIONS:]


def compute_baseline(sessions: list[dict], feature_names: tuple[str, ...],
                     task_type: str) -> Baseline:
    if not sessions:
        return Baseline(task_type=task_type, n=0, features={})

    values = np.array([[float(s[f]) for f in feature_names] for s in sessions])
    medians = np.median(values, axis=0)
    mads = np.median(np.abs(values - medians), axis=0)
    spreads = MAD_TO_SD * mads

    return Baseline(
        task_type=task_type,
        n=len(sessions),
        pause_counts=tuple(int(s["pause_count"]) for s in sessions),
        features={
            name: FeatureBaseline(median=float(m), spread=float(s))
            for name, m, s in zip(feature_names, medians, spreads)
        },
    )
