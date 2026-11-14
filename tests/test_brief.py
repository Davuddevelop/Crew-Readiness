"""The printable readiness brief: a plain page for the human reviewer; levels and words come from the server, nothing is stored."""


def test_brief_page_has_the_limits_and_a_hand_filled_record(client):
    html = client.get("/brief").get_data(as_text=True)
    assert "js/brief.js" in html and "What this brief cannot tell you" in html
    assert "Nothing here is stored" in html and "does not say anyone is fit or unfit" in html
    assert "Print or save as PDF" in html


def test_brief_is_linked_from_mission_and_reads_the_mission_api(client):
    assert 'href="/brief"' in client.get("/mission").get_data(as_text=True)
    js = client.get("/static/js/brief.js").get_data(as_text=True)
    assert '"/api/mission"' in js and "fetch(" not in js.replace("api(", "")   # data only via the shared api() helper
    assert client.get("/api/mission").get_json()["advisory"]["level"] in ("NOMINAL", "CHECK_IN", "REVIEW")
