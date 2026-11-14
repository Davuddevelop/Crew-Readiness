"""The Privacy & limits page (task R-1): every number must come from the benchmark output or docs/ML_RESULTS.md."""
import json
import re
from pathlib import Path

from tests.test_claims import text_of

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT / "app" / "results_data.json").read_text(encoding="utf-8"))
ML = (ROOT / "docs" / "ML_RESULTS.md").read_text(encoding="utf-8")


def page(client):
    return text_of(client.get("/about").data.decode())


def test_benchmark_numbers_match_the_results_file(client):
    t = page(client)
    op = next(r for r in DATA["operating_point"] if r["slowdown"] == 0.1)
    assert f"{op['before']['false_alerts'] * 100:.1f} % to about {op['now']['false_alerts'] * 100:.1f} %" in t
    assert f"{op['before']['detection']:.2f} to {op['now']['detection']:.2f}" in t
    for burst in ("none", "high"):
        r = next(r for r in DATA["table"] if r["slowdown"] == 0.1 and r["burstiness"] == burst)
        assert f"{r['incumbent']:.2f} to {r['neg_binomial']:.2f}" in t
    s = DATA["setup"]
    assert f"{s['people_per_cell']} simulated people per row, {s['sessions_per_person']} sessions each" in t


def test_contamination_numbers_match_ml_results(client):
    t = page(client)
    keep = re.search(r"\| 20 % \| keep all \(today\) \| ([\d.]+) \|.*\| \*\*([\d.]+)\*\* \|", ML)
    excl = re.search(r"\| 20 % \| exclude flagged.*\| \*\*([\d.]+)\*\* \|", ML)
    assert f"from {keep.group(1)} to {keep.group(2)} by the fifteenth" in t
    assert f"held it at {excl.group(1)}" in t


def test_page_covers_the_r1_topics_and_labels_the_proposal(client):
    t = page(client)
    assert "This is a proposal, not something the prototype does." in t
    for word in ("Keyboard.", "Language.", "Time of day.", "Sleep.", "Practice."):
        assert word in t
    for phrase in ("simulated data", "very small volunteer check", "Almost no real people", "no data from astronauts or crews", "partly circular", "approved or endorsed by NASA"):
        assert phrase in t


def test_baseline_window_on_the_page_matches_the_code(client):
    from app.baseline import MAX_BASELINE_SESSIONS
    assert f"at most the {MAX_BASELINE_SESSIONS} most recent comparable sessions" in page(client)


def test_about_has_the_offline_self_check_and_says_what_it_does_not_cover(client):
    html = client.get("/about").get_data(as_text=True)
    assert 'id="offline-check"' in html and "js/netcheck.js" in html
    assert "Not tested: a real on-board computer" in html and "turn off Wi-Fi" in html


def test_about_places_the_tool_beside_health_monitoring_without_health_claims(client):
    html = client.get("/about").get_data(as_text=True)
    assert 'id="health-fit"' in html and "not</strong> a health monitor" in html
    assert "Reaction Self Test" in html and "no endorsement by NASA is implied" in html
    assert "tell crew medical support directly" in html
    landing = client.get("/").get_data(as_text=True)
    assert "beside crew health monitoring, not in place of it" in landing
