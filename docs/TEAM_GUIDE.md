# Team Guide: Read This First

Welcome aboard. This guide gets you from zero to productive in about **40 minutes**: 10 to set up, 15 to read the code, 15 to answer the comprehension questions. Then you pick up your task card.

> **How we work:** we're engineers, not prompt-forwarders. You may use AI tools, but you must be able to **explain every line you merge** to a judge. If you can't explain it, don't merge it. Ask instead; asking is fast, and debugging code nobody understands at 2 a.m. is slow.

Also read: [PLAN.md](PLAN.md) (the why and when) · [DATA_CONTRACT.md](DATA_CONTRACT.md) (the shapes we all agree on)

---

## 1. The product in 30 seconds

1. A crew member does a **simulated pre-docking checklist** (types fixed confirmation phrases).
2. The browser records **only timing**: gaps between keys, pauses, how long before they start each step. **Never the text.**
3. The server compares those numbers with **that person's own usual numbers** (their baseline).
4. The dashboard shows **GREEN / YELLOW / RED** with plain-language reasons, for a **human** to review before docking.

**It does not detect fatigue.** It detects *changes in how someone interacts*, which *may* merit a check-in. Hold onto this sentence; it's the most important one in the project.

---

## 2. Setup (10 min)

Requires **Python 3.10+** and Git. No Node, no database server.

```bash
git clone https://github.com/Davuddevelop/Crew-Readiness.git
cd Crew-Readiness

python -m venv .venv
# macOS / Linux:
source .venv/bin/activate
# Windows (PowerShell):
.venv\Scripts\Activate.ps1

pip install -r requirements.txt
python run.py
```

Open **http://127.0.0.1:5050**. You should see 4 fictional crew cards; Kai Okafor should be **YELLOW**.

Then run the tests (in a second terminal, venv activated):

```bash
python -m pytest
```

Expected: `36 passed, 6 skipped`. The 6 skipped are the Team Lead's task L-1.

| Problem | Fix |
|---|---|
| `python` not found (macOS/Linux) | use `python3` |
| PowerShell refuses to activate venv | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` then retry |
| Port in use | `PORT=5051 python run.py` (Windows: `$env:PORT=5051; python run.py`) |
| Want fresh demo data | `flask --app run reset-demo` |
| Page shows old JS after you edit it | hard refresh: Ctrl+Shift+R / Cmd+Shift+R |

---

## 3. Codebase tour

```
run.py                  one-command launcher (port 5050)
app/
  __init__.py           app factory; auto-creates + seeds the DB on first run
  features.py           ★ DATA CONTRACT: the 9 allowed features + validation  (Lead + M2)
  schema.sql            SQLite tables (no column can hold text, on purpose)
  store.py              ALL SQL lives here, nowhere else
  baseline.py           ★ median + MAD of a person's past sessions            (Member 2)
  scoring.py            ★ robust z → weighted score → band, reasons           (Member 2)
  readiness.py          glue: load history → baseline → score → trend
  tasks.py              the fixed checklist text (versioned!)
  mission.py            docking scenario + mission_advisory() TODO           (Lead, L-1)
  seed.py               fictional crew + synthetic sessions (demo story)
  api.py                JSON endpoints (documented in DATA_CONTRACT.md)
  views.py              HTML pages (thin shells)
  cli.py                flask commands: reset-demo, reset-empty, add-profile
  templates/            Jinja pages                                           (Member 3)
  static/js/
    capture.js          ★ privacy-preserving timing capture                  (Member 3)
    monitor.js          checklist flow + payload preview + submit            (Member 3)
    dashboard.js        crew selector, detail, trend chart                    (Member 3)
    ridgeline.js        ★ stacked-sessions art, drawn from trend[].deviations (Member 3)
    keytrace.js         live key-press trace on Monitoring (timestamps only)  (Member 3)
    mission.js          mission view
    attention.js        reaction-time check TODO                              (A-1)
    common.js           fetch helper, escaping, chips
  static/vendor/        Chart.js (vendored so the demo works offline)
  static/fonts/         Space Grotesk + JetBrains Mono (self-hosted, SIL OFL)
