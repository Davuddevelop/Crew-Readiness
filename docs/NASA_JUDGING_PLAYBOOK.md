# NASA Space Apps 2026: judging and submission playbook for Crew Readiness

For: Davud, Alex and Alex's coding agent. Source: the official **Judging & Awards Guide** and **Project Submission Guide** (both dated
2026-11-13, saved copies in the team's uploads). Page numbers below are those PDFs. Read sections 1 to 3, then take your tasks in section 5.

**Clock (Baku time).** Written Sunday 15 November about 13:30. The official deadline is **Sunday 15 November 23:59 local time** (Judging
Guide p3; Submission Guide p2, p11). Our internal deadline is **23:30**. Plan: feature freeze **18:30**, record and assemble **18:30 to 21:30**, submit
**by 22:30**, leaving an hour for a form that misbehaves. Only the **last saved submission** is reviewed (Submission Guide p11), so submit early and resubmit if needed.

---

## 1. What the judges actually score (Judging Guide p5 to p7)

Every project is scored **1 to 5** on five criteria, at every level of judging.

| Criterion | What a 5 looks like, in their words | What it means for us |
|---|---|---|
| **Impact** | Addresses a significant problem; extensive reach; "far exceeds expectations" | Say who benefits and what changes for them. A crew deciding who does a critical task with no quick link to the ground. |
| **Creativity** | A novel concept not attempted before, or a meaningful improvement on existing ideas | Own-baseline, human-decides, device-only, plus the missed check-in watchdog. State what is new compared with a population threshold and with sensor dashboards. |
| **Validity** | Scientifically sound, technically feasible, strong alignment with established principles, fully developed, **usable and user-friendly** | Honest evaluation (simulated plus pilot plus NASA data), a working product, simple to use (the three doors). |
| **Relevance** | "Fully and directly addresses the challenge", **"meaningfully integrates NASA data, utilizing it as a core component of the solution rather than a superficial addition"** | **Our weakest point today.** We use no NASA data as a core component. See blocker B1. |
| **Presentation** | Clear challenge, solution and significance; engaging, well-structured storytelling; "judges evaluate the demo **and** full project" | The demo, the project page text and the product itself all count. |

**Awards** (Judging Guide p10). Executive judges pick ten Global Awards: Best Use of Science (best and most valid use of the scientific method),
Best Use of Data, Best Use of Technology, Galactic Impact, **Best Mission Concept** (most plausible concept and design), Most Inspirational,
Best Storytelling, Global Connection, **Art & Technology** (technical and creative skills combined), Local Impact. Our best fits: **Best Use of
Science** (our honesty, negative results and pre-stated limits are the scientific method), **Art & Technology** (the hands poster plus the
engineering), **Best Mission Concept**. Write the project description so a judge can see which award we are reaching for.

**Timeline.** Global Nominees announced 3 December 2026, Global Finalists 17 December, Global Winners 26 January 2027.

---

## 2. Hard requirements (a miss means we are not judged, or not eligible for awards)

From Judging Guide p3 to p4 and Submission Guide p4 to p11. Davud owns this checklist; tick every box before pressing Submit.

- [ ] We respond to **one official challenge**: "Create Health Monitoring Software for Astronauts on Space Missions". Use its **exact title** from the challenge list in the form.
- [ ] **All teammates registered** for the **same Local Event** (or the Universal Event), none waitlisted, all visible on the team's Members tab. Max 6 members; Universal Event needs at least 2.
- [ ] **All required form fields completed**, all content in **English**. If any is missing the Submit button does not work.
- [ ] **Demo**: **either** a slide deck of **at most 7 slides, including title and intro slides**, **or** a video of **at most 30 seconds**. Exceeding either limit means **not eligible for Global Judging**. English only (a video may use another language only with English subtitles).
- [ ] The slides must show the **team name**, the **names of the team members** and **the challenge the team selected**, plus an image of the project, the user experience, and **how NASA and space-agency data or technology make the solution possible** (Submission Guide p9).
- [ ] **Public links, no login, no password, no permission request** for the demo and for the final project (p4 to p5). Test both in a private browser window and with a teammate.
- [ ] **To be eligible for a Global Award we must use at least one NASA data set or resource**, and describe it in the NASA Data field (p7).
- [ ] **Every external resource** (code, text, images, data, tools, even open source or free) is listed in the References field. We confirm in a checkbox that it is our original work and that we used no copyrighted material without permission (Judging Guide p3).
- [ ] **AI ("Super Intelligence", SI) use is disclosed** (p6): images and videos carry a **visible watermark** saying they are SI-generated; audio, code and data acknowledge SI generation in descriptive text and metadata. SI "should not be used to come up with your idea of how to solve the challenge". Generated content may **not use, contain or modify NASA branding** (logos, flags, mission identifiers). The SI answer is not shown to judges, but **judges can see SI indicators in the project** and score originality and execution on what we disclose.
- [ ] **No image, video, audio or likeness of anyone under 18** in the demo or project (p11).
- [ ] Both checkboxes ticked (terms and conditions; "confirm all work is original"), then **"Submit for Judging" before 23:59 local time on 15 November**.
- [ ] Optional but recommended for a new website: request the **FortiGuard Web Filter classification** (Submission Guide p4: category "web-based application" or similar, company name "N/A"), so judges' networks do not block our site.

