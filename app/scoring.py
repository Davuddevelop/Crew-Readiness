"""
Readiness scoring — ILLUSTRATIVE PROTOTYPE LOGIC.

Nothing in this file is clinically validated or NASA-approved. Every
constant below is a demo choice that we document and can defend, not a
medical threshold. The UI must label it that way.

How it works (explainable on one slide):
  1. For each scored feature, how far is today's value from this person's
     own median, in robust-SD units?  z = (value - median) / spread
  2. Only count the "worse" direction (slower, more pausing). Being faster
     than usual is not penalised.  d = clip(max(0, z), 0, 4)
  3. Average d inside each group, then weight the groups
     (typing 40 %, pauses 30 %, checklist response 30 %).
  4. Map the weighted score to a band: < 1.0 GREEN, < 2.0 YELLOW, else RED.

Owner: Member 2 (Data & ML). Pure functions — no database access here.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .baseline import MIN_BASELINE_SESSIONS, Baseline
from .features import FEATURES_BY_NAME

# feature -> (group, direction, absolute spread floor)
#   direction +1 means "higher value = further from usual in the concerning way"
#   the spread floor stops division by ~0 when someone is extremely consistent
#   (e.g. pause_count is 0 in every baseline session -> MAD = 0)
SCORED_FEATURES: dict[str, tuple[str, int, float]] = {
    "iki_median_ms":                ("typing",    +1, 10.0),
    "iki_iqr_ms":                   ("typing",    +1, 10.0),
    "pause_count":                  ("pauses",    +1, 1.0),
    "pause_total_ms":               ("pauses",    +1, 1000.0),
    "checklist_response_median_ms": ("checklist", +1, 150.0),
}
GROUP_WEIGHTS = {"typing": 0.40, "pauses": 0.30, "checklist": 0.30}
GROUP_LABELS = {"typing": "Typing rhythm", "pauses": "Pausing", "checklist": "Checklist response"}

RELATIVE_SPREAD_FLOOR = 0.05   # spread is at least 5 % of the median
DEVIATION_CAP = 4.0            # one extreme feature can't dominate everything
REASON_THRESHOLD = 1.0         # features at/above this deviation get a plain-language reason
BAND_CUTOFFS = ((1.0, "GREEN"), (2.0, "YELLOW"))   # anything above -> RED

ADVISORIES = {
    "GREEN":  "Interaction timing is within this crew member's usual range. No action suggested.",
    "YELLOW": "Timing differs from this crew member's usual pattern. Suggest a brief check-in "
              "or the optional attention check before the critical operation.",
    "RED":    "Large change from this crew member's personal baseline. Recommend human review "
              "and a second verification before assigning the critical operation.",
    "CALIBRATING": "Still learning this crew member's usual pattern. No score is shown until "
                   "enough comparable sessions exist.",
    "INSUFFICIENT_DATA": "No completed sessions yet for this crew member.",
}
DISCLAIMER = ("Advisory only. Detects changes in task interaction timing, not fatigue, "
              "illness or fitness for duty. Thresholds are illustrative prototype choices.")


@dataclass
class FeatureDeviation:
    feature: str
    label: str
    unit: str
    group: str
    value: float
    baseline_median: float
    spread_used: float
    z: float           # signed: + means higher than usual
    deviation: float   # directional, clipped: what actually feeds the score

    def to_dict(self) -> dict:
        return {k: (round(v, 2) if isinstance(v, float) else v) for k, v in self.__dict__.items()}


@dataclass
class ReadinessView:
    status: str                      # SCORED | CALIBRATING | INSUFFICIENT_DATA
    band: str | None                 # GREEN | YELLOW | RED | None
    score: float | None              # weighted deviation, robust-SD units (0 = exactly usual)
    confidence: str                  # NONE | LOW | MEDIUM | HIGH
    baseline_n: int
    baseline_needed: int
    data_quality: str | None
    group_scores: dict[str, float] = field(default_factory=dict)
    deviations: list[FeatureDeviation] = field(default_factory=list)
    reasons: list[str] = field(default_factory=list)
    advisory: str = ""
    disclaimer: str = DISCLAIMER

    def to_dict(self) -> dict:
        return {
            "status": self.status,
            "band": self.band,
            "score": None if self.score is None else round(self.score, 2),
            "confidence": self.confidence,
            "baseline_n": self.baseline_n,
            "baseline_needed": self.baseline_needed,
            "data_quality": self.data_quality,
            "group_scores": {k: round(v, 2) for k, v in self.group_scores.items()},
            "deviations": [d.to_dict() for d in self.deviations],
            "reasons": self.reasons,
            "advisory": self.advisory,
            "disclaimer": self.disclaimer,
        }


def band_for(score: float) -> str:
    for cutoff, band in BAND_CUTOFFS:
        if score < cutoff:
            return band
    return "RED"


def confidence_for(baseline_n: int, data_quality: str) -> str:
    """How much should a human trust this score? Driven by data sufficiency, not by the score.

    Member 2: consider adding task comparability (same keyboard? same time of day?).
    """
    if baseline_n < MIN_BASELINE_SESSIONS:
        return "NONE"
    level = 1 if baseline_n < 10 else 2 if baseline_n < 15 else 3
    if data_quality != "ok":
        level = max(1, level - 1)
    return ("NONE", "LOW", "MEDIUM", "HIGH")[level]


def _reason_text(d: FeatureDeviation) -> str:
    direction = "higher" if d.z > 0 else "lower"
    if d.unit == "ms":
        now, usual = f"{d.value:.0f} ms", f"{d.baseline_median:.0f} ms"
    else:
        now, usual = f"{d.value:.0f}", f"{d.baseline_median:.1f}"
    return f"{d.label}: {now} vs usual {usual} ({d.z:+.1f} robust SD, {direction} than usual)."


def insufficient_data_view() -> ReadinessView:
    """For a crew member with no completed sessions at all."""
    return ReadinessView(status="INSUFFICIENT_DATA", band=None, score=None,
                         confidence="NONE", baseline_n=0,
                         baseline_needed=MIN_BASELINE_SESSIONS, data_quality=None,
                         advisory=ADVISORIES["INSUFFICIENT_DATA"])


def score_session(features: dict, baseline: Baseline, data_quality: str) -> ReadinessView:
    """Compare one session's features with the person's own baseline."""
    if not baseline.ready:
        return ReadinessView(status="CALIBRATING", band=None, score=None,
                             confidence="NONE", baseline_n=baseline.n,
                             baseline_needed=MIN_BASELINE_SESSIONS, data_quality=data_quality,
                             advisory=ADVISORIES["CALIBRATING"])

    deviations: list[FeatureDeviation] = []
    for name, (group, direction, abs_floor) in SCORED_FEATURES.items():
        spec = FEATURES_BY_NAME[name]
        fb = baseline.features[name]
        spread = max(fb.spread, RELATIVE_SPREAD_FLOOR * abs(fb.median), abs_floor)
        z = (float(features[name]) - fb.median) / spread
        d = min(max(0.0, z * direction), DEVIATION_CAP)
        deviations.append(FeatureDeviation(
            feature=name, label=spec.label, unit=spec.unit, group=group,
            value=float(features[name]), baseline_median=fb.median,
            spread_used=spread, z=z, deviation=d,
        ))

    group_scores: dict[str, float] = {}
    for group in GROUP_WEIGHTS:
        ds = [d.deviation for d in deviations if d.group == group]
        group_scores[group] = sum(ds) / len(ds)
    score = sum(GROUP_WEIGHTS[g] * s for g, s in group_scores.items())
    band = band_for(score)

    ranked = sorted(deviations, key=lambda d: d.deviation, reverse=True)
    reasons = [_reason_text(d) for d in ranked if d.deviation >= REASON_THRESHOLD]

    return ReadinessView(
        status="SCORED", band=band, score=score,
        confidence=confidence_for(baseline.n, data_quality),
        baseline_n=baseline.n, baseline_needed=MIN_BASELINE_SESSIONS,
        data_quality=data_quality, group_scores=group_scores,
        deviations=ranked, reasons=reasons, advisory=ADVISORIES[band],
    )
