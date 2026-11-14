"""Provenance and budget for every image we ship. See docs/ASSETS.md."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMG_DIR = ROOT / "app" / "static" / "img"
ASSETS_DOC = (ROOT / "docs" / "ASSETS.md").read_text(encoding="utf-8")
BUDGET_BYTES = 400_000


def images():
    return sorted(p for p in IMG_DIR.glob("*") if p.is_file())


def test_there_are_images_to_check():
    assert images(), "the landing page expects images in app/static/img/"


def test_every_image_has_recorded_provenance():
    missing = [p.name for p in images() if p.name not in ASSETS_DOC]
    assert not missing, f"add a section to docs/ASSETS.md for: {missing}"


def test_every_image_section_records_a_licence_and_a_credit():
    for p in images():
        section = ASSETS_DOC.split(f"`{p.name}`", 1)[1].split("\n## ", 1)[0]
        assert "Licence" in section and ("Credit" in section or "credit" in section), p.name


def test_images_stay_within_the_size_budget():
    heavy = {p.name: p.stat().st_size for p in images() if p.stat().st_size > BUDGET_BYTES}
    assert not heavy, f"over {BUDGET_BYTES} bytes: {heavy}"


def test_landing_credits_the_images_and_describes_the_illustration(client):
    html = client.get("/").data.decode()
    assert "NASA/JPL-Caltech" in html and "public domain" in html       # visible credit
    assert 'class="sr-only"' in html and "astronaut" in html            # the art has words for assistive tech
