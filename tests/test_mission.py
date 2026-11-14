"""
SPEC for task L-1 (Team Lead): mission_advisory().

These tests are SKIPPED until you implement app/mission.py. Workflow:
  1. Decide the rules (write them in docs/PLAN.md, decision D-5).
  2. Adjust these tests if your decisions differ. The tests ARE the spec.
  3. Delete the skip marker below, then make them pass.
"""
import pytest

from app.mission import mission_advisory

pytestmark = pytest.mark.skip(reason="TODO(L-1): implement mission_advisory, then remove this marker")

BANNED_WORDS = ("fatigue", "fatigued", "impaired", "unfit", "diagnos")


def a(role, name, band, critical=True, status="SCORED", confidence="MEDIUM"):
    return {"role": role, "profile_id": name.lower(), "display_name": name,
            "critical": critical, "status": status, "band": band, "confidence": confidence}


def test_all_green_is_nominal():
    out = mission_advisory([a("Primary pilot", "Kai", "GREEN"), a("Backup pilot", "Lena", "GREEN")])
    assert out["level"] == "NOMINAL"


def test_yellow_on_critical_role_suggests_check_in():
    out = mission_advisory([a("Primary pilot", "Kai", "YELLOW"), a("Backup pilot", "Lena", "GREEN")])
    assert out["level"] == "CHECK_IN"
    assert any("Kai" in s for s in out["suggested_actions"])


def test_red_on_critical_role_requires_review_and_mentions_green_backup():
    out = mission_advisory([a("Primary pilot", "Kai", "RED"), a("Backup pilot", "Lena", "GREEN")])
    assert out["level"] == "REVIEW"
    assert any("Lena" in s for s in out["suggested_actions"])


def test_yellow_on_non_critical_role_does_not_escalate():
    out = mission_advisory([a("Primary pilot", "Kai", "GREEN"),
                            a("Comms", "Tomas", "YELLOW", critical=False)])
    assert out["level"] == "NOMINAL"


def test_calibrating_critical_member_is_flagged_as_unknown():
    out = mission_advisory([a("Primary pilot", "Kai", None, status="CALIBRATING", confidence="NONE")])
    assert out["level"] != "NOMINAL"
    assert any("baseline" in m.lower() for m in out["messages"])


def test_language_guardrails():
    out = mission_advisory([a("Primary pilot", "Kai", "RED"), a("Backup pilot", "Lena", "YELLOW")])
    text = " ".join(out["messages"] + out["suggested_actions"]).lower()
    assert not any(w in text for w in BANNED_WORDS)
