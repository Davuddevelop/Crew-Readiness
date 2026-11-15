"""H3: private notes live only in the browser. The file that handles them must be unable to send them anywhere, and the server must have no place to put them."""
import re


def test_the_notes_script_cannot_send_anything(client):
    js = client.get("/static/js/notes.js").get_data(as_text=True)
    code = re.sub(r"/\*.*?\*/|//[^\n]*", "", js, flags=re.S)                      # ignore comments, which explain what is NOT used
    for forbidden in ("fetch(", "XMLHttpRequest", "sendBeacon", "api(", "WebSocket", "import ", "EventSource"):
        assert forbidden not in code, forbidden
    assert "localStorage" in code and "clipboard" in code


def test_the_server_has_no_route_or_column_for_notes(client, app):
    rules = {r.rule for r in app.url_map.iter_rules()}
    assert not any("note" in r.lower() for r in rules)
    schema = open(__import__("pathlib").Path(app.root_path) / "schema.sql", encoding="utf-8").read().lower()
    assert "sleep" not in schema and not re.search(r"^\s*(notes?|feel\w*|mood\w*)\s", schema, re.M)      # no column that could hold them


def test_my_status_explains_where_notes_live_and_what_they_are_not(client):
    html = client.get("/me").get_data(as_text=True)
    assert 'id="me-notes"' in html and "These stay on this device" in html and "never sent to the app" in html
    assert "does not use them in your status" in html and "js/notes.js" in html


def test_insight_script_sends_no_note_data_and_the_history_endpoint_is_read_only(client):
    js = client.get("/static/js/insight.js").get_data(as_text=True)
    code = re.sub(r"/\*.*?\*/|//[^\n]*", "", js, flags=re.S)
    for forbidden in ("method:", "POST", "body:", "sendBeacon", "XMLHttpRequest", "WebSocket", "fetch("):
        assert forbidden not in code, forbidden
    assert code.count("api(") == 1 and "/api/attention/" in code and "localStorage.getItem" in code and "localStorage.setItem" not in code
    r = client.get("/api/attention/fe-sato")
    assert r.status_code == 200 and set(r.get_json()["checks"][0]) == {"created_at", "median_rt_ms", "trials", "miss_count", "lapse_count"}
    assert client.get("/api/attention/nobody").status_code == 404
    assert client.post("/api/attention/fe-sato", json={}).status_code == 405                  # no way to write through this route


def test_my_status_explains_the_insight_and_that_it_is_not_a_finding(client):
    html = client.get("/me").get_data(as_text=True)
    assert 'id="notes-insight"' in html and "not a finding and not advice" in html and "nothing is sent" in html and "js/insight.js" in html
