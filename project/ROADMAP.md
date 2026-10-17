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

- **mPSK is its own lesson** (L9, about two periods), using the GNU Radio
  tutorial in `ECE448-faculty/L19_MPSK`. It wasn't on the 2025 schedule.

- **Teach it the way ECE 444 is taught**: same site, shell, voice, and checks.
  Keep L01 and the decisions in `ECE448_PROJECT.md`. Spring 2027.
- **Use the Spring 2025 lesson content, numbered by topic** (the ECE 444
  rule: lessons are topics, not periods). Periods that repeated a topic in
  2025 merge into one lesson. Flex days, project days, and the midterm stay
  on the calendar and don't get lesson numbers. The 7-module list now in
  `book/syllabus.md` was never taught and will be replaced.
- **The 2025 per-signal projects become ECE 444-style lab packets.** Each
  packet is a child page `LNN-lab-<slug>` titled "LNN Lab — <Topic>". It has
  three parts (Pre-Lab, Bench, Writeup) and one submission, which is one
  Gradescope assignment.
- **Grades use the 2025 weights**: Final Project 40%, Projects (labs) 25%,
  Engagement 20%, Midterm 15%.
- **Write new two-level objectives** ("I can…", numbered module.N) to match
  the lesson list. Neil reviews them before anything is scaffolded.

## Draft lesson list (awaiting Neil's sign-off)

| Module | Lessons and labs |
| :-- | :-- |
| 1 · Link & Signal Foundations | L1 Course Introduction · L2 Noise Figure and Link Budget · L3 Signal Space |
| 2 · Digital Modulation in GNU Radio | L4 PAM Theory · L5 ASCII over PAM → L5 Lab PAM Link · L6 Out-of-Tree Modules and Custom Blocks → L6 Lab Custom Block |
| 3 · Waveforms (midterm after L10) | L7 CW → L7 Lab · L8 DTMF → L8 Lab · L9 mPSK (about 2 periods) · L10 Frequency Hopping (Tx/Rx) |
| 4 · Real-World Signals + Final Project | L11 RF Reverse Engineering (GQRX, URH, remotes) → L11 Lab · L12 ADS-B · L13 AIS → L12–L13 Lab ADS-B/AIS · L14 Broadcast FM and RDS · L15 HD Radio · L16 QAM and OFDM |

## Draft objectives (awaiting Neil's sign-off)

- **1.1** I can cascade noise figure through a receiver chain.
- **1.2** I can compute a link budget and predict received SNR.
- **1.3** I can place a modulation in signal space and draw its decision regions.
- **2.1** I can relate pulse shape, symbol rate, and bandwidth for PAM.
- **2.2** I can build a GNU Radio PAM link that sends ASCII text end to end.
- **2.3** I can recover symbol timing with a matched filter.
- **2.4** I can write a custom Python block and package it as an OOT module.
- **3.1** I can generate and decode CW.
- **3.2** I can detect DTMF tones (Goertzel).
- **3.3** I can build a BPSK, QPSK, and 8PSK modem in GNU Radio, recover carrier and symbol timing, and check the constellation against theory.
- **3.4** I can build a frequency-hopping transmitter and receiver that stay in sync.
- **4.1** I can identify an unknown signal's modulation, symbol rate, and framing, and replay it.
- **4.2** I can receive and decode ADS-B and AIS.
- **4.3** I can demodulate broadcast FM and RDS and explain how HD Radio's OFDM sidebands are laid out.
- **4.4** I can explain QAM and OFDM.
- **4.5** I can scope, build, and defend a final project against my own success criteria.

## Open

- Sign-off on the lesson list and objectives above.
- **mPSK lab**: give L9 a lab built from the `ECE448-faculty/L19_MPSK`
  GNU Radio tutorial, or keep it lecture plus demo?
- **2025 "Theory Project"** (due at period 9): turn it into the L2–L3
  practice set, or make it a lab packet?
- **FHSS**: give L10 a lab, or keep it lecture plus demo?
- Spring 2027 meeting periods and calendar dates.

## Next

1. Port ECE 444's shell, scaffolder, and checks into `ece448`, keeping L01.
2. Rebuild the legacy slides as frame lessons, one lesson at a time, in
   teaching order.
