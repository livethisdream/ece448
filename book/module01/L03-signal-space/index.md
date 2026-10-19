---
frame_view: true
---

# L3 - Signal Space

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">Signal Space</h1>

<div class="title-rule"></div>

Every digital modulation is a set of points in the I-Q plane, and noise decides how close together those points can sit.

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

::::{frame} What the Receiver Sees
:::{present}
- An SDR delivers complex samples, $I + jQ$.
- One sample per symbol, plotted on the I-Q plane, is a **constellation**.
- The receiver decides which point was sent; noise spreads each point into a cloud.
:::
:::{present}
<img src="../../viz/img/L03-noise-clouds.svg"
     alt="QPSK received through noise at three signal-to-noise ratios. At Es/N0 of 20 dB the four clouds are tight and no symbol crosses a boundary; at 10 dB the clouds widen and 2 of 600 symbols land in the wrong quadrant; at 4 dB the clouds overlap and 69 of 600 are wrong"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::

Lesson 2 ended with a number we took on faith: the drone's modem needed 14 dB of SNR. Today we find out where a number like that comes from, and we do it by looking at the signal the way the receiver does. An SDR hands the computer a stream of complex samples, $I + jQ$. If we take one sample per symbol and plot it on the I-Q plane, the symbols of a digital signal fall at a handful of points, the **constellation**. Demodulating is deciding, for each received sample, which of those points was sent.

The figure shows four-point QPSK at three signal-to-noise ratios. Each transmitted point arrives as a cloud, because the noise floor of Lesson 2 adds a random offset to every sample. At 20 dB the clouds are tight and every symbol lands in its own quadrant. At 4 dB the clouds overlap and more than one symbol in ten lands in the wrong one. Everything in this lesson, from the choice of modulation to the SNR a modem needs, comes from that picture.
::::

::::{frame} Part 1: Two Basis Functions
:::{present}
$$\begin{aligned}
s(t) = {} &I\cos(2\pi f_c t) \\
&- Q\sin(2\pi f_c t)
\end{aligned}$$

- Cosine and sine at the same frequency are orthogonal, so $I$ and $Q$ carry two independent numbers.
- Each symbol is a point $(I, Q)$; the two waveforms are its **basis functions**.
:::

A radio transmits a carrier at frequency $f_c$, and it can change two things about it per symbol: how much cosine and how much sine it sends. Those two waveforms are **orthogonal**: over a symbol the product of $\cos(2\pi f_c t)$ and $\sin(2\pi f_c t)$ averages to zero, so the receiver can recover the cosine amount and the sine amount separately, with no crosstalk between them. That makes the cosine and the sine a pair of **basis functions**, the axes of a two-dimensional **signal space**, and it makes every symbol a point with coordinates $(I, Q)$.

The SDR does that separation in hardware. Its receiver mixes the incoming signal with a cosine and a sine at $f_c$, filters, and digitizes both outputs; Lesson 4 opens the hardware. What arrives in GNU Radio is already the pair $(I, Q)$ for every sample, packed into one complex number. That is why every course SDR streams complex samples, and why a constellation is the natural way to look at a digital signal.
::::

::::{frame} Constellations
:::{present}
<img src="../../viz/img/L03-constellations.svg"
     alt="Five constellations at the same average symbol energy: BPSK with two points 2.00 apart, 4-PAM with four points on a line 0.89 apart, QPSK with four points 1.41 apart, 8-PSK with eight points on a circle 0.77 apart, and 16-QAM with a four-by-four grid 0.63 apart"
     style="max-width: 900px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- $M$ points carry $k = \log_2 M$ bits per symbol.
- At the same average energy, more points sit closer together.
:::

Each modulation is a choice of points. **BPSK** uses two, on the I axis, and carries one bit per symbol. **4-PAM** puts four on the same line. **QPSK** uses four on a circle, one per quadrant, and carries two bits. **8-PSK** puts eight on the circle, and **16-QAM** fills a four-by-four grid. A constellation with $M$ points carries $k = \log_2 M$ bits per symbol, so more points move more data in the same bandwidth.

The figure draws all five at the same average symbol energy, the same transmitter power. The dashed circle is that energy. More points in the same energy means the points sit closer together, and the closest spacing, printed under each one, falls from 2.00 for BPSK to 0.63 for 16-QAM. That spacing, not the number of points, sets how much noise a modulation can tolerate.
::::

