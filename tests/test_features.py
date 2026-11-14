"""The data contract is our privacy boundary. These tests make it enforceable."""
import pytest

from app.features import ValidationError, assess_quality, validate_session_payload
from tests.conftest import valid_features, valid_payload


def test_valid_payload_passes():
    clean = validate_session_payload(valid_payload())
    assert clean["profile_id"] == "plt-okafor"
    assert clean["features"]["pause_count"] == 1


@pytest.mark.parametrize("bad_key", ["typed_text", "keys", "raw_keystrokes", "password"])
def test_privacy_unknown_feature_is_rejected(bad_key):
    payload = valid_payload()
    payload["features"][bad_key] = "CORRIDOR CLEAR"
    with pytest.raises(ValidationError, match="Unexpected feature"):
        validate_session_payload(payload)


def test_privacy_unknown_top_level_field_is_rejected():
    payload = valid_payload()
    payload["text"] = "anything"
    with pytest.raises(ValidationError, match="Unexpected top-level"):
        validate_session_payload(payload)


def test_missing_feature_is_rejected():
    payload = valid_payload()
    del payload["features"]["iki_median_ms"]
    with pytest.raises(ValidationError, match="Missing"):
        validate_session_payload(payload)


@pytest.mark.parametrize("field,value", [
    ("iki_median_ms", "fast"),      # not a number
    ("pause_count", True),          # bool sneaks in as int in Python
    ("pause_count", 1.5),           # counts must be whole
    ("iki_median_ms", 5.0),         # below plausible range
    ("task_duration_ms", -1),       # negative
])
def test_bad_values_are_rejected(field, value):
    with pytest.raises(ValidationError):
        validate_session_payload(valid_payload(**{field: value}))


def test_unknown_task_type_is_rejected():
    payload = valid_payload()
    payload["task_type"] = "free_typing"
    with pytest.raises(ValidationError, match="task_type"):
        validate_session_payload(payload)


def test_quality_flags_incomplete_task():
    quality, notes = assess_quality(valid_features(keystroke_count=20))
    assert quality == "low" and notes


def test_quality_ok_for_normal_session():
    assert assess_quality(valid_features()) == ("ok", [])
