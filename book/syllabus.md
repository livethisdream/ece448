# Syllabus

## Course

**ECE 448 — Software Defined Radios**
Spring 2027

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
in **GNU Radio**, building real flowgraphs against real signals. The course
culminates in a substantial, **self-defined final project** that integrates
every concept in the course into a specific wireless application of your
choosing.

### An applications course

**Watch what the signal does; don't calculate it.** We use real radios and
GNU Radio to observe effects, such as what happens when the noise goes up, and,
when it helps, tie what we see back to theory. ECE 447 derives communications
theory; here we use it. Every lesson starts with a
signal to build, receive, or decode, and most of every period is spent in
GNU Radio with real hardware and real captures. When a lesson brings in an
equation, it is because a block parameter, a sample rate, or a filter needs
it.

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
| 1.1 | I can define noise figure and explain how each stage of a receiver chain, the first above all, sets the system's noise performance. |
| 1.2 | I can compute a link budget for a specified geometry, transmitter, and antenna configuration, and compare it with the signal an SDR shows. |
| 1.3 | I can describe signal-space concepts (basis functions, constellations, decision regions) and apply them to a digital modulation scheme. |

### Module 2 — SDR & GNU Radio Foundations

| LO | Description |
| :-: | :- |
| 2.1 | I can describe what a Software Defined Radio is, contrast it with a traditional hardware radio, and identify the SDR platforms used in this course (PlutoSDR, ADALM-PHASER). |
| 2.2 | I can identify the roles of the RF frontend, ADC/DAC, and host in an SDR signal chain and describe sample-rate, bandwidth, and dynamic-range trade-offs. |
| 2.3 | I can install GNU Radio and use GNU Radio Companion (GRC) to build, inspect, and run a basic flowgraph. |
| 2.4 | I can capture a real RF signal using an SDR and interpret its time- and frequency-domain representations. |

### Module 3 — Analog Modulation

| LO | Description |
| :-: | :- |
| 3.1 | I can describe DSB-AM, DSB-SC, and SSB and identify each on a spectrum. |
| 3.2 | I can implement an AM modulator and demodulator in GNU Radio and verify demodulated audio against the source. |
| 3.3 | I can implement an FM receiver in GNU Radio, demodulate a live broadcast FM signal, and decode its RDS data. |
| 3.4 | I can explain and demonstrate the trade-off between bandwidth and noise performance for AM vs. FM. |

### Module 4 — Digital Modulation

| LO | Description |
| :-: | :- |
| 4.1 | I can describe FSK modulation and implement an FSK transmitter and receiver in GNU Radio. |
| 4.2 | I can describe PAM theory and identify the pulse-shaping, symbol-rate, and bandwidth trade-offs. |
| 4.3 | I can apply matched filtering and symbol-timing recovery to a received PAM signal. |
| 4.4 | I can implement a PAM link that transmits and receives ASCII text end-to-end. |

### Module 5 — Custom Blocks & Midterm

| LO | Description |
| :-: | :- |
| 5.1 | I can create a GNU Radio out-of-tree (OOT) module and add a custom Python block to it. |
| 5.2 | I can implement a custom signal-processing block from scratch and integrate it into a GNU Radio flowgraph. |
| 5.3 | I can find a hidden transmitter in a direction-finding fox hunt using an SDR and a directional antenna. |
| 5.4 | I can solve capture-the-flag challenges that require finding, capturing, demodulating, and decoding unknown signals with GNU Radio. |

### Module 6 — Waveform Applications & RF Reverse Engineering

| LO | Description |
| :-: | :- |
| 6.1 | I can transmit and receive CW (Morse) using GNU Radio and decode a received CW stream. |
| 6.2 | I can decode DTMF tones from a captured audio signal. |
| 6.3 | I can describe how HD Radio works and demodulate an HD Radio signal. |
| 6.4 | I can implement an mPSK modulator and demodulator (BPSK, QPSK, 8PSK) and recover carrier and symbol timing. |
| 6.5 | I can implement FHSS transmission and reception, including hop-sequence synchronization. |
| 6.6 | I can perform RF reverse engineering on an unknown signal: identify its modulation, symbol rate, and payload structure. |
| 6.7 | I can receive and decode ADS-B messages from aircraft transponders. |
| 6.8 | I can receive and decode AIS messages from marine vessels. |

### Module 7 — Final Project

