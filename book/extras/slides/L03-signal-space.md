<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 448

Software Defined Radios

## Lesson 3 — Signal Space

Spring 2027 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where We Were

- Lesson 2: a link closes when the received power clears the noise floor by the SNR the modem needs
- The drone link delivered 24.2 dB of SNR at 3 km
- We took the modem's 14 dB requirement on faith

Today: **where the required SNR comes from**, and which modulation the drone should use.

Note:
Open by putting the Lesson 2 ledger back on the screen and pointing at the sensitivity line. Today we replace "the modem needs 14 dB" with a number we can look up for any modulation.

---

## Today's Plan

1. What the receiver sees: complex samples and constellations
2. Basis functions, energy, and distance
3. Noise, decision regions, and errors
4. Eb/N0, BER curves, and Gray coding
5. Choosing the drone's modulation
6. Reading a constellation in GNU Radio

Note:
The derivations live in ECE 447. We take the error-rate results as given and spend the time on what they mean for a link.

---

## What the Receiver Sees

<div class="fig" data-inline-svg="./fig/L03-noise-clouds.svg" style="max-width:900px; margin:0 auto;"></div>

One complex sample per symbol, plotted on the I-Q plane, is a constellation; noise turns each point into a cloud.

Note:
QPSK at three SNRs. At 20 dB nothing crosses a boundary; at 10 dB, 2 of 600; at 4 dB, 69 of 600. Ask them to guess which SNR a modem would need before we compute it.

---

## Two Basis Functions

$$s(t) = I\cos(2\pi f_c t) - Q\sin(2\pi f_c t)$$

- Cosine and sine at the same frequency are orthogonal, so $I$ and $Q$ carry two independent numbers.
- Each symbol is a point $(I, Q)$; the two waveforms are its **basis functions**.

Note:
The SDR mixes with a cosine and a sine and hands GNU Radio the pair as one complex number. That is why every course SDR streams complex samples. Lesson 4 opens the hardware.

---

## Constellations

<div class="fig" data-inline-svg="./fig/L03-constellations.svg" style="max-width:1100px; margin:0 auto;"></div>

$M$ points carry $\log_2 M$ bits; at the same energy, more points sit closer together.

Note:
Same transmitter power for all five; the dashed circle is that power. Point at the spacing under each one: 2.00 for BPSK down to 0.63 for 16-QAM. Spacing, not the number of points, sets how much noise a modulation tolerates.

---

## Energy and Distance

| Modulation | Bits/symbol | Closest spacing |
| :-- | :-: | :-: |
| BPSK | 1 | 2.00 |
| QPSK | 2 | 1.41 |
| 4-PAM | 2 | 0.89 |
| 8-PSK | 3 | 0.77 |
| 16-QAM | 4 | 0.63 |

Note:
Unit average symbol energy. QPSK and 4-PAM carry the same two bits, but QPSK uses both axes and spaces its points farther apart. 4-PAM comes back in Lesson 10 as a baseband signal, where only one axis exists.

---

## Noise and Decisions

$$r = s + n$$

- Thermal noise adds an independent Gaussian offset to $I$ and to $Q$, each with variance $N_0/2$.
- The receiver picks the nearest point; the set of samples nearest each point is its **decision region**.

Note:
For QPSK the regions are the quadrants, so the receiver only needs the signs of I and Q. An error is a sample carried across a boundary.

---

<!-- .slide: class="viz-cue-slide" -->

## Constellation Explorer

- QPSK at 8 dB, then 16-QAM at 8 dB: the grid fills its regions.
- About 4 dB more brings 16-QAM back to QPSK's error rate.
- Add a phase offset to QPSK: the clouds rotate toward the boundaries.

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Demo live. Let the measured BER settle onto the predicted value so they see the theory hold. End on the phase offset: at 45 degrees every symbol is wrong with no noise at all, which motivates carrier recovery in Lesson 15.

---

## Error Rate

$$P_s \approx N_\text{nb}\ Q\left(\frac{d_\text{min}}{\sqrt{2N_0}}\right)$$

