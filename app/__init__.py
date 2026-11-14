"""Crew Readiness — Flask application factory."""
from __future__ import annotations

import os
from pathlib import Path

from flask import Flask


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    # CREW_DB_PATH lets a host point the database somewhere writable (see index.py:
    # serverless hosts only allow writes under /tmp). Locally it defaults to instance/.
    default_db = os.environ.get("CREW_DB_PATH") or str(
        Path(app.instance_path) / "crew_readiness.sqlite3")
    app.config.from_mapping(
        DATABASE=default_db,
        APP_VERSION="0.1.0-prototype",
        AUTO_SEED=True,   # first run creates the DB and loads the fictional demo crew
    )
    app.json.sort_keys = False  # keep API fields in a readable order
    if test_config:
        app.config.update(test_config)
    # Create the folder the database actually lives in, not a hard-coded instance/.
    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)

    from . import api, cli, db, views
    db.init_app(app)
    cli.init_app(app)
    app.register_blueprint(views.bp)
    app.register_blueprint(api.bp)

    if app.config["AUTO_SEED"]:
        with app.app_context():
            if not db.is_initialized():
                from .seed import seed_demo
                db.init_db()
                seed_demo(db.get_db())
                app.logger.info("Initialised database with fictional demo crew.")
            else:
                db.ensure_columns()

    return app
