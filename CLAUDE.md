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

**Sources and noise** (Neil, 2026-10-21): Neil's 2025 slides are the primary
source for a lesson, then the GNU Radio wiki and tutorials, then PySDR.org.
Noise is shown, not calculated: "look what happens when noise goes up." No
Eb/N0, BER, or probability-of-error math anywhere a cadet sees. Details in
`project/ROADMAP.md`, "Sources and noise".

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
| `book/extras/labs/*_blank.pdf` | lab packets, student copy only; answers come from `ECE448-faculty/lab-keys/src` through `\keysol`, and the KEY goes to `ECE448-faculty/lab-keys/` |
| `latex/` | lab-packet sources and build scripts (444's harness); the retired practice sources stay, unlinked |
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

**Write it with the `write-lesson` skill** (Neil, 2026-11-04, from ECE 444:
"why not just build those rules into the creation of lessons?"). A new or
rewritten lesson or lab page applies the voice, why, and illustration rules
while it is written, then runs one review with the three lenses in parallel
and stops once for Neil's pick; the three sweep skills are for pages written
before it. `scripts/verify/check_voice.py` holds the mechanical rules and
runs in CI on every page, so a FAIL blocks the PR.

Lessons move to the 444 format one at a time, in teaching order. A converted
lesson replaces its generated page with a real frame lesson, following 444's
`book/module01/L05-field-regions/` as the worked example and 444's budgets
and checks. L1-L20 are converted. Keep the legacy slide links until the new
material covers the same ground, then set the lesson's decks to `[]` in the
manifest. GNU Radio flowgraphs (`.grc`) and example code a cadet runs go with
the lesson; solutions stay in `ECE448-faculty`.

## Labs

**Labs are puzzles: build it, recover it** (Neil, 2026-11-26/27: "It's a
class of puzzles and thinking, not a traditional comms class"; "The point of
the class is not to measure every little dB of SNR or bandwidth. It's to see
how modulated signals are built and how to recover them"). A lab builds
whichever half the class did not: usually the receiver that recovers a
message, often from a recording whose settings the cadet works out, and
sometimes the transmitter that a given receiver must decode, and sometimes
both, the lesson discussing the chain's principles and the lab building the
transmitter and receiver end to end (Neil, 2026-11-28). Steps guide toward that
goal with checkpoints; predictions are reasoning, not numbers; impairments
are puzzles to diagnose and fix, never sweeps to tabulate. This leads every
lab rule below; details in `project/ROADMAP.md`, "Labs are puzzles".

**Labs follow ECE 444's lab rules, and there are no practice sets** (Neil,
2026-11-21: "I don't really need practice sets. The labs are the main
thing"). A lesson works every method its lab's Part 1 needs, at settings the
lab does not use, and ends with a read-only "Preparing for the Lab" frame
that points to Part 1 of the packet; a lesson without a lab has neither that
frame nor a Practice frame. The lab page presents title, objectives, The Big
Picture (no outcomes), Predict First (a widget that hides its answer until
the cadet commits), and one beat per procedure block, at most `LAB_BEATS`
(10), and teaches nothing. The packet is lean: one submission in three parts,
**Predict, Measure, Analyze**, with predicted beside measured and two or
three open analysis prompts, and only the few measured cells those prompts use (Neil, 2026-11-21: too many "measure this" cells and they "miss the forest for the trees"); no problem invents a person or a reading; page 1 shows the procedure at a glance, one line per block, so the packet reads on its own, and the documentation statement closes the last page (Neil, 2026-11-22). Never
"bench" where a cadet reads it. A provided block (gr-adsb, gr-hdradio, any
out-of-tree or library block) is taught only to what to expect. Details,
what 448 keeps of its own (the public packet sources and `\keysol`), and the
labs still to rework are in `project/ROADMAP.md`, "Labs follow 444's lab
rules"; the wording rules are VOICE.md 27-43.

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
   `xvfb-run`, and use that screenshot on the page. Pass `--size WxH` for a
   window with more than one row of plots; the script points ALSA at its null
   device, so a flowgraph with an Audio Sink runs too. Screenshot GRC's canvas
   with `scripts/grc/grc_canvas.sh file.grc out.png [WxH]`. A flowgraph that
   needs an SDR is compiled only; say so in the PR. A figure that stands in
   for a real capture is labeled "Simulated" on the figure itself.

**The PlutoSDR is the radio and GNU Radio is the tool** (Neil, 2026-10-29).
Every radio path is a flowgraph with a PlutoSDR Source or Sink; the Plutos
run in extended-frequency mode (70 MHz to 6 GHz). Where GNU Radio has a module
for a signal (gr-adsb in radioconda), use it. Every cadet is issued a Pluto,
and lessons are written for it alone (no HackRF or PHASER); an RTL-SDR,
SDR Flex, and GQRX are optional extras at most, and URH is out. A signal the course generates is
recorded or sent at 915 MHz (cable or low-power over the air), never on its
real frequency. See
`project/ROADMAP.md`, "How Neil teaches it".

Recordings a cadet downloads or makes are **SigMF** (`.sigmf-data` plus
`.sigmf-meta`), the preferred data format (Neil, 2026-10-23); see
`project/ROADMAP.md`, "Settled".

The GNU Radio bindings are built for `/usr/bin/python3.12`; call `grcc` and the
scripts through it, not through whatever `python3` is first on `PATH`.

## Public repo

This repo is **public**. Assessments, the midterm and its keys, grades, and lab
KEY PDFs live in the private `livethisdream/ECE448-faculty` (lab keys under
`lab-keys/`), never here. Lab-packet LaTeX sources are here (444 keeps its
own private), and the retired practice sets' SOLUTIONS PDFs stay published,
unlinked; a lab's KEY PDF is built locally and never committed. `.gitignore` blocks the usual names, but
check every PDF before adding it.

American spelling everywhere. No thin spaces. "GNU Radio", two words. Never
MATLAB for anything a cadet runs.
