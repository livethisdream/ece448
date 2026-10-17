---
frame_view: true
---

# ECE 448 — Software Defined Radios

::::{frame}
:class: title-frame

<div class="course-mark">USAFA · Dept. of Electrical &amp; Computer Engineering · Spring 2027</div>

<h1 class="frame-title">Software Defined Radios</h1>

<div class="title-rule"></div>

Real signals, real flowgraphs.

Seven modules, 20 lessons, and a final project you define yourself.

<div class="hero-pills">
<div class="hero-cta hero-grid">
  <a class="cta cta-primary" href="module01/index.html">Module 1</a>
  <a class="cta cta-primary" href="module02/index.html">Module 2</a>
  <a class="cta cta-primary" href="module03/index.html">Module 3</a>
  <a class="cta cta-primary" href="module04/index.html">Module 4</a>
  <a class="cta cta-primary" href="module05/index.html">Module 5</a>
  <a class="cta cta-primary" href="module06/index.html">Module 6</a>
  <a class="cta cta-primary" href="module07/index.html">Module 7</a>
</div>
<div class="hero-cta hero-grid hero-links">
  <a class="cta" href="syllabus.html#course-schedule">Schedule</a>
  <a class="cta" href="syllabus.html">Syllabus</a>
  <a class="cta" href="materials.html">Materials</a>
</div>
</div>
::::

::::{frame} An Applications Course

:::{callout}
This course is about **building radios, not deriving them**. You get just
enough theory to make the flowgraph work, then spend the period on real
signals in GNU Radio.
:::

:::{depth}
ECE 447 is where communications theory is derived. Here we use it: every
lesson starts with a signal to build, receive, or decode, and brings in the
theory only when the flowgraph needs it.
:::
::::

::::{frame} Modules 1-2: Foundations

<div class="block-grid">
  <a class="block-card" href="module01/index.html">
    <span class="num">01</span>
    <h3>Foundations of Detection &amp; Link Budgets</h3>
    <p>Noise figure, link budgets, and signal space: enough to predict whether a link closes.</p>
    <footer>Lessons 1–3</footer>
  </a>
  <a class="block-card" href="module02/index.html">
    <span class="num">02</span>
    <h3>SDR &amp; GNU Radio Foundations</h3>
    <p>What is inside an SDR, and your first GNU Radio flowgraphs against real captures.</p>
    <footer>Lessons 4–5</footer>
  </a>
</div>
::::

::::{frame} Modules 3-4: Modulation

<div class="block-grid">
  <a class="block-card" href="module03/index.html">
    <span class="num">03</span>
    <h3>Analog Modulation</h3>
    <p>AM and FM: simulate them, build receivers, and pull a live station and its RDS data off the air.</p>
    <footer>Lessons 6–7</footer>
  </a>
  <a class="block-card" href="module04/index.html">
    <span class="num">04</span>
    <h3>Digital Modulation</h3>
    <p>FSK and PAM, end to end, finishing with a link that carries ASCII text.</p>
    <footer>Lessons 8–10</footer>
  </a>
</div>
::::

::::{frame} Modules 5-7: Applications

<div class="block-grid">
  <a class="block-card" href="module05/index.html">
    <span class="num">05</span>
    <h3>Custom Blocks &amp; Midterm</h3>
    <p>Write your own GNU Radio blocks, then the midterm: a fox hunt and a capture-the-flag.</p>
    <footer>Lesson 11 · Midterm</footer>
  </a>
  <a class="block-card" href="module06/index.html">
    <span class="num">06</span>
    <h3>Waveform Applications &amp; RF Reverse Engineering</h3>
    <p>CW, DTMF, HD Radio, mPSK, frequency hopping, ADS-B, AIS, and the unknown signal.</p>
    <footer>Lessons 12–19</footer>
  </a>
  <a class="block-card" href="module07/index.html">
    <span class="num">07</span>
    <h3>Final Project</h3>
    <p>QAM and OFDM, then your own project, graded against success criteria you write.</p>
    <footer>Lesson 20 · Final Project</footer>
  </a>
</div>
::::

::::{frame} What You Are Graded On

<div class="deliverable-cards">
  <div class="deliverable-card">
    <p class="d-eyebrow">Individual</p>
    <h3>Final Project</h3>
    <p class="d-weight"><span class="d-w-num">40%</span> of course grade</p>
    <p class="d-due">Self-defined success criteria, report, and live demonstration</p>
    <a class="d-link" href="syllabus.html#final-project">How it is graded →</a>
  </div>
  <div class="deliverable-card">
    <p class="d-eyebrow">Per lab</p>
    <h3>Labs</h3>
    <p class="d-weight"><span class="d-w-num">25%</span> of course grade</p>
    <p class="d-due">One packet per lab: Pre-Lab, Bench, Writeup</p>
    <a class="d-link" href="syllabus.html#labs">How labs work →</a>
  </div>
  <div class="deliverable-card">
    <p class="d-eyebrow">Ongoing</p>
    <h3>Engagement</h3>
    <p class="d-weight"><span class="d-w-num">20%</span> of course grade</p>
    <p class="d-due">Quizzes, practice problems, EI, and peer review</p>
    <a class="d-link" href="syllabus.html#engagement-credits-ec">Ways to earn engagement →</a>
  </div>
  <div class="deliverable-card">
    <p class="d-eyebrow">Individual</p>
    <h3>Midterm</h3>
    <p class="d-weight"><span class="d-w-num">15%</span> of course grade</p>
    <p class="d-due">Fox hunt and capture-the-flag, after <strong>Lesson 11</strong></p>
    <a class="d-link" href="syllabus.html#midterm">How it is graded →</a>
  </div>
</div>
::::

::::{frame} Course Goals
By the end of this course you should be able to:

1. Simulate, receive, and transmit signals with modern software and modulation techniques.
2. Describe filtering, interpolation, decimation, and matched filtering.
3. Apply them to real signals, noise and non-idealities included.
4. Reverse-engineer, decode, and characterize an unknown RF signal.
5. Define, execute, and defend your own SDR project.
::::

::::{frame} How This Course Is Graded

:::{callout}
Every learning objective is scored on a **binary 1 / 0** scale, with no
partial credit. A 0 comes with detailed feedback rather than the answer, and
if you submitted real effort on time you may **revise your work** until you
earn the 1.
:::
::::

::::{frame} This Site Is Being Built
The course is moving to this site one lesson at a time. Until a lesson is
converted, its page carries the objectives and the legacy slides it was last
taught from. Everything is also on the [materials page](materials.md).

:::{depth}
The contents of this website are for educational use only and do not
necessarily reflect the official policy or position of the United States Air
Force Academy, the Department of the Air Force, or the U.S. Government.
:::
::::
