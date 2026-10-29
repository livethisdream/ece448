# ECE 448 roadmap

Last updated 2026-10-17. Read with ECE 444's `project/ROADMAP.md`, whose
working rules apply here.

## Course philosophy (Neil, 2026-10-17)

**This is an applications course. Teach only enough theory to get by.**

**Watch what the signal does; don't calculate it** (Neil, 2026-10-21). We use
real radios to observe effects and, when it helps, tie them back to theory.
This is the line the landing page, syllabus, and Lesson 1 use.

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

### Sources and noise (Neil, 2026-10-21)

**The point is to build flowgraphs and modulate and demodulate signals,
not to calculate BER or probability of error.** About half the class has no
communications background. The rules below override anything in a lesson
written before this date.

- **Sources, in order.** (1) Neil's 2025 slides for the lesson, in
  `book/extras/legacy/`; they are the primary source, and a lesson keeps
  their topics and order. (2) The GNU Radio wiki and its tutorials
  (wiki.gnuradio.org). (3) PySDR (pysdr.org). Material from none of these
  stays out unless a flowgraph needs it to set a block parameter.
- **Noise is something to watch, not to calculate.** Show what happens as
  noise goes up: the constellation spreads, the eye closes, the text breaks,
  the audio hisses. No Eb/N0, no BER or Pe formulas, no Q-functions, no
  error-rate curves against theory. The one noise number the course uses is
  SNR as the SDR display shows it (Lesson 2), and only where a slider or a
  display needs it.
- **Labs observe; they do not predict from formulas.** A Pre-Lab may ask
  for a block setting (a sample rate, a decimation, a filter cutoff) or a
  quick arithmetic step a flowgraph needs. It does not ask cadets to predict
  error rates, SNR tables, or loop limits. Bench parts turn a slider and
  record what they see; Writeup questions ask what changed and why, in
  words.
- **Practice sets** follow the same rule: block parameters, reading a
  display, choosing a setting, and explaining what a change does.
- **Deckless lessons** (L5, L8, L11, L12, L15, L16 and later ones without a
  2025 deck) follow the GNU Radio tutorials and PySDR for scope, and stay at
  the level of the lessons that do have decks.

### How Neil teaches it (2026-10-21)

Neil taught 2025 by walking through the GNU Radio tutorials
(wiki.gnuradio.org) with GNU Radio Companion or GQRX on screen the whole
period. That is why several lessons have no 2025 deck: the tutorials were
the material. A lesson is a guided walkthrough, not a chapter.

- **Name the tutorial.** Each lesson lists the GNU Radio wiki tutorial
  pages it follows (and PySDR chapters, if any) and follows their sequence.
  Where a lesson has a 2025 deck, the deck sets the topics and the tutorials
  supply the hands-on steps.
- **The page is a demo script.** Frames walk through what to build, run, and
  watch in GRC or GQRX, in the order Neil does it live. Explanation is the
  minimum needed to know what to look at.
- **SDR Flex is the primary explore tool** (Neil, 2026-10-21). Neil's own
  `livethisdream/sdr-flex` starts at the spectrum and builds a GNU Radio
  flowgraph behind each drag, demodulator, and decoder, so a lesson can show
  cadets the flowgraph they just made. Use it for receive-and-explore steps
  (a band, an unknown signal, HD Radio, ADS-B, AIS, L17's reverse
  engineering).
  - **Which version.** The full version (Docker image, or the server against
    the cadet's own GNU Radio) carries the external decoders (rtl_433,
    dump1090, direwolf, and others) and live radios. The browser version
    (livethisdream.github.io/sdr-flex) needs no install but lacks those
    decoders; use it only for steps that work on its example captures or
    the client-side decoders.
  - **Write explore steps as actions** (tune, select a signal, demodulate,
    attach a decoder), so they read the same in SDR Flex and GQRX. GQRX is
    the named fallback.
  - **Go/no-go: first week of January 2027.** Neil is testing it on macOS
    and Windows (outside WSL it is untested, and the image is amd64 only).
    Until then no lab *requires* SDR Flex; after it, the Integrator makes
    SDR Flex the only named tool or leaves GQRX as written.

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

