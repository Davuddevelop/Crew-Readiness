"""HTML pages. Deliberately thin: each page loads its data from /api/* with JavaScript."""
from flask import Blueprint, render_template

from .tasks import DEFAULT_TASK_TYPE, TASKS

bp = Blueprint("views", __name__)


@bp.get("/")
def dashboard():
    return render_template("dashboard.html", active="dashboard")


@bp.get("/monitor")
def monitor():
    return render_template("monitor.html", active="monitor",
                           task_type=DEFAULT_TASK_TYPE, task=TASKS[DEFAULT_TASK_TYPE])


@bp.get("/attention")
def attention():
    return render_template("attention.html", active="attention")


@bp.get("/mission")
def mission():
    return render_template("mission.html", active="mission")


@bp.get("/about")
def about():
    return render_template("about.html", active="about")
