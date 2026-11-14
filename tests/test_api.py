"""End-to-end through HTTP. The 'demo' tests protect the pitch: if they fail, fix before demo."""
from tests.conftest import valid_payload


def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200 and r.json["status"] == "ok"


def test_all_pages_render(client):
    for path in ["/", "/dashboard", "/monitor", "/attention", "/mission", "/about"]:
        assert client.get(path).status_code == 200, path


def test_landing_and_dashboard_are_distinct_pages(client):
    assert b"A second look before docking" in client.get("/").data
    assert b"Compared only with yourself" in client.get("/dashboard").data


def test_no_page_calls_out_to_the_network(client):
    """Offline demo rule (risk R-6): every script, stylesheet and font is served by us."""
    import re
    for path in ["/", "/dashboard", "/monitor", "/attention", "/mission", "/about"]:
        html = client.get(path).data.decode()
        links_out = re.findall(r'<(?:script|link|img)[^>]+(?:src|href)=["\'](https?://[^"\']+)', html)
        assert not links_out, f"{path} loads from the network: {links_out}"


# ---------- demo story protection ----------

def _by_id(client):
    return {c["profile"]["id"]: c for c in client.get("/api/readiness").json["crew"]}


def test_demo_pilot_shows_yellow_with_reasons(client):
    pilot = _by_id(client)["plt-okafor"]["readiness"]
    assert pilot["status"] == "SCORED" and pilot["band"] == "YELLOW"
    assert pilot["reasons"], "the demo needs plain-language reasons"


def test_demo_has_a_calibrating_member(client):
    assert _by_id(client)["ms-ibarra"]["readiness"]["status"] == "CALIBRATING"


def test_demo_commander_is_green(client):
    assert _by_id(client)["cdr-vega"]["readiness"]["band"] == "GREEN"


# ---------- session submission ----------

def test_submit_session_returns_readiness(client):
    r = client.post("/api/sessions", json=valid_payload())
    assert r.status_code == 201
    assert r.json["latest_session"]["source"] == "live"
    assert r.json["readiness"]["status"] == "SCORED"


def test_privacy_text_is_rejected_and_not_stored(client):
    before = len(client.get("/api/readiness/plt-okafor").json["trend"])
    payload = valid_payload()
    payload["features"]["typed_text"] = "CORRIDOR CLEAR"
    r = client.post("/api/sessions", json=payload)
    assert r.status_code == 400
    after = client.get("/api/readiness/plt-okafor").json
    assert len(after["trend"]) == before
    assert "typed_text" not in str(after)


def test_unknown_profile_404(client):
    payload = valid_payload()
    payload["profile_id"] = "nobody"
    assert client.post("/api/sessions", json=payload).status_code == 404


def test_non_json_body_400(client):
    r = client.post("/api/sessions", data="not json", content_type="text/plain")
    assert r.status_code == 400


# ---------- attention endpoint (used by task A-1) ----------

def test_attention_result_roundtrip(client):
    body = {"profile_id": "plt-okafor", "trials": 10, "median_rt_ms": 312.5,
            "premature_count": 1, "miss_count": 0}
    assert client.post("/api/attention", json=body).status_code == 201
    latest = client.get("/api/readiness/plt-okafor").json["attention"]
    assert latest["median_rt_ms"] == 312.5


def test_attention_rejects_extra_fields(client):
    body = {"profile_id": "plt-okafor", "trials": 10, "median_rt_ms": 300,
            "premature_count": 0, "miss_count": 0, "notes": "free text"}
    assert client.post("/api/attention", json=body).status_code == 400


# ---------- trend carries what the dashboard art draws ----------

def test_trend_has_per_feature_deviations_for_scored_sessions(client):
    from app.scoring import SCORED_FEATURES
    trend = client.get("/api/readiness/plt-okafor").json["trend"]
    assert len(trend) == 14, "one line of art per session"
    latest = trend[-1]
    assert set(latest["deviations"]) == set(SCORED_FEATURES)
    assert latest["deviations"]["iki_median_ms"] > 3, "the seeded demo deviation must show"


def test_latest_trend_point_matches_the_readiness_evidence(client):
    data = client.get("/api/readiness/plt-okafor").json
    evidence = {d["feature"]: d["deviation"] for d in data["readiness"]["deviations"]}
    assert data["trend"][-1]["deviations"] == evidence


def test_trend_deviations_are_null_while_calibrating(client):
    trend = client.get("/api/readiness/ms-ibarra").json["trend"]
    assert trend and all(t["deviations"] is None for t in trend)


def test_evidence_page_renders_from_the_results_file(client):
    import json
    from app.views import RESULTS_FILE
    r = client.get("/evidence")
    assert r.status_code == 200
    html = r.data.decode()
    assert "Synthetic data" in html and "Simulated data only" in html and "fatigue" in html
    data = json.loads(RESULTS_FILE.read_text())
    assert data["synthetic"] is True
    for row in data["table"]:                           # every number on the page comes from the file
        assert f"{row['neg_binomial']:.2f}" in html and f"{row['incumbent']:.2f}" in html


def test_evidence_operating_point_numbers_come_from_the_file(client):
    import json
    from app.views import RESULTS_FILE
    html = client.get("/evidence").data.decode()
    for row in json.loads(RESULTS_FILE.read_text())["operating_point"]:
        assert f"{row['now']['false_alerts'] * 100:.1f} %" in html
        assert f"{row['now']['detection']:.2f}" in html
