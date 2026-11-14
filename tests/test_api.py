"""End-to-end through HTTP. The 'demo' tests protect the pitch: if they fail, fix before demo."""
from tests.conftest import valid_payload


def test_health(client):
    r = client.get("/api/health")
    assert r.status_code == 200 and r.json["status"] == "ok"


def test_all_pages_render(client):
    for path in ["/", "/monitor", "/attention", "/mission", "/about"]:
        assert client.get(path).status_code == 200, path


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
