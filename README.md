# Geometry Quest

An interactive geometry course for learners aged 9 to 18, built for home education. Sixteen worlds take you from a single point to infinite snowflakes, with hands-on labs, a guide character called Vertex, printable worksheets and progress tracking that needs no accounts.

## Features

- **16 worlds in curriculum order**, each opening with a real-life hook (scissors, railway crossings, bike wheels, A4 paper, the £1 coin).
- **23 interactive labs.** Tear the corners off a triangle to see 180°, roll out a wheel to find π, fold nets into 3D shapes, measure with an on-screen protractor, hunt for treasure on a coordinate grid.
- **Challenges** at the end of every world, 5 questions each: multiple choice, typed answers and drag-to-make-an-angle. Up to 3 stars per world.
- **Quest map** that unlocks worlds as stars are earned, with an Explore mode to unlock everything.
- **XP, ranks and 16 badges**, some hidden inside the labs.
- **Boss battle:** a 60-second quiz across all worlds.
- **Printable worksheets and separate answer sheets** for every world (A4 PDF), including a cut-out dice net.
- **Progress report for parents**, with a world-by-world table, curriculum references and a copyable summary for home-education records.
- **Progress code:** an 18-character code that stores stars, XP, badges and the boss score. Enter it on any device to check progress or carry on there.

## The worlds

| # | World | Curriculum (England, approximate) |
|---|---|---|
| 1 | Points & Lines | Y3: lines, parallel and perpendicular |
| 2 | Angles | Y3–Y5: types of angle, degrees |
| 3 | Protractor Skills | Y5: measure and draw angles |
| 4 | Angle Rules | Y5–Y6: angles on a line, at a point, opposite |
| 5 | Triangles | Y4–Y6: classify, angle sum, area |
| 6 | Polygons | Y4–Y6: polygons, quadrilaterals; KS3 angle sums |
| 7 | Circles & π | Y6: parts of a circle; KS3 circumference, area |
| 8 | 3D Shapes & Nets | Y5–Y6: 3D shapes and nets |
| 9 | Parallel Lines | Y3: parallel lines; KS3 angle facts |
| 10 | Symmetry | Y4: line symmetry; KS3 rotational |
| 11 | Coordinates | Y4: first quadrant; Y6: four quadrants |
| 12 | Transformations | Y5–Y6: translate, reflect; KS3 rotate |
| 13 | Constructions | KS3: ruler and compass |
| 14 | Congruence | KS3–KS4: congruent triangles |
| 15 | Pythagoras & √2 | KS3–KS4: Pythagoras, irrational numbers |
| 16 | Fractals | Enrichment |

Curriculum references are a guide only.

## Using it for home education

1. Let the learner work through a world: the guide's intro, the labs, then the challenge.
2. Print that world's worksheet for pencil-and-paper practice. Print at **100% / actual size** so the measuring questions work with a real ruler and protractor.
3. Mark it with the separate answer sheet.
4. Open **Report** to see progress, copy the summary into your records, or note down the progress code.

## Running it

It's a single HTML page with no build step and no dependencies to install.

```bash
# serve the folder so the worksheet links work
python3 -m http.server 8000
# then open http://localhost:8000
```

Opening the HTML file directly also works, but the worksheet links need the page to be served over HTTP.

The "Download" buttons for worksheets and summaries use a download feature of the claude.ai artifact viewer. They hide themselves elsewhere, and the "Open to print" links are always available.

## Project structure

```
index.html               # the whole app: HTML, CSS and JavaScript
worksheets/              # generated PDFs
  w01-worksheet.pdf … w16-worksheet.pdf
  w01-answers.pdf   … w16-answers.pdf
  geometry-quest-worksheet-pack.pdf
  geometry-quest-answer-pack.pdf
make_worksheets.py       # generates every PDF in worksheets/
```

### Regenerating the worksheets

```bash
pip install reportlab
python3 make_worksheets.py
```

The script uses DejaVu Sans fonts from `/usr/share/fonts/truetype/dejavu/`. Change the paths at the top of the script if your fonts live elsewhere.

## Technical notes

- Vanilla JavaScript with SVG, Canvas and CSS 3D transforms. No frameworks.
- Fonts come from Google Fonts (Bricolage Grotesque, Atkinson Hyperlegible, JetBrains Mono), with system fallbacks.
- Light and dark themes follow the device setting.
- Respects `prefers-reduced-motion`. Draggable handles also work with arrow keys.
- Sound effects are generated with the Web Audio API and can be switched off.

## Privacy

There are no accounts, no tracking and no server. Progress is saved only in the browser's local storage. The progress code holds no name or personal details.

## Credits and licence

Course content is adapted from the open textbook [*Geometry for Elementary School*](https://en.wikibooks.org/wiki/Geometry_for_Elementary_School) on Wikibooks, licensed under [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/). Adapted content in this project, including the worksheets, is shared under the same licence.

Choose a separate licence for the code (MIT, for example) and add it as `LICENSE`.
