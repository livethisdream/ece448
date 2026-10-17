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

## Draft lesson list (awaiting Neil's sign-off)

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
| 5 · Custom Blocks & Midterm | L11 Out-of-Tree Modules and Custom Blocks → L11 Lab · Midterm (GNU Radio + fox hunt, calendar) |
| 6 · Waveform Applications & RF Reverse Engineering | L12 CW → L12 Lab · L13 DTMF → L13 Lab · L14 HD Radio → L14 Lab · L15 mPSK (about 2 periods) → L15 Lab · L16 Frequency Hopping → L16 Lab · L17 RF Reverse Engineering (GQRX, URH, remotes) → L17 Lab · L18 ADS-B · L19 AIS → L18–L19 Lab ADS-B/AIS |
| 7 · Final Project | L20 QAM and OFDM · project days and presentations (calendar) |

## Objectives (awaiting Neil's sign-off)

Use the seven-module objectives already in `book/syllabus.md` (1.1–7.4),
since they follow this structure. Two changes:

- **3.3** also covers RDS.
- **6.4** (mPSK) adds carrier and symbol-timing recovery.

## Open

- Sign-off on the lesson list and objectives above.
- **2025 "Theory Project"** (due at period 9): turn it into the L2–L3
  practice set, or make it a lab packet?
- Midterm format: the old site's GNU Radio plus fox hunt, or the 2025
  in-class portion plus a practical?
- Spring 2027 meeting periods and calendar dates.

## Next

1. Port ECE 444's shell, scaffolder, and checks into `ece448`, keeping L01.
2. Rebuild the legacy slides as frame lessons, one lesson at a time, in
   teaching order.