- **SigMF is the preferred data format** (Neil, 2026-10-23). A recording a
  cadet downloads, or one a lab has them make, is a SigMF pair: the samples in
  `<name>.sigmf-data` and the sample rate, center frequency, and datatype in
  `<name>.sigmf-meta`. The data file is raw samples, so a File Source reads it
  with the type the meta file names. To convert: L14's handed-out `.cu8`
  captures, and the L5 Lab recording, which the lesson already says to save
  as SigMF.

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
| 6 · Waveform Applications & RF Reverse Engineering | L12 CW → L12 Lab · L13 DTMF → L13 Lab · L14 HD Radio → L14 Lab · L15 mPSK (about 2 periods) → L15 Lab · L16 Frequency Hopping → L16 Lab · L17 RF Reverse Engineering (PlutoSDR, URH, remotes) → L17 Lab · L18 ADS-B · L19 AIS → L18–L19 Lab ADS-B/AIS |
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

## Lesson threads, first batch (2026-10-19)

- **L6, L8, and L9 done** in three overnight lesson threads (PRs #9, #11,
  #10), merged together after one Integrator review round. Each thread passed
  its own checklist, and an independent review still found about a dozen
  items per lesson, including one real technical error apiece (L6's
  overmodulation threshold, L8's claim about the I trace, L9's matched-filter
  gain). **Keep the Integrator review pass for every batch:** a reviewer per
  lesson recomputes every number and re-runs the flowgraphs before anything
  merges.
- **Lab KEYs.** Lesson threads cannot attach `ECE448-faculty`. The Integrator
  builds each lab's KEY from the reviewed head and opens the faculty PR, which
  merges with the lesson PR.
- **Tooling the threads asked for**, now in `scripts/grc/`: `grc_shot.py`
  takes `--size WxH`, finds a flowgraph's embedded Python blocks, and runs
  Audio Sinks on ALSA's null device; `grc_canvas.sh` sets GRC's window size
  in `grc.conf`, because bare Xvfb cannot resize it.
- L6 and L9 now have `[]` for decks; their legacy PDFs stay on the materials
  page.

## Lesson threads, second batch (2026-10-19)

- **L4, L7, and L10 done** (PRs #13, #14, #16). The threads now ran their own
  reviewer before opening a PR, and the Integrator review still found real
  errors: L4 quoted the PlutoSDR's burst rate as a streaming rate and claimed
  one receiver chain for all four radios; L7 had the de-emphasis mismatch
  backwards and no build-it-yourself part in its lab; L10 cabled the
  PlutoSDR's TX straight to its RX with no attenuator and leaked its pre-lab
  answers onto the lesson page. Keep both review passes.
- **Lab rules from this batch:** every lab has a build-from-an-empty-canvas
  part; the lesson page never prints the numbers its lab asks cadets to
  predict; any TX-to-RX cable carries an inline attenuator; anything only
  simulated says so.
- **Bench checks for Neil** before the labs run: the L7 receivers on a live
  station, and the L10 PlutoSDR cable link across 30-89 dB TX attenuation,
  including whether zero-IF DC tracking biases long runs of zeros.
- **gr-rds** is in the session hook; L7's RDS flowgraphs need it.

## Lesson threads, third batch (2026-10-20)

- **L11, L12, and L13 done** (PRs #18, #20, #19). Each thread ran two or three
  reviewers of its own, and the Integrator review still found blocking items:
  L11 called 433.92 MHz an ISM band and printed Pre-Lab answers; L12's
  PlutoSDR path would have reached the receiver about 40 dB below what its
  controls could show; L13 shipped a 6.9 MB vector spectrogram and a public
  script that printed the KEY's tables.
- **More rules:** a figure with more than a few thousand marks is rasterized
  (`rasterized=True`, about 150 dpi) and stays under about 100 KB; a
  downloadable script never prints a lab's answers; a PlutoSDR flowgraph
  that runs through the 30 dB pad carries an AGC, as L10's and L12's do.
- **Lab keys and reference code** now live in `ECE448-faculty`:
  `lab-keys/` for the KEY PDFs and `lab-solutions/` for code a cadet writes
  (L11's Key Timer) or a full script whose public copy was trimmed (L13).
- **L11 Windows route:** WSL2 with Ubuntu 24.04 first, then an Embedded
  Python Block, then a teammate's laptop. Open for Neil.
- **Bench checks for Neil:** L12's PlutoSDR cable link across 30-89 dB, and
  L13's microphone flowgraph with a real phone.
- **Next batch:** L14 to L16.

## Lesson threads, fourth batch and fidelity passes (2026-10-21)

- **L14, L15, and L16 done** (PRs #22, #24, #23). Four fidelity passes took L2
  to L13 back to the 2025 slides under "Sources and noise" (PRs #27, #29, #28,
  #26). The site now has no Eb/N0, BER, or Q-function anywhere a cadet sees it.
- **Lab answers are private** (Neil, 2026-10-21). Every lab packet prints its
  answers through `\keysol{<id>}`. The values live in
  `ECE448-faculty/lab-keys/src/*_solutions.tex`, `latex/build_lab.sh` reads
  them through `KEYDIR` (default: a sibling clone of the faculty repo), and a
  KEY build without them stops with an error. `*_solutions.tex` is
  gitignored here. Answers from before the split are still in this repo's git
  history.
- **No public page prints a lab answer.** That covers lesson and lab pages,
  decks, practice sets and their solutions, widgets, and `.grc` descriptions.
  A lab uses inputs of its own, so its answers differ from the lesson's worked
  examples, and lesson demos run at settings the lab does not use. "Expected
  Numbers" frames are gone.
- **Bench checks for Neil:** the KEY values marked as estimates in PR #29
  (L5 to L8, notably L7's click onsets), L15's PlutoSDR link and zero-IF DC
  tracking, and L14 on a live HD station with nrsc5.
- **Settled after the batch** (Neil, 2026-10-29): objective 6.4 drops "verify
  constellation behavior against theory"; the legacy HD Radio deck is the one
  he taught from; the L13 answer left in public history is not worth a new
  capture (regenerate only if L13's lab is reworked for another reason).

## Lesson threads, fifth batch (2026-10-29)

- **L17, L18-L19, and L20 done** (PRs #35, #37, #36). L1-L20 are converted.
- **Simulated signals, real ones where they exist.** L17's demo and lab
  devices are simulated remotes; the lab adds a graded receive-only capture of
  a real remote the cadet owns. ADS-B is live at USAFA; AIS is a simulated
  two-channel recording, because no ships are in range. Every handed-out
  recording is SigMF, and each lab recording comes from a private generator in
  `ECE448-faculty/lab-solutions/` that reproduces it byte for byte.
- **Generators that could transmit say they must not.** 1090 MHz (ADS-B) and
  161.975/162.025 MHz (AIS) carry safety-of-life traffic; their flowgraphs
  write files only, and their descriptions say never to connect a transmitter.
- **Bench checks for Neil:** L17's PlutoSDR-to-SDR cable link and the
  RTL-SDR capture path (1.024 MS/s, URH Samples/Symbol 512); live ADS-B on an
  RTL-SDR; L20's Wi-Fi and LTE steps on a HackRF at 20 MS/s.
- **L17 over-the-air fan demo** (Neil, 2026-10-29): L17 closes with an
  instructor demo that operates the classroom's Hunter fan over the air, at
  very low power and a few meters away, from Neil's own encoder flowgraph
  (`ECE448-faculty/L20_Remotes`). Cadets still transmit only into a cable.
- **Open for Neil:** whether to publish the third-party AIS recording
  ("bebau") from the faculty repo for L19.

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
