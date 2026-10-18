# ECE 448 roadmap

Last updated 2026-10-17. Read with ECE 444's `project/ROADMAP.md`, whose
working rules apply here.

## Course philosophy (Neil, 2026-10-17)

**This is an applications course. Teach only enough theory to get by.**

Every lesson exists to get a real signal built, received, or decoded in
GNU Radio. Theory earns a place only when the application needs it, and only
as much as the application needs. Write lesson pages, slides, practice sets,
and lab packets with these rules in mind:

- **Start with the signal, not the math.** Open with what the cadet will
  build or decode and why it matters. Bring in theory when the flowgraph
  needs it.
- **No derivations for their own sake.** State the result, say what it means
  for the flowgraph (a block parameter, a sample rate, a filter length), and
  move on. ECE 447 is the course that derives things.
- **Do more than you explain.** Most of each period goes to flowgraphs,
  captures, and live demos. A slide of equations needs a demo or a block
  diagram right after it.
- **Assess what cadets can build.** Labs, the midterm, and the final project
  grade working flowgraphs and decoded signals. Proofs are not graded.

This rule is meant to stand out. ECE 444's conventions (shell, voice,
budgets, checks) still apply. Where 444 would put a derivation on screen,
448 puts a flowgraph there.

## Settled (Neil, 2026-10-17)

- **Seven modules approved** (lesson list below).
- **The midterm is a fox hunt plus a CTF.**
- **Drop the 2025 "Theory Project"** (nobody remembers what it covered).
  L2–L3 get ordinary practice sets, like every other lesson.

- **mPSK is its own lesson** (L15, about two periods), using the GNU Radio
  tutorial in `ECE448-faculty/L19_MPSK`. It wasn't on the 2025 schedule.

- **Teach it the way ECE 444 is taught**: same site, shell, voice, and checks.
  Keep L01 and the decisions in `ECE448_PROJECT.md`. Spring 2027.
- **Keep the old site's seven modules, and fit in every 2025 lesson.**
  Lessons are numbered by topic (the ECE 444 rule: lessons are topics, not
  periods), so periods that repeat a topic merge into one lesson. Flex days,
  project days, and the midterm are calendar entries, not numbered lessons.
- **The 2025 per-signal projects become ECE 444-style lab packets.** Each
  packet is a child page `LNN-lab-<slug>` titled "LNN Lab — <Topic>". It has
  three parts (Pre-Lab, Bench, Writeup) and one submission, which is one
  Gradescope assignment.
- **Grades use the 2025 weights**: Final Project 40%, Projects (labs) 25%,
  Engagement 20%, Midterm 15%.
- **Objectives** are the two-level "I can…" list (module.N). Neil reviews
  them before anything is scaffolded.

## Lesson list (approved by Neil, 2026-10-17)

Neil, 2026-10-17: keep the seven-module structure from the old site
syllabus, and make sure it holds every lesson from the 2025 list. Lessons
are numbered by topic. Each "(LAB)" period in the old schedule becomes a
lab under its lesson.

| Module | Lessons and labs |
| :-- | :-- |
| 1 · Foundations of Detection & Link Budgets | L1 Course Introduction · L2 Noise Figure and Link Budget · L3 Signal Space |
| 2 · SDR & GNU Radio Foundations | L4 SDR Introduction · L5 GNU Radio Introduction → L5 Lab |
| 3 · Analog Modulation | L6 AM Simulation → L6 Lab · L7 AM and FM Receivers (incl. broadcast FM and RDS) → L7 Lab |
| 4 · Digital Modulation | L8 FSK → L8 Lab · L9 PAM Theory · L10 ASCII over PAM → L10 Lab |
| 5 · Custom Blocks & Midterm | L11 Out-of-Tree Modules and Custom Blocks → L11 Lab · Midterm (fox hunt + CTF, calendar) |
| 6 · Waveform Applications & RF Reverse Engineering | L12 CW → L12 Lab · L13 DTMF → L13 Lab · L14 HD Radio → L14 Lab · L15 mPSK (about 2 periods) → L15 Lab · L16 Frequency Hopping → L16 Lab · L17 RF Reverse Engineering (GQRX, URH, remotes) → L17 Lab · L18 ADS-B · L19 AIS → L18–L19 Lab ADS-B/AIS |
| 7 · Final Project | L20 QAM and OFDM · project days and presentations (calendar) |

## Objectives

Use the seven-module objectives already in `book/syllabus.md` (1.1–7.4),
since they follow this structure. Two changes:

- **3.3** also covers RDS.
- **6.4** (mPSK) adds carrier and symbol-timing recovery.
- **5.3–5.4** become the midterm: a fox hunt and a CTF.

## Open

- Spring 2027 meeting periods and calendar dates.

## Status (2026-10-17)

- **Shell ported.** The site runs on ECE 444's shell (by way of ECE 343):
  frame pages, the bottom bar, the verify scripts, and the voice and review
  skills. `scripts/scaffold_lessons.py` holds the manifest. All 20 lessons,
  13 labs, the midterm, and the final project have generated pages, linking
  their legacy slides where those exist. `jupyter-book build --all` runs with
  no warnings, and `check_shell`, `check_frames`, and `check_bar` pass.
