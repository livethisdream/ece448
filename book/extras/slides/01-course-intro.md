<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 448

Introduction to Software Defined Radios

## Lesson 1 — Course Introduction

Spring 2026 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](/assets/ece448/img/USAFA-logo.png)

</div>

---

## Welcome

- Who I am
- Who you are
- What this course is going to ask of you

Note:
Instructor bio; ask each student for name, background, one thing they hope to learn.

---

## About your instructor

**Lt Col Neil Rogers, USAF (Ret.)**

<small>BS — TU · MSEE — AFIT · PhD — AFIT</small>

**Erdle Chair**, USAFA
**Field Applications Engineer**, Analog Devices

---

## Where I've been

![Duty stations](/assets/ece448/img/01-course-intro/Duty_stations.png)

<small>DF/USAFA · AFRL Directed Energy · NASIC · AFIT ×2 · AFLCMC</small>

---

## Radios, radar, and high-power RF

<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0.4em;align-items:center;">
  <img src="/assets/ece448/img/01-course-intro/nr-ots.jpg" alt="OTS" style="max-height:180px;object-fit:cover;">
  <img src="/assets/ece448/img/01-course-intro/ads2.jpg" alt="Active Denial System 2" style="max-height:180px;object-fit:cover;">
  <img src="/assets/ece448/img/01-course-intro/ig-team.JPG" alt="379th AEW" style="max-height:180px;object-fit:cover;">
  <img src="/assets/ece448/img/01-course-intro/E8C.jpg" alt="E-8C Joint STARS" style="max-height:180px;object-fit:cover;">
  <img src="/assets/ece448/img/01-course-intro/Rogers_UAS_Lab.jpg" alt="ACUASR UAS Lab" style="max-height:180px;object-fit:cover;">
  <img src="/assets/ece448/img/01-course-intro/usafa-retirement.jpg" alt="Retirement" style="max-height:180px;object-fit:cover;">
</div>

<small>OTS · ADS2 · 379th AEW · E-8C · ACUASR · retirement</small>

Note:
Section chief for Active Denial and High-Power Sources at AFRL Directed Energy.
E-8C Joint STARS work at NASIC.
Directed the Academy Center for UAS Research (ACUASR) at USAFA through 2025.

---

## Now — Analog Devices

<p style="text-align:center;">
<img src="/assets/ece448/img/01-course-intro/nr-adi.jpg" alt="Analog Devices">
</p>

**Field Applications Engineer** with the team behind the
**ADALM-PLUTO** and **ADALM-PHASER** you'll use in this course.

---

## Off the clock

<div style="display:grid;grid-template-columns:auto 1fr;gap:0.6em 1em;align-items:center;max-width:720px;margin:0 auto;">
  <img src="/assets/ece448/img/01-course-intro/fam_newhouse.jpg" alt="Family" style="height:130px;width:220px;object-fit:cover;">
  <div style="font-size:0.75em;">Family — four kids (11 · 13 · 15 · 17)</div>

  <img src="/assets/ece448/img/01-course-intro/CF_dying.png" alt="CrossFit" style="height:130px;width:220px;object-fit:cover;">
  <div style="font-size:0.75em;">CrossFit</div>

  <img src="/assets/ece448/img/01-course-intro/trace_guitar.jpg" alt="Guitar" style="height:130px;width:220px;object-fit:cover;">
  <div style="font-size:0.75em;">Guitar with the band at <strong>Trace</strong> church</div>
</div>

---

## How I teach

- **We're learning this together** — I don't know it all.
- **Mistakes are part of learning** — make them, and make them count.
- **Ask questions** — there is no such thing as a dumb one.

---

## Think about the last hour…

- Cellular data
- WiFi
- Bluetooth
- Car key fob · RFID badge
- GPS
- ADS-B chirping overhead

<div class="callout">
Modern life is <strong>soaked in RF.</strong>
</div>

Note:
Ask the class: how many wireless links have you used today?
Get to 10 without much effort.

---

## What is a Software Defined Radio?

<div class="slide-box">

Traditionally, a radio is a **stack of specialized hardware** — mixers, filters, IF stages — tuned at the factory for one job.

An **SDR** puts an **ADC as close to the antenna as possible**, and moves everything else — filtering, mixing, demodulation, decoding — into **software** on a general-purpose CPU or FPGA.

</div>

Note:
Same $30 dongle → FM radio, ADS-B receiver, GPS receiver, spectrum analyzer, garage-door reverse-engineering tool.
Software defines the radio.

---

## The signal is data

<div class="callout">
Once digitized, a radio wave is just a <strong>stream of complex numbers</strong>. Every DSP tool you know applies.
</div>

