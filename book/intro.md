<script>
  /* The visible page title lives in the raw-HTML hero below, which Sphinx
     can't see — so it derives the browser-tab title from the first Markdown
     heading. Set it explicitly here. */
  document.title = "ECE 448 — Software Defined Radios";
</script>

<section class="hero">
  <p class="hero-eyebrow">USAFA · Dept. of Electrical &amp; Computer Engineering · ECE 448 · Spring 2026</p>
  <h1 class="hero-title">Software Defined Radios</h1>
  <p class="hero-lede">Seven modules, 40 lessons, and a self-defined final project. Use GNURadio to build real flowgraphs against real signals — analog, digital, and everything from AM to ADS-B.</p>
  <div class="hero-cta">
    <a class="cta cta-primary" href="module01/index.html">Start Module 1 →</a>
    <a class="cta" href="syllabus.html#course-schedule">Course schedule</a>
    <a class="cta" href="syllabus.html">Syllabus</a>
    <a class="cta" href="materials.html">Materials</a>
  </div>
</section>

<section class="block-grid" aria-label="Course modules">
  <a class="block-card" href="module01/index.html">
    <span class="num">01</span>
    <h3>Foundations of Detection &amp; Link Budgets</h3>
    <p>Noise figure, cascade analysis, and signal space — the math you need before hardware ever touches a signal.</p>
    <footer>Lessons 1–3</footer>
  </a>
  <a class="block-card" href="module02/index.html">
    <span class="num">02</span>
    <h3>SDR &amp; GNURadio Foundations</h3>
    <p>Hardware architectures, sample rates, and your first hands-on flowgraphs in GNURadio.</p>
    <footer>Lessons 4–6</footer>
  </a>
  <a class="block-card" href="module03/index.html">
    <span class="num">03</span>
    <h3>Analog Modulation</h3>
    <p>AM and FM: simulate them, build receivers, and see what makes each one hard.</p>
    <footer>Lessons 7–9</footer>
  </a>
  <a class="block-card" href="module04/index.html">
    <span class="num">04</span>
    <h3>Digital Modulation</h3>
    <p>FSK and PAM from first principles — the gateway drug to every other modulation on the spectrum.</p>
    <footer>Lessons 10–16</footer>
  </a>
  <a class="block-card" href="module05/index.html">
    <span class="num">05</span>
    <h3>Custom Blocks &amp; Midterm</h3>
    <p>Write your own GNURadio blocks in Python and C++, then use them in the fox-hunt midterm activity.</p>
    <footer>Lessons 17–20</footer>
  </a>
  <a class="block-card" href="module06/index.html">
    <span class="num">06</span>
    <h3>Waveform Applications &amp; RF Reverse Engineering</h3>
    <p>CW, DTMF, HD Radio, FHSS, mPSK, ADS-B, AIS — real signals, real decoders, real reverse engineering.</p>
    <footer>Lessons 21–36</footer>
  </a>
  <a class="block-card" href="module07/index.html">
    <span class="num">07</span>
    <h3>Final Project</h3>
    <p>You define the success criteria and defend them. QAM, OFDM, and whatever else fits your project.</p>
    <footer>Lessons 37–40</footer>
  </a>
</section>

<section class="deliverable-cards" aria-label="Course deliverables">
  <div class="deliverable-card">
    <p class="d-eyebrow">Individual deliverable</p>
    <h3>Final Project</h3>
    <p class="d-weight"><span class="d-w-num">40%</span> of course grade</p>
    <p class="d-due">Self-defined success criteria, technical presentation, and demo</p>
    <a class="d-link" href="syllabus.html#grading">How mastery grading works →</a>
  </div>
  <div class="deliverable-card">
    <p class="d-eyebrow">Individual deliverable</p>
    <h3>Midterm Activity</h3>
    <p class="d-weight"><span class="d-w-num">35%</span> of course grade</p>
    <p class="d-due">GNURadio-based fox hunt · <strong>Lesson 20</strong></p>
    <a class="d-link" href="syllabus.html#grading">How mastery grading works →</a>
  </div>
  <div class="deliverable-card">
    <p class="d-eyebrow">Ongoing</p>
    <h3>Engagement</h3>
    <p class="d-weight"><span class="d-w-num">25%</span> of course grade</p>
    <p class="d-due">Practice problems, EI, lab prep, and course-improvement contributions</p>
    <a class="d-link" href="syllabus.html#engagement-credits-ec">Ways to earn engagement →</a>
  </div>
</section>

## Terminal Learning Objectives

By the end of this course you should be able to:

1. Analyze a wireless link at the system level — noise figure, cascade analysis, and signal space — and predict whether it closes.
2. Set up, configure, and use an SDR platform to receive and transmit real-world signals.
3. Simulate, analyze, and implement common analog and digital modulation schemes in GNURadio.
4. Write custom GNURadio blocks in Python and C++, and package them as an out-of-tree module.
5. Reverse-engineer an unknown RF signal from spectrum to bitstream, using GQRX, URH, and GNURadio.
6. Scope, execute, and defend a self-directed final project using SDR hardware and open-source tooling.

:::{admonition} How this course is graded
:class: key-concept

Every learning objective is scored on a **binary 1 / 0** scale — no partial credit.
A 0 comes with detailed feedback rather than the answer, and if you submitted real
effort on time you may **revise your work** until you earn the 1.

The bar is simple: I want you to learn this material, and I would rather you learn
it late than not at all.
:::

:::{admonition} Rules of engagement
:class: ground-rules

1. **The website is the course.** Lesson pages, practice problems, and slide decks are updated during the semester — pull the latest before class.
2. **Practice problems are your reps.** They are ungraded for correctness but graded for a genuine, documented attempt. Do the work.
3. **EI early and often.** It is the single best predictor of doing well in this course, and it counts toward engagement.
4. **Ask questions in public.** If you had it, someone else had it too. The person who was afraid to ask is grateful.
:::

## What Each Lesson Contains

- **Reading.** Expanded notes on the objective — the equations worked through, the flowgraphs annotated, the connections to real hardware called out.
- **Slides.** The reveal.js deck used in class. Open it in a browser and read along.
- **Practice Problems.** Ungraded reps keyed to the lesson's learning objectives, with worked solutions on a separate page.
- **Labs and projects (where they apply).** Pre-lab plan, procedure, and rubric — plus links to the midterm and final project packets.

> Disclaimer: The contents of this website are for educational use only and do
> not necessarily reflect the official policy or position of the United States
> Air Force Academy, the Department of the Air Force, or the U.S. Government.