::::{frame} Energy and Distance
:::{present}
| Modulation | Bits/symbol | Closest spacing |
| :-- | :-: | :-: |
| BPSK | 1 | 2.00 |
| QPSK | 2 | 1.41 |
| 4-PAM | 2 | 0.89 |
| 8-PSK | 3 | 0.77 |
| 16-QAM | 4 | 0.63 |
:::
:::{present}
- Spacing at unit average symbol energy $E_s$.
- QPSK spaces two bits per symbol farther apart than 4-PAM.
:::

The energy of a symbol is its squared distance from the origin, $\vert s\vert^2 = I^2 + Q^2$, and the average over the constellation is the **symbol energy** $E_s$. With $E_s$ fixed, what matters for errors is the **minimum distance** $d_\text{min}$ between neighboring points, because noise causes an error by pushing a sample across the halfway line to a neighbor.

QPSK and 4-PAM both carry two bits per symbol, but QPSK spreads its four points over both axes while 4-PAM crowds them onto one. QPSK's spacing is 1.41 against 0.89 for 4-PAM, which is why radios use QPSK rather than 4-PAM on a carrier. 4-PAM still has its place: Lesson 9 shapes it as a baseband signal, where only one axis exists.
::::

::::{frame} Part 2: Noise and Decisions
:::{present}
$$r = s + n$$

- Thermal noise adds an independent Gaussian offset to $I$ and to $Q$, each with variance $N_0/2$.
- The receiver picks the nearest point; the set of samples closest to each point is its **decision region**.
:::

The received sample $r$ is the transmitted point $s$ plus a noise sample $n$. Thermal noise, the $kTB$ of Lesson 2, is additive white Gaussian noise (AWGN), and it adds an independent Gaussian offset to each axis with variance $N_0/2$, where $N_0$ is the noise power per hertz. In the I-Q plane that makes a round cloud centered on each transmitted point, and its radius grows as the SNR falls.

The best guess for equally likely symbols in Gaussian noise is the nearest point. Every sample closer to one point than to any other falls in that point's **decision region**, and the boundaries sit halfway between neighbors. For QPSK the regions are the four quadrants, so the receiver needs only the signs of $I$ and $Q$. For BPSK the boundary is the Q axis. An error happens when noise carries a sample across a boundary, which is what the red points in the opening figure did.
::::

::::{frame} Constellation Explorer
:class: viz-frame

:::{depth}
The widget transmits random symbols, adds Gaussian noise at the chosen $E_b/N_0$, and decides each one by the nearest point. The shaded tiles are the decision regions, and a symbol that lands in the wrong one turns red. Watch the measured bit error rate settle onto the predicted value as the symbols accumulate. Start on QPSK at 8 dB, then switch to 16-QAM at the same $E_b/N_0$: the grid fills its regions edge to edge and the error count climbs, because its points are 0.63 apart instead of 1.41. Raise $E_b/N_0$ until 16-QAM is as clean as QPSK was, about 4 dB more. Then return to QPSK and add a phase offset: the clouds rotate toward the boundaries, and past $45^\circ$ every symbol would be wrong even with no noise at all, which is why the receivers of Lessons 9 and 15 correct the phase before they decide.
:::

:::{present}
<iframe src="../../viz/constellation-explorer.html"
        width="100%" height="411"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Constellation explorer: random symbols for BPSK, QPSK, 8-PSK, 4-PAM, or 16-QAM through Gaussian noise at a chosen Eb/N0 and phase offset, with the decision regions shaded, errors in red, and measured against predicted bit error rate">
</iframe>
:::
::::

::::{frame} Part 3: Error Rate
:::{present}
$$P_s \approx N_\text{nb}\ Q\left(\frac{d_\text{min}}{\sqrt{2N_0}}\right)$$

$$P_b^\text{BPSK} = Q\left(\sqrt{\frac{2E_b}{N_0}}\right)$$

- $Q(x)$ is the probability a unit Gaussian exceeds $x$.
- $N_\text{nb}$ counts the nearest neighbors.
:::