**The Project page fields** (Submission Guide p5 to p7) and where our text lives. Judges' main evaluation is the project submission; the demo is considered too.

| Field | Source in our repo |
|---|---|
| Project Name | Crew Readiness |
| High-Level Project Summary (what, how it addresses the challenge, why important) | `docs/SUBMISSION.md` (to be reshaped, task N4) |
| Link to Project Demo | the public deck or video link (task N2) |
| Link to Final Project | the public product URL; the public repo URL |
| Detailed Project Description (what, how it works, benefits, aims, tools and languages) | `docs/SUBMISSION.md` |
| Use of Super Intelligence (SI) | `docs/AI_USE.md` (task N3) |
| NASA Data | `docs/NASA_DATA.md` (task N1) |
| Space Agency Partner Data and Other References | `docs/REFERENCES.md` (task N4) |

---

## 3. Where we stand against that (honest)

| ID | Gap | Severity | Why |
|---|---|---|---|
| **B1** | **No NASA data used as a core component** | **BLOCKER** for Relevance and for Global Award eligibility | Relevance is scored on "NASA data as a core component rather than superficial". Global Awards need at least one NASA data or resource. Today we only use a NASA photograph (the glove) and cite a NASA reaction-test experiment as background: that is the "superficial addition" they describe. |
| **B2** | **Demo does not meet the checklist** | **BLOCKER** | The deck (7 slides) has no team name, no member names, no challenge title, no slide on NASA data, and is a private link. |
| **B3** | **AI-use disclosure and watermark** | **BLOCKER** for honesty and compliance | The logo is AI-generated and carries no visible watermark. Our code was written with an AI assistant and says so only in the docs, not in project metadata. |
| B4 | Project page copy not in the form's shape; no references list | HIGH | `docs/SUBMISSION.md` is written for a general audience, not for these eight fields. |
| B5 | Public access and site classification untested | HIGH | Judges cannot score what they cannot open. Vercel protection settings and the repo's visibility must be checked in a private window. |
| B6 | Exact challenge title and team registration unverified | HIGH | Both are needed to submit. |
| M1 | The pilot is two people | MEDIUM | Already stated honestly; do not oversell. |
| M2 | The Evidence page lists simulated results first | MEDIUM | Fine, but with NASA data it should lead with the real data. |

**Our own scores on their 1 to 5 scale, honestly:** Impact 3.5, Creativity 4, Validity 3.5, **Relevance 2 (until B1 is closed)**, Presentation 3.5.
(Our earlier "7.5 out of 10 for relevance" ignored the NASA-data requirement. It was too generous.) Closing B1 well could move Relevance to 3.5
or 4, and lifts Validity and Presentation too. That single item is worth more than every other item combined.

---

## 4. The one decision that unlocks B1: using the NASA bed-rest data

We already found a real NASA dataset that fits our method: **NASA Life Sciences Data Archive, "Neurocognitive Assessment (WinSCAT) (Flight
Analog)", DOI 10.83263/sbne-th55** (details and what we ran: `docs/DATA_SEARCH.md`). Real people, 60 to 90 day head-down-tilt bed rest (a
ground analog of spaceflight), the WinSCAT subtests described as those used on the ISS, **24 people with at least 8 sessions each**. The
archive states "Data preservation is complete. All datasets are publicly available." The files download without a login.

