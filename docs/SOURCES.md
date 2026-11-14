# Sources (task F3, R-2)

**Status: DRAFT. Every link below was opened by the teammate's coding agent on 2026-11-14, and every quote was copied from the
opened page, not from memory or a search summary. A HUMAN MUST STILL OPEN EACH LINK AND CHECK EACH LINE before this file is merged
or cited.** Tick the box when you have.

Each entry separates **what they found** (their work) from **how it informed us** (our choices). None of these sources tested
Crew Readiness, and none of our results come from them. Our own results are simulated (`docs/ML_RESULTS.md`), plus a small pilot
with deliberate perturbations (`docs/PILOT.md`) once it has been run.

## 1. NASA Human Research Program: Behavioral Health risk (evidence report, 2025)

- [ ] Checked by a human
- **Source:** Dev SI, Whiting SE, Nelson GA, Dotson V, Mulavara A, Schorn JM, et al. *Risk of Adverse Cognitive or Behavioral Changes
  and Psychiatric Disorders Leading to In-Mission Health and Performance and Long-Term Health Effects.* NASA Johnson Space Center
  Evidence Report, 2025. <https://ntrs.nasa.gov/citations/20250001454>
- **What they found:** the report "emphasizes the need to characterize cognitive and behavioral outcomes, develop tools to monitor
  behavioral health, and ultimately implement countermeasures". It states that "no behavioral emergencies have been reported to date
  during spaceflight", but that the likelihood of an adverse change "rises with increases with mission duration, distance from Earth,
  and greater exposure to spaceflight hazards" (quoted as written in the abstract).
- **How it informed us:** it is why we frame the product as a monitoring *tool* for a known NASA risk area on longer missions, and
  why we do not claim that it detects any condition: the report itself says incidence on current missions is low and the field is
  still characterising outcomes.

## 2. Cognition: NASA's computerized test battery for astronauts (2015)

- [ ] Checked by a human
- **Source:** Basner M, Savitt A, Moore TM, et al. *Development and Validation of the Cognition Test Battery for Spaceflight.*
  Aerospace Medicine and Human Performance 2015;86(11):942-952. doi:10.3357/AMHP.4343.2015. PubMed:
  <https://pubmed.ncbi.nlm.nih.gov/26564759/> (open full text: <https://pmc.ncbi.nlm.nih.gov/articles/PMC4691281/>)
- **What they found:** a battery of 10 tests "specifically designed for the high-performing astronaut population". "Practice effects
  and test-retest variability differed substantially between the 10 Cognition tests, illustrating the importance of normative data
  that both reflect practice effects" and differences in difficulty.
- **How it informed us:** two design choices. (a) Repeated short computer tasks are an established way to track performance in
  spaceflight research, which supports a routine checklist as the measurement. (b) Practice effects are real, so we compare each
  person with their *own recent* sessions, add a practice run to the pilot protocol, and list practice as a confounder on the
  Privacy & limits page.

## 3. The psychomotor vigilance test (PVT): how to score reaction times (2011)

- [ ] Checked by a human
- **Source:** Basner M, Dinges DF. *Maximizing Sensitivity of the Psychomotor Vigilance Test (PVT) to Sleep Loss.* Sleep
  2011;34(5):581-591. doi:10.1093/sleep/34.5.581. <https://pmc.ncbi.nlm.nih.gov/articles/PMC3079937/>
- **What they found:** "A PVT response was regarded valid if RT was ≥ 100 ms", and "Responses without a stimulus or RTs < 100 ms were
  counted as false starts (errors of commission)". They also report "marked inter-individual differences" in how performance changes.
- **How it informed us:** our optional attention check (`app/static/js/attention.js`) uses the same rule: a response before the light
  or under 100 ms counts as too early. The inter-individual differences support comparing each person with their own baseline rather
  than a population threshold. We use the method only; we do not claim our short check measures what their study measured.

## 4. Keyboard timing as a monitoring signal, without the text (2016)

- [ ] Checked by a human
- **Source:** Giancardo L, Sánchez-Ferro A, Arroyo-Gallego T, et al. *Computer keyboard interaction as an indicator of early
  Parkinson's disease.* Scientific Reports 2016;6:34468. doi:10.1038/srep34468. Open access (Creative Commons Attribution 4.0):
  <https://pmc.ncbi.nlm.nih.gov/articles/PMC5050498/>
- **What they found:** key hold times during normal computer use "discriminated early PD groups from controls with an AUC = 0.81
  (n = 42/43 ...)". Their approach "does not require information about the text being typed or the actual key being pressed, only the
  hold time for each key".
- **How it informed us:** evidence from outside spaceflight that typing *timing alone* carries information about a person's state,
  and that it can be measured without recording the text, which is our privacy rule. **The difference matters:** they built a disease
  classifier on a clinical sample; we flag *changes from a person's own pattern* for a human, and claim to detect no condition.

## 5. NASA bed-rest WinSCAT data: repeated cognitive tests per person (data record)

- [ ] Checked by a human
- **Source:** NASA Life Sciences Data Archive. *Neurocognitive Assessment (WinSCAT) (Cognitive Assessment Tool for Windows) (Flight
  Analog).* DOI 10.83263/sbne-th55. <https://nlsp.nasa.gov/explore/data/details/80ee3231-7c42-5be4-b6c2-b8c788feeb50?dataType=EXPERIMENTS>
- **What they found:** in head-down-tilt bed rest (a ground analog of spaceflight), subjects took WinSCAT subtests that were "the same
  as those currently used onboard the International Space Station (ISS)", about 12 times each; the record states "No consistent
  decrements in cognitive performance were observed across subjects or across time in bed rest."
- **How it informed us:** it is the only openly downloadable NASA dataset we found with 8 or more sessions per person, and we used it
  for an exploratory check of our per-measure rule on real people (`docs/DATA_SEARCH.md`). **Its licence is not confirmed**, so that
  check is a feasibility note, not a result we cite, until a person confirms the terms.

## Not used, and why

- The official challenge page (<https://www.spaceappschallenge.org/2026/challenges/health-monitoring-software/>) could not be opened
  from the build environment (certificate failure). Its wording belongs in `docs/CHALLENGE.md` (task T0.1), read by a person.
- Nature's own page for source 4 redirected to a login host that was blocked; the identical article on PubMed Central was used instead.
