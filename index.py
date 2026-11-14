"""
Vercel entrypoint. Vercel looks for a WSGI object named `app` in a root file such as
index.py. Locally, keep using `python run.py`.

Serverless functions can only write to /tmp, so the SQLite file goes there.
CONSEQUENCE (important, see README -> Deploy): that database is private to one function
instance and disappears when the instance is recycled. Each new instance re-seeds the
same fictional crew, so the dashboard looks identical everywhere, but sessions submitted
through the hosted Monitoring page are NOT durable and may not be visible on the next request.
"""
import os

os.environ.setdefault("CREW_DB_PATH", "/tmp/crew_readiness.sqlite3")

from app import create_app  # noqa: E402  (must come after CREW_DB_PATH is set)

app = create_app()
