"""
The simulated monitoring task, defined once on the server and sent to the browser.

The text is FIXED on purpose. Typing speed depends heavily on *what* you
type, so a baseline is only meaningful if every session uses the same
text. Changing any line below = new task version (docking_checklist_v2),
otherwise old baselines silently become incomparable.

All content is fictional and for demonstration only.
"""

DEFAULT_TASK_TYPE = "docking_checklist_v1"

TASKS = {
    "docking_checklist_v1": {
        "title": "Pre-docking checklist (simulated)",
        "intro": "Read each step and type its confirmation phrase exactly, then press Enter.",
        "items": [
            {"step": "Verify approach corridor is clear of traffic.", "confirm": "CORRIDOR CLEAR"},
            {"step": "Confirm the docking target is acquired by sensors.", "confirm": "TARGET LOCK"},
            {"step": "Arm the soft-capture system.", "confirm": "CAPTURE ARMED"},
            {"step": "Set closing rate to 0.1 metres per second.", "confirm": "RATE 0.1"},
            {"step": "Confirm the abort path is loaded.", "confirm": "ABORT PATH GO"},
            {"step": "Report ready for final approach.", "confirm": "READY FINAL"},
            {"step": "Log entry: type the standard status sentence.",
             "confirm": "Approach checklist complete and all systems nominal"},
        ],
    },
}
