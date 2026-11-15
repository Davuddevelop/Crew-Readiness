"""W4: the alert-burden calculator is driven by the benchmark file's own rates and makes no requests of its own."""
import json
import re

from app import views


def test_calculator_options_are_the_results_files_rates(client):
    html = client.get("/evidence").get_data(as_text=True)
    assert 'id="alert-burden"' in html and 'src="/static/js/burden.js"' in html
    data = json.loads(re.search(r'<script type="application/json" id="burden-data">(.*?)</script>', html, re.S).group(1))
    file = json.loads(views.RESULTS_FILE.read_text())["budget_calibration"]
    rates = [o["rate"] for o in data["options"]]
    assert rates == [r["observed"] for r in file["rows"]] + [file["shipped"]["false_alert_rate"]]
    assert data["options"][-1]["label"].startswith("The level the product uses (about 1 in 24")
    assert "from simulated people" in html and "your own assumption" in html           # what it is and is not


def test_calculator_script_cannot_send_anything(client):
    js = client.get("/static/js/burden.js").get_data(as_text=True)
    code = re.sub(r"/\*.*?\*/|//[^\n]*", "", js, flags=re.S)
    for forbidden in ("fetch(", "XMLHttpRequest", "sendBeacon", "WebSocket", "import "):
        assert forbidden not in code
