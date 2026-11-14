# Pilot runbook for Windows: two volunteers, step by step

For the person running the pilot (the operator). It follows `docs/PILOT.md`; if the two ever disagree, `docs/PILOT.md` wins.
Time: about 15 minutes to set up, then about 30 minutes per volunteer.

**What this is:** a small feasibility check with two volunteers. It is not validation, and it must be described that way
("2 volunteers, one laptop"). **Rules:** pseudonyms only, never a real name anywhere; never edit a number in a CSV; do not
look at or talk about the result colour while a volunteer is doing sessions.

- `pilot-01` = the operator. Perturbed sessions: type with the **non-dominant hand only**.
- `pilot-02` = the second volunteer (Davud, or anyone present). Perturbed sessions: **count backwards out loud by 3** (300, 297, 294...) while typing.

Use ONE laptop and ONE keyboard for everyone. Do not use the live website: its database resets.

## A. Install (once)
1. **Python.** Open https://www.python.org/downloads/ , download Python 3, run it, tick **"Add python.exe to PATH"**, click Install Now. Close PowerShell, open a new one, type `python --version`. It must print a version.
2. **Git.** Install from https://git-scm.com/download/win (all defaults). Open a new PowerShell.
3. **Get the project:**
   ```
   cd C:\Users\User
   git clone https://github.com/Davuddevelop/Crew-Readiness.git
   cd Crew-Readiness
   ```
   (Use your own user folder if it is not `User`. If the folder already exists, just `cd` into it and run `git checkout main` then `git pull`.)
4. **Install the app's packages:**
   ```
   python -m venv .venv
   .venv\Scripts\pip install -r requirements.txt
   ```
   Always use `.venv\Scripts\python` and `.venv\Scripts\flask` below, so you never need to "activate" anything.

## B. Prepare (once)
5. Make sure you are on the newest code: `git checkout main` then `git pull`.
6. Add the two pseudonymous profiles:
   ```
   .venv\Scripts\flask --app run add-profile pilot-01 "Pilot 01" Volunteer
   .venv\Scripts\flask --app run add-profile pilot-02 "Pilot 02" Volunteer
   ```
   Each must answer `Added team_test profile ...`.
7. Copy the prefilled sheet (24 rows: 12 sessions for each person):
   ```
   copy docs\pilot\session_sheet_two_people_template.csv docs\pilot\session_sheet.csv
   ```
   It describes the plan. **After the pilot you will delete any row for a session that was not submitted** (step 15).
8. Start the app and **leave this window open**:
   ```
   .venv\Scripts\python run.py
   ```
9. In your browser open http://127.0.0.1:5050/monitor . Keep the browser at normal zoom (100 %).

## C. Run each volunteer (do `pilot-01` completely, then `pilot-02`)
10. **Consent.** Read the consent text in `docs/PILOT.md` section 4 aloud. If they say no, stop: nothing is recorded.
11. **Practice run (not saved).** Choose their pseudonym, press **Start task**, type the checklist, and on the review screen press **Discard**.
12. **Twelve real sessions**, about a minute's break between them. For each: choose the pseudonym, **Start task**, type every confirmation phrase and press Enter, then press **Submit timing features** on the review screen.

    | Session | How to type |
    |---|---|
    | 1 to 8 | Normal pace, normal way |
    | 9, 10, 11 | `pilot-01`: non-dominant hand only. `pilot-02`: count backwards by 3 out loud while typing |
    | 12 | Normal again |

13. After the result screen appears, press **Run again**. Do not read out or discuss the colour.
14. **If something goes wrong** (interruption, crash): press **Discard** and redo that session. Then, in the sheet, set that row's `issue` to `redone`. If an interruption happened but you kept the session, set `interrupted`.

## D. Finish
15. **Check the sheet.** Open `docs\pilot\session_sheet.csv` (Notepad is fine). Keep one row per session that was actually submitted; delete rows for sessions that never happened. Keep the commas exactly as they are, add no notes.
16. Stop the app (click its window, press Ctrl+C), then export:
    ```
    .venv\Scripts\python scripts\export_pilot.py
    ```
    It must report 12 sessions for `pilot-01` and for `pilot-02` (or fewer only if you deleted rows in step 15). If the counts do not match the sheet, fix the sheet; do not touch the exported numbers.
17. **Run the analysis** (this only reads the two files):
    ```
    .venv\Scripts\python -m ml.pilot_report
    ```
    Copy what it prints into a message to Davud. Do not interpret it; the wording for the docs is decided afterwards.
18. **Send the files to GitHub** on a new branch:
    ```
    git checkout -b data/pilot-results
    git add docs/pilot/pilot_sessions.csv docs/pilot/session_sheet.csv docs/pilot/pilot_report.json
    git commit -m "Pilot data: 2 volunteers, 12 sessions each"
    git push -u origin data/pilot-results
    ```
    Then open a pull request on GitHub and message Davud. Do not merge it yourself.

## If something fails
- `python` not found: reinstall and tick "Add python.exe to PATH", then open a new PowerShell.
- `flask` or `python` not found inside `.venv\Scripts`: step 4 did not finish; run it again and read the last lines.
- Port 5050 already in use: close the other window running the app.
- Anything else: copy the last 10 lines of the error and send them to Davud.

## What not to say afterwards
It is 2 volunteers on one laptop with a deliberate change in how they type. It is not validation, not astronauts, not fatigue, illness or fitness for duty.
