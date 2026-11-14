"""Baseline + scoring behaviour. If you change a constant, these tell you what you broke."""
import math

from app.baseline import (MAD_TO_SD, MIN_BASELINE_SESSIONS, compute_baseline,
                          select_baseline_sessions)
from app.features import FEATURE_NAMES
from app.scoring import band_for, confidence_for, score_session
from tests.conftest import valid_features

TASK = "docking_checklist_v1"


def make_sessions(n, **overrides):
    return [{**valid_features(**overrides), "data_quality": "ok"} for _ in range(n)]


def baseline_from(values, feature="iki_median_ms"):
    sessions = [{**valid_features(**{feature: v}), "data_quality": "ok"} for v in values]
    return compute_baseline(sessions, FEATURE_NAMES, TASK)


# ---------- baseline ----------

def test_baseline_uses_median_and_robust_spread():
    b = baseline_from([100, 110, 120, 130, 1000])  # one wild outlier
    fb = b.features["iki_median_ms"]
    assert fb.median == 120                            # outlier barely matters
    assert math.isclose(fb.spread, MAD_TO_SD * 10)     # MAD of |x-120| = 10


def test_baseline_not_ready_below_minimum():
    assert not compute_baseline(make_sessions(MIN_BASELINE_SESSIONS - 1), FEATURE_NAMES, TASK).ready
    assert compute_baseline(make_sessions(MIN_BASELINE_SESSIONS), FEATURE_NAMES, TASK).ready


def test_low_quality_sessions_are_excluded_from_baseline():
    history = make_sessions(3) + [{**valid_features(), "data_quality": "low"}]
    assert len(select_baseline_sessions(history)) == 3


# ---------- scoring ----------

def test_calibrating_when_baseline_too_small():
    b = compute_baseline(make_sessions(2), FEATURE_NAMES, TASK)
    view = score_session(valid_features(), b, "ok")
    assert view.status == "CALIBRATING" and view.score is None and view.band is None


def test_session_identical_to_baseline_is_green_zero():
    b = compute_baseline(make_sessions(10), FEATURE_NAMES, TASK)
    view = score_session(valid_features(), b, "ok")
    assert view.status == "SCORED" and view.band == "GREEN" and view.score == 0
    assert view.reasons == []


def test_slower_typing_increases_score_and_gives_reason():
    b = baseline_from([180, 185, 190, 195, 200, 190, 188])
    view = score_session(valid_features(iki_median_ms=260), b, "ok")
    assert view.score > 0
    assert any("Typing rhythm" in r for r in view.reasons)


def test_faster_than_usual_is_not_penalised():
    b = baseline_from([180, 185, 190, 195, 200, 190, 188])
    view = score_session(valid_features(iki_median_ms=120), b, "ok")
    typing = next(d for d in view.deviations if d.feature == "iki_median_ms")
    assert typing.z < 0 and typing.deviation == 0


def test_zero_spread_feature_does_not_explode():
    # pause_count is 0 in every baseline session -> MAD = 0 -> must use the floor
    b = compute_baseline(make_sessions(8, pause_count=0, pause_total_ms=0), FEATURE_NAMES, TASK)
    view = score_session(valid_features(pause_count=1, pause_total_ms=2500), b, "ok")
    assert math.isfinite(view.score)


def test_deviation_is_capped():
    b = baseline_from([190] * 10)
    view = score_session(valid_features(iki_median_ms=2900), b, "ok")
    assert max(d.deviation for d in view.deviations) <= 4.0


def test_bands_and_confidence():
    assert band_for(0.5) == "GREEN" and band_for(1.5) == "YELLOW" and band_for(2.5) == "RED"
    assert confidence_for(3, "ok") == "NONE"
    assert confidence_for(6, "ok") == "LOW"
    assert confidence_for(16, "ok") == "HIGH"
    assert confidence_for(16, "low") == "MEDIUM"   # low data quality downgrades
