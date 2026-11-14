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

    DECIDED RULES (docs/PLAN.md, "D-5 rules"). Level = highest row that applies, critical roles only:
      * any critical RED                      -> REVIEW; if another critical member is GREEN,
                                                 name them as an option for the reviewer
      * else any critical YELLOW              -> CHECK_IN
      * else any critical CALIBRATING/no data -> CHECK_IN ("no baseline yet", never "fine")
      * else                                  -> NOMINAL
      * no clean backup (e.g. RED + YELLOW)   -> REVIEW, flag both, name NOBODY as a replacement
      * non-critical roles                    -> never change the level or the messages
    OPEN EDGES you must settle and then write into PLAN.md: RED backup with GREEN primary;
    RED + CALIBRATING together; whether LOW confidence softens wording.
    """
    return {
        "level": "TODO",
        "messages": ["Mission advisory logic not implemented yet (task L-1)."],
        "suggested_actions": [],
    }
