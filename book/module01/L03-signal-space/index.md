---
frame_view: true
---

# L3 - Signal Space

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">Signal Space</h1>

<div class="title-rule"></div>

Every digital modulation is a set of points, and noise decides how often the receiver picks the wrong one.

Lesson 3 · Module 1: Foundations of Detection & Link Budgets · Dr. Neil Rogers
::::

::::{frame} Slides
:class: read-only

:::{admonition} Slides
:class: slides
<a href="../../slides/L03-signal-space.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L03-signal-space.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L03-signal-space.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '1'; counter-reset: lo 2">
  <li>I can describe signal-space concepts (basis functions, constellations, decision regions) and apply them to a digital modulation scheme.</li>
</ol>
::::

::::{frame} Four Ways to Carry Bits
:::{present}
| Family | What changes per symbol | In this course |
| :-- | :-- | :-- |
| ASK / PAM | amplitude | Lessons 9 and 10 |
| PSK | phase | Lesson 15 |
| FSK | frequency | Lesson 8 |
:::
:::{present}
- $M$ choices per symbol carry $\log_2 M$ bits.
- "$M$-ary" means $M$ choices: 4-PAM, 8-PSK, 2-FSK.
:::

A digital transmitter sends one **symbol** at a time, and each symbol is one of a small set of waveforms agreed on in advance. The modulation families differ in what they change from symbol to symbol. **Amplitude-shift keying** (ASK) and **pulse amplitude modulation** (PAM) change the height of the signal. **Phase-shift keying** (PSK) keeps the height and changes the phase of the carrier. **Frequency-shift keying** (FSK) changes the frequency.

With $M$ waveforms to choose from, each symbol carries $\log_2 M$ bits: two choices carry one bit, four carry two, eight carry three. The receiver's whole job is to decide, for each symbol, which of the $M$ waveforms was sent. Today we look at that decision the way the receiver does, as a picture, and watch what noise does to it. Each family gets its own flowgraph later in the course.
::::

::::{frame} Part 1: Binary PAM
:::{present}
<img src="../../viz/img/L03-binary-pam.svg"
     alt="A binary PAM waveform for the bits 1 0 1 1 0 0 1 0: one rectangular pulse per bit, at plus A for a 1 and minus A for a 0, with one sample marked at the middle of each pulse. Beside it the samples collapse to two points, minus A and plus A, on a line with the threshold at zero"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- A 1 is a pulse at $+A$; a 0 is a pulse at $-A$.
- Sample once per pulse and decide by sign: the threshold is 0.
:::

The simplest digital signal is **binary PAM**. Each bit becomes one pulse, $+A$ for a 1 and $-A$ for a 0, and the pulses follow one another at the symbol rate. The two waveforms are the same pulse with opposite signs, so they are called **antipodal**.

The receiver takes one sample in the middle of each pulse. Without noise, every sample is exactly $+A$ or $-A$, and the right-hand panel shows all eight collapsing onto two points on a line. Deciding is then trivial: a sample above zero is a 1 and a sample below zero is a 0. Zero, halfway between the two points, is the **decision threshold**. Lesson 10 builds exactly this receiver, and GNU Radio's Binary Slicer block is this threshold.
::::

::::{frame} Noise and the Threshold
:::{present}
<img src="../../viz/img/L03-pam-noise.svg"
     alt="1500 received binary PAM samples, each drawn as a dot at its value. At an SNR of 14 dB the dots form two narrow bands at minus A and plus A and none crosses zero. At 4 dB the bands are wide and meet at zero, and the 21 samples that land on the wrong side are drawn in red"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Noise turns each point into a spread of samples.
- A sample that lands past 0 is decided wrong.
- As the SNR falls, the spreads widen and meet.
:::

A real receiver adds noise to every sample, the noise floor of Lesson 2, so the received value is $+A$ or $-A$ plus a random offset. The figure shows 1500 received samples at two SNRs, each drawn as a dot at its value; the up-and-down spread only keeps the dots apart. At 14 dB each point becomes a narrow band, and no sample comes anywhere near zero. At 4 dB the bands spread out until their edges meet at the threshold, and every sample that lands on the wrong side, drawn in red, is a wrong bit.

That is the whole story of noise in a digital receiver, and we will see it again on every display in the course. Nothing about the decision changes as the noise goes up; the threshold stays at zero. The samples just stray farther, and more of them stray across. Two things keep them on the right side: a higher SNR, which narrows the bands, and points that sit farther apart, which moves the threshold farther from each one.
::::

::::{frame} Antipodal and Orthogonal
:::{present}
<img src="../../viz/img/L03-antipodal-orthogonal.svg"
     alt="Two binary signal sets at the same energy and the same 6 dB SNR. The antipodal set has its points on opposite sides of the origin, with the boundary between them on the vertical axis, and few samples land on the wrong side. The orthogonal set has one point on each axis, closer together, with the boundary on the diagonal, and several times as many samples land on the wrong side"
     style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Antipodal: opposite signs, as far apart as the energy allows.
