"""
Developer commands. Run from the repo root, e.g.:

    flask --app run reset-demo
    flask --app run add-profile tester-a "Test Subject A" Pilot
"""
import click
from flask import Flask

from . import store
from .db import get_db, init_db
from .seed import seed_demo


def init_app(app: Flask) -> None:

    @app.cli.command("reset-demo")
    @click.confirmation_option(prompt="This deletes ALL sessions. Continue?")
    def reset_demo():
        """Wipe the database and reload the fictional demo crew."""
        init_db()
        seed_demo(get_db())
        click.echo("Database reset and demo crew seeded.")

    @app.cli.command("reset-empty")
    @click.confirmation_option(prompt="This deletes ALL data. Continue?")
    def reset_empty():
        """Wipe the database with no demo data (for clean validation runs)."""
        init_db()
        click.echo("Database reset (empty).")

    @app.cli.command("add-profile")
    @click.argument("profile_id")
    @click.argument("display_name")
    @click.argument("mission_role")
    def add_profile(profile_id, display_name, mission_role):
        """Add a pseudonymous team_test profile for real validation sessions."""
        db = get_db()
        store.insert_profile(db, profile_id, display_name, mission_role, kind="team_test")
        db.commit()
        click.echo(f"Added team_test profile {profile_id!r}. Use a pseudonym, never a real name.")
