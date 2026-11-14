# Design system and rationale

The look of Crew Readiness is a set of decisions, not a theme. This page records them so anyone on the team can defend or change them.
Code: [`app/static/css/style.css`](../app/static/css/style.css) · art: [`ridgeline.js`](../app/static/js/ridgeline.js) · live trace: [`keytrace.js`](../app/static/js/keytrace.js)

## 1. The idea: stacked sessions

The hero is a plate of **one line per recent session**, oldest at the top. A line is **flat** when that session matched the person's own baseline, and it **rises** where timing was slower or pausier than their usual. Early sessions recorded before a baseline existed are **dashed**. The latest session is drawn in its status colour.

It is the product's whole argument ("compared only with yourself") drawn from real data, not decoration. Every curve is built from `trend[].deviations` returned by the API (`docs/DATA_CONTRACT.md` §5). The only non-data movement is a sub-pixel idle drift and the entrance/morph animation.

**Inspiration, credited.** The form is a *stacked pulse plot*. The best-known example is Harold D. Craft Jr.'s 1970 plot of 80 pulses from pulsar CP 1919, which later became a famous album cover. We borrowed the idea of stacking repeated measurements so that deviation is visible. We did not use that artwork or any code. Our plot is drawn from our own data.

## 2. What we rejected, and why

| Rejected | Reason |
|---|---|
| EEG / heart-rate waveforms, "Hardware", "Clinical Validation" | We measure none of that. It would be an unsupported health claim (PLAN §1). We draw typing rhythm, which is what we actually capture |
| Glassmorphism, blur, glow, gradients | Flat is calmer, cheaper to render on a demo laptop, and the dark-plus-glow look is widely overused |
| Flow-field / particle backgrounds | Generic and decorative: they explain nothing. Sources advise low counts, one ink and a static fallback precisely because they cost performance and accessibility |
| External font or CDN | Breaks offline demos (risk R-6). Fonts are self-hosted |

## 3. Principles

1. **Flat.** No gradients, blur or shadows. Depth comes from hairlines and space.
2. **One ink.** Off-white on obsidian. Colour only ever carries status.
3. **Two typefaces.** Space Grotesk for words, JetBrains Mono for numbers and labels.
4. **Motion must explain something.** If it can't be justified in one sentence, remove it.
5. **Status is text first.** Every status chip says its word; colour is secondary.
6. **Honest.** No claim in the UI that the data can't support.

## 4. Tokens

| Token | Value | Use |
|---|---|---|
| `--bg` | `#090A0F` | page |
| `--ink` | `#F8FAFC` | text, lines |
| `--muted` | `#9AA0AA` | secondary text (7.5 : 1 on bg) |
| `--line` / `--line-strong` | `#1D212C` / `#2C3140` | hairlines (decorative only) |
| `--cyan` | `#00F0FF` | interactive, and NOMINAL |
| `--amber` | `#FFB800` | CHECK-IN, the deviating line |
| `--coral` | `#FF5A6E` | REVIEW. **Added** to the brief's palette: three status levels need three distinguishable colours |

Type: display 38–82 px / 500 / −0.05 em; body 16 px / 1.6; labels 11–12 px mono, uppercase, +0.12 em. Fonts: `static/fonts/` (variable woff2, SIL OFL licences alongside).

## 5. Motion inventory

| Motion | What it explains | Detail | Reduced motion |
|---|---|---|---|
| Art entrance | Sessions accumulate over time; the newest draws last | ~1.5 s once, starts when the plate is first visible | drawn instantly |
| Art morph on crew change | Same plot, different person's history | exponential smoothing, ~0.6 s | snaps |
| Idle drift | The data is live | ±0.8 px, ~3 s periods | off |
| Line hover | Which session is this line | highlights line + readout | still works (no animation) |
| Live key trace (Monitoring) | What is captured: *when*, never *what* | blip per counted key; amber while a pause is happening | redraws per key, no scroll |
| Text rise on load | Orientation only | 0.9 s | instant |

Performance: canvas loops pause when off-screen or the tab is hidden; DPR capped at 2.

## 6. Accessibility

- Contrast: text ≥ 7 : 1 (muted) and ≥ 14 : 1 (ink) on `--bg`.
- Status is always written as well as coloured.
- Canvas art has a text alternative (`aria-label`, caption, and the advisory / reasons / evidence table beside it carry the same information).
- `prefers-reduced-motion` respected everywhere; `[hidden]` always wins (a bug we hit: a component's `display` once overrode `hidden` and showed "Monitoring active" before monitoring).
- Visible focus ring (`--cyan`) on every interactive element.

## 7. Sources (verify each before the submission: task R-2)

Search summaries only; **not yet independently read**. Confirm before citing.

- Scientific American, "Pop Culture Pulsar: Origin Story of Joy Division's Unknown Pleasures Album Cover": https://www.scientificamerican.com/blog/sa-visual/pop-culture-pulsar-origin-story-of-joy-division-s-unknown-pleasures-album-cover-video/ (origin of the stacked pulse plot, Craft 1970)
- University of Cambridge, "Journeys of discovery: pulsars": https://www.cam.ac.uk/stories/journeysofdiscovery-pulsars (the pulsar discovery context)
- Big Think, "Known pleasures: from pulsar signal to post-punk icon": https://bigthink.com/strange-maps/known-pleasures-from-pulsar-signal-to-post-punk-icon/
- NASA Graphics Standards Manual (NHB 1430.2, 1976): https://www.nasa.gov/wp-content/uploads/2015/01/nasa_graphics_manual_nhb_1430-2_jan_1976.pdf (informed the restraint: few typefaces, strict system, legibility first)
- Design commentary on restrained dark interfaces (Linear landing-page breakdown): https://webtrends.pages.dev/posts/linear-landing-page-breakdown (flat dark with a single accent)
- Flow-field background component docs (21st.dev, Framer): considered and **rejected**; their guidance on low particle counts, one ink and reduced-motion fallbacks informed our motion rules.
- Fonts: Space Grotesk and JetBrains Mono, SIL Open Font License 1.1 (`app/static/fonts/OFL-*.txt`).

## 8. Open items

- Brand name. The brief used a placeholder (ASTRAPULSE). We kept **Crew Readiness**: "pulse" suggests a physiological signal we don't measure. Check name availability before using any other.
- The landing-style copy from the brief ("Request Mission Demo") became **Start monitored task**, because there is no sign-up flow and we collect no contact details.
- Attention page and Privacy & limits page inherit the system but still carry task-owner TODOs (A-1, R-1).