An error needs the noise along the line to a neighbor to exceed half the spacing, $d_\text{min}/2$. The noise along any direction is Gaussian with standard deviation $\sqrt{N_0/2}$, so the probability of crossing one boundary is the Gaussian tail beyond $(d_\text{min}/2)/\sqrt{N_0/2}$, which is the argument on the slide. The **Q function** is that tail: $Q(x)$ is the probability that a zero-mean, unit-variance Gaussian exceeds $x$. It falls fast, from $Q(1) = 0.16$ to $Q(3) = 1.3\times10^{-3}$ and $Q(4) = 3.2\times10^{-5}$. A point with $N_\text{nb}$ neighbors can cross any of their boundaries, so the symbol error rate is about $N_\text{nb}$ times that tail.

For BPSK the two points are $2\sqrt{E_b}$ apart and each has one neighbor, which gives the second expression. We will use these results rather than derive them; ECE 447 does the derivation. The practical content is that the error rate depends only on the spacing measured against the noise, $d_\text{min}/\sqrt{N_0}$, and that it drops by orders of magnitude for each few dB once that ratio is large.
::::

::::{frame} Eb/N0, Es/N0, and SNR
:::{present}
$$\frac{E_s}{N_0}\bigg\vert_\text{dB} = \frac{E_b}{N_0}\bigg\vert_\text{dB} + 10\log_{10}k$$

- $E_b/N_0$ compares modulations fairly, per bit.
- With the receiver bandwidth equal to the symbol rate, $E_s/N_0$ is the SNR of Lesson 2.
:::

Three signal-to-noise ratios appear in practice, and they measure the same thing on different scales. $E_s/N_0$ is the symbol energy over the noise density. A symbol carries $k$ bits, so the energy per bit is $E_b = E_s/k$, and $E_b/N_0$ is the fair way to compare modulations that carry different numbers of bits; BER curves always use it. Converting adds $10\log_{10}k$ dB: 3.0 dB for QPSK, 4.8 dB for 8-PSK, 6.0 dB for 16-QAM.

The SNR of Lesson 2 is a power ratio in the receiver's bandwidth $B$. Signal power is $E_s$ times the symbol rate $R_s$, and noise power is $N_0 B$, so $\text{SNR} = (E_s/N_0)(R_s/B)$. A receiver filtered to its symbol rate has $B = R_s$, and then $E_s/N_0$ and the SNR are the same number. We will assume that from here on unless a lesson says otherwise.
::::

::::{frame} Bit Error Rate Curves
:::{present}
<img src="../../viz/img/L03-ber-curves.svg"
     alt="Bit error rate against Eb/N0 from 0 to 20 dB. BPSK and QPSK share one curve and reach one error in 100,000 bits at 9.6 dB; 8-PSK reaches it at 13.0 dB; 16-QAM and 4-PAM share a curve and reach it at 13.4 dB"
     style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- BPSK and QPSK need 9.6 dB for one error in $10^5$ bits.
- Each step up in bits per symbol needs more $E_b/N_0$.
:::

The curves plot the bit error rate against $E_b/N_0$ for the five constellations. BPSK and QPSK sit on the same curve: QPSK is two BPSK signals on the cosine and the sine, so per bit it performs exactly as well while carrying twice the data. Gray-coded 16-QAM is likewise two 4-PAM signals, so those two share a curve as well. At a bit error rate of $10^{-5}$, a common target for an uncoded link, BPSK and QPSK need 9.6 dB, 8-PSK needs 13.0 dB, and 16-QAM needs 13.4 dB.

Read the curves as a trade. Moving from QPSK to 16-QAM doubles the bits per symbol, and so doubles the data rate in the same bandwidth, but it needs 3.8 dB more $E_b/N_0$, or 6.9 dB more $E_s/N_0$, for the same error rate. Whether that trade is worth making depends on the margin the link budget leaves, which is the next worked example.
::::

::::{frame} Gray Coding
:::{present}
<img src="../../viz/img/L03-gray-8psk.svg"
     alt="8-PSK with Gray-coded labels: going around the circle, 000, 001, 011, 010, 110, 111, 101, 100, each differing from its neighbors in one bit"
     style="max-width: 340px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Neighbors differ in exactly one bit.
- The likely error, to a neighbor, corrupts one bit, so $P_b \approx P_s/k$.
:::

