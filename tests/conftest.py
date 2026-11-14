import pytest

from app import create_app
from app.db import get_db, init_db
from app.seed import seed_demo


@pytest.fixture
def app(tmp_path):
    """Empty app with a throwaway database."""
    app = create_app({"TESTING": True, "DATABASE": str(tmp_path / "test.sqlite3"),
                      "AUTO_SEED": False})
    with app.app_context():
        init_db()
    return app


@pytest.fixture
def seeded_app(app):
    with app.app_context():
        seed_demo(get_db())
    return app


@pytest.fixture
def client(seeded_app):
    return seeded_app.test_client()


def valid_features(**overrides):
    f = {
        "keystroke_count": 125,
        "iki_median_ms": 190.0,
        "iki_iqr_ms": 75.0,
        "pause_count": 1,
        "pause_total_ms": 2600.0,
        "checklist_response_median_ms": 1500.0,
        "task_duration_ms": 45000.0,
        "correction_count": 2,
        "retry_count": 0,
    }
    f.update(overrides)
    return f


def valid_payload(**feature_overrides):
    return {"profile_id": "plt-okafor", "task_type": "docking_checklist_v1",
            "features": valid_features(**feature_overrides)}