| LO | Description |
| :-: | :- |
| 7.1 | I can describe QAM and OFDM and identify use cases for each. |
| 7.2 | I can define the scope, objectives, and measurable success criteria for a self-directed SDR project. |
| 7.3 | I can research, design, and implement a wireless communication system using an SDR and GNU Radio. |
| 7.4 | I can present my project results in a professional-grade report and live demonstration and defend engineering trade-offs against my own stated success criteria. |

</div>

## Grading

Grades are based on **mastery** of the learning objectives, demonstrated by
what you build: lab flowgraphs, the midterm, and the final project.

### Final grade

| Component | Weight |
| :- | :-: |
| Final project | 40% |
| Labs | 25% |
| Engagement | 20% |
| Midterm | 15% |

### Mastery-based assessment

Labs, the midterm, and the final project checkpoints are assessed against the
learning objectives on a **binary scale**:

- **1**: you have mastered the objective.
- **0**: you have not *yet* mastered the objective.

You may **revise your work** based on the detailed feedback provided, unless no
effort is evident (the work is blank, incomplete, or significantly late).

The bar is simple: I want you to *learn this material*, and I would rather you
learn it late than not at all.

### Labs

Each lab is **one packet, one submission**, hung off the lesson it follows:

- **Part 1, Pre-Lab**: individual, before the period.
- **Part 2, Bench**: in class, on the hardware.
- **Part 3, Writeup**: after the lab, in report format.

### Midterm

The midterm follows Lesson 11 and has two parts: a **fox hunt**, finding a
hidden transmitter with an SDR and a directional antenna, and a
**capture-the-flag**, a set of challenges that require finding, capturing,
demodulating, and decoding unknown signals. It is an individual effort.

### Final project

The final project is intentionally open-ended. You choose the wireless
application, **write your own success criteria** for A-, B-, and C-level
outcomes, and defend the result. Each checkpoint below develops a section of
your final report and is graded 1 / 0, with revisions under course policy:

1. **Project proposal**: what you want to build, why it is meaningful and
   feasible, and your success criteria.
2. **Background research**: at least four high-quality sources and how your
   project builds on them.
3. **Design description**: your initial design, its critical components, use
   cases, and test plan.
4. **Prototype description**: build and test results, and your plan to
   finish.
5. **Final report and presentation**: an IEEE-quality report (typically 7-10
   pages) and a five-minute presentation and live demonstration. Code goes in
   a GitHub repository.

### Engagement credits (EC)

Engagement is earned in several ways:

- **Weekly quizzes** on Gradescope, 1 EC each. Revisions are allowed.
- **Practice problems.** Graded for a genuine, documented attempt, not for
  correctness.
- **Extra Instruction (EI).** 1 EC for each session you schedule and attend.
- **Peer review.** 1 EC for reviewing or revising a classmate's report.
- **Course improvement.** Spotted a bug in a lab packet, an unclear slide, or
  a broken link on this site? Tell me and it counts.

Request EC for EI and peer review through the running Gradescope assignment.

### Grade scale

<table class="grade-scale">
  <thead>
    <tr>
      <th>A</th><th>A−</th><th>B+</th><th>B</th><th>B−</th>
      <th>C+</th><th>C</th><th>C−</th><th>D</th><th>F</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>100%</td><td>93%</td><td>90%</td><td>87%</td><td>83%</td>
      <td>80%</td><td>77%</td><td>73%</td><td>70%</td><td>≤ 60%</td>
    </tr>
  </tbody>
</table>

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

The midterm and final project have their own resource policies
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
you'll encounter here, and often produce GNU Radio flowgraphs that don't quite
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

## Course schedule

Lessons are topics, not class periods: a lesson takes as many periods as it
needs, and its lab follows on the bench. Dates will follow the Spring 2027
academic calendar.

### Module 1 — Foundations of Detection & Link Budgets

| Lesson | Topic | Objectives |
| :-: | :- | :- |
| L1 | [Course Introduction](module01/L01-course-intro/index.md) | — |
| L2 | [Noise Figure and Link Budget](module01/L02-noise-figure-link-budget/index.md) | 1.1, 1.2 |
| L3 | [Signal Space](module01/L03-signal-space/index.md) | 1.3 |

### Module 2 — SDR & GNU Radio Foundations