tests/                  pytest; test_api.py protects the demo story
docs/                   PLAN, TEAM_GUIDE, DATA_CONTRACT, DESIGN, TEST_LOG
```

### Follow one session end to end (do this with the code open)

1. **`monitor.js`**: user clicks Start → `capture.startTask()`. Each step → `capture.startItem()`.
2. **`capture.js` `onKeyDown`**: looks at `event.key` *only* to decide "character / correction / ignore", then stores **a timestamp**. The key itself is thrown away.
3. User presses Enter. `monitor.js` compares the input with the expected phrase **in the browser**. Match → next item; mismatch → `recordRetry()`.
4. After the last item: `capture.summarize()` → 9 numbers. The page **shows them** ("this is everything that leaves the browser").
5. Submit → `POST /api/sessions` → **`api.py`** → **`features.validate_session_payload`**. Any unknown field is a 400.
6. **`store.insert_session`** writes one row. **`readiness.readiness_for_profile`** loads the person's history.
7. **`baseline.compute_baseline`** uses only sessions *before* this one → median and robust spread per feature.
8. **`scoring.score_session`** → z per feature → weighted score → band + reasons + advisory.
9. JSON back to the page → result shown → dashboard reads the same data via `GET /api/readiness`.

---

## 4. Comprehension check (answer before you code)

Post your answers in the team chat. Short answers are fine. If you can't answer one, **that's the point of the exercise**: ask, and we'll fix the gap in 2 minutes now instead of 2 hours later.

1. Name two places where we *enforce* that typed text never reaches the server.
2. Why must the checklist text be identical in every session? What happens to baselines if you edit a phrase in `tasks.py`?
3. Ibarra has 2 sessions in his baseline. Why do we show CALIBRATING instead of a score? What would go wrong if we showed one?
4. Why median and MAD rather than mean and standard deviation? (Hint: `test_baseline_uses_median_and_robust_spread`.)
5. Kai's typing is 219 ms vs. usual 188 ms, which is +3.1 SD, yet his band is only YELLOW. Walk through the arithmetic in `scoring.py` that gives 1.22.
6. Being *faster* than usual scores 0. Is that right? Give one case where faster-than-usual might matter.
7. Why does a session never take part in its own baseline?
8. What's the difference between the `band` and the `confidence`?

---

## 5. How we use Git

* `main` is **always demo-able**. Never commit directly to it.
* Branch per task: `feat/L-1-mission-advisory`, `fix/F-1-monitor-focus`, `docs/R-1-limits`.
* **Small PRs** (ideally < 200 lines), title starts with the task ID: `L-1: mission advisory rules`.
* Before opening a PR: `python -m pytest` is green, and you clicked through the pages you touched.
* The **Team Lead merges**. A second person reviews anything touching `features.py`, `scoring.py`, `baseline.py`, `capture.js`, or `DATA_CONTRACT.md`.
* Pull `main` often (`git pull --rebase origin main`), at least at every checkpoint.
* **Never commit** `instance/` (your local DB) or anything with a real name. `.gitignore` already covers the DB.

---

## 6. Your first tasks

Each card: **goal → files → done when → think about → hints.** If a card is unclear, that's a bug in the card; tell the Lead.

### Team Lead

**L-0 · Repo hygiene** (13:00–13:45)
- Merge this skeleton to `main`; enable branch protection (PR required).
- Create one GitHub issue per task row in PLAN §8; assign owners.
- Run checkpoint C0 (everyone's app runs, tests green).

**L-1 · Mission advisory** (after you decide D-5)
- **Files:** `app/mission.py`, `tests/test_mission.py`
- **Done when:** you've removed the skip marker, all mission tests pass, and the Mission page shows a real advisory for the seeded crew.
- **Think about:** what counts as an alert (decision D-5)? Is CALIBRATING on a critical role "unknown" or "fine"? Should LOW confidence soften wording? What is the *most useful single sentence* for a flight director?
- **Hints:** write the rules as a small table in PLAN D-5 first, then code them. Start from the failing tests: red → green → refactor. The banned-word test is your ethics guardrail; keep it.

**L-2 / L-3 / L-4:** see PLAN §8.

### Member 2: Data & ML

**M-1 · Own the scoring** (13:45–15:30)
- **Files:** `app/baseline.py`, `app/scoring.py`, `tests/test_scoring.py`, `docs/DATA_CONTRACT.md §4`
- **Done when:** you can explain every constant, and you've written a short "keep / change because…" for D-3 and D-4 in PLAN §5.
- **Think about:** Is one-sided deviation right (question 6)? Should a RED session be excluded from future baselines (see the note in `select_baseline_sessions`)? Is MIN = 5 too few? Should `correction_count` or `retry_count` be scored?
- **Hints:** change one constant, run `pytest`, and look at which tests fail and *why*. That's the fastest way to understand a scoring system.

**M-2 · False-alarm simulation** (15:30–19:00): **the most valuable evidence we can bring to judges**
- **Files:** new `scripts/false_alarm_sim.py` (pure Python, reuse `seed._synth_features`, `compute_baseline`, `score_session`)
- **Done when:** a table like "with cutoffs 1.0/2.0, X % of *normal* synthetic sessions are YELLOW and Y % RED; a 12 % slowdown is detected Z % of the time", written into PLAN D-4.
- **Think about:** what trade-off are you making when you raise the YELLOW cutoff? What *should* the false-alarm rate be for a tool whose action is "have a quick chat"?
- **Hints:** 1,000 simulated normal sessions per person; for each, build a baseline from 14 others. Remember this only measures the noise *in our synthetic model*, so say so.

**M-3 · Stretch: Isolation Forest** (Nov 15, only after C2)
- Secondary "unusualness" signal shown **next to**, never instead of, the explainable score. Show a sample-size warning when n < 15. Never present it as a probability.

### Member 3: Frontend & UX

**F-1 · "A judge can do it without explanation"** (13:45–17:00)
- **Files:** `templates/monitor.html`, `templates/dashboard.html`, `static/js/monitor.js`, `static/js/dashboard.js`, `static/css/style.css`
- **Done when:** Member 4 (or someone outside the team) completes Monitoring → Dashboard **without you saying anything**, and you've fixed the top 3 points where they hesitated.
- **Think about:** what should a GREEN card say? (Right now Vega is GREEN but shows a +1.9 SD reason; is that reassuring or confusing?) Where does the eye go first on the detail panel?
- **Hints:** watch silently, take notes, don't help. Colour must never be the only signal (chips already show text; keep it that way).

**F-2 · Trend + evidence readability** (17:00–21:00)
- `renderTrend` in `dashboard.js` is minimal. Ideas: tooltip with band and score, distinguish synthetic vs. live points, mark the latest session. The evidence table could highlight rows that drive the score.

**F-3 · Responsive + accessibility** (Nov 15): keyboard-only run-through, 390 px phone width, contrast check.

> ⚠️ `capture.js` is privacy-critical. Changes need review from Member 2 **and** the Lead. Never add anything that stores `event.key`, `input.value`, or a per-keystroke timeline.

### Member 4: Research, Validation & QA

**V-1 · Validation protocol** (13:45–15:00)
- **File:** `docs/TEST_LOG.md` (template provided)
- **Done when:** protocol written *before* any session: participants, device, time of day, how many baseline sessions, what perturbation, what you predict.
- **Hints:** set up pseudonymous profiles with `flask --app run add-profile tester-a "Tester A" Pilot`. Use `flask --app run reset-empty` for a clean validation DB (but **export the log first**; it wipes everything).

**R-1 · Privacy & limits page** (13:45–17:00)
- **File:** `app/templates/about.html` (the TODO panel lists what's missing)
- **Done when:** retention/access proposal, confounders, our validation summary and sources are on the page, all in plain language.

**R-2 · Sources** (Nov 15)
- Every source gets one line on **how it informed us**. Separate *their* findings from *our* prototype results.
- Leads to research (**verify each one yourself before citing; don't cite from memory or from an AI summary**): the official NASA Space Apps 2026 challenge page and its listed resources; NASA's psychomotor vigilance / reaction-time work on the ISS; NASA Human Research Program material on behavioural health and performance; academic literature on keystroke dynamics and cognitive state.

**V-3 · Claims audit** (Nov 15 15:00–17:00): read every string in the UI, README, slides and video script against the language table in PLAN §1.

**A-1 · Stretch: attention check** (Nov 15, only after C2; Member 3 if we're three)
- **Files:** `static/js/attention.js` (full spec in the header comment), `templates/attention.html`. The API `POST /api/attention` already works and is tested.
- **Done when:** 10 trials, random foreperiod, premature and miss handling, median RT, result stored and shown with the "illustrative, not a medical test" label.
- **Think about:** why is the foreperiod random? Why treat RT < 100 ms as premature?

---

## 7. Engineering rules

1. **Privacy invariants** in DATA_CONTRACT §1 are tests, not suggestions. Never weaken a `test_privacy_*` test.
2. **Every number shown to a user is labelled** as illustrative / prototype where relevant.
3. **No new dependencies** without asking the Lead (each one is a setup risk on 4 laptops).
4. **No external network calls** at runtime: CDN scripts, APIs, fonts. The demo must work offline.
5. **Explainable over clever.** If you can't explain it to a judge in two sentences, it waits until after C2.
6. **The data contract is shared.** Changing features or API shapes means a PR touching `DATA_CONTRACT.md`, with Lead approval.
7. If `test_api.py::test_demo_*` fails, the pitch story broke. Fix it before anything else.

---

## 8. Language guide (UI, README, slides, video, *and* how we talk to judges)

| Instead of… | Say… |
|---|---|
| fatigue detected | change from personal baseline |
| the astronaut is impaired / unfit | timing differs from their usual pattern; check-in suggested |
| accuracy 92 % | in our small feasibility test, N = …, … |
| the AI decided | the prototype flagged; a human decides |
| keylogger, tracking | timing-only capture, visible, inside the task |
| validated threshold | illustrative threshold (prototype choice) |

---

## 9. Testing & debugging

```bash
python -m pytest                       # everything
python -m pytest tests/test_scoring.py -k faster -v   # one test, verbose
flask --app run reset-demo             # back to the seeded demo state
```

* **API by hand:** open `http://127.0.0.1:5050/api/readiness/plt-okafor` in the browser to see the raw JSON.
* **Frontend:** DevTools → Console for errors, Network tab to see exactly what `POST /api/sessions` sent. (Great for checking the privacy promise yourself!)
* A 400 from `/api/sessions` means the payload broke the contract; the `message` tells you which field.

---

## 10. Definition of done (every task)

- [ ] Does what the task card says, and you can explain how
- [ ] `python -m pytest` green; new logic has at least one test
- [ ] Clicked through the affected pages; no console errors
- [ ] Copy follows the language guide
- [ ] PR title has the task ID; reviewer assigned if you touched a ★ file
