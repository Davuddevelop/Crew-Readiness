"""
JSON API. Every endpoint here is documented in docs/DATA_CONTRACT.md.
The pages (views.py) are thin shells; they fetch everything from here.
"""
from __future__ import annotations

from flask import Blueprint, current_app, jsonify, request
from werkzeug.exceptions import HTTPException

from . import store
from .db import get_db
from .features import ValidationError, assess_quality, validate_session_payload
from .mission import MISSION, mission_advisory
from .readiness import readiness_for_all, readiness_for_profile
from .tasks import TASKS

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.errorhandler(ValidationError)
def _validation_error(err: ValidationError):
    return jsonify(error="validation_error", message=str(err)), 400


@bp.errorhandler(HTTPException)
def _http_error(err: HTTPException):
    return jsonify(error=err.name.lower().replace(" ", "_"), message=err.description), err.code


def _require_profile(profile_id: str) -> dict | None:
    return store.get_profile(get_db(), profile_id)


@bp.get("/health")
def health():
    db = get_db()
    db.execute("SELECT 1").fetchone()
    return jsonify(status="ok", version=current_app.config["APP_VERSION"],
                   profiles=len(store.list_profiles(db)))


@bp.get("/tasks/<task_type>")
def get_task(task_type: str):
    task = TASKS.get(task_type)
    if task is None:
        return jsonify(error="not_found", message=f"Unknown task type {task_type!r}."), 404
    return jsonify(task_type=task_type, **task)


@bp.get("/profiles")
def list_profiles():
    return jsonify(profiles=store.list_profiles(get_db()))


@bp.post("/sessions")
def create_session():
    """Store one completed task. Body: {profile_id, task_type, features{...}}."""
    clean = validate_session_payload(request.get_json(silent=True))
    db = get_db()
    profile = _require_profile(clean["profile_id"])
    if profile is None:
        return jsonify(error="not_found", message="Unknown profile_id."), 404

    quality, notes = assess_quality(clean["features"])
    session_id = store.insert_session(
        db, profile_id=profile["id"], task_type=clean["task_type"],
        features=clean["features"], source="live", data_quality=quality,
        quality_notes="; ".join(notes) or None,
    )
    db.commit()
    result = readiness_for_profile(db, profile, clean["task_type"])
    return jsonify(session_id=session_id, **result), 201


@bp.get("/readiness")
def readiness_all():
    return jsonify(crew=readiness_for_all(get_db()))


@bp.get("/readiness/<profile_id>")
def readiness_one(profile_id: str):
    profile = _require_profile(profile_id)
    if profile is None:
        return jsonify(error="not_found", message="Unknown profile_id."), 404
    return jsonify(readiness_for_profile(get_db(), profile))


@bp.post("/attention")
def create_attention_result():
    """Store a reaction-time attention check result (task A-1).

    Body: {profile_id, session_id?, trials, median_rt_ms|null, premature_count, miss_count}
    """
    body = request.get_json(silent=True) or {}
    allowed = {"profile_id", "session_id", "trials", "median_rt_ms",
               "premature_count", "miss_count"}
    if not isinstance(body, dict) or set(body) - allowed:
        raise ValidationError(f"Only these fields are accepted: {sorted(allowed)}.")

    profile = _require_profile(str(body.get("profile_id", "")))
    if profile is None:
        return jsonify(error="not_found", message="Unknown profile_id."), 404

    def _int(name: str, lo: int, hi: int) -> int:
        v = body.get(name)
        if isinstance(v, bool) or not isinstance(v, int) or not lo <= v <= hi:
            raise ValidationError(f"{name} must be an integer in [{lo}, {hi}].")
        return v

    trials = _int("trials", 1, 100)
    premature = _int("premature_count", 0, 1000)
    misses = _int("miss_count", 0, trials)
    rt = body.get("median_rt_ms")
    if rt is not None and (isinstance(rt, bool) or not isinstance(rt, (int, float))
                           or not 50 <= rt <= 5000):
        raise ValidationError("median_rt_ms must be null or a number in [50, 5000].")
    session_id = body.get("session_id")
    if session_id is not None and (isinstance(session_id, bool) or not isinstance(session_id, int)):
        raise ValidationError("session_id must be an integer or null.")

    db = get_db()
    result_id = store.insert_attention_result(
        db, profile_id=profile["id"], session_id=session_id, trials=trials,
        median_rt_ms=None if rt is None else float(rt),
        premature_count=premature, miss_count=misses,
    )
    db.commit()
    return jsonify(id=result_id), 201


@bp.get("/mission")
def mission():
    db = get_db()
    assignments = []
    for a in MISSION["assignments"]:
        profile = store.get_profile(db, a["profile_id"])
        if profile is None:
            continue
        r = readiness_for_profile(db, profile, with_trend=False)["readiness"]
        assignments.append({**a, "display_name": profile["display_name"],
                            "mission_role": profile["mission_role"],
                            "status": r["status"], "band": r["band"],
                            "confidence": r["confidence"], "reasons": r["reasons"]})
    return jsonify(
        name=MISSION["name"],
        critical_operation=MISSION["critical_operation"],
        t_minus_hours=MISSION["t_minus_hours"],
        assignments=assignments,
        advisory=mission_advisory(assignments),
    )
