# Design system and rationale

**Direction: International Typographic ("Swiss") style on a dark ground.** One grid, one typeface, flush-left type, structure from rules and space, and colour only when something needs a human. Status: **trial on a branch**, chosen by the team lead after comparing styles (decision D-9 in PLAN.md).

Code: [`style.css`](../app/static/css/style.css) · tokens for canvas code: [`tokens.js`](../app/static/js/tokens.js) · art: [`ridgeline.js`](../app/static/js/ridgeline.js) · live trace: [`keytrace.js`](../app/static/js/keytrace.js)

## 1. The idea in one sentence

The page is a grid with a **label gutter** on the left (section names, small and bold) and **ten columns of content** on the right; the one expressive element is a data graphic, **stacked sessions**, that is the product's whole argument drawn from real data.

## 2. The grid (enforced, not eyeballed)

| Rule | Value |
|---|---|
| Columns | 12, gutter 24 px, outer margin `clamp(20px, 4vw, 56px)`, max width 1440 px |
| Label gutter | columns 1–2 (`.label`): section number and name |
| Content | columns 3–12 (`.body`), subdivided by `.g10` into the *same* 10 columns, so nested edges land on the outer grid |
| Narrow screens (≤ 860 px) | 4 columns; labels stack above content |
| Alignment | everything starts and ends on a column edge |

**See it:** add `?grid` to any URL to overlay the columns (`static/js/grid.js`, a dev aid; nothing depends on it).
**Check it:** `scripts/check_grid.js` reads the browser's real track sizes and asserts that the edges of labels, bodies, hero copy, art and crew cells land on column edges within 1.5 px, across 4 widths and 5 pages. It was verified to *fail* when a block is nudged 7 px off-grid. Optional; needs Node and Playwright.

## 3. Principles

