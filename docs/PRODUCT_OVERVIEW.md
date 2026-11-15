# Crew Readiness: what it is, what it does, and why it can win

A one-file explanation for the team, the judges and anyone new. Honest by design: it says what we have shown and what we have not.
Numbers below are read from the result files and checked by `tests/test_submission.py`.

## What it is, in one paragraph

**Crew Readiness is a prototype of on-board decision support.** On a long mission the ground may be minutes away, and someone still has to
decide who does a critical task. Our software compares each crew member **only with themselves**, using nine timing numbers from a short typed
checklist and an optional reaction check, and puts any difference in front of **a human** with a plain-language reason. It never reads what is
typed, never decides, and never claims to detect fatigue, illness or fitness for duty. It is a **behavioural signal that sits beside crew health
monitoring, not in place of it.**

## The idea, and why it is not obvious

People differ: 220 ms between keys is normal for one person and a big change for another. A single threshold for everyone therefore fits nobody.
So every comparison is against the person's own earlier sessions, and every decision stays with a person.

**This is now backed by real NASA data.** In NASA's bed-rest study (WinSCAT test battery, 24 people, 118 sessions before bed rest), **65 to 87 percent of
the variation in response times was between people**, not within one person. A single shared threshold would need a change **1.7 to 2.8 times bigger**
than a personal baseline to notice the same thing.

## What it does (features)

**For the crew member**
- **My check-in:** one path. A short typed checklist (timed silently, nine aggregate numbers kept, never the text), then an optional one-minute
  reaction check, then your own status in plain words and what you can do. The same person is carried through every step.
- **Responsiveness:** your reaction check compared with your own earlier checks ("usual 277 ms, today 328 ms").
- **Private notes:** sleep and how you feel, kept only in your own browser. The notes code physically cannot send anything (a test proves it);
  you can copy a summary to share if you choose, and delete everything.

**For the reviewer**
- **Mission view:** the suggestion first (nominal, check in, or review) with reasons, then check-ins, then assignments. It never assigns, clears or grounds anyone.
- **Missed check-in watchdog:** if someone has not checked in for longer than the agreed gap, it suggests looking in on them in person, and says
  nothing is necessarily wrong. (Not a consciousness measure; it uses a timestamp we already store.)
- **Printable brief:** one page with reasons, what it cannot tell you, and a blank record to fill in by hand, including "crew medical support
  informed". Nothing is stored.
- **Dashboard:** the "stacked sessions" view of each person's pattern against their own baseline.

**Built for a mission with no quick answer from the ground**
- **New-equipment handling:** if gloves or a different device slow someone for good, a human accepts the change as the new normal; simulated, repeated alerts then fall from 27 % to 11 %. The software never accepts a change on its own.
- **Flagged sessions stay out of the baseline,** so a lasting change is not learned as normal (found and fixed in simulation).
- **Offline:** no network at runtime. A button lists every file a page loaded, and none comes from elsewhere.
- **Health of the monitor:** a self-test page checks the software itself (database, scoring on a fixed example, clock, no outside network), plus backup and restore with a checksum.

**Trust**
- **Privacy by construction:** only nine aggregate numbers per session are stored; the server rejects typed text and key identities.
- **Honest everywhere:** every page says what it does not show; every number comes from a result file; negative results are published.
- **Accessible:** the accessibility audit (axe-core) finds no violations on any page at phone or desktop width.
- **AI use disclosed:** the Privacy page, the README, page metadata and `docs/AI_USE.md` say how AI assistants were used. The product contains no AI-generated image.

## The evidence we have, in order of strength

| Evidence | What it shows | What it does not show |
|---|---|---|
| **Real NASA bed-rest data** (24 people) | 65 % to 87 % of response-time variation is between people, so a personal baseline is the right frame | The two rules (own baseline versus one threshold) raise similar alerts at the same budget: no advantage shown there. Not our typing task. Not validation of the product |
| **Simulated crews** (300 people per row) | False alerts on normal sessions fall from 13.0 % to 4.7 %; detection at a 10 % slowdown also falls, from 0.42 to 0.35 (the cost is shown) | A simulation we wrote; partly circular |
| **Two-volunteer pilot** (real people, one laptop) | 0 of 8 normal sessions flagged; 5 of 6 deliberate changes flagged (one labelled change showed no timing change and counts as a miss) | Two people; changes far bigger than the simulated ones; not validation |

## Why it can win (and which awards it is aimed at)

Judges score five criteria from 1 to 5. Our honest case:

- **Relevance:** it answers the health-monitoring challenge from the behavioural side, with real NASA bed-rest data as a core part of the evidence, and says plainly that it sits beside health monitoring.
- **Validity ("usable and user-friendly"):** a working, accessible, offline product with three clear doors, a one-path check-in, and evidence that states its own limits. Most teams will not publish a result that does not favour them; we do.
- **Creativity:** own-baseline decision support that hands every decision to a person, the missed check-in watchdog, device-only notes, and the equipment-change handling, in one coherent design.
- **Impact:** a concrete answer to "who does the critical task when the ground is not available", with a printable artefact a reviewer would actually use.
- **Presentation:** a distinctive visual identity (the hands: a person and a spacesuit, and a gap the system never closes; a person does) and a product that explains itself.

Awards it fits best: **Best Use of Science** (the scientific method, including negative results and stated limits), **Art & Technology** (the hands poster plus the
engineering), **Best Mission Concept** (a plausible on-board concept and design).

## The honest ceiling

It is a prototype. It has **not** been tested on crews or astronauts or in space. The pilot is two people. The NASA data check is of the method, not the product,
and the terms of use for that dataset are being confirmed with NASA's portal. The simulator is ours. We make no claim about fatigue, illness or fitness for duty.
That honesty is a strength with expert judges, but it also means the project cannot claim a breakthrough; its case is a sound idea, real data behind its core
assumption, and a trustworthy, usable build.

## A 60-second tour for a judge who opens the link

1. **Landing:** the hands, the one-line pitch, two doors: crew or reviewer.
2. **My check-in:** your status first, in plain words; Start check-in; private notes.
3. **Reviewer:** the suggestion first; the missed check-in; the printable brief.
4. **Evidence:** "Tested on real NASA data" first, then the simulated results with their costs, then the pilot.
5. **Privacy and limits:** what it does not do, what we did not validate, how AI was used, and a button that proves the page loads nothing from elsewhere.

## What is left before pressing Submit

- [ ] A public link for the **Project Demo** (the form requires one: a slide deck of at most 7 slides, or a video of at most 30 seconds). Without it the form will not submit.
- [ ] Team name and the exact challenge title in the form; both are in `docs/SUBMISSION.md`.
- [ ] Open the production link and the repository link in a private browser window with no login (see `docs/NASA_JUDGING_PLAYBOOK.md`, task N5).
- [ ] Confirm the NASA dataset terms with NASA's portal and update the status line in `docs/NASA_DATA.md`.
- [ ] Davud reads `docs/AI_USE.md` and confirms it is true.
- [ ] Both checkboxes ticked; **Submit for Judging** before 23:59 local time on 15 November.