- **L01 converted** to a frame page. Its deck now loads its images, and its
  schedule matches the new lesson list.
- The syllabus, landing page, and materials page are rewritten for the seven
  modules, the 2025 weights, the lab packets, and the fox-hunt-and-CTF
  midterm. The applications-first philosophy is stated in the syllabus and on
  the landing page.

## Trial lessons (master thread, before lesson threads start)

- **L2 done (2026-10-18).** Frame page (18/20 beats), deck (19 slides), three
  figures from `scripts/graphics/l02_figures.py`, the `link-budget.html`
  widget (drone, Wi-Fi, and GPS presets), and a 5-question practice set.
  `mech_check.sh 02 noise-figure-link-budget` passes with 0 failures.
- **L3 done (2026-10-18).** Frame page (16/20 beats), deck (17 slides), five
  figures from `scripts/graphics/l03_figures.py`, the
  `constellation-explorer.html` widget (live symbols through noise, measured
  against predicted BER), and a 5-question practice set. It closes L2's open
  question: the drone's 14 dB is QPSK at $10^{-5}$ plus a real-receiver
  allowance. `mech_check.sh 03 signal-space` passes with 0 failures.
- **Phone-width math (2026-10-18).** Neil found L2 equations scrolling on his
  phone. `scripts/verify/check_math.py` now gates every lesson at 320, 360,
  and 390 px, and it caught one L3 equation before it shipped.
- **L5 and the L5 Lab done (2026-10-18).** The first flowgraph lesson: two
  `.grc` files and a Python IQ script under `book/extras/grc/`, real GRC and
  QT GUI screenshots taken from GNU Radio 3.10.9 running under Xvfb, a
  sampling-wheel widget for complex sampling and aliasing, a simulated FM-band
  figure labeled as simulated, a short practice set, and the first lab packet
  (Pre-Lab, Bench, Writeup). The FM flowgraph needs an RTL-SDR, so it is
  compiled but not run. `mech_check.sh 05 gnu-radio-intro` passes.
- **Beat budgets.** `scripts/verify/budgets.py` had carried ECE 444's
  per-lesson exceptions, which let 448's L05-L14 run to 30 beats. They are
  gone; every 448 lesson is held to 20.
- What L2 settled for the lesson threads:
  - The practice harness is in `latex/` (ported from 444). It needs
    `livethisdream/latex-tools` attached and TeX Live installed (the session
    hook does both).
  - A lesson that serves two objectives puts one `Learning Objective M.N:`
    line per objective in its practice banner, which is what `mech_check`
    looks for.
  - Every lesson ends its content with an application frame that says how
    the idea shows up on the SDR (for L2, reading SNR off a dBFS display).
    This is the applications-first rule made concrete.
  - Once a lesson is converted, its manifest entry gets `[]` for decks. The
    legacy PDF stays listed on the materials page.

## Lesson threads (from L6 on)

The trial is done. From L6 on, each lesson is its own thread, and this thread
is the Integrator, as in ECE 444 (`project/ROADMAP.md` sections 1-3 there).

**A lesson thread for lesson NN may edit only:**

| What | Path |
| :-- | :-- |
| the lesson page and its lab page | `book/moduleMM/LNN-*/index.md` |
| its deck | `book/extras/slides/LNN-*.md` and the generated `.html` |
| its practice set | `latex/ECE448_Practice_LNN.tex` and its PDFs in `book/extras/practice/` |
| its lab packet | `latex/ECE448_Lab_LNN_*.tex` and the blank PDF in `book/extras/labs/`; the KEY to `ECE448-faculty/lab-keys/` |
| its figures | `book/extras/{viz/img,slides/fig,slides/img/NN-*}/LNN-*` and `scripts/graphics/lNN_figures.py` |
| its flowgraphs and scripts | `book/extras/grc/LNN-*` |
| a widget only it uses | `book/extras/viz/<widget>.html` |

Everything else, including the manifest, the syllabus, the module pages, the
shell, `scripts/verify/`, and this file, belongs to the Integrator; a lesson
thread lists what it needs under "For the Integrator" in its PR body.

**Every lesson PR carries, before it opens:**

1. A frame page within 20 beats and 40 words a frame, opening from the
   signal and closing with an application frame on the SDR or in GNU Radio.
2. The deck, the practice set (one `Learning Objective M.N:` line per
   objective served), and, where the lesson has a lab, the packet.
3. Every flowgraph normalized, compiled, and, if it needs no hardware, run
   for its screenshots (CLAUDE.md, "Flowgraphs").
4. `mech_check.sh NN <slug>` with 0 failures, which includes the phone-math
   gate, and `check_grc.py`, `check_shell.py`, and `check_frames.py` passing.
5. A voice pass against `VOICE.md`: no fragments, no money metaphors, no
   passive tells, American spelling.

**Branches.** Each thread branches from current `main` as
`claude/lNN-<slug>`, opens one PR, and does not merge it.

## Next

1. Rebuild the legacy slides as frame lessons, one lesson at a time, in
   teaching order, starting with L2. Theory stays minimal (see Course
   philosophy above).
2. Lab packets, one per lab, before each lab runs.
3. Midterm (fox hunt and CTF) and final project packets, in
   `ECE448-faculty` where they carry answers.
