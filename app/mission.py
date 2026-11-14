"""
Mission scenario: gives a readiness change *operational meaning*.

A YELLOW band on a quiet day is trivia; a YELLOW band on the primary
pilot six hours before manual docking is a decision. This module holds
the (fictional) scenario and the advisory rules.

Owner: Team Lead (task L-1 in docs/TEAM_GUIDE.md).
"""
from __future__ import annotations

MISSION = {
    "name": "Gateway docking — simulated scenario",
    "critical_operation": "Manual approach and docking",
    "t_minus_hours": 6,
    "assignments": [
        {"role": "Primary pilot",   "profile_id": "plt-okafor", "critical": True},
        {"role": "Backup pilot",    "profile_id": "cdr-vega",   "critical": True},
        {"role": "Systems monitor", "profile_id": "fe-sato",    "critical": False},
        {"role": "Comms and log",   "profile_id": "ms-ibarra",  "critical": False},
    ],
}


def mission_advisory(assignments: list[dict]) -> dict:
    """Turn crew readiness into a human-facing recommendation for the critical operation.

    TODO(L-1, Team Lead): implement. The spec is in tests/test_mission.py
    (remove the skip marker and make the tests pass).

    Input — one dict per assignment, already joined with readiness:
        {"role": str, "profile_id": str, "display_name": str, "critical": bool,
         "status": "SCORED"|"CALIBRATING"|"INSUFFICIENT_DATA",
         "band": "GREEN"|"YELLOW"|"RED"|None, "confidence": str}

    Output:
        {"level": "NOMINAL" | "CHECK_IN" | "REVIEW",
         "messages": [str, ...],           # plain language, one per concern
         "suggested_actions": [str, ...]}  # e.g. "Run attention check for Kai Okafor"

    Rules you must respect (from our ethics guardrails):
      * The system SUGGESTS. It never assigns, clears, or grounds anyone.
      * Never use the words fatigue, impaired, unfit, diagnosis.
      * A CALIBRATING person is "unknown", not "fine".

    Questions to decide before you code (write your answers in docs/PLAN.md, Decision D-5):
      * What exactly counts as an alert? Any YELLOW? Only on critical roles?
      * When do we suggest the backup? Only if the backup is GREEN?
      * Does LOW confidence soften the message?
    """
    return {
        "level": "TODO",
        "messages": ["Mission advisory logic not implemented yet (task L-1)."],
        "suggested_actions": [],
    }