$$P_b^\text{BPSK} = Q\left(\sqrt{\frac{2E_b}{N_0}}\right)$$

$Q(x)$ is the probability that a unit Gaussian exceeds $x$; $Q(3) = 1.3\times10^{-3}$, $Q(4) = 3.2\times10^{-5}$.

Note:
An error needs the noise to cover half the spacing. The Q function is that Gaussian tail, and it falls by orders of magnitude for each few dB. We use the result; ECE 447 derives it.

---

## Eb/N0, Es/N0, and SNR

$$\frac{E_s}{N_0} = \frac{E_b}{N_0} + 10\log_{10}k \quad \text{(dB)}$$

- $E_b/N_0$ compares modulations fairly, per bit.
- With the receiver bandwidth equal to the symbol rate, $E_s/N_0$ is the SNR of Lesson 2.

Note:
Add 3.0 dB for QPSK, 4.8 dB for 8-PSK, 6.0 dB for 16-QAM. We assume B equals the symbol rate from here on unless a lesson says otherwise.

---

## Bit Error Rate Curves

<div class="fig" data-inline-svg="./fig/L03-ber-curves.svg" style="max-width:720px; margin:0 auto;"></div>

At one error in $10^5$ bits: BPSK and QPSK 9.6 dB, 8-PSK 13.0 dB, 16-QAM 13.4 dB.

Note:
QPSK is two BPSK signals, so per bit it matches BPSK while carrying twice the data. 16-QAM doubles the rate again but needs 3.8 dB more Eb/N0, or 6.9 dB more Es/N0.

---

## Gray Coding

<div class="two-col">
<div class="col-text">

- Neighbors differ in exactly one bit.
- The likely error, to a neighbor, corrupts one bit, so $P_b \approx P_s/k$.

</div>
<div class="col-fig">
<div class="fig" data-inline-svg="./fig/L03-gray-8psk.svg" style="max-width:360px; margin:0 auto;"></div>
</div>
</div>

Note:
Have them label 8-PSK in natural binary and find the neighbors that differ in all three bits: 011 and 100. Gray coding removes that case. Every curve today assumes it.

---

## Choosing the Drone's Modulation

| Modulation | $E_s/N_0$ needed | Margin at 24.2 dB |
| :-- | :-: | :-: |
| QPSK | 12.6 dB | 11.6 dB |
| 8-PSK | 17.7 dB | 6.5 dB |
| 16-QAM | 19.5 dB | 4.7 dB |

Only QPSK keeps 10 dB of margin at 3 km.

Note:
This closes the loop with Lesson 2. The radio's 14 dB matches QPSK's 12.6 dB plus about 1.4 dB for a real demodulator's losses. 16-QAM would double the data rate in the same 1 MHz but would fail first when the drone banks.

---

## Reading a Constellation in GNU Radio

<div class="fig" data-inline-svg="./fig/L03-impairments.svg" style="max-width:1100px; margin:0 auto;"></div>

Noise makes clouds, a phase offset rotates, a frequency offset spins into a ring, and a timing offset smears.

Note:
The constellation sink is the first place to look when a receiver fails. Lesson 9 fixes timing; Lesson 15 fixes phase and frequency. Each fix shows up as these shapes collapsing back into tight clouds.

---

## Key Point

<div class="callout">A modulation is a set of points in the I-Q plane. Noise turns each point into a cloud, and the error rate depends on the spacing between points measured against the noise, so more bits per symbol need more SNR.</div>

Note:
If they keep one number, it is 9.6 dB of Eb/N0 for QPSK at ten to the minus five.

---

## Looking Ahead

- Lesson 4: the SDR hardware that turns a carrier into $I + jQ$
- Lesson 5: a constellation sink on a real signal
- Lessons 9, 10, and 15: PAM and PSK receivers built on these ideas

Note:
Before next time: sketch BPSK, QPSK, 8-PSK, and 16-QAM, Gray-label 8-PSK, and look up the Es/N0 a modulation needs for ten to the minus five.
