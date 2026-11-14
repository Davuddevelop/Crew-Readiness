# Notes for coding agents (Codex etc.)

Crew Readiness: Flask + vanilla JS + SQLite + NumPy. Decision support that flags changes in a person's task-interaction
timing against their OWN baseline, for a human to review. Start with `docs/NEXT_STEPS.md`, `docs/TEAM_GUIDE.md` (code tour),
`docs/ML_RESULTS.md`.

Run: `python -m venv .venv && .venv/bin/pip install -r requirements.txt`, then `python run.py` (http://127.0.0.1:5050).
Before every change is done: `.venv/bin/python -m pytest -q` (expect everything passing, some skipped) and, with the app running,
`node scripts/check_grid.js`.

Non-negotiable:
- **Privacy:** never store or send typed text, key identities or raw keystroke timelines. Only the nine aggregate features in `app/features.py`.
- **Honest claims:** never say it detects fatigue, illness or fitness for duty, or that NASA approved it. Anything from the benchmark is
  "simulated". Do not edit `app/results_data.json` by hand; regenerate it with `python -m ml.export_results`.
- **Positioning:** it is a prototype of on-board decision support, tested only on simulated data. Never write that astronauts use it, that it is proven or tested in space, or that it is validated on crews.
- **No network at runtime** (no CDN fonts or scripts); a test enforces it.
- **Images:** only public-domain or licensed, recorded in `docs/ASSETS.md` (a test enforces it).
- **Design:** one grid, one typeface, colour only for status. Read `docs/DESIGN.md` before changing styles. No new gradients, shadows or glass.
- Keep changes small, one topic per branch/PR, and update the relevant doc and tests in the same change. Don't leave TODO text on user-visible pages.