- Orthogonal: two unrelated waveforms, such as two FSK tones, sit closer together.
- Same energy and noise, more wrong decisions.
:::

Binary PAM is not the only way to send one bit. Binary FSK sends one of two tones, and the two tones are **orthogonal**: neither looks anything like the other, so each gets its own axis. Drawn at the same energy, the antipodal points sit on opposite sides of the origin, while the orthogonal points sit one on each axis, closer together, with the boundary on the diagonal between them.

The figure sends both through the same 6 dB of noise. The clouds are the same size in both panels, but the orthogonal pair has less room between its points and its boundary, so several times as many samples cross. That is the reason PAM and PSK, which can use antipodal points, get more out of the same transmitter power than FSK does. FSK has its own advantages, and Lesson 8 builds it anyway.
::::

::::{frame} Part 2: Two Basis Functions
:::{present}
$$\begin{aligned}
s(t) = {} &I\cos(2\pi f_c t) \\
&- Q\sin(2\pi f_c t)
\end{aligned}$$

- Cosine and sine at the same frequency are orthogonal, so $I$ and $Q$ carry two independent numbers.
- Each symbol is a point $(I, Q)$; the two waveforms are its **basis functions**.
:::

On a carrier, a transmitter can change two things per symbol: how much cosine and how much sine it sends. Those two waveforms are orthogonal, in the same sense as the two FSK tones, so the receiver can recover the cosine amount and the sine amount separately. That makes the cosine and the sine a pair of **basis functions**, the axes of a two-dimensional **signal space**, and every symbol a point with coordinates $(I, Q)$.

The SDR does that separation in hardware, and Lesson 4 opens it. What arrives in GNU Radio is already the pair for every sample, packed into one complex number, $I + jQ$. Plotting one sample per symbol on the I-Q plane gives the picture this lesson is named for.
::::

::::{frame} Constellation Diagrams
:::{present}
<img src="../../viz/img/L03-constellations.svg"
     alt="Four constellations at the same average symbol energy: BPSK, which is 2-PAM, with two points on the I axis; 4-PAM with four points on the I axis; QPSK with four points on a circle, one per quadrant; and 8-PSK with eight points on the circle"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- PAM puts its points on a line; PSK puts them on a circle.
- At the same energy, more points sit closer together.
:::

A **constellation diagram** plots the points a modulation uses. **2-PAM** is the binary PAM of Part 1, two points on the I axis; on a carrier the same two points are called **BPSK**, since flipping the sign is a 180° phase shift. **4-PAM** puts four points on that line and carries two bits per symbol. **$M$-PSK** spreads $M$ points around a circle: **QPSK** has four, one in each quadrant, and **8-PSK** has eight.

The figure draws all four at the same average energy, which is the same transmitter power, marked by the dashed circle. More points in the same power means the points sit closer together. QPSK and 4-PAM both carry two bits, but QPSK uses both axes and keeps its points farther apart, which is why radios use QPSK rather than 4-PAM on a carrier. 4-PAM still has its place: Lesson 9 shapes it as a baseband signal, where only one axis exists.
::::

::::{frame} Noise and Decision Regions
:::{present}
<img src="../../viz/img/L03-noise-clouds.svg"
     alt="QPSK received through noise at three SNRs. At 20 dB the four clouds are tight and no symbol crosses a boundary; at 10 dB the clouds widen and a few land in the wrong quadrant; at 4 dB the clouds overlap and many land in the wrong quadrant"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The receiver picks the nearest point.
- The samples nearest each point form its **decision region**.
- For QPSK the regions are the four quadrants.
:::

The receiver decides each symbol the way it did for binary PAM: it picks the nearest point. Every sample closer to one point than to any other falls in that point's **decision region**, and the boundaries sit halfway between neighbors. For QPSK the regions are the four quadrants, so the receiver needs only the signs of $I$ and $Q$. Binary PAM's threshold at zero is the same idea on a line.

The figure sends 600 QPSK symbols at three SNRs. Noise adds a random offset to both $I$ and $Q$, so each point arrives as a round cloud. At 20 dB the clouds are tight and every symbol lands in its own quadrant. At 10 dB a few stray across. At 4 dB the clouds overlap and the red samples, the ones in the wrong region, are everywhere. This is what the GNU Radio constellation sink will show us from Lesson 5 on.
::::

::::{frame} Constellation Explorer
:class: viz-frame

:::{depth}
The widget transmits random symbols, adds noise at the chosen SNR, and decides each one by the nearest point. The shaded tiles are the decision regions, and a symbol that lands in the wrong one turns red; the readouts count them. Start on QPSK at 12 dB, then switch to 8-PSK at the same SNR: the points sit closer together, the clouds reach the boundaries, and the red count climbs. Raise the SNR until 8-PSK is as clean as QPSK was. Then try 4-PAM against QPSK at the same SNR. Last, return to QPSK and add a phase offset: the clouds rotate toward the boundaries, and past $45^\circ$ every symbol would land in the wrong region even with no noise at all, which is why the receivers of Lessons 9 and 15 correct the phase before they decide.
:::