1. **One grid.** Section names hang in the left gutter; content aligns to the columns.
2. **One typeface.** Inter, weights 400 and 700 do the work: hierarchy from size and weight, never decoration. Numbers that are compared use tabular figures; running text does not (tabular figures widen Inter's hyphen).
3. **Flush left, ragged right.** Nothing is centred.
4. **Structure from rules and space.** No boxes, shadows, blur or gradients. A crisp 1 px ink rule opens every section; 1 px grey rules separate rows.
5. **Colour only when something needs a human.** The interface is monochrome. Nominal is plain ink. Amber = check-in, coral = review. Status is always written as a word as well.
6. **Motion must explain something** and has a reduced-motion fallback.
7. **Honest.** No claim the data can't support (PLAN §1).

## 4. Tokens (colour roles)

CSS custom properties are the single source of truth. CSS and JavaScript read **roles**, never hex codes (`tokens.js` exposes them to canvas and chart code), so a theme change is a change to `:root` only.

| Role | Value | Use |
|---|---|---|
| `--bg` / `--ink` / `--muted` | `#090A0F` / `#F8FAFC` / `#9AA0AA` | ground, text and rules, secondary text (7.5 : 1) |
| `--rule` / `--line` / `--line-faint` | `#F8FAFC` / `#2C3140` / `#1D212C` | section rules, row separators, art guides |
| `--accent` | `#F8FAFC` | interactive (buttons, focus): monochrome on purpose |
| `--signal` | `#FFB800` | the brand highlight: the rising line |
| `--nominal` / `--checkin` / `--review` | ink / `#FFB800` / `#FF5A6E` | status. **Coral was added** to the original palette: three levels need three distinguishable states |
| `--surface` | `#16181F` | raised surface (chart tooltip) |

Type: Inter (variable woff2, `static/fonts/`, SIL OFL licence alongside); `ui-monospace` stack for code and the payload preview only.
Scale: display 44–104 px / 0.94 / −0.045 em / 700; title 32–64 px; advisory 22–32 px; body 16 / 24; labels 13 / 20 / 600; fine print 12 / 16.

## 5. The art: stacked sessions

One canvas line per recent session, oldest at the top. A line is **flat** when that session matched the person's own baseline and **rises** where timing was slower or pausier. Dashed = recorded before a baseline existed. The latest session is drawn thick, in its status colour (plain ink when nominal).

Every curve is built from `trend[].deviations` (`docs/DATA_CONTRACT.md` §5). The only non-data movement is a sub-pixel idle drift and the entrance/morph animation.

**Credit.** The form is a *stacked pulse plot*; the best-known example is Harold D. Craft Jr.'s 1970 plot of pulsar CP 1919. We borrowed the idea of stacking repeated measurements to make deviation visible. No artwork or code was used.

## 6. Motion inventory

| Motion | What it explains | Reduced motion |
|---|---|---|
| Art entrance (~1.5 s once, when first visible) | Sessions accumulate; the newest draws last | drawn instantly |
| Art morph on crew change | Same plot, different person's history | snaps |
| Idle drift (±0.8 px) | The data is live | off |
| Line hover | Which session is this line | works, no animation |
| Live key trace (Monitoring) | What is captured: *when*, never *what*. Pauses show amber while they happen | redraws per key, no scroll |

Canvas loops pause when off-screen or the tab is hidden; DPR capped at 2.

## 7. Accessibility

- Text ≥ 7 : 1 (muted) and ≥ 14 : 1 (ink) on `--bg`.
- Status is a word first (`GREEN`, `YELLOW`, `RED`, `CALIBRATING`) with a square marker second.
- Canvas art has a text alternative (`aria-label`, caption, and the advisory, reasons and evidence table carry the same information).
- `prefers-reduced-motion` respected; `[hidden]` always wins (a bug we hit: a component's `display` once overrode `hidden` and showed "Monitoring active" before monitoring).
- Visible focus ring on every interactive element; inputs thicken their underline on focus.

## 8. History of this decision

1. First pass: dark mission-control look with a flat system. Merged.
2. Alternatives researched (dark mission-control, Swiss, editorial/bento such as Uiverse's Boldcase, neo-brutalism). Boldcase could not be read from the build environment (the site blocks it), so it was not implemented.
3. Team lead chose **Swiss**. Rejected earlier: glassmorphism, gradients, flow-field backgrounds, EEG/HRV imagery (we measure none of that), external fonts (offline demo, risk R-6).

## 9. Sources (verify each before the submission: task R-2)

Search summaries only; the article hosts are outside the build environment's network allowlist, so **none of these pages was independently read**. Confirm before citing.

- Swiss style on the web (12-column grid, one neutral sans, asymmetry, never centre text): [UX Planet](https://uxplanet.org/swiss-style-web-design-everything-you-need-to-know-2b128fd327b9) · [Justinmind](https://www.justinmind.com/blog/swiss-style-web-design-everything-you-need-to-know/) · [Webdesigner Depot, Swiss in CSS](https://www.webdesignerdepot.com/2016/01/swiss-in-css-animating-the-international-typographic-style/) · [daisyUI](https://trends.daisyui.com/trend/swiss-style/)
- Stacked pulse plot origin: [Scientific American](https://www.scientificamerican.com/blog/sa-visual/pop-culture-pulsar-origin-story-of-joy-division-s-unknown-pleasures-album-cover-video/) · [University of Cambridge](https://www.cam.ac.uk/stories/journeysofdiscovery-pulsars)
- NASA Graphics Standards Manual (restraint, few typefaces, strict system): https://www.nasa.gov/wp-content/uploads/2015/01/nasa_graphics_manual_nhb_1430-2_jan_1976.pdf
- Mission-control UX patterns: [UX Planet benchmark](https://uxplanet.org/mission-control-software-ux-design-patterns-benchmarking-e8a2d802c1f3)
- Font: Inter, SIL Open Font License 1.1 (`app/static/fonts/OFL-Inter.txt`).

## 10. Open items

- Brand name: kept **Crew Readiness**. "Pulse" suggests a physiological signal we don't measure; check availability before using any other name.
- The Attention and Privacy & limits pages carry the style but still hold task-owner TODOs (A-1, R-1).
- Possible refinement: align the art's five axes to grid column centres (they currently sit at 10/30/50/70/90 % of the plate, within ~10 px of the column centres).
