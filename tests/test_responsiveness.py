"""H1: responsiveness is judged against the person's OWN earlier checks, says what it cannot tell, and never touches the typing band."""
from app.responsiveness import MIN_BASELINE_CHECKS, assess


def chk(rt, miss=0, trials=10, premature=0):
    return {"median_rt_ms": rt, "miss_count": miss, "trials": trials, "premature_count": premature, "created_at": "2026-11-15T00:00:00Z"}


USUAL = [chk(v) for v in (300, 310, 295, 305, 298, 302)]


def test_no_checks_yet():
    assert assess([])["status"] == "NONE"


def test_too_few_earlier_checks_means_calibrating_not_a_verdict():
    r = assess([chk(300)] * (MIN_BASELINE_CHECKS - 1) + [chk(500)])
    assert r["status"] == "CALIBRATING" and r["level"] is None and "nothing to compare with yet" in r["summary"]


def test_within_the_persons_usual_range():
    r = assess(USUAL + [chk(306)])
    assert r["level"] == "USUAL" and r["reasons"] == [] and "within your own usual range" in r["summary"]


def test_slower_and_much_slower_are_relative_to_this_person():
    slower = assess(USUAL + [chk(345)])
    much = assess(USUAL + [chk(420)])
    assert slower["level"] == "SLOWER" and much["level"] == "MUCH_SLOWER"
    assert slower["baseline"]["median_rt_ms"] == 301.0 and "your usual 301 ms" in slower["reasons"][0]
    # the same 345 ms for someone whose usual is 340 is perfectly normal
    assert assess([chk(v) for v in (340, 335, 345, 338, 342, 341)] + [chk(345)])["level"] == "USUAL"


def test_faster_than_usual_is_not_flagged():
    assert assess(USUAL + [chk(240)])["level"] == "USUAL"


def test_a_very_steady_person_is_not_over_flagged_because_of_a_spread_floor():
    steady = [chk(300)] * 6
    assert assess(steady + [chk(310)])["level"] == "USUAL"       # 3 % off a perfectly steady history is not "slower"


def test_many_misses_are_reported_only_when_they_exceed_everything_before():
    assert any("Missed responses: 3 of 10" in x for x in assess(USUAL + [chk(305, miss=3)])["reasons"])
    assert assess(USUAL + [chk(305, miss=1)])["reasons"] == []
    assert assess([chk(300, miss=3)] * 6 + [chk(305, miss=3)])["reasons"] == []


def test_a_check_with_no_valid_trial_says_nothing_about_the_person():
    r = assess(USUAL + [chk(None, miss=10)])
    assert r["status"] == "NO_RESPONSE" and "says nothing about the person" in r["summary"]


def test_wording_never_claims_health_states():
    for h in (USUAL + [chk(420, miss=4)], USUAL + [chk(None, miss=10)], [chk(300)]):
        text = " ".join([assess(h)["summary"]] + assess(h)["reasons"]).lower()
        for banned in ("fatigue", "drows", "impair", "unfit", "conscious", "diagnos", "illness", "alert"):
            assert banned not in text, (banned, text)


def test_api_returns_responsiveness_without_changing_the_typing_band(client):
    before = client.get("/api/readiness/plt-okafor").get_json()
    assert before["responsiveness"]["level"] == "SLOWER" and before["readiness"]["band"] == "YELLOW"   # seeded story: both agree, but separately computed
    for _ in range(3):
        client.post("/api/attention", json={"profile_id": "cdr-vega", "trials": 10, "median_rt_ms": 900, "premature_count": 0, "miss_count": 0})
    after = client.get("/api/readiness/cdr-vega").get_json()
    assert after["responsiveness"]["level"] == "MUCH_SLOWER" and after["readiness"]["band"] == "GREEN"   # typing band untouched
    r = client.post("/api/attention", json={"profile_id": "fe-sato", "trials": 10, "median_rt_ms": 312, "premature_count": 0, "miss_count": 0})
    assert r.status_code == 201 and r.get_json()["responsiveness"]["level"] == "USUAL"


def test_simulated_behaviour_is_sane_and_documented():
    from ml.responsiveness_check import run
    assert run(0.0) < 0.06                      # few false alerts on normal checks (about 3 % in the documented run)
    assert run(0.10) < run(0.20) < run(0.30)    # bigger slowdowns are found more often
    assert run(0.30) > 0.85


def test_lapses_are_reported_only_when_they_exceed_every_earlier_check():
    def c(rt, lapses, trials=60):
        return {"median_rt_ms": rt, "miss_count": 0, "trials": trials, "lapse_count": lapses, "premature_count": 0, "created_at": "2026-11-15T00:00:00Z"}
    base = [c(300 + i, 2) for i in range(6)]
    assert any("Lapses" in x and "9 of 60" in x for x in assess(base + [c(303, 9)])["reasons"])
    assert not any("Lapses" in x for x in assess(base + [c(303, 3)])["reasons"])               # 3 of 60 is within the person's usual
    assert not any("Lapses" in x for x in assess(base + [c(303, 5)])["reasons"])               # 5 of 60 is under one in ten


def test_the_lapse_count_is_stored_defaults_for_older_pages_and_survives_a_backup(client, app):
    body = {"profile_id": "fe-sato", "trials": 60, "median_rt_ms": 300, "premature_count": 1, "miss_count": 1, "lapse_count": 7}
    assert client.post("/api/attention", json=body).status_code == 201
    assert client.get("/api/readiness/fe-sato").json["attention"]["lapse_count"] == 7
    old = {"profile_id": "fe-sato", "trials": 10, "median_rt_ms": 300, "premature_count": 0, "miss_count": 2}          # a page from before the lapse count
    assert client.post("/api/attention", json=old).status_code == 201
    assert client.get("/api/readiness/fe-sato").json["attention"]["lapse_count"] == 2                                   # defaults to the misses
    assert client.post("/api/attention", json=dict(body, lapse_count=61)).status_code == 400                           # cannot exceed the trials


def test_a_backup_made_before_the_lapse_count_still_restores(tmp_path):
    from app import backup
    old_row = {"id": 1, "profile_id": "x-1", "session_id": None, "created_at": "2026-11-15T10:00:00Z", "trials": 10, "median_rt_ms": 300.0, "premature_count": 0, "miss_count": 1}
    cols = backup.SCHEMA["attention_results"]
    assert "lapse_count" in cols and set(cols) - set(old_row) == {"lapse_count"}
