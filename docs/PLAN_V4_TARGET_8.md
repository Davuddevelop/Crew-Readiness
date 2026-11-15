# Plan v4: lift Impact, Relevance, Health relevance and Evidence to 7.5 or more

Written Sunday 15 November about 14:45 Baku. Deadline 23:30 (official 23:59). **Product freeze 19:00**, then the presentation, then submit by 22:30.
The presentation is separate and later; this plan is about the product and the evidence.

## 1. Honest targets (what each number needs, and how sure we are)

| Dimension | Now | Target | What gets it there | Depends on | Confidence |
|---|---|---|---|---|---|
| **Strength of evidence** | 6.5 | **7.5** | A NASA data set with a **known health stressor** (sleep loss), showing whether our own-baseline rule finds the induced change; more volunteers; a data-driven baseline length | A usable NASA sleep-loss data set (W1) | 65 % |
| **Health relevance** | 5.5 | **7.5 to 8** | The same sleep-loss test (a real health stressor, in real people); a vigilance check that follows NASA's own Reaction Self Test design; an escalation ladder to crew medical support; an on-device "your sleep and your timing" view | W1 positive or at least honest; W2 built | 55 % for 8, 80 % for 7 |
| **Relevance to NASA, space, astronauts** | 6.5 | **8** | NASA data as a core part of the evidence (done) plus **in the product** (a NASA-derived design parameter), a second NASA data set, space-specific operations (comms delay, store-and-forward), mapping to NASA's behavioural-health risk | W1; W3 | 70 % |
| **Impact** | 6.5 | **7.5 to 8** | Turn our numbers into operational impact: an **alert-burden calculator** for a mission planner; an escalation ladder; Earth-independent operation framing; a shareable summary for the ground | W3, W4 (all mine, no outside dependency) | 80 % |
| **Validity** | 7 | **7.5 to 8** | Reliability measured (fault injection and a long-mission soak); the above evidence | W5 | 75 % |
| Creativity | 7.5 | 7.5 to 8 | Already there; the on-device sleep-and-timing view adds to it | W2 | 85 % |

**What we will not promise.** An 8.5 to 9 across the board is not honest. We have no real crew data and a two-person pilot; we make no health claim. The realistic result is
**7.5 to 8 on most rows, 8 on Relevance**, and Health relevance 8 only if the sleep-loss test works. If it fails we publish that, and Health relevance stays at 7.
A negative result shown honestly still lifts Validity.

## 2. The workstreams

### W1: a NASA data set with a known stressor (Alex's agent; the most valuable item)
NASA's Life Sciences Portal lists human **sleep-loss vigilance** and bed-rest performance data sets marked "All datasets are publicly available" (`docs/DATA_SEARCH.md`).
Find one with at least 8 repeated measures per person that includes rested sessions and sleep-loss sessions. Test, on **people the rule was not fitted on**:
- does the own-baseline rule flag the sleep-loss sessions, and how often does it flag rested ones, at a stated alert budget;
- the same for one shared threshold at the same budget;
- how the flag rate rises with each night of loss, if the data allow.
Output `app/nasa_stress_results.json` (format in section 5). If no usable set is found within 90 minutes, write that down and stop; do not stretch a poor fit.
Wording rule: "a change in performance under sleep loss, in a laboratory analog". Never a diagnosis; never fatigue detection.

### W1b: a data-driven baseline length (Alex's agent, 45 minutes, on the WinSCAT data we already have)
Use the real data to show how the false-alert rate behaves with 3, 4, 5, 6, 7 baseline sessions. This puts **NASA data inside a product design choice** (how many sessions before we say anything, now 5, arbitrary) and justifies CALIBRATING. Add `baseline_length` to `app/nasa_results.json`.

### W2: health features that stay honest (Claude)
- **A vigilance check that follows NASA's Reaction Self Test.** NASA's PVT-based test is a 3-minute reaction test with random intervals of about 1 to 4 seconds. Add an optional 3-minute mode alongside the 10-trial check; record lapses (responses over 355 ms, the PVT-B convention) and false starts; compare against the person's own earlier checks. Rated as the same measure NASA flew, not as a diagnosis.
- **Your sleep and your timing, on your device.** Joins the private notes to the person's own reaction-check history, in the browser, and shows "on nights you noted less than 6 hours, your reaction time was X ms different" once there are enough paired entries. A description of your own data, labelled as not a finding. Nothing leaves the device.
- **An escalation ladder** on Mission and the brief: self-check, a peer looks in, the reviewer, crew medical support, the ground. Who decides at each step; no step is automatic; "if anyone feels unwell, tell crew medical support directly".