| Lesson | Topic | Objectives |
| :-: | :- | :- |
| L4 | [SDR Introduction](module02/L04-sdr-introduction/index.md) | 2.1, 2.2 |
| L5 | [GNU Radio Introduction](module02/L05-gnu-radio-intro/index.md) | 2.3, 2.4 |
| L5 Lab | [First Flowgraphs](module02/L05-lab-first-flowgraphs/index.md) | 2.3, 2.4 |

### Module 3 — Analog Modulation

| Lesson | Topic | Objectives |
| :-: | :- | :- |
| L6 | [AM Simulation](module03/L06-am-simulation/index.md) | 3.1, 3.2 |
| L6 Lab | [AM Simulation](module03/L06-lab-am-simulation/index.md) | 3.1, 3.2 |
| L7 | [AM and FM Receivers](module03/L07-am-fm-receivers/index.md) | 3.3, 3.4 |
| L7 Lab | [AM and FM Receivers](module03/L07-lab-am-fm-receivers/index.md) | 3.3, 3.4 |

### Module 4 — Digital Modulation

| Lesson | Topic | Objectives |
| :-: | :- | :- |
| L8 | [FSK](module04/L08-fsk/index.md) | 4.1 |
| L8 Lab | [FSK](module04/L08-lab-fsk/index.md) | 4.1 |
| L9 | [PAM Theory](module04/L09-pam-theory/index.md) | 4.2, 4.3 |
| L10 | [ASCII over PAM](module04/L10-ascii-pam/index.md) | 4.4 |
| L10 Lab | [PAM Link](module04/L10-lab-pam-link/index.md) | 4.4 |

### Module 5 — Custom Blocks & Midterm

| Lesson | Topic | Objectives |
| :-: | :- | :- |
| L11 | [Out-of-Tree Modules and Custom Blocks](module05/L11-custom-blocks/index.md) | 5.1, 5.2 |
| L11 Lab | [Custom Block](module05/L11-lab-custom-block/index.md) | 5.1, 5.2 |
|  | [Midterm — Fox Hunt and CTF](module05/midterm/index.md) | 5.3, 5.4 |

### Module 6 — Waveform Applications & RF Reverse Engineering

| Lesson | Topic | Objectives |
| :-: | :- | :- |
| L12 | [CW](module06/L12-cw/index.md) | 6.1 |
| L12 Lab | [CW](module06/L12-lab-cw/index.md) | 6.1 |
| L13 | [DTMF](module06/L13-dtmf/index.md) | 6.2 |
| L13 Lab | [DTMF](module06/L13-lab-dtmf/index.md) | 6.2 |
| L14 | [HD Radio](module06/L14-hd-radio/index.md) | 6.3 |
| L14 Lab | [HD Radio](module06/L14-lab-hd-radio/index.md) | 6.3 |
| L15 | [mPSK](module06/L15-mpsk/index.md) | 6.4 |
| L15 Lab | [mPSK](module06/L15-lab-mpsk/index.md) | 6.4 |
| L16 | [Frequency Hopping](module06/L16-fhss/index.md) | 6.5 |
| L16 Lab | [Frequency Hopping](module06/L16-lab-fhss/index.md) | 6.5 |
| L17 | [RF Reverse Engineering](module06/L17-rf-reverse-engineering/index.md) | 6.6 |
| L17 Lab | [RF Reverse Engineering](module06/L17-lab-rf-reverse-engineering/index.md) | 6.6 |
| L18 | [ADS-B](module06/L18-adsb/index.md) | 6.7 |
| L19 | [AIS](module06/L19-ais/index.md) | 6.8 |
| L18–L19 Lab | [ADS-B and AIS](module06/L18-L19-lab-adsb-ais/index.md) | 6.7, 6.8 |

### Module 7 — Final Project

| Lesson | Topic | Objectives |
| :-: | :- | :- |
| L20 | [QAM and OFDM](module07/L20-qam-ofdm/index.md) | 7.1 |
|  | [Final Project](module07/final-project/index.md) | 7.2, 7.3, 7.4 |

## Textbooks & materials

See the [materials page](materials.md).

## Software & hardware

- **GNU Radio** with GNU Radio Companion (GRC)
- **RTL-SDR** — introductory receive-only SDR
- **HackRF** — half-duplex SDR (Tx and Rx)
- **PlutoSDR / ADALM-PLUTO** — full-duplex SDR
- **ADALM-PHASER** — phased-array SDR platform (guest appearance from ECE 444)
- **Directional antennas** — for the midterm fox hunt
