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
| Work | "Astronaut Glove Tested in JPL's CITADEL", NASA ID **PIA26430**, 2025-04-24 |
| Description | An EVA glove for spacewalks on the International Space Station, prepared for thermal vacuum testing at NASA's Jet Propulsion Laboratory on 1 Nov 2023 |
| Credit | **NASA/JPL-Caltech** |
| Licence | NASA media: generally not subject to copyright in the US; NASA's media usage guidelines apply (no endorsement implied) |
| Details page | https://images.nasa.gov/details/PIA26430 |
| Original | `https://images-assets.nasa.gov/image/PIA26430/PIA26430~orig.jpg`, 7141 x 4017 px, SHA-1 `20f482f20315eb74c1dd3df6dea104c300fe914e` |
| Contains people? | No. Test rig, glove, thermocouple wires only |

## Processing (both images)

Reproducible with one command: `scripts/assets/make_landing_images.py` (see its docstring).

1. Crop the region of interest. 2. Cut out the subject: a coarse outline drawn by a person seeds OpenCV GrabCut, which
decides the true edge. 3. Convert to black and white and apply a mild tone curve. 4. Mirror the glove so it points
toward the hand. 5. Pad each image so its leading fingertip sits on the vertical centre line at its inner edge (this
is why the page can place the hands and the gap with plain CSS). 6. Fade the outer 10 percent to transparent so the
sleeves dissolve. 7. Save as WebP (quality 84).

The images are altered (cut out, recoloured, mirrored). They are not presented as the original photographs.

## How to add an image

Put it in `app/static/img/`, add a section here with source, licence, credit, checksum and processing, and keep it
under 400 KB. The test suite enforces all three.
