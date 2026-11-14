# Image assets: sources, licences, processing

**Rule:** every image in `app/static/img/` must be public domain or licensed to us, and must be recorded here
(`tests/test_assets.py` fails otherwise). Never another company's artwork. No NASA logos (the "meatball" and "worm"
marks need separate permission). Nothing here implies NASA endorsement.

Verification status: facts below were read from the Wikimedia Commons API and NASA's Image API on 2026-11-14.
Member 4 should re-check each licence on the linked pages before submission (task R-2).

## `hand-human.webp`: Adam's forearm and hand

| | |
|---|---|
| Work | Michelangelo Buonarroti, *The Creation of Adam*, Sistine Chapel ceiling, c. 1508-1512 |
| Status of the work | Public domain (the artist died in 1564) |
| Reproduction used | Wikimedia Commons file **"Michelangelo - Creation of Adam (cropped).jpg"**, 3524 x 1599 px, 2,163,447 bytes |
| File page | https://commons.wikimedia.org/wiki/File:Michelangelo_-_Creation_of_Adam_(cropped).jpg |
| Licence (as tagged on Commons) | **PD-Art / PD-old-auto-expired** (public domain: a faithful reproduction of a two-dimensional work whose author died more than 100 years ago) |
| Credit | Michelangelo Buonarroti (artist); the Commons page lists no separate photographer credit ("Extracted from" *Creación de Adán.jpg*, another public-domain Commons file) |
| Original SHA-1 | `bb5e02952269db83df0f6ac4b6561cd0d30269d0` |
| Why this file | It carries a plain public-domain tag and no usage conditions. Its limit is resolution: the forearm-and-hand crop is about 850 px wide in the source and is enlarged to 1500 px (about 1.8x), so the hand is **soft** at hero size. |

**Possible upgrade.** A far sharper reproduction exists on Commons: "A Criação de Adão - Michelangelo Buonarroti.jpg"
(14090 x 7075 px, SHA-1 `81a6d2d2513d01d94321f9ae4280fcbc88e29dfb`, tagged **CC0**, credited there to Pixabay user
"Kolímprint"). We could not download it during the build (Wikimedia rate-limited this environment, and we did not try
to get around that), so it is **not** used. If Member 4 fetches it, the same script works: pass it as `--adam` and
re-measure `--adam-crop` on an overview of that file, because its framing differs. Whoever swaps it must update this
section.

## `hand-astronaut.webp`: spacesuit glove

| | |
|---|---|
| Work | **"Man and Machine"**, NASA photograph (March 2012): Robonaut 2 reaching toward a spacesuit-gloved hand, staged as a nod to Michelangelo's *Creation of Adam*. We use only the spacesuit glove (the right-hand side of the photo) |
| Credit | **NASA** ("Image Credit: NASA" in NASA's image article and in Live Science, Phys.org and NBC News coverage) |
| Licence | NASA media: generally not subject to copyright in the US; NASA's media usage guidelines apply (credit NASA, no endorsement implied, no NASA logos) |
| Where it came from | A 1200 x 600 WebP copy supplied by the team lead from the space.com republication (https://www.space.com/15088-robonaut-photo-michelangelo-sistine-chapel.html). SHA-1 of that file: `6202ba9c74c71c32845a2ed3590a7fcd55503dab` (62,412 bytes) |
| NASA page | https://www.nasa.gov/image-article/man-machine/ (credit line read from search summaries; **the page itself could not be opened from the build environment**) |
| NASA image ID / original | **Not found.** Our searches of NASA's Image and Video Library did not return it, so we have no NASA ID and no higher-resolution original |
| Contains people? | No. A robot and a glove |

**Open verification (task R-2, Member 4).** Open the NASA page above, confirm the credit line and that the photograph carries
no restriction, and if possible find the original in NASA's library and its ID, then replace the small copy with the original
(the script takes it as `--glove`; the outline may need re-checking at a different resolution). Until then this image rests on
NASA's credit as reported by four outlets, not on a NASA page we read ourselves.

**Honest caveat.** The source is only 1200 px wide, so the glove is about 570 px wide before we enlarge it to 1140 px. It is
a smooth-textured glove, so it holds up, but it is softer than the NASA JPL photograph we used before. That photograph
(**NASA/JPL-Caltech, PIA26430**, "Astronaut Glove Tested in JPL's CITADEL", https://images.nasa.gov/details/PIA26430,
7141 x 4017 px, SHA-1 `20f482f20315eb74c1dd3df6dea104c300fe914e`) remains supported by the script with
`--glove-kind pia26430` and is a sharper fallback.

## `logo.webp`, `favicon.png`, `share-card.png`: brand images

| | |
|---|---|
| Work | The Crew Readiness logo: line drawings of a human hand and a robotic hand reaching toward each other on a grey disc (a nod to the *Creation of Adam*) |
| Origin | **AI-generated**, supplied by the team lead as a 1024 x 550 PNG (SHA-1 `39541e6fa9e2fc73a8e05579e5dbdb319c790a06`, 92,670 bytes). **The generator was not named**, so we cannot cite its terms |
| Credit | Crew Readiness team (prompting and selection); generator **[NOT STATED: fill in the tool name]** |
| Licence | **None stated.** Rights in AI-generated images are unsettled and depend on the generator's own terms, and in some places such images attract no copyright. We use it as our logo on that basis and make no claim to exclusive rights |
| Derived files | `logo.webp`: cropped, background keyed to transparent. `favicon.png`: 64 x 64. `share-card.png`: 1200 x 630 social preview built from the logo plus text in Inter (`scripts/assets/make_share_card.js`) |
| Contains people? | No |

**Open verification (task R-2, Member 4).** Name the generator and read its terms for commercial and competition use; if they do
not allow it, replace the logo (the site works without it; the nav keeps its own stacked-sessions mark). Space Apps asks teams to
disclose AI use: `docs/SUBMISSION.md` says the logo is AI-generated.

**Honest caveat.** The source is small (the drawing is about 434 px across). It is thin line art, so it reads well at hero size,
as a recognisable mark at 32 px, and as a grey disc with a white mark at 16 px. The nav keeps the small stacked-sessions mark, which
we drew ourselves and which stays legible at 30 px. Rebuild with `scripts/assets/make_brand_assets.py`.

## Processing (both images)

Reproducible with one command: `scripts/assets/make_landing_images.py` (see its docstring).

1. Crop the region of interest. 2. Cut out the subject: a coarse outline drawn by a person seeds OpenCV GrabCut, which
decides the true edge. 3. Convert to black and white and apply a mild tone curve. 4. Mirror the glove if it points away from
the hand (the Man and Machine glove already points left, so it is not mirrored). 5. Pad each image so its leading fingertip sits on the vertical centre line at its inner edge (this
is why the page can place the hands and the gap with plain CSS). 6. Fade the outer 10 percent to transparent so the
sleeves dissolve. 7. Save as WebP (quality 84).

The images are altered (cut out and recoloured; the older JPL glove was also mirrored). They are not presented as the original photographs.

## How to add an image

Put it in `app/static/img/`, add a section here with source, licence, credit, checksum and processing, and keep it
under 400 KB. The test suite enforces all three.