Note:
This is the core mental model shift.
Not "an FM signal" — a stream of I/Q samples.

---

## Real radios are messy

- Noise
- Clock offsets
- Non-linearity
- Multipath
- LO leakage · DC offset · quantization

<div class="callout">
The hard part isn't the math. It's the <strong>non-ideal hardware and channel</strong>.
</div>

---

## Why this matters — the AF mission

- **Comms** — tactical radios, data links, SATCOM, Link-16
- **EW** — DF, jamming, protection, cognitive EW
- **SIGINT** — collection and analysis
- **Radar** — coherent, cognitive, adaptive (see ECE 444)
- **T&M** — spectrum monitoring, over-the-air testing

---

## Course roadmap

1. Foundations — detection &amp; link budgets
2. SDR &amp; GNURadio
3. Analog modulation (AM, FM)
4. Digital modulation (FSK, PAM)
5. Custom blocks &amp; midterm
6. Waveform applications &amp; RF-RE
7. Final project — **you define it**

<small>40 lessons · ~15 labs · midterm activity · self-defined final project.</small>

---

## Course schedule

<div class="schedule-grid cols-7">
  <!-- Row 1: module number + title -->
  <div class="mod-top"><span class="mod-num">1</span><span class="mod-title">Foundations</span></div>
  <div class="mod-top"><span class="mod-num">2</span><span class="mod-title">SDR &amp; GNURadio</span></div>
  <div class="mod-top"><span class="mod-num">3</span><span class="mod-title">Analog Mod</span></div>
  <div class="mod-top"><span class="mod-num">4</span><span class="mod-title">Digital Mod</span></div>
  <div class="mod-top"><span class="mod-num">5</span><span class="mod-title">Custom Blocks &amp; Midterm</span></div>
  <div class="mod-top"><span class="mod-num">6</span><span class="mod-title">Waveforms &amp; RF-RE</span></div>
  <div class="mod-top"><span class="mod-num">7</span><span class="mod-title">Final Project</span></div>

  <!-- Row 2: lesson range -->
  <div class="mod-lessons">L1 – L3</div>
  <div class="mod-lessons">L4 – L6</div>
  <div class="mod-lessons">L7 – L9</div>
  <div class="mod-lessons">L10 – L16</div>
  <div class="mod-lessons">L17 – L20</div>
  <div class="mod-lessons">L21 – L36</div>
  <div class="mod-lessons">L37 – L40</div>

  <!-- Row 3: activities + project milestones -->
  <div class="mod-bottom">
    <div>Link budget</div>
    <div>Signal space</div>
  </div>
  <div class="mod-bottom">
    <div>Install GNURadio</div>
    <div>First flowgraphs</div>
  </div>
  <div class="mod-bottom">
    <div>AM/FM sim &amp; Rx</div>
  </div>
  <div class="mod-bottom">
    <div>FSK · PAM · ASCII/PAM</div>
    <div><span class="milestone">Final project intro · L16</span></div>
  </div>
  <div class="mod-bottom">
    <div>OOT modules · custom blocks</div>
    <div><span class="milestone">Midterm · L20</span></div>
  </div>
  <div class="mod-bottom">
    <div>CW · DTMF · HD Radio</div>
    <div>mPSK · FHSS · RF-RE</div>
    <div>ADS-B · AIS</div>
  </div>
  <div class="mod-bottom">
    <div>QAM · OFDM</div>
    <div><span class="milestone">Final due · L40</span></div>
  </div>
</div>

---

## Two graded events

**Midterm activity — L20**
- GNURadio + custom-block practical + fox hunt

**Final project — L40**
- **You** pick the wireless application
- **You** write the success criteria
- **You** defend the result

Note:
The final project is deliberately open-ended.
The proposal (L23) is where you lock in what "done" means for your project.

---

## Show & tell

A real SDR, tuned live, on a whip antenna.

<!-- fire up GNURadio FFT sink
     sweep across FM broadcast · ADS-B (1090) · cellular · WiFi
     point out signals we'll decode by end of semester -->

Note:
Have students guess what each blip is before revealing.
Callback: "we'll decode most of these ourselves."

---

## For next time

<figure class="qr qr-corner">
  <img src="/assets/ece448/img/syllabus-qr.png" alt="QR to syllabus">
  <figcaption>Full syllabus</figcaption>
</figure>

Reading:
- [PySDR](https://pysdr.org/) — *Introduction* and *Frequency Domain*
- [GNU Radio Tutorials](https://wiki.gnuradio.org/index.php/Tutorials) — skim the landing page

<div class="callout">
Next lesson: what's inside an <strong>SDR</strong>.
</div>