### W3: space-specific operations (Claude)
- **Communication-delay mode:** a store-and-forward summary a person can choose to send to the ground when a link window opens (downloadable text, aggregates only, their choice), plus a Mission note on what the crew does when the delay is minutes each way.
- **A long-mission replay (180 days)** in the existing Replay: a simulated crew over six months with an equipment change, a missed check-in and a real slowdown; counts of alerts and of reviewer actions.
- **NASA-derived parameter in the product:** the baseline length from W1b replaces the arbitrary 5 only if the data support it; otherwise 5 stays and the data say so.

### W4: impact, in numbers a mission planner can use (Claude)
- **Alert-burden calculator** on the Evidence page: choose crew size, check-ins per day, mission length and alert budget; it shows the expected false alerts and the reviewer time, from our own calibration table. For example, a 4-person crew with 1 check-in a day at a 1-in-20 budget has about one false alert every 5 days. All numbers from `app/results_data.json`.
- **Impact framing** in the product and the submission: Earth-independent operations on long missions, with a cited NASA source for the communication delay (a human opens the link).

### W5: reliability (Alex's agent, optional, 2 hours)
`scripts/soak.py` and `ml/export_reliability.py`: 1000 hostile inputs (zero crashes expected), and a 700-day, 6-person soak (scoring time, database size). Output `app/reliability_data.json` and an Evidence "Reliability" section. Lifts Validity.

### W6: more real people (Davud and Alex, humans)
Four more volunteers (family, friends, anyone present), using the existing runbook: the typed checklist **and**, new, the 3-minute reaction check once at the start and once after a deliberately demanding stretch (a long counting task), with their consent. Pseudonyms only; nobody under 18. Even 4 more people turns "2 people" into "6".

## 3. Schedule (Baku time)

| When | Alex's agent | Claude | Davud and Alex |
|---|---|---|---|
| 14:45 to 15:15 | Start W1 (find the data) | W4 alert-burden calculator | Email NLSP; start finding volunteers |
| 15:15 to 17:00 | W1 analysis, then W1b | W2 PVT mode and escalation ladder | Volunteers (W6) |
| 17:00 to 18:30 | W5 if time | W2 sleep-and-timing view, W3 | Volunteers |
| 18:30 to 19:00 | Final results into the JSON files | Evidence pages for W1 and W1b; docs | |
| **19:00** | **Freeze** | Final QA, update `docs/PRODUCT_OVERVIEW.md` and the submission numbers | Prepare the presentation |
| 19:00 to 22:30 | | | Presentation, links, Submit |

**Cut order if late:** W5, then W3's replay, then W2's sleep-and-timing view. **Never cut:** W1, W4, the escalation ladder, QA, the honest wording.

## 4. Rules that do not bend
- No fatigue, illness, impairment or fitness claims; sleep-loss results are "a change in performance under sleep loss in a laboratory analog".
- Every number on a page comes from a result file; a test ties it. Raw NASA files are never committed; aggregates only; NASA and the DOI are credited.
- New stored fields are aggregates (a lapse count). Sleep and feeling notes stay in the browser.
- If a result is negative or null, we publish it with the same prominence as a positive one.

## 5. File formats (so both sides build to the same shape)

`app/nasa_stress_results.json` (W1; Claude renders it on the Evidence page, hidden until the file exists):
```json
{"source": {"title": "...", "doi": "...", "url": "...", "accessed": "2026-11-15", "sha256": "...", "stressor": "e.g. total sleep deprivation / sleep restriction"},
 "measure": "Psychomotor vigilance: median response time",
 "people": 20, "rested_sessions": 100, "stress_sessions": 60,
 "rules": {"alert_budget": 0.05,
           "rested": {"own_baseline": {"false_alert_rate": 0.05, "ci95": [0.02, 0.09]}, "population": {"false_alert_rate": 0.05, "ci95": [0.02, 0.1]}},
           "stress": {"own_baseline": {"flag_rate": 0.6, "ci95": [0.45, 0.75]}, "population": {"flag_rate": 0.3, "ci95": [0.15, 0.45]}}},
 "by_night": [{"label": "After 1 night", "own_baseline": 0.4, "population": 0.2}],
 "limits": ["..."]}
```
`baseline_length` added to `app/nasa_results.json` (W1b): `[{"sessions": 3, "false_alert_rate": 0.09, "ci95": [0.05, 0.14]}, ...]`.

## 6. Decisions for Davud
1. **D1:** approve W2's on-device "your sleep and your timing" view (reads only the person's own data in their browser; adds a read-only endpoint for their own reaction-check history).
2. **D2:** approve one new stored aggregate, a **lapse count** on the reaction check (schema change with a safe migration). Typed text and key identities stay out as ever.
3. **D3:** who finds four volunteers, and when (16:00 to 18:30)?
4. **D4:** confirm Alex's agent may use his network to download the NASA sleep-loss data (raw files stay out of the repo).
