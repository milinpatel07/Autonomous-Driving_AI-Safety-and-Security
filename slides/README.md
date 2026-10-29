# Lecture slides

A course overview and one deck per module, written in Markdown for [Marp](https://marp.app) and built to HTML,
PDF and PowerPoint. The built decks are on the course website:
<https://milinpatel07.github.io/Autonomous-Driving_AI-Safety-and-Security/slides/>.

| Deck | Slides | Lectures | Status |
|---|---|---|---|
| [00 · Course overview](00_course_overview.md) | 23 | 1 | available |
| 01 · Perception and Prediction | | 3 | planned |
| 02 · Failures and Robustness | | 1 | planned |
| 03 · Functional Safety (ISO 26262) | | 3 | planned |
| [04 · SOTIF (ISO 21448)](04_sotif.md) | 52 | 2 | available |
| 05 · Cybersecurity (ISO/SAE 21434) | | 2 | planned |
| 06 · AI Safety (ISO/PAS 8800) | | 2 | planned |
| 07 · Runtime Assurance and Operations | | 1–2 | planned |
| 08 · Standards, Regulation and Safety Case | | 1–2 | planned |

## Build

```bash
python scripts/build_slides.py --check          # every figure reference resolves (no Node.js needed)
python scripts/build_slides.py                  # HTML in slides/_build/
python scripts/build_slides.py --pdf --pptx     # also PDF and PowerPoint
python scripts/build_slides.py --deck 04_sotif  # one deck
```

The build needs Python with Matplotlib, Node.js (Marp CLI 4.5.1 is run with `npx`) and, for PDF and PowerPoint,
a Chromium-based browser; set `CHROME_PATH` if Marp does not find one. The PowerPoint file is image-based: one
picture per slide, with the speaker notes as text.

## How the decks are written

**Figures come from the notebooks.** A figure is referenced by notebook and cell id, and the build extracts the
image from the committed notebook:

```markdown
![w:1150](nb:04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb#42b592ba)
![h:450](nb:04_SOTIF_ISO21448/02_triggering_conditions_and_scenarios.ipynb#9c269d98/1)
```

`/1` selects the second output of the cell; without it the first image output is used. Diagrams that are not in
a notebook (course map, background figures) are drawn by [`diagrams.py`](diagrams.py) and referenced as
`diagrams/<name>.svg`.

**One message per slide.** The title is a full sentence that states the result, with the number from the
notebook ("Pedestrian recall falls from 0.77 in clear air to 0.52 at 25 m visibility"), not a topic
("Results"). The figure is the evidence. At most one line of text under the figure (`<div class="take">`).

**The explanation is in the speaker notes** (`<!-- ... -->` after the slide content): how to read the figure,
what to say, a question for the class, the common mistake, and the link to other modules.

**Every figure names its source** in the slide footer (`<!-- _footer: "Source: notebook 04-02 · KITTI (CC BY-NC-SA 3.0)" -->`),
including the data licence when the figure shows data.

**Structure of a module deck**

1. Title slide and the course map with the module highlighted
2. What the module needs from earlier modules, and where to revise it
3. Background slides for the quantitative prerequisites
4. Per notebook: a divider with its questions, then 4–8 result slides
5. What the module hands to the next modules
6. Terms, exercises and discussion questions, references

**Wording.** Plain and precise: state what was measured, on what, with what uncertainty. Say *synthetic* or
*illustrative* when a figure is not from real data, and state the limits of each result where it is shown.

**Theme.** [`theme/course.css`](theme/course.css): 16:9, light, the colours of the notebooks (Okabe-Ito). Slide
classes: `title`, `notebook` (divider), `compact` (long table), and `m01`–`m08` for the module colour. To use an
institutional template, adapt the theme or copy titles and figures into it.
