# Syllabus

<style>
.lo-table h3 { margin-top: 1.4em; color: #0067b9; font-size: 1.1em; }
.lo-table table { width: 100%; border-collapse: collapse; margin-bottom: 0.6em; font-size: 0.95em; }
.lo-table th { background: #f2f6fb; color: #003a75; text-align: left; border-bottom: 1px solid #cfd8e3; padding: 0.35em 0.6em; }
.lo-table td { border-bottom: 1px solid #eef2f7; padding: 0.4em 0.6em; vertical-align: top; }
.lo-table td:first-child { font-weight: 600; color: #0067b9; text-align: right; width: 3em; white-space: nowrap; font-variant-numeric: tabular-nums; }
</style>

<div style="float:right;margin:0 0 1em 1.5em;text-align:center;max-width:180px;">
<img src="/assetsintro.mdimg/syllabus-qr.png" alt="QR code to this syllabus" style="width:160px;height:160px;">
<div style="font-size:0.85em;color:#666;margin-top:0.3em;">Scan for the live syllabus</div>
</div>

## Course

**ECE 448 — Introduction to Software Defined Radios**
Spring 2026

## Instructor

- **Dr. Neil Rogers**
- Office hours: **by appointment only**
- Phone: **937-361-2545**

## Meeting time & location

- See USAFA class schedule for room assignment

## Course overview

Have you ever thought about the sheer number of wireless signals surrounding
you in the modern world? From cell phones to WiFi to Bluetooth — wireless
communications enable just about everything you do. This course looks at those
signals — how they're generated, transmitted, and received — through the lens
of **Software Defined Radios (SDRs)**.

ECE 447 (Communications Theory) covers the fundamental principles of many
methods of communication. **This course focuses on the applied side** of
wireless communications: introducing SDRs, familiarizing you with the benefits
and limitations of various SDR platforms and, more importantly, the various
software packages used to interact with them. You'll spend most of your time
in **GNURadio**, building real flowgraphs against real signals. The course
culminates in a substantial, **self-defined final project** that integrates
every concept in the course into a specific wireless application of your
choosing.

## Course goals

By the end of this course, you will be able to:

1. Make use of modern software applications to simulate, receive, and transmit
   signals using modern modulation and encoding techniques.
2. Describe the principles of basic signal-processing techniques, such as
   filtering, interpolation, decimation, and matched filtering.
3. Implement basic signal-processing techniques in the presence of noise and
   other non-idealities.
4. Reverse-engineer, decode, and characterize an unknown RF signal captured
   off the air.
5. Define, execute, and defend a self-directed SDR project against your own
   engineering success criteria.

## Learning objectives

The course is organized around specific, testable learning objectives (LOs).
Each LO is assessed at least once. Mastery of every LO earns an "A" on the
mastery-based portion of the grade.

<div class="lo-table" markdown="1">

### Module 1 — Foundations of Detection & Link Budgets

| LO | Description |
| :-: | :- |
| 1.1 | I can define noise figure and cascade it through a receiver chain to predict system noise performance. |
| 1.2 | I can compute a link budget and predict received SNR for a specified geometry, transmitter, and antenna configuration. |
| 1.3 | I can describe signal-space concepts (basis functions, constellations, decision regions) and apply them to a digital modulation scheme. |

### Module 2 — SDR & GNURadio Foundations

| LO | Description |
| :-: | :- |
| 2.1 | I can describe what a Software Defined Radio is, contrast it with a traditional hardware radio, and identify the SDR platforms used in this course (RTL-SDR, HackRF, PlutoSDR, ADALM-PHASER). |
| 2.2 | I can identify the roles of the RF frontend, ADC/DAC, and host in an SDR signal chain and describe sample-rate, bandwidth, and dynamic-range trade-offs. |
| 2.3 | I can install GNURadio and use GNU Radio Companion (GRC) to build, inspect, and run a basic flowgraph. |
| 2.4 | I can capture a real RF signal using an SDR and interpret its time- and frequency-domain representations. |

### Module 3 — Analog Modulation

| LO | Description |
| :-: | :- |
| 3.1 | I can describe DSB-AM, DSB-SC, and SSB and identify each on a spectrum. |
| 3.2 | I can implement an AM modulator and demodulator in GNURadio and verify demodulated audio against the source. |
| 3.3 | I can implement an FM receiver in GNURadio and demodulate a live broadcast FM signal. |
| 3.4 | I can explain and demonstrate the trade-off between bandwidth and noise performance for AM vs. FM. |

### Module 4 — Digital Modulation

| LO | Description |
| :-: | :- |
| 4.1 | I can describe FSK modulation and implement an FSK transmitter and receiver in GNURadio. |
| 4.2 | I can describe PAM theory and identify the pulse-shaping, symbol-rate, and bandwidth trade-offs. |
| 4.3 | I can apply matched filtering and symbol-timing recovery to a received PAM signal. |
| 4.4 | I can implement a PAM link that transmits and receives ASCII text end-to-end. |

### Module 5 — Custom Blocks & Midterm

| LO | Description |
| :-: | :- |
| 5.1 | I can create a GNURadio out-of-tree (OOT) module and add a custom Python block to it. |
| 5.2 | I can implement a custom signal-processing block from scratch and integrate it into a GNURadio flowgraph. |
| 5.3 | I can perform a direction-finding fox hunt using an SDR and a directional antenna. |
| 5.4 | I can integrate detection theory, analog modulation, digital modulation, GNURadio flowgraph construction, and custom-block development into a graded practical exercise. |

### Module 6 — Waveform Applications & RF Reverse Engineering

| LO | Description |
| :-: | :- |
| 6.1 | I can transmit and receive CW (Morse) using GNURadio and decode a received CW stream. |
| 6.2 | I can decode DTMF tones from a captured audio signal. |
| 6.3 | I can describe how HD Radio works and demodulate an HD Radio signal. |
| 6.4 | I can implement an mPSK modulator and demodulator (BPSK, QPSK, 8PSK) and verify constellation behavior against theory. |
| 6.5 | I can implement FHSS transmission and reception, including hop-sequence synchronization. |
| 6.6 | I can perform RF reverse engineering on an unknown signal — identify its modulation, symbol rate, and payload structure. |
| 6.7 | I can receive and decode ADS-B messages from aircraft transponders. |
| 6.8 | I can receive and decode AIS messages from marine vessels. |

### Module 7 — Final Project

| LO | Description |
| :-: | :- |
| 7.1 | I can describe QAM and OFDM and identify use cases for each. |
| 7.2 | I can define the scope, objectives, and measurable success criteria for a self-directed SDR project. |
| 7.3 | I can research, design, and implement a wireless communication system using an SDR and GNURadio. |
| 7.4 | I can present my project results in a professional-grade report and live demonstration and defend engineering trade-offs against my own stated success criteria. |

</div>

## Grading

Grades in this course are based on **mastery** of learning objectives, not
single-attempt performance. Three components make up your final grade:

| Component | Weight |
| :- | :-: |
| Engagement | 25% |
| Midterm activity | 35% |
| Final project | 40% |

### Mastery-based assessment

The Midterm Activity and Final Project are assessed against the learning
objectives on a **binary scale**:

- **1** — you have mastered the objective.
- **0** — you have not *yet* mastered the objective.

You may **revise your work** based on the detailed feedback provided, unless no
effort is evident (the assessment is blank, incomplete, or significantly late).
In those cases, a retake may be earned by giving a **5-minute technical
presentation** during class on a relevant, pre-approved topic.

The bar is simple: I want you to *learn this material*, and I would rather you
learn it late than not at all.

### Self-defined success criteria (Final Project)

The Final Project is intentionally open-ended. Instead of being graded against
a one-size-fits-all rubric, you will **write your own success criteria** as
part of the Project Proposal (due at Lesson 23). Those criteria — reviewed and
signed off by me before you build — become the rubric your project is graded
against. Craft them ambitiously but honestly: overshooting scope and missing is
harder to defend than a tight, well-executed scope you cleared cleanly.

### Engagement credits (EC)

Engagement is worth **25% of your final grade** and rewards active participation
in the course rather than single-attempt performance on graded work. You may
earn engagement points in the following ways:

- **Module homework.** Each module ships with a small project keyed to that
  module's learning objectives, **due 1–2 weeks after the module wraps up**.
  These are your reps — not graded for correctness, but graded for a genuine,
  documented attempt at every LO the module covers.
- **Attending Extra Instruction (EI).** Book time with me and come prepared with
  specific questions or a concept you want to work through.
- **Lab prep and lab writeup engagement.** Coming to lab prepared with a
  pre-lab plan, and turning in a thoughtful writeup, both count.
- **Research paper (up to 5 EC).** You may complete a research paper on a
  relevant, pre-approved topic — an SDR platform, a modulation scheme, a
  reverse-engineering case study, or a mission application. Must be in **IEEE
  format**, contain at least **3 scholarly references**, and adhere to the
  submission standards in this syllabus.
- **Course improvement contributions.** Spotted a bug in a lab writeup, an
  unclear slide, a broken link on the course site? Tell me and it counts.

Engagement is capped at 25%; extra credit does not roll over.

### Grade scale

| F | D | C− | C | C+ | B− | B | B+ | A− | A |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| ≤ 60% | 70% | 73% | 77% | 80% | 83% | 87% | 90% | 93% | 100% |

## Projects

Two graded projects anchor the course:

- **Midterm Activity — GNURadio + Fox Hunt.** Runs at Lesson 20. A hands-on
  practical that combines flowgraph construction, custom-block development,
  and a direction-finding fox hunt against a hidden transmitter on campus.
  Assessed against Module 1–5 learning objectives.
- **Final Project — Self-Defined SDR Application.** Introduced at Lesson 16;
  proposal due at Lesson 23; background research due at Lesson 28; prototype
  description due at Lesson 38; final report and live demonstration due at
  Lesson 40. You choose the wireless application; you write the success
  criteria; you defend the result.

## Course policies

### Instructor philosophy

You have chosen one of the most difficult majors at USAFA — I applaud your
commitment. My role in your journey is to enable your success. My intent is to
do this by creating an inclusive environment and putting in the work *with*
you. If you work hard and communicate with me, I will do everything in my power
to make sure you succeed.

Have questions? **Ask** — there is genuinely no such thing as a stupid question.
Have concerns, especially about your learning environment? Let's talk. You face
many challenges here at USAFA; I am in your corner — so let's go.

### 1. Absences

Communicate with me **beforehand** in the event of an absence. If you will miss
any graded event due to a scheduled absence (SCA, sport team trip, scheduled
medical procedure), a makeup plan should be in place **before** the absence
occurs. In the event of bedrest, notify me **via email** as soon as possible
after receiving approval.

### 2. Academic honor

Your honor is extremely important. The course's academic security policies are
designed to help you succeed in meeting academic requirements while practicing
the honorable behavior our country rightfully demands of its military. Do not
compromise your integrity by violating academic security or by taking unfair
advantage of your classmates.

### 3. Assignment availability & late work

All work will be available through Teams, the course website, and/or Gradescope.
A **24-hour grace period** is generally observed, after which **25% of available
points will be deducted for each calendar day** the graded assignment is late.
I may waive part or all of this penalty for legitimate, pre-coordinated
extenuating circumstances.

### 4. Authorized resources

The midterm activity and final project have their own resource policies
described in their assignment packets. When electronic devices are authorized
for viewing reference materials during any graded event, use of **internet,
Teams, and generative AI tools is not allowed** unless explicitly permitted.

### 5. Collaboration

**Collaboration (not copying)** on skill checkpoints and assessments is highly
encouraged, unless your instructor provides direction otherwise. A good litmus
test: you must be able to **explain every step** on your submitted work.
If you can't, it's copying, not collaboration. All help received on graded work
must be documented per the documentation policy below.

Collaboration is allowed on the Final Project, but must be **explicitly and
thoroughly documented** per the Dean's documentation policy.

### 6. Documentation

In accordance with the Dean's policy for documentation, all ECE assignments
must have a documentation statement. For team projects, you are not required
to document collaboration within your own team. The statement should be
clearly identified with the word **"Documentation."** If you did not
collaborate, write **"Documentation: None."** Assignments without a
documentation statement are incomplete and may be returned for completion; a
1-day-late penalty (up to 25%) may be assessed in lieu of returning the
assignment.

### 7. Extra Instruction (EI)

EI is one of the best and easiest ways to succeed in this class. Walk-in EI is
not generally available — please book with me directly.

### 8. Generative AI

I am **pro-AI**; however, I expect you to use generative AI platforms
(ChatGPT, Copilot, Claude, etc.) as a **tool**, not as a replacement for your
own learning. It will be very clear if you are using AI irresponsibly: these
tools frequently generate incorrect solutions to the DSP and RF problems
you'll encounter here, and often produce GNURadio flowgraphs that don't quite
work or don't align with our course conventions. **If you use generative AI on
any assignment, include a documentation statement** as outlined in the
Documentation policy.

### 9. Submission standards

- All homework must be submitted electronically.
- Skill checkpoints and lab writeups should be submitted in **report format**
  with appropriate sections (Introduction, Background, Implementation,
  Results, Discussion). Tailor sections as needed, but include enough detail
  to demonstrate mastery.
- Use engineering units consistently.
- All submissions **MUST BE TYPED** and well-organized unless specifically
  noted. Use of **LaTeX** is encouraged.

## Schedule

Lessons link to notes on the [course home](intro.md).
Labs are marked **LAB**.

### Module 1 — Foundations of Detection & Link Budgets

1. Course Overview & Introduction — what an SDR is, why it matters, course roadmap, live SDR demo
2. Noise Figure & Link Budget
3. Signal Space

### Module 2 — SDR & GNURadio Foundations

4. SDR Introduction — hardware architectures, sample rate, bandwidth, dynamic range
5. GNURadio Intro
6. GNURadio Intro **(LAB)** &nbsp; · &nbsp; **Module 1 HW due**

### Module 3 — Analog Modulation

7. AM Simulation **(LAB)**
8. AM & FM Receivers
9. AM & FM Receivers **(LAB)** &nbsp; · &nbsp; **Module 2 HW due**

### Module 4 — Digital Modulation

10. FSK
11. FSK
12. FSK **(LAB)** &nbsp; · &nbsp; **Module 3 HW due**
13. PAM Theory
14. ASCII/PAM
15. ASCII/PAM **(LAB)**
16. ASCII/PAM &nbsp; · &nbsp; **Final Project introduced**

### Module 5 — Custom Blocks & Midterm

17. GRC: OOT Modules
18. GRC: Custom Blocks **(LAB)** &nbsp; · &nbsp; **Module 4 HW due**
19. GRC: Custom Blocks **(LAB)**
20. **Midterm Activity — GNURadio + Fox Hunt**

### Module 6 — Waveform Applications & RF Reverse Engineering

21. CW **(LAB)**
22. DTMF
23. DTMF **(LAB)** &nbsp; · &nbsp; **Project Proposal due**
24. HD Radio
25. HD Radio **(LAB)**
26. Flex day
27. mPSK &nbsp; · &nbsp; **Module 6a HW due (CW / DTMF / HD Radio)**
28. mPSK **(LAB)** &nbsp; · &nbsp; **Project Background Research due**
29. FHSS — Transmitter
30. FHSS — Receiver **(LAB)**
31. RF Reverse Engineering
32. RF Reverse Engineering
33. RF Reverse Engineering **(LAB)**
34. Flex day
35. ADS-B **(LAB)**
36. AIS **(LAB)** &nbsp; · &nbsp; **Module 6b HW due (mPSK / FHSS / RF-RE)**

### Module 7 — Final Project

37. Project Work Day **(LAB)**
38. QAM & OFDM &nbsp; · &nbsp; **Prototype Description due**
39. Project Day **(LAB)**
40. **Final Project Presentations** &nbsp; · &nbsp; **Final Project due**

## Textbooks & materials

See the [materials page](materials.md).

## Software & hardware

- **GNURadio** with GNU Radio Companion (GRC)
- **RTL-SDR** — introductory receive-only SDR
- **HackRF** — half-duplex SDR (Tx and Rx)
- **PlutoSDR / ADALM-PLUTO** — full-duplex SDR
- **ADALM-PHASER** — phased-array SDR platform (guest appearance from ECE 444)
- **Directional antennas** — for the Lesson 20 fox hunt
