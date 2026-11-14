"""
Demo helper: add a short run of clearly slower sessions for the demo pilot through the PUBLIC API, so the
"Review needed" panel can be shown without typing slowly on stage. Standard library only.

    python run.py &                                   # the app must be running
    python scripts/demo_flag_pilot.py                 # 4 slow sessions for plt-okafor on http://127.0.0.1:5050
    python scripts/demo_flag_pilot.py --base http://127.0.0.1:5050 --n 6

These are SYNTHETIC sessions (they are posted like live ones, so the dashboard will list them as live). Undo with
`flask --app run reset-demo`. Never use this against anything but a demo database.
"""
import argparse
import json
import urllib.request

SLOW = {"keystroke_count": 125, "iki_median_ms": 330.0, "iki_iqr_ms": 140.0, "pause_count": 4, "pause_total_ms": 9000.0,
        "checklist_response_median_ms": 2600.0, "task_duration_ms": 60000.0, "correction_count": 2, "retry_count": 0}

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--base", default="http://127.0.0.1:5050")
    ap.add_argument("--profile", default="plt-okafor")
    ap.add_argument("--n", type=int, default=4)
    a = ap.parse_args()
    for i in range(a.n):
        body = json.dumps({"profile_id": a.profile, "task_type": "docking_checklist_v1", "features": SLOW}).encode()
        req = urllib.request.Request(f"{a.base}/api/sessions", data=body, headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as r:
            out = json.load(r)
        print(f"session {i + 1}: {out['readiness']['status']} {out['readiness']['band']} score={out['readiness']['score']}")
    print("Open /dashboard?crew=" + a.profile + " and look for 'Review needed'.")
