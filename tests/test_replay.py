"""The Replay endpoint: deterministic, validated, and labelled synthetic."""


def get(client, **q):
    return client.get("/api/simulate", query_string=q)


def test_same_seed_same_result_different_seed_different(client):
    a = get(client, scenario="step", seed=3).get_json()
    assert a == get(client, scenario="step", seed=3).get_json()
    assert a["sessions"] != get(client, scenario="step", seed=4).get_json()["sessions"]


def test_result_is_labelled_synthetic_and_has_both_models(client):
    d = get(client, scenario="step", magnitude=0.25, length=10, seed=1).get_json()
    assert d["synthetic"] is True and len(d["sessions"]) == 40
    assert sum(s["event"] for s in d["sessions"]) == 10
    assert {"before", "now"} == set(d["summary"])
    assert all(s["before"] is None for s in d["sessions"][:5])          # calibrating, no score invented


def test_steady_scenario_has_no_event(client):
    d = get(client, scenario="steady", seed=2).get_json()
    assert not any(s["event"] for s in d["sessions"])


def test_a_big_sustained_slowdown_is_flagged_by_the_new_scoring(client):
    d = get(client, scenario="step", magnitude=0.4, length=12, seed=5).get_json()
    assert d["summary"]["now"]["flagged_in_event"] >= d["summary"]["before"]["flagged_in_event"]
    assert d["summary"]["now"]["flagged_in_event"] > 0


def test_bad_parameters_are_rejected(client):
    for q in ({"scenario": "nope"}, {"magnitude": 5}, {"length": 0}, {"seed": -1}, {"magnitude": "x"}):
        assert get(client, **q).status_code == 400


def test_replay_page_renders(client):
    r = client.get("/replay")
    assert r.status_code == 200 and "Synthetic" in r.data.decode()


def test_equipment_change_scenario_tells_the_whole_story(client):
    d = client.get("/api/simulate?scenario=equipment&magnitude=0.4&seed=1").get_json()
    assert d["synthetic"] and d["scenario"] == "equipment" and len(d["sessions"]) == 45
    assert d["accepted_sessions"] > 0                                      # a big change is flagged, so there is a run to accept
    assert [r[0] for r in d["table"]["rows"]] == ["Old scoring", "Current scoring"]
    assert len(d["table"]["headers"]) == 4 and all(len(r) == 4 for r in d["table"]["rows"])
    assert {b["label"] for b in d["bands"]} == {"New equipment", "A real slowdown"}


def test_a_tiny_equipment_change_has_nothing_to_accept(client):
    d = client.get("/api/simulate?scenario=equipment&magnitude=0.03&seed=2").get_json()
    assert d["accepted_sessions"] == 0 and "Nothing was flagged" in d["markers"][0]["label"]
