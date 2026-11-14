"""Flagged sessions must not teach the baseline what 'normal' is; a human can accept a new normal."""
import sqlite3

from tests.conftest import valid_payload

SLOW = dict(iki_median_ms=330.0, iki_iqr_ms=140.0, checklist_response_median_ms=2600.0,
            pause_count=4, pause_total_ms=9000.0)


def post_slow(client, n):
    for _ in range(n):
        assert client.post("/api/sessions", json=valid_payload(**SLOW)).status_code == 201


def readiness(client):
    return client.get("/api/readiness/plt-okafor").get_json()


def test_a_sustained_slowdown_is_not_absorbed_into_the_baseline(client):
    post_slow(client, 8)
    d = readiness(client)
    # with the old behaviour the baseline would have drifted toward the slow sessions and the score would fade
    assert d["readiness"]["band"] == "RED"
    assert d["baseline_review"]["excluded_sessions"] >= 6
    assert d["baseline"]["features"]["iki_median_ms"]["median"] < 230


def test_trend_marks_which_sessions_were_excluded(client):
    post_slow(client, 3)
    flags = [p["excluded_from_baseline"] for p in readiness(client)["trend"]]
    assert flags[-3:] == [True, True, True]
    assert flags[-4] is False                       # the session before the slow run was ordinary


def test_accepting_the_new_normal_lets_it_shape_the_baseline(client):
    post_slow(client, 8)
    r = client.post("/api/readiness/plt-okafor/accept-new-normal")
    assert r.status_code == 200 and len(r.get_json()["accepted_session_ids"]) >= 6
    assert client.post("/api/sessions", json=valid_payload(**SLOW)).get_json()["readiness"]["band"] != "RED"
    d = readiness(client)
    assert d["baseline_review"] is None
    assert d["baseline"]["features"]["iki_median_ms"]["median"] > 250   # baseline restarted from the accepted run


def test_accepting_a_short_run_means_calibrating_until_enough_sessions(client):
    post_slow(client, 2)
    assert client.post("/api/readiness/plt-okafor/accept-new-normal").status_code == 200
    assert readiness(client)["readiness"]["status"] == "CALIBRATING"   # we do not pretend to know the new pattern yet
    post_slow(client, 4)
    assert readiness(client)["readiness"]["status"] == "SCORED"


def test_accept_is_refused_when_nothing_is_pending_or_profile_unknown(client):
    assert client.post("/api/readiness/plt-okafor/accept-new-normal").status_code == 409
    assert client.post("/api/readiness/nobody/accept-new-normal").status_code == 404


def test_a_normal_session_after_a_flagged_run_ends_the_pending_review(client):
    post_slow(client, 2)
    assert readiness(client)["baseline_review"]
    client.post("/api/sessions", json=valid_payload())            # back to usual
    assert readiness(client)["baseline_review"] is None


def test_old_databases_get_the_new_column(tmp_path):
    from app import create_app
    from app.db import ensure_columns, get_db
    path = tmp_path / "old.sqlite3"
    app = create_app({"TESTING": True, "DATABASE": str(path), "AUTO_SEED": True})
    with app.app_context():
        get_db().execute("ALTER TABLE sessions DROP COLUMN accepted_at")   # simulate a pre-feature database
        get_db().commit()
        ensure_columns()
        cols = {r["name"] for r in get_db().execute("PRAGMA table_info(sessions)")}
        assert "accepted_at" in cols
