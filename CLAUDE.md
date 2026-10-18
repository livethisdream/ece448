# ECE 448 — working notes for Claude

Course site for **ECE 448, Software Defined Radios** (USAFA, Spring 2027),
taught by Dr. Neil Rogers. Jupyter Book under `book/`, published to GitHub
Pages at `livethisdream.github.io/ece448/` on every push to `main`. 7 modules,
20 lessons, 13 labs, a midterm (fox hunt and CTF), and a self-defined final
project (Neil, 2026-10-17).

**This is an applications course: only enough theory to get by** (Neil,
2026-10-17). Every lesson exists to build, receive, or decode a real signal
in GNU Radio. Theory appears only as far as the flowgraph needs it. Where
ECE 444 would put a derivation on screen, 448 puts a flowgraph. The rules are
in `project/ROADMAP.md`, "Course philosophy"; apply them to every page,
slide, lab, and assessment.

**Follow ECE 444.** `livethisdream/ece444` is the model for this site's
format, conventions, and rules. Its `CLAUDE.md`, `project/ROADMAP.md`,
`COURSE_SPEC.md`, `VOICE.md`, and `REVIEW.md` apply here unless a rule is
about 444's own subject (antennas, the ADALM-PHASER, radar). The shell
(`book/_templates/`, `book/_static/`, `book/_ext/`) and `scripts/verify/` are
444's (copied by way of ECE 343), with only what a cadet sees changed. Fix the
shell in 444 first, then copy it here.

`project/ROADMAP.md` holds this course's plan and its settled decisions, and
`project/ECE448_PROJECT.md` is the running project note. Read both before any
work.

## What is here

| Path | What |
| :-- | :-- |
| `book/moduleNN/LNN-<slug>/index.md` | the lesson page (a frame page) |
| `book/moduleNN/LNN-lab-<slug>/index.md` | a lesson's lab, a child page listed after it; no lesson number of its own |
| `book/module05/midterm/`, `book/module07/final-project/` | the midterm and final project pages |
| `book/moduleNN/index.md` | module landing page, generated |
| `book/extras/slides/<slug>.md` | a reveal.js deck; `.html` wrapper from `scripts/make_deck_html.py` |
| `book/extras/legacy/*.pdf` | the legacy Beamer slides, served at `/legacy/`; `refs/` holds third-party references |
| `book/extras/grc/` | flowgraphs (`.grc`) and scripts a cadet downloads, served at `/grc/` |
| `book/extras/labs/*_blank.pdf` | lab packets, student copy only; the KEY goes to `ECE448-faculty/lab-keys/` |
| `latex/` | practice-set and lab-packet sources and build scripts (444's harness) |
| `scripts/grc/` | normalize a `.grc`, run one headless for screenshots, screenshot GRC itself |
| `figures/` | course figure library for LaTeX (`\graphicspath{{./figures/}}`) |
| `scripts/scaffold_lessons.py` | the manifest: lessons, labs, objectives, legacy decks |

## The manifest

`scripts/scaffold_lessons.py` is the one source for lesson numbers, titles,
objectives, labs, and which legacy deck a lesson links. It writes the pages it
does not find, regenerates the module pages and `book/_toc.yml`, and checks
that every objective is served and every linked PDF exists. **Don't hand-edit
`_toc.yml` or a module page**; edit the manifest and re-run. The schedule and
objective tables in `book/syllabus.md` and the deck table in
`book/materials.md` were generated from it once and are now hand maintained,
so change them together with the manifest.

## Converting a lesson

Lessons move to the 444 format one at a time, in teaching order. A converted
lesson replaces its generated page with a real frame lesson, following 444's
`book/module01/L05-field-regions/` as the worked example and 444's budgets
and checks. L01 is converted. Keep the legacy slide links until the new
material covers the same ground, then set the lesson's decks to `[]` in the
manifest. GNU Radio flowgraphs (`.grc`) and example code a cadet runs go with
the lesson; solutions stay in `ECE448-faculty`.

## Build and verify

```sh
pip install -r requirements.txt     # Python 3.10-3.12; 3.13 lacks imghdr
jupyter-book build book/ --all      # ALWAYS --all
scripts/verify/check_shell.py
scripts/verify/check_frames.py
scripts/verify/check_bar.py
scripts/verify/check_math.py        # no display equation scrolls sideways at 320-390 px
scripts/verify/check_grc.py         # every downloadable flowgraph compiles under GNU Radio 3.10
scripts/verify/check_deck.py L01-course-intro
```

The checks need `pip install playwright` and `npm install` in
`scripts/verify/` once per container; see `scripts/verify/README.md`.

## Flowgraphs

GNU Radio 3.10 is the course version (Neil, 2026-10-18), installed by
radioconda on cadet laptops and by the session hook here. Every `.grc` a lesson
ships goes through three steps before it is committed:

1. **Normalize** it with `scripts/grc/grc_normalize.py`, which loads it through
   GRC's own platform and saves it back with every default filled in, so it
   opens without warnings.
2. **Compile** it: `scripts/verify/check_grc.py`.
3. **Run** it, if it needs no hardware, with `scripts/grc/grc_shot.py` under
   `xvfb-run`, and use that screenshot on the page. A flowgraph that needs an
   SDR is compiled only; say so in the PR. A figure that stands in for a real
   capture is labeled "Simulated" on the figure itself.

The GNU Radio bindings are built for `/usr/bin/python3.12`; call `grcc` and the
scripts through it, not through whatever `python3` is first on `PATH`.

## Public repo

This repo is **public**. Assessments, the midterm and its keys, grades, and lab
KEY PDFs live in the private `livethisdream/ECE448-faculty` (lab keys under
`lab-keys/`), never here. Practice-set and lab-packet LaTeX sources are here,
as in ECE 444, and practice SOLUTIONS PDFs are published; a lab's KEY PDF is
built locally and never committed. `.gitignore` blocks the usual names, but
check every PDF before adding it.

American spelling everywhere. No thin spaces. "GNU Radio", two words. Never
MATLAB for anything a cadet runs.