**The only open question is the licence** (none stated; NASA's own catalogue says "License not specified"). Recommended decision for Davud:

> **D1. Use it, with these guard rails.** Credit NASA and the DOI everywhere; commit **only aggregate results, never the raw rows**; the
> analysis script takes a local path and the app itself still makes no network calls; and **email the NLSP help desk today** asking the
> terms of use. If they say no, we remove the NASA-data section and fall back to the NASA resources we can honestly list. Reason: the
> dataset is declared publicly available, the use is research-style and credited, and without NASA data we cannot compete for a Global Award.

**What we do with it, honestly** (so it is a core component and not decoration), `ml/nasa_eval.py`:
1. **Between-person versus within-person variation** (an intraclass correlation) of the real WinSCAT response times, using sessions before bed rest.
   This is the scientific reason for our whole approach: if most of the variation is between people, a population threshold is the wrong tool.
2. **Own-baseline rule versus a population-wide threshold on the same real data**, at the same alert budget, with held-out people (reuse `ml/calibrate_cutoffs.py`
   machinery). Report false alerts on pre-bed-rest sessions and how each rule behaves during bed rest. No health claim: the original study reports no consistent cognitive decrement, so flags are "differences from the person's own pattern", not impairment.
3. The multiple-comparisons finding already in `docs/DATA_SEARCH.md` (any-of-five flags 40 % of sessions), which supports our single weighted, budget-calibrated score.
4. Output: `app/nasa_results.json` (aggregates only, regenerated by the script, never edited by hand), an **Evidence section "Tested on NASA bed-rest data"** driven by that file,
   the dataset citation in `docs/NASA_DATA.md`, the Privacy and limits page and the deck.

Say plainly in all of it: WinSCAT is not our typing task, sessions are days apart, it is a check of the **method** on real NASA repeated
measures, not validation of the product or of anything about health.

---

## 5. Tasks, owners and order

File ownership prevents merge conflicts: do not edit files owned by someone else; ask.

| ID | Task | Owner | Time | Done when |
|---|---|---|---|---|
| **N0** | **Davud decides D1 and emails NLSP.** Also confirms the exact challenge title, team registration (same Local Event, member list), and who submits. Gives the team name and members' names for the deck | Davud | 30 min | answers written in `docs/TASKS.md` |
| **N1** | **NASA data as a core component.** `ml/nasa_eval.py`, `tests/test_nasa_eval.py` (on a small labelled synthetic fixture only, never real rows), `app/nasa_results.json`, Evidence section `id="nasa"`, `docs/NASA_DATA.md` (what data, DOI, how we used it, the limits, a plain list of NASA resources used including the glove photograph and the Reaction Self Test record, each with its link) | Alex's agent (script, results, `NASA_DATA.md`); Claude (Evidence page section, About page, tests tying the page to the file) | 3 h | page numbers come from the file; test fails if they drift |
| **N2** | **Demo v3, rebuilt to the checklist.** 7 slides at most: 1 title with **team name, member names, challenge title** and the hands; 2 problem; 3 idea and how it works; 4 the product and user experience (screens); **5 how NASA data makes it possible** (the N1 result); 6 evidence and honest limits; 7 impact and what is next. Public link: share the deck publicly **and** export a PDF to a public place (Google Drive "anyone with the link" or GitHub). The 30-second video, if made, follows the guide's timing: 0:00 names, 0:02 the challenge, 0:05 project name and tagline, 0:10 how it works and NASA data, 0:20 to 0:30 the future | Claude (deck); Davud (members' names, public sharing, optional video) | 2 h | exactly 7 slides or fewer; opens in a private window |
| **N3** | **AI-use disclosure and watermark.** Replace the AI-generated logo (nav, favicon, share card, landing footer) with a mark we draw ourselves, or add a visible "AI-generated" watermark; `docs/AI_USE.md` with the **true** account (see note below); an "AI assistance" paragraph on the Privacy page, the README top and a `<meta name="ai-assistance">` tag; remove the logo-tool placeholder from `docs/SUBMISSION.md` and `docs/ASSETS.md` | Claude (code, pages); Alex's agent (`AI_USE.md`, README); Davud (reviews the wording) | 1.5 h | no unwatermarked SI image remains; tests check it |
| **N4** | **Submission copy in the form's shape**: rewrite `docs/SUBMISSION.md` as the eight fields above, each paragraph a paste-ready block; `docs/REFERENCES.md` listing every code, text, image, font, data set and tool with its licence (Flask, NumPy, SQLite, Chart.js, Instrument Sans and Serif and JetBrains Mono with the OFL, Michelangelo reproduction, the NASA glove photograph, the NASA data, Playwright for development) | Alex's agent | 2 h | every field filled, nothing marked TODO |
| **N5** | **Public access check**: the production URL opens in a private window with no login or Vercel protection prompt; the GitHub repository is public; deck and video links open for a stranger; submit the **FortiGuard classification** request for the production domain | Davud | 45 min | a teammate opens every link on a phone off Wi-Fi |
| **N6** | **Project page images** (JPG or PNG, up to 10 MB each): 4 to 5 product screenshots (My status, Mission, brief, Replay, Evidence NASA section) with no logo watermark problems and **no one under 18** | Claude (captures); Davud (uploads) | 30 min | images added to the form |
| **N7** | **Final QA** and merge order, `smoke.py` on the live URL, claims scan, grid and keyboard checks | Claude | 1 h | all green on the live URL |
| N8 | Optional: the 30-second video, recorded last | Davud and Alex | 1 h | under 30 seconds, English or subtitled |