Which bits go on which point is a design choice, and it matters. Almost every symbol error is a slip to a nearest neighbor, so the labels should make that slip corrupt as few bits as possible. **Gray coding** labels the points so that neighbors differ in exactly one bit, as in the 8-PSK figure. A symbol error then corrupts one of the $k$ bits, and the bit error rate is about the symbol error rate divided by $k$. With a natural binary order instead, the slip from 011 to 100 between two adjacent points would corrupt all three bits. Every BER curve in this lesson assumes Gray coding, and every modulator we build will use it.
::::

::::{frame} Worked Example: A Modulation for the Drone
:::{present}
| Modulation | $E_s/N_0$ needed | Margin at 24.2 dB |
| :-- | :-: | :-: |
| QPSK | 12.6 dB | 11.6 dB |
| 8-PSK | 17.7 dB | 6.5 dB |
| 16-QAM | 19.5 dB | 4.7 dB |
:::
:::{present}
- Only QPSK keeps 10 dB of margin at 3 km.
:::

:::{admonition} Worked example — choosing the drone's modulation
:class: tip
Lesson 2's drone link delivers an SNR of 24.2 dB in 1 MHz at 3 km. Take the receiver bandwidth equal to the symbol rate, so $E_s/N_0 = 24.2$ dB, and ask for a bit error rate of $10^{-5}$.

The BER curves give the $E_b/N_0$ each modulation needs, and adding $10\log_{10}k$ converts it to $E_s/N_0$:

| Modulation | $k$ | $E_b/N_0$ | $E_s/N_0$ | Margin |
| :-- | :-: | :-: | :-: | :-: |
| QPSK | 2 | 9.6 dB | 12.6 dB | 11.6 dB |
| 8-PSK | 3 | 13.0 dB | 17.7 dB | 6.5 dB |
| 16-QAM | 4 | 13.4 dB | 19.5 dB | 4.7 dB |

QPSK meets the 10 dB goal with 1.6 dB left over. 16-QAM would double the data rate in the same 1 MHz but leaves only 4.7 dB of margin, so it would fail first when the drone banks or flies past 5 km. The 14 dB the radio's datasheet quoted in Lesson 2 matches QPSK's 12.6 dB plus about 1.4 dB allowed for the losses of a real demodulator, which Lessons 9 and 15 measure.
:::
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

GNU Radio's constellation sink plots received samples exactly as in this lesson, and it is the fastest diagnostic a radio engineer has, because each problem leaves its own shape. **Noise** spreads each point into a round cloud, and the cloud's size reads the SNR. A **phase offset** between the transmitter and receiver oscillators rotates the whole constellation. A **frequency offset** makes that rotation continuous, so the points smear into a ring. A **timing offset**, sampling each symbol off its peak, mixes in neighboring symbols and smears each point into a spread that noise does not explain.

Lesson 9 recovers symbol timing for PAM, and Lesson 15 recovers carrier phase and frequency for PSK. Each fix shows up on the constellation sink as these shapes collapsing back into tight clouds, and that is how we will check every receiver we build.
::::

::::{frame} Key Point
:::{present}
:class: callout
A modulation is a set of points in the I-Q plane. Noise turns each point into a cloud, and the error rate depends on the spacing between points measured against the noise, so more bits per symbol need more SNR.
:::
::::

::::{frame} Summary
:class: read-only

| Idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Basis functions | $\cos$ and $\sin$ at $f_c$; axes $I$ and $Q$ | one complex sample per symbol |
| Constellation | the $M$ points a modulation uses | $k = \log_2 M$ bits/symbol |
| Decision region | samples nearest each point | QPSK: the four quadrants |
| Error rate | $N_\text{nb}\ Q(d_\text{min}/\sqrt{2N_0})$ | $Q(4) = 3.2\times10^{-5}$ |
| $E_s/N_0$ | $E_b/N_0 + 10\log_{10}k$ | equals SNR when $B = R_s$ |
| BER $10^{-5}$ | $E_b/N_0$ needed | BPSK/QPSK 9.6, 8-PSK 13.0, 16-QAM 13.4 dB |
| Gray coding | neighbors differ in one bit | $P_b \approx P_s/k$ |
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

The rest of the course builds on this picture. Lessons 9 and 10 build a PAM link and recover its symbol timing, and Lesson 15 does the same for PSK with carrier recovery. Before the next lesson, be able to sketch BPSK, QPSK, 8-PSK, and 16-QAM, label 8-PSK with a Gray code, and look up the $E_s/N_0$ a modulation needs for a bit error rate of $10^{-5}$.
::::
