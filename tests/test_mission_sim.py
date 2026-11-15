"""W3: the six-month simulated mission is reproducible, honest and rendered only from its file."""
import json

from ml.mission_sim import OUT, simulate


def test_the_committed_file_is_what_the_simulation_produces():
    assert json.loads(OUT.read_text()) == json.loads(json.dumps(simulate()))            # nothing hand-edited


def test_alerts_add_up_and_the_story_is_consistent():
    r = json.loads(OUT.read_text())
    assert r["alerts"] == r["flags_during_real_changes"] + r["false_alerts"] == sum(r["weekly_alerts"])
    assert r["checkins"] == 4 * r["days"] - r["story"]["gap_days"] and r["synthetic"] is True
    assert r["reviewer_hours"] == round(r["alerts"] * r["review_minutes"] / 60, 1)
    assert 0 <= r["slowdown_days_flagged"] <= r["story"]["slowdown_days"]


def test_replay_renders_the_six_month_section_from_the_file_and_labels_it_synthetic(client):
    r = json.loads(OUT.read_text())
    html = client.get("/replay").get_data(as_text=True)
    assert 'id="six-months"' in html and "Synthetic: the story is ours" in html
    assert f"<strong>{r['checkins']}</strong>" in html and f"<strong>{r['alerts']}</strong>" in html and f"{r['reviewer_hours']} hours" in html
    quiet = sum(1 for n in r["weekly_alerts"] if n <= 1)
    assert f"{quiet} of {len(r['weekly_alerts'])} weeks have none or one, and the busiest week has {max(r['weekly_alerts'])}" in html      # computed, not typed
    assert "not evidence of accuracy" in html and "Nothing here is about anyone" in html


def test_the_section_is_absent_without_the_file(client, tmp_path, monkeypatch):
    from app import views
    monkeypatch.setattr(views, "MISSION_SIM_FILE", tmp_path / "missing.json")
    assert 'id="six-months"' not in client.get("/replay").get_data(as_text=True)