**Note on the SI answer (honesty, and it protects us).** The guide says SI must not be used to come up with the idea of how to solve the
challenge. Describe truthfully who did what: the team lead set the direction (personal-baseline decision support, human decides, privacy
first), made every product and claim decision and ran the pilot; an AI coding assistant (Claude) wrote much of the code, tests and
documentation and proposed some features that the lead approved. Do not claim the idea was solely human if it was not, and do not hide the
assistant. Judges can already see SI indicators in the project and evaluate originality on what we disclose.

**NASA branding.** Our NASA glove photograph is a NASA photograph, edited by code (cut out and recoloured); it is not generated, and it contains no NASA logo. List it as a
NASA resource with credit. Do not add the NASA "meatball" or "worm" logos, flags or mission patches anywhere, including the deck.

---

## 6. Schedule (Baku time, Sunday 15 November)

| When | What |
|---|---|
| 13:30 to 14:00 | **N0**: Davud decides D1, emails NLSP, confirms title, team and members. Alex's agent starts N1. |
| 14:00 to 17:00 | Alex's agent: N1 script and results, N4 copy. Claude: N3, then N1 Evidence section. Davud: N5, N6 prep. |
| 17:00 to 18:30 | Claude: N2 deck v3 once the N1 numbers exist. Merge in batches, redeploy. |
| **18:30** | **Feature freeze.** After this only fixes. |
| 18:30 to 20:00 | Claude: N7 QA on the live URL. Davud and Alex: fill the Project page, upload images. |
| 20:00 to 21:30 | Optional video (N8). Final read-through of every field. |
| **22:30** | **Submit for Judging.** Then verify the banner, test every link again in a private window. |
| 23:30 | Internal deadline. 23:59 is the official one; do not use the last hour. |

**Cut order if we run late:** N8 (video), N6 (extra images), the Evidence polish. **Never cut:** N1, N2, N3, N4, N5, the final submit.

---

## 7. Prompt for Alex's coding agent (copy and paste)

