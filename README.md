# Crew Readiness

**NASA Space Apps 2026.** A privacy-conscious prototype that flags **changes in an astronaut's task interaction timing**, compared with **their own** baseline, for **human review** before a critical operation.

> ⚠️ **Prototype.** Fictional crew, synthetic demo data, illustrative thresholds. It detects changes in interaction timing; it does **not** detect fatigue, diagnose anything, or clear anyone for duty.

---

## The problem
Before high-stakes operations such as manual docking, mission teams want early, low-burden signals that someone may benefit from a check-in. Dedicated tests interrupt work and can't run continuously, and population "norms" ignore that every person types and works differently.

## Our approach
1. **Passive:** timing is captured during routine (simulated) checklist work; no extra test.
2. **Private by design:** the browser reduces keystrokes to **9 aggregate numbers**; text and key identities never leave the device, and the server rejects anything else.
3. **Personal:** each session is compared only with **the same person's** previous sessions (robust median/MAD baseline). No score until enough data exists (**CALIBRATING**).
4. **Explainable:** a GREEN / YELLOW / RED band with plain-language reasons and an evidence table, plus a **confidence** level based on data sufficiency.
5. **Human in the loop:** the mission view *suggests* a check-in or second verification. It never assigns or grounds anyone.

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
python run.py                                       # → http://127.0.0.1:5050
python -m pytest                                    # tests
```

The first run creates `instance/crew_readiness.sqlite3` with four fictional crew members.
Reset any time: `flask --app run reset-demo`.

## Demo walkthrough
1. **Mission:** docking at T-6h; the primary pilot shows YELLOW.
2. **Monitoring:** pick a crew member, read what is and isn't recorded, complete the checklist. Before submitting, the app shows the **exact JSON** that leaves the browser.
3. **Dashboard:** click a crew card → advisory, reasons, trend vs. own baseline, and evidence table.
4. **Attention check** *(in progress)*: short illustrative reaction-time task for added context.

## Architecture

```
Browser (capture.js)  ──9 aggregate numbers──▶  Flask API (strict allowlist)
                                                   │
                                SQLite (aggregates only) ◀── store.py
                                                   │
                     baseline.py (median + MAD of own past sessions)
                                                   │
                scoring.py (robust z → weighted score → band + reasons)
                                                   │
                         Dashboard · Mission view (human decides)
```

Python 3.10+ · Flask · SQLite · NumPy · vanilla JS · Chart.js (vendored; works offline).
Full details: [docs/DATA_CONTRACT.md](docs/DATA_CONTRACT.md).

## Data handling
- Stored per session: inter-key interval median and IQR, pause count and total, checklist response median, task duration, correction and retry counts, keystroke count.
- **Never stored or transmitted:** typed text, which keys were pressed, raw keystroke timelines, passwords.
- Capture runs only inside the task, with a visible "Monitoring active" indicator.
- The demo uses fictional profiles with synthetic data, labelled as such. Validation sessions used pseudonymous team profiles.

## Scoring (illustrative)
Per feature: `z = (today − personal median) / robust spread`; only the "slower / more pausing" direction counts; capped at 4.
Groups: typing 40 %, pauses 30 %, checklist response 30 %. Bands: < 1.0 GREEN, < 2.0 YELLOW, ≥ 2.0 RED.
**These are demo choices, not validated or NASA-approved limits.**

## Limitations
- Small internal feasibility test; **not** clinical or operational validation. *(Results: TODO V-2, see [docs/TEST_LOG.md](docs/TEST_LOG.md).)*
- Timing is affected by keyboard, language, practice, task difficulty, time of day, sleep and more.
- An unusual session means unusual **behaviour**, not a cause.

## Sources and acknowledgements
*TODO (R-2): each NASA resource / dataset / paper, with one line on how it informed this work.*
Chart.js © Chart.js contributors, MIT License.

## Team
See [docs/PLAN.md](docs/PLAN.md) for roles, timeline and decisions, and [docs/TEAM_GUIDE.md](docs/TEAM_GUIDE.md) to start contributing.
