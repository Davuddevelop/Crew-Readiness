"""The numbers in docs/SUBMISSION.md must come from the benchmark output, not from memory."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = (ROOT / "docs" / "SUBMISSION.md").read_text(encoding="utf-8")
DATA = json.loads((ROOT / "app" / "results_data.json").read_text(encoding="utf-8"))


def row(slowdown, burstiness=None):
    return next(r for r in (DATA["table"] if burstiness else DATA["operating_point"])
                if r["slowdown"] == slowdown and (burstiness is None or r["burstiness"] == burstiness))


def test_operating_point_numbers_match_the_results_file():
    r = row(0.1)
    assert f"**{r['before']['detection']:.2f}** to **{r['now']['detection']:.2f}**" in DOC
    assert f"**{r['before']['false_alerts'] * 100:.1f} %** to about **{r['now']['false_alerts'] * 100:.1f} %**" in DOC


def test_matched_false_alert_numbers_match_the_results_file():
    none, high = row(0.1, "none"), row(0.1, "high")
    assert f"**{none['incumbent']:.2f}** to **{none['neg_binomial']:.2f}**" in DOC
    assert f"**{high['incumbent']:.2f}** to **{high['neg_binomial']:.2f}**" in DOC


def test_the_document_states_its_limits_and_placeholders():
    for phrase in ("on simulated data only", "No real people", "partly circular", "Nothing here detects fatigue or illness", "approved or endorsed by NASA",
                   "[TEAM NAME]", "[EXACT CHALLENGE TITLE"):
        assert phrase in DOC