```
Read AGENTS.md, docs/NASA_JUDGING_PLAYBOOK.md, docs/DATA_SEARCH.md, docs/PLAN_V3.md. Pull main first. One branch and one PR per task, in this
order. Do not merge; Davud merges. Run `.venv/bin/python -m pytest -q` and, with the app running, `node scripts/check_grid.js` before every PR.
Honest-claims rules in AGENTS.md never bend (no fatigue, illness or fitness claims; "simulated" for benchmark numbers; no NASA endorsement).

You own: ml/nasa_eval.py, tests/test_nasa_eval.py, app/nasa_results.json, docs/NASA_DATA.md, docs/REFERENCES.md, docs/AI_USE.md, README.md,
docs/SUBMISSION.md, scripts/nasa_winscat_check.py. Do NOT edit templates, static files or app/*.py (Claude owns them); ask in the PR if you need a hook.

N1 (first, 3 h): the NASA bed-rest data as a CORE component, never decoration. Source: NASA Life Sciences Data Archive WinSCAT (Flight
Analog), DOI 10.83263/sbne-th55, UTMB Campaign 3 (24 people with >= 8 sessions). The raw files stay OUT of the repo: the script takes a local
folder path and the app never reads them. Write ml/nasa_eval.py so that `python -m ml.nasa_eval <folder>` writes app/nasa_results.json with
AGGREGATES ONLY (no per-session rows, no raw values):
  (a) intraclass correlation (between-person vs within-person variance) for each WinSCAT median response-time measure, using pre-bed-rest sessions only,
      with a bootstrap interval over people;
  (b) own-baseline rule (reuse the product's baseline/scoring constants as scripts/nasa_winscat_check.py does) versus a population-wide threshold,
      at the SAME alert budget, evaluated on held-out people (reuse ml/calibrate_cutoffs.py ideas): false alerts on pre-bed-rest sessions and the
      flag rate during bed rest for each rule;
  (c) the multiple-comparisons figure already in docs/DATA_SEARCH.md, regenerated by the script.
Rules: flags are "differences from the person's own pattern", never impairment; the original study reports no consistent decrement. Say in the
JSON's "limits" list: not our typing task, sessions days apart, five baseline sessions, a method check not product validation, nothing about health.
Tests use a small clearly-labelled SYNTHETIC fixture in the same file layout; never commit real rows. Then write docs/NASA_DATA.md: what data,
DOI and URL, how we used it, the limits, and a plain list of every NASA resource we use (the glove photograph with credit, the Reaction Self
Test record NTRS 20090029851, this dataset), each with its link and what we did with it. Davud is asking NLSP about the terms: put the status at the top.

N4 (2 h): reshape docs/SUBMISSION.md into the exact form fields: High-Level Project Summary; Detailed Project Description (what it does, how it
works, benefits, aims, tools/languages/hardware/software); Use of Super Intelligence; NASA Data; Space Agency Partner Data and Other References.
Each is a paste-ready block. Write docs/REFERENCES.md listing EVERY code, text, image, font, dataset and tool with its licence (Flask, NumPy,
SQLite, Chart.js, Instrument Sans/Serif and JetBrains Mono under the OFL, the Michelangelo reproduction, the NASA glove photograph, the NASA data,
Playwright as a dev tool). Keep tests/test_submission.py green: numbers come from the result files, never typed.

N3 (part, 1 h): docs/AI_USE.md and an "AI assistance" paragraph at the top of README.md. TRUTHFUL account: the team lead set the direction
(personal-baseline decision support, human decides, privacy first), made every product and claim decision and ran the volunteer pilot; an AI coding
assistant (Claude) wrote much of the code, tests and documentation and proposed some features that the lead approved. State that no AI-generated
image is used in the product after the logo is replaced (Claude handles that part). Do not overstate or hide anything.

Finish N1 before N4. Open each PR as soon as it is green. Deadline for all: 17:00 Baku.
```

---

## 8. Decisions needed from Davud (answer in this file or in chat)

1. **D1:** use the NASA bed-rest data with the guard rails in section 4? (Recommended: yes; email NLSP today.)
2. **D2:** replace the AI-generated logo with a mark we draw ourselves (recommended), or keep it with a visible "AI-generated" watermark?
3. **D3:** the exact challenge title, the team name, and the member names for slide 1.
4. **D4:** video (30 s) or slides (7)? The checklist above assumes **slides are required** and the video optional. If you must pick one, pick slides: our strength is the honest argument.
5. **D5:** who presses Submit, and who stays online until the banner appears?

---

## 9. After this is done: what we expect (their 1 to 5 scale)

| Criterion | Now | After N1 to N7, if done well |
|---|---|---|
| Impact | 3.5 | 3.5 to 4 |
| Creativity | 4 | 4 |
| Validity | 3.5 | 4 (real NASA data, honest limits, a usable product) |
| Relevance | 2 | 3.5 to 4 (NASA data as the test of the method) |
| Presentation | 3.5 | 4 (a deck built to their checklist) |

That is a credible Global Nominee. A top-three finish still depends on how many other teams also use NASA data as a core component; this
is the one thing we can still change today.