:::{present}
<iframe src="../../viz/constellation-explorer.html"
        width="100%" height="411"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Constellation explorer: random symbols for BPSK, QPSK, 8-PSK, or 4-PAM through noise at a chosen SNR and phase offset, with the decision regions shaded and the symbols that land in the wrong region in red">
</iframe>
:::
::::

::::{frame} Part 3: Gray Coding
:::{present}
<img src="../../viz/img/L03-gray-8psk.svg"
     alt="8-PSK with Gray-coded labels: going around the circle, 000, 001, 011, 010, 110, 111, 101, 100, each differing from its neighbors in one bit"
     style="max-width: 340px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Each label differs from its neighbors by one bit.
- A slip to a neighbor then costs one bit, not three.
:::

Which bits go on which point is a design choice, and it matters. When noise pushes a sample into the wrong region, it is almost always a neighbor's region, so the labels should make that slip corrupt as few bits as possible. **Gray coding** labels the points so that each one differs from its neighbors in exactly one bit.

Try it before looking at the figure: label the eight points of 8-PSK, starting from 000 at 0°, so that every pair of neighbors, including the last and the first, differs in one bit. With the natural binary order instead, 011 and 100 sit next to each other, and a slip between them corrupts all three bits. Every modulator we build in GNU Radio uses a Gray code, set in the table of its Chunks to Symbols or Constellation Object block.
::::

::::{frame} Reading a Constellation in GNU Radio
:::{present}
<img src="../../viz/img/L03-impairments.svg"
     alt="Four QPSK constellations with one problem each: noise spreads each point into a round cloud; a 25 degree phase offset rotates all four clouds; a frequency offset spins the points into a ring; a timing offset of 0.3 symbol smears each point into a square spread"
     style="max-width: 900px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Each receiver problem has its own shape on the constellation.
- From Lesson 5 on, the constellation sink is the first place we look.
:::

GNU Radio's constellation sink plots received samples exactly as in this lesson, and it is the fastest diagnostic a radio engineer has, because each problem leaves its own shape. **Noise** spreads each point into a round cloud, and the cloud's size tells us how good the SNR is. A **phase offset** between the transmitter and receiver oscillators rotates the whole constellation. A **frequency offset** makes that rotation continuous, so the points smear into a ring. A **timing offset**, sampling each symbol off its peak, mixes in neighboring symbols and smears each point into a spread that noise does not explain.

Lesson 9 recovers symbol timing for PAM, and Lesson 15 recovers carrier phase and frequency for PSK. Each fix shows up on the constellation sink as these shapes collapsing back into tight clouds, and that is how we will check every receiver we build.
::::

::::{frame} Key Point
:::{present}
:class: callout
A modulation is a set of points. Noise turns each point into a cloud, and a sample that lands in a neighbor's region is decided wrong. Points farther apart, or a higher SNR, keep the clouds in their own regions.
:::
::::

::::{frame} Summary
:class: read-only

| Idea | What it is | What to remember |
| :-- | :-- | :-- |
| PAM, PSK, FSK | change amplitude, phase, or frequency | $M$ choices carry $\log_2 M$ bits |
| Binary PAM | pulses at $+A$ and $-A$ | threshold at 0 |
| Antipodal vs orthogonal | opposite signs vs separate axes | antipodal points sit farther apart |
| Basis functions | $\cos$ and $\sin$ at $f_c$; axes $I$ and $Q$ | one complex sample per symbol |
| Constellation | the $M$ points a modulation uses | more points, closer together |
| Decision region | samples nearest each point | QPSK: the four quadrants |
| Noise | spreads each point into a cloud | lower SNR, more samples in the wrong region |
| Gray coding | neighbors differ in one bit | a slip costs one bit |
::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE448_L03_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE448_L03_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Looking Ahead
:::{present}
- Lesson 4 opens the SDR that turns a carrier into $I + jQ$.
- Lesson 5 puts a constellation sink on a real signal.
- Lessons 9, 10, and 15 build PAM and PSK receivers on these ideas.
:::

Today we treated the receiver as an ideal box that hands us $(I, Q)$ once per symbol. Lesson 4 opens that box: the mixers that multiply by the cosine and the sine, the filters, and the analog-to-digital converter that produce the complex sample stream. Lesson 5 then puts a real signal into GNU Radio and onto a constellation sink.

The rest of the course builds on this picture. Lessons 9 and 10 build a PAM link and recover its symbol timing, and Lesson 15 does the same for PSK with carrier recovery. In each one we will turn up the noise and watch the clouds grow, just as we did today. Before the next lesson, be able to sketch 2-PAM, 4-PAM, QPSK, and 8-PSK, mark their decision regions, and label 8-PSK with a Gray code.
::::
