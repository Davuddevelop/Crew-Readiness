Build a 7-slide PowerPoint deck (16:9) for our NASA Space Apps Challenge 2026 project demo. The official rule is a demo of AT MOST 7 slides, in English, judged on Impact, Creativity, Validity, Relevance and Presentation (telling the story: the challenge, our solution, why it matters). Exactly 7 slides, no appendix, no extra title or "thank you" slide.

PROJECT: Crew Readiness. A privacy-first second look before a critical operation (e.g. docking). It compares how each crew member works with THEIR OWN usual pattern and puts any change in front of a human. It never reads what is typed and never decides.

== LOOK AND FEEL: futuristic mission-control, near-black, restrained ==
- Background #090A0F on every slide. Text #F8FAFC. Secondary text #9AA0AA. Thin rules and grid lines #2C3140.
- Accent colours ONLY for status, never decoration: amber #FFB800 = "check-in suggested"; coral #FF5A6E = "review". Green status is plain white text, not green.
- One typeface: Instrument Sans if installed, otherwise Aptos (fallback Segoe UI). Titles 40-54 pt semibold, tight letter-spacing; body 18-22 pt; small labels 11-12 pt, ALL CAPS, wide letter-spacing, grey (e.g. "01 / PROBLEM").
- Swiss grid: flush-left text, generous margins, structure from 1 px lines and space. No boxes with shadows, no gradients, no glass, no clip-art, no stock photos, no emoji, NO NASA logo or "meatball" anywhere.
- Signature motif: "stacked sessions", 8-12 thin horizontal white lines stacked vertically (one per work session), mostly flat, the bottom one rising in a bump drawn in amber. Use it big on slide 1 and small as a recurring corner element.
- Every slide: a thin top rule, the small caps label top-left, and a footer in grey 10 pt: "Prototype · simulated data · decision support only".
- Max ~35 words of body text per slide; big numbers instead of sentences where possible.

== ANIMATION (modern, purposeful, short) ==
- Morph transition between ALL slides (0.8-1.0 s), keeping the stacked-lines motif and the title position as shared objects so they glide between slides.
- Entrance: titles "Fade + Float In" (0.5 s); bullets/steps appear one by one "Wipe from left" (0.3 s each, 0.15 s delay, After Previous); big numbers "Zoom" subtle (0.4 s).
- On slide 1 the stacked lines draw in one by one (Wipe from left, 0.1 s stagger), the amber bump last.
- Nothing loops, spins or bounces. The deck must also read perfectly as a static PDF, because judges may only see it as a link or PDF.
- If you cannot add an animation or transition yourself, finish the slides and then list exactly which effects I should add manually, per slide.

== CONTENT, SLIDE BY SLIDE (use these words and numbers; do not add new claims or numbers) ==

1. TITLE / HOOK
Label: "NASA SPACE APPS 2026 · [EXACT CHALLENGE TITLE]"
Title: "Crew Readiness"
Subtitle: "A second look before docking."
One line: "It compares each person only with themselves, and a human decides."
Small: "[TEAM NAME]". Large stacked-lines motif on the right half.

2. 01 / THE PROBLEM
Title: "One threshold for everyone fits nobody."
Big number: "220 ms" with caption "between keystrokes: normal for one person, a large change for another."
Two short lines: "Crews are usually compared with population norms." / "Before a critical operation, a personal change is what matters, and a person should see it."

3. 02 / HOW IT WORKS
Title: "Personal baseline. Plain reasons. Human decision."
Four numbered steps in a horizontal row joined by a thin line (animate one by one):
1 "Routine checklist" (types fixed confirmation phrases)
2 "Timing only" (9 aggregate numbers computed in the browser)
3 "Own baseline" (median and robust spread of their own past sessions)
4 "Human review" (GREEN / YELLOW / RED with a plain-language reason)
Example reason in small italic: "a pause count this high would be expected about 1 session in 9".
Placeholder rectangle (1 px grey outline) labelled "SCREENSHOT: dashboard" for me to fill.

4. 03 / PRIVACY BY DESIGN
Title: "It measures when, never what."
Three lines: "Only nine aggregate timing numbers per session leave the browser." / "No typed text, no key identities, no keystroke timeline. The server rejects them, and tests check it." / "Monitoring runs only inside the task, with a visible indicator and a preview of exactly what is sent."
Visual: a row of 9 small white squares labelled "9 numbers" next to a crossed-out grey "typed text".

5. 04 / EVIDENCE (SIMULATED)
Title: "Fewer false alarms, shown with the trade-off."
Label under title in amber: "SIMULATED DATA: 300 simulated people per row, 40 sessions each".
Big-number pair: "13.0 % → 4.7 %" caption "false alerts on normal sessions at the product's alert level".
Second pair: "0.42 → 0.35" caption "detection also falls (10 % slowdown). We show the cost."
Third pair: "0.24 → 0.36" caption "detection at a matched 5 % false-alert rate".
Fourth, small: "Sustained 20 % slowdown: the old method learned it as normal (0.88 → 0.07 by session 15). Keeping flagged sessions out of the baseline held 0.40."

6. 05 / HONEST LIMITS
Title: "What we did not validate."
Five short lines: "No real people: the demo crew is fictional, the data synthetic." / "No licensed public dataset with enough sessions per person." / "Our own simulator, so the benchmark is partly circular." / "Thresholds are illustrative, not clinical." / "It detects changes in interaction timing, not fatigue or illness, and it never clears anyone for duty."
Make this slide look as confident and designed as the others: honesty is a strength here.

7. 06 / IMPACT AND NEXT STEPS
Title: "A human closes the gap."
Three next steps: "Validate on real repeated-session data with a licence we can cite." / "Decide with domain experts what false-alert rate a crew would accept." / "Add task types beyond a typed checklist."
Links block: "Live: https://crew-readiness-cmqs.vercel.app" and "Code: [REPO URL]".
Small credits in grey 9 pt: "Built with Flask, SQLite, NumPy. AI coding assistance used; the team reviewed and owns all decisions. Not affiliated with or endorsed by NASA."

== WORDING RULES (strict) ==
Never write: "detects fatigue", "impaired", "fit for duty", "accuracy", "proven", "AI-powered", "the AI decided", "NASA-approved". Say instead: "change from personal baseline", "check-in suggested", "the prototype flagged; a human decides". Every number on slide 5 is simulated and must say so. Keep [BRACKETED] placeholders exactly as written so I can fill them.

Speaker notes: add 2-3 sentences per slide that I can read aloud (about 20 seconds per slide).
