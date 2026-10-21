---
frame_view: true
---

# L15 - mPSK

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">mPSK</h1>

<div class="title-rule"></div>

BPSK, QPSK, and 8PSK in GNU Radio, with carrier and symbol-timing recovery.

Lesson 15 · Module 6: Waveform Applications & RF Reverse Engineering · Dr. Neil Rogers
::::

::::{frame} Slides
:class: read-only

:::{admonition} Slides
:class: slides
<a href="../../slides/L15-mpsk.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L15-mpsk.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L15-mpsk.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '6'; counter-reset: lo 3">
  <li>I can implement an mPSK modulator and demodulator (BPSK, QPSK, 8PSK), recover carrier and symbol timing, and verify constellation behavior against theory.</li>
</ol>
::::

::::{frame} Text over QPSK
:::{present}
<img src="../../viz/img/L15-link-clean.png"
     alt="The L15 link flowgraph running QPSK at an Eb/N0 of 12 dB with a 50 Hz frequency offset: before carrier recovery the Symbol Sync output is a ring, after the Costas Loop it is four tight clusters, the frequency estimate sits at 50 Hz, and the labels read USAFA ECE 448: ASCII over mPSK. and 244 correct of 244 received in 12 s, BER 0 in 62,464 bits"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The L10 text link now sends two bits per symbol on the phase of a carrier.
- The receiver has to find the carrier's phase and frequency before it can decide.
:::

The figure is today's flowgraph, `L15-psk-link.grc`, running. It sends the same packets of text as Lesson 10, but each symbol now carries two bits as one of four phases, which is **QPSK**. The channel adds noise, and here its frequency offset slider is set to move the carrier 50 Hz away from where the receiver expects it; the slider opens at 0.

The left plot shows the received symbols after timing recovery. They form a ring, because the frequency offset turns the constellation a little further with every symbol. The middle plot shows the same symbols after **carrier recovery**, which a **Costas Loop** does: the ring becomes four clusters, and the text arrives. Today we build each part of this link and measure it against the bit error rates of Lesson 3.
::::

::::{frame} Phase-Shift Keying
:::{present}
<img src="../../viz/img/L15-tx-constellations.png"
     alt="Three QT GUI constellation plots from L15-psk-tx.grc: BPSK with two points at plus and minus 1 on the I axis, QPSK with four points at 45, 135, 225, and 315 degrees, and 8PSK with eight points at 22.5 degrees plus multiples of 45 degrees, all on the unit circle"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- $M$ phases on a circle carry $k = \log_2 M$ bits per symbol.
- BPSK, QPSK, and 8PSK carry 1, 2, and 3 bits.
:::

**M-ary phase-shift keying** (mPSK) puts $M$ points on a circle of radius 1. Every point has the same amplitude, so only the phase carries information. Lesson 3 introduced these constellations; here they come from `L15-psk-tx.grc`, with a chooser that switches $M$ while the flowgraph runs.

A constellation with $M$ points carries $k = \log_2 M$ bits per symbol. At the same symbol rate, QPSK sends twice as many bits as BPSK, and 8PSK three times as many. The points of QPSK sit at 45° plus multiples of 90°, and those of 8PSK at 22.5° plus multiples of 45°, because those are the positions the Costas Loop's detectors expect.
::::

::::{frame} The Transmitter in GNU Radio
:::{present}
<img src="../../viz/img/L15-grc-tx.png"
     alt="The L15 transmitter flowgraph in GNU Radio Companion: a Random Source of values 0 to 7, Chunks to Symbols with the table of points, a Throttle at 4 kHz, and an Interpolating FIR Filter with the RRC taps, feeding a constellation sink, a time sink, and a frequency sink; a QT GUI Chooser sets M"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- **Chunks to Symbols** looks up each symbol's point; the L9 RRC filter shapes it.
- Every $M$ fills the same 5.4 kHz band.
:::

The transmitter is Lesson 9's, with complex points in place of real levels. **Chunks to Symbols** takes a number from 0 to $M - 1$ and outputs that point of the constellation, and the Interpolating FIR Filter shapes it with the same RRC taps as Lesson 9: $\alpha = 0.35$, 8 samples per symbol, and 32 kHz sampling, so 4,000 symbols a second. GNU Radio also has a **Constellation Modulator** block, which packs the bit grouping, the mapping, and the RRC filter into one block; we build the chain from its parts so that each step is visible.

The spectrum does not change with $M$. The band is $(1 + \alpha) R_s = 1.35 \times 4$ kHz $= 5.4$ kHz wide whether each symbol carries one bit or three. More bits per symbol move more data through the same bandwidth, but each extra bit needs more $E_b/N_0$, as Lesson 3 measured.
::::

::::{frame} Bits to Points with Gray Coding
:::{present}
<img src="../../viz/img/L15-8psk-map.svg"
     alt="The L15 8PSK constellation: eight points on the unit circle at 22.5 degrees plus multiples of 45, each marked with its phase index 0 to 7 counterclockwise from the first quadrant and with its Gray label: 000, 001, 011, 010, 110, 111, 101, 100"
     style="max-width: 420px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- **Repack Bits** groups the bits $k$ at a time.
- A **Map** block turns each group into a phase index with a Gray code.
- Neighbors differ in one bit.
:::

The text arrives as bytes, so the link flowgraph uses **Repack Bits** to regroup each byte's bits $k$ at a time, most significant first. A **Map** block then turns each $k$-bit group into a **phase index** $i$, the number of steps of $360°/M$ counterclockwise from the first point. The figure shows the map for 8PSK: the index is in amber and the bits it carries are in blue.

The labels follow a **Gray code**, as in Lesson 3, so that the two neighbors of any point differ from it in exactly one bit. Almost every symbol error is a slip to a neighbor, so one symbol error corrupts one bit. The Gray label of index $i$ is $i \oplus (i \gg 1)$, the index XORed with itself shifted right one bit; the flowgraph computes it as the variable `gray`, and the transmitter's Map uses its inverse, `ungray`.
::::

::::{frame} Bits per Symbol
:class: read-only

At $R_s = 4{,}000$ symbols per second, each modulation fills the same 5.4 kHz and carries $k$ bits per symbol:

| Modulation | $M$ | $k$ | Bit rate | $E_b/N_0$ for BER $10^{-5}$ (Lesson 3) | $E_s/N_0$ for BER $10^{-5}$ |
| :-- | :-: | :-: | :-: | :-: | :-: |
| BPSK | 2 | 1 | 4 kb/s | 9.6 dB | 9.6 dB |
| QPSK | 4 | 2 | 8 kb/s | 9.6 dB | 12.6 dB |
| 8PSK | 8 | 3 | 12 kb/s | 13.0 dB | 17.7 dB |

$E_s/N_0$ is $E_b/N_0$ plus $10 \log_{10} k$, which is 3.0 dB for QPSK and 4.8 dB for 8PSK. QPSK doubles the bit rate of BPSK at the same $E_b/N_0$, which is why most links use it in place of BPSK. 8PSK adds another 50% but needs 3.4 dB more $E_b/N_0$ for the same error rate.

The link flowgraph's slider sets $E_b/N_0$ directly. The transmitted signal has power 1 and 8 samples per symbol, so each symbol carries energy 8 and each bit $8/k$, and the flowgraph sets the noise amplitude to

$$\sigma = \sqrt{\frac{8}{k \cdot 10^{(E_b/N_0)/10}}}.$$
::::

::::{frame} The Receiver
:::{present}
<img src="../../viz/img/L15-grc-link.png"
     alt="The L15 link flowgraph in GNU Radio Companion: the L10 packet transmitter, Repack Bits 8 to k, a Map, a Differential Encoder and a Selector, Chunks to Symbols, Throttle, and the RRC filter; a Channel Model; then the matched filter, Symbol Sync, the Costas Loop, a Constellation Decoder, a Differential Decoder and a Selector, a Map, Repack Bits k to 1, Correlate Access Code - Tag Stream, Repack Bits 1 to 8, and the Text Sink, with two constellation sinks and a time sink of the loop's frequency"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The matched filter and **Symbol Sync** keep Lesson 9's settings.
- A **Costas Loop** removes the carrier's phase and frequency error.
- A **Constellation Decoder** picks the nearest point.
:::

The top row is the transmitter: Lesson 10's packets, Repack Bits, the Gray Map, and Chunks to Symbols, with a Differential Encoder that a later frame explains. A **Channel Model** block stands in for the radio path. It adds Gaussian noise, a frequency offset, a fixed phase rotation, and a clock error, each set by a slider.

The receiver keeps Lesson 9's matched filter and Symbol Sync with the same settings: Gardner detector, 8 samples per symbol, loop bandwidth 0.045. The **Costas Loop** follows, with its order set to $M$. The **Constellation Decoder** outputs the phase index of the nearest point, and from there the receiver undoes each transmitter step in reverse order and hands the bits to Lesson 10's access-code search and Text Sink. The Text Sink now also counts the bit errors in every line it receives, which gives the link's bit error rate (BER).
::::

::::{frame} What the Channel Does
:::{present}
- Noise spreads each point into a cloud.
- A fixed phase rotates the constellation.
- A frequency offset spins it into a ring.
- A clock error slides the sampling instant.
:::

Lesson 3 showed these four problems on a QPSK constellation, and the Channel Model adds all four. A real receiver meets every one of them. The transmitter and receiver oscillators are never exactly equal, so the carrier arrives a few hertz to kilohertz away from where the receiver tunes, and the path length sets an unknown phase. The two sample clocks also differ, which is the clock error Symbol Sync tracked in Lesson 10.

A frequency offset $\Delta f$ turns the constellation by $360° \times \Delta f / R_s$ every symbol. At 50 Hz and 4,000 symbols per second that is 4.5° per symbol, so the points go once around the circle every 80 symbols and land everywhere on the ring, as in the opening figure, and the receiver has to remove that rotation before it decides any symbol.
::::

::::{frame} Order of Recovery
:::{present}
- Symbol Sync finds the sampling instant with the carrier still spinning.
- The Costas Loop then works at one sample per symbol.
:::

The receiver recovers the timing first. Gardner's detector compares samples taken half a symbol apart, and a carrier that turns only a few degrees per symbol barely changes that comparison, so Symbol Sync locks with the frequency offset still present. Its output is one sample per symbol at the right instant, which is the ring in the left plot of the opening figure.

The Costas Loop then needs only those samples. Working at the symbol rate, it sees one clean point per symbol and has 8 times fewer samples to process than it would before Symbol Sync. The order matters in the other direction too: a carrier loop placed before timing recovery would see samples taken between symbols, where the points are not on the constellation.
::::

::::{frame} The Costas Loop
:::{present}
<img src="../../viz/img/L15-costas.svg"
     alt="Block diagram of the Costas Loop: symbols in are rotated back by the phase estimate and go out; the rotated symbols also go to a phase-error detector of order M, then a loop filter whose state is the frequency estimate, then the phase estimate, which sets the rotation"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Rotate each symbol back, measure how far it misses a point, and correct the estimate.
- The loop tracks both phase and frequency.
:::

The **Costas Loop** keeps an estimate of the carrier's phase and rotates each incoming symbol back by it. A **phase detector** then measures how far the rotated symbol sits from the nearest constellation point, without knowing which point was sent. For BPSK it uses the product $I \times Q$, which is zero on the I axis. For QPSK GNU Radio's detector uses the signs of $I$ and $Q$ to find the nearest point, and for 8PSK it also checks which of $|I|$ and $|Q|$ is larger; that is why the loop needs the order $M$, and why the points have to sit where the detector expects them.

A **loop filter** turns the error into two corrections, a small step in phase and a smaller change in frequency, as Symbol Sync did for timing in Lesson 9. The frequency part makes the loop follow a constant offset with no lasting phase error. The block's second output is that frequency estimate, in radians per symbol, and the flowgraph scales it by $R_s/2\pi$ to plot it in hertz. The loop bandwidth, 0.02 here, sets how fast the loop responds: a wider loop locks faster from a larger offset but lets more noise into the phase estimate.
::::

::::{frame} Acquisition
:::{present}
<img src="../../viz/img/L15-link-acquire.png"
     alt="The L15 link with QPSK at 12 dB and a 200 Hz frequency offset: the Costas Loop's frequency estimate rises from 0 to 200 Hz in about 0.7 s and stays there, the Costas output shows four clusters, and every line of text arrives"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The loop starts at 0 Hz and reaches the 200 Hz offset in under a second.
- The text arrives once it locks.
:::

Here the frequency offset is 200 Hz, and the loop starts from 0 Hz. The right plot shows the frequency estimate climbing to 200 Hz and settling there in about 0.7 s, about 2,800 symbols. Until it settles the constellation keeps turning and the packets fail; after that the four clusters hold still and every line arrives.

The time a loop takes to lock is its **acquisition time**, and the range of offsets from which it locks at all is its **pull-in range**. Both depend on the loop bandwidth, the constellation, and the noise.
::::

::::{frame} Pull-In Range
:::{present}
<img src="../../viz/img/L15-link-nolock.png"
     alt="The L15 link with QPSK at 12 dB and a 450 Hz frequency offset: the frequency estimate settles at about minus 50 Hz instead of 450 Hz, the Costas output shows eight clusters instead of four, and no packet arrives"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- At 450 Hz the QPSK loop settles at −50 Hz, a **false lock**.
- Its pull-in range shrinks as $M$ grows.
:::

At 450 Hz the QPSK loop does not lock. Its estimate settles near −50 Hz, 500 Hz from the true offset. The symbols then keep turning by $360° \times 500/4000 = 45°$ each, so they alternate between the four QPSK positions and the four positions between them, and the plot shows eight clusters. The detector's error averages to zero there, so the loop stays. This is a **false lock**, and no packet arrives.

The detector sees the constellation repeat every $360°/M$, so it can only sort out a phase error smaller than $180°/M$. With more points that limit is smaller, and the pull-in range shrinks as $M$ grows. A real receiver therefore corrects most of the frequency error before the Costas Loop, often with a frequency-locked loop such as GNU Radio's **FLL Band-Edge** block, and leaves the Costas Loop only the last few tens of hertz.
::::

::::{frame} Measured Pull-In
:class: read-only

We measured the loop with the flowgraph's blocks running headless at $E_b/N_0 = 12$ dB, starting cold six times at each offset with a different channel phase and noise, and counted a lock when the frequency estimate stayed within 10% of the offset to the end of a 15 s run.

| Offset | BPSK locks | Median time | QPSK locks | Median time |
| :-: | :-: | :-: | :-: | :-: |
| 300 Hz | 6 of 6 | 2.9 s | 6 of 6 | 2.0 s |
| 375 Hz | 6 of 6 | 5.2 s | 6 of 6 | 4.1 s |
| 400 Hz | 6 of 6 | 5.9 s | 3 of 6 | 3.2 s |
| 450 Hz | 6 of 6 | 7.6 s | 0 of 6 | – |
| 500 Hz | 6 of 6 | 10.0 s | 0 of 6 | – |
| 600 Hz | 0 of 6 | – | 0 of 6 | – |

At 4,000 symbols per second, BPSK pulls in from about 500 Hz and QPSK from about 375 Hz, roughly a tenth of the symbol rate. The acquisition time grows steeply near the limit. Noise changes the range too: the sign-based QPSK detector gives almost no correction to a fast-turning constellation without noise, and at 20 dB the same loop pulled in reliably only from about 200 Hz.

The PlutoSDR's own oscillator is accurate to about 25 ppm, so two radios at 915 MHz can differ by up to about 46 kHz, a hundred times the Costas Loop's range. The L15 Lab uses one Pluto, whose transmitter and receiver share the same reference, so its frequency offset is close to zero.
::::

::::{frame} Phase Ambiguity
:::{present}
<img src="../../viz/img/L15-link-ambiguity.png"
     alt="The L15 link with QPSK, no frequency offset, differential coding off (diff = 0), and the channel phase at 90 degrees: the Symbol Sync and Costas Loop outputs both show four clean clusters, the frequency estimate sits at 0 Hz, but the Received label still says waiting for a packet and no line has arrived"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The constellation looks perfect, but no text arrives.
- The loop locked one point away, $90°$ off.
:::

The figure removes the frequency offset, turns the channel phase to 90°, and switches differential coding off. The Costas Loop locks and the four clusters look perfect, yet no packet arrives. The loop has no way to tell which point is which: a QPSK constellation turned by 90° looks exactly like the original, so the loop locks to whichever of the $M$ rotations is nearest the received phase. Every decision is then one point off, every bit pattern changes, and the access code never matches.

This is the **phase ambiguity** that Lesson 10's PlutoSDR link met as a polarity switch. A BPSK loop can lock right side up or upside down. A QPSK loop can lock in 4 positions and an 8PSK loop in 8, so on a real radio, where the channel phase is random, the text would arrive only on the runs that happen to lock in the right one.
::::

::::{frame} Differential Coding
:::{present}
| Index sent | 0 | 1 | 3 | 3 | 2 |
| :-- | :-: | :-: | :-: | :-: | :-: |
| Received, one step off | 1 | 2 | 0 | 0 | 3 |
| Change, mod 4 | – | 1 | 2 | 0 | 3 |
:::
:::{present}
- Send the data as the change in phase.
- A rotation shifts every index but not the changes.
:::

**Differential coding** removes the ambiguity. The **Differential Encoder** adds each new phase index to the last one it sent, mod $M$, so the data rides on the change in phase from one symbol to the next. The **Differential Decoder** subtracts the index before it from each received index, mod $M$. A loop that locked one step off adds 1 to every received index, and the differences do not change. The table shows QPSK: the data 1, 2, 0, 3 arrives as the changes whatever the rotation. The differential-encoding tutorial in the references works the same idea for bits.

Differential coding has one drawback in noise. One wrong decision spoils two differences, the one into it and the one out of it, so the bit error rate roughly doubles. In the flowgraph the encoder and decoder each sit beside a **Selector**, and the variable `diff`, 1 or 0, picks the coded or the uncoded path at both ends; change it and run the flowgraph again.
::::

::::{frame} Carrier Recovery Explorer
:class: viz-frame

:::{depth}
The explorer runs GNU Radio's Costas Loop at one sample per symbol for 10 s at 4,000 symbols per second. The left panel shows the loop's output for the last 600 symbols, with the ideal points as amber rings; the right panel shows the frequency estimate, with the true offset dashed. Start with QPSK at 12 dB and 100 Hz: the loop locks within a fraction of a second. Raise the offset in 25 Hz steps until it no longer locks. Then set the offset to 0, turn differential coding off, and step the channel phase: the lock rotation readout jumps in steps of $360°/M$, and the BER is 0 only when the rotation is 0°. With differential coding on, the BER stays low at every phase. Finally, raise $E_b/N_0$ to 30 dB at 300 Hz and press "new noise" a few times: with little noise the QPSK loop often fails to pull in at all.
:::

:::{present}
<iframe src="../../viz/psk-carrier.html"
        width="100%" height="450"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Carrier recovery explorer: the Costas Loop locking to BPSK, QPSK, or 8PSK symbols with a chosen frequency offset, channel phase, and Eb/N0, with its frequency estimate, its lock rotation, and the bit error rate with and without differential coding">
</iframe>
:::
::::

::::{frame} Noise: Measured against Theory
:::{present}
<img src="../../viz/img/L15-ber-measured.svg"
     alt="Bit error rate against Eb/N0 from 0 to 16 dB: Lesson 3's theory curves for BPSK and QPSK and for 8PSK, with the L15 link's measured points at even Eb/N0, filled without differential coding and open with it; the filled points sit just above the curves and the open points about twice as high"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The link stays within 0.3 dB of Lesson 3's curves at $10^{-4}$.
- Differential coding adds 0.3 to 0.4 dB.
:::

The figure plots the simulated link's measured bit error rate on Lesson 3's theory curves. The filled points are coherent, with differential coding off and the channel phase at 0°, so the loop locks in the right position; the open points have differential coding on. QPSK falls on the BPSK curve, as Lesson 3 predicted, and 8PSK needs about 3.3 dB more $E_b/N_0$ for a BER of $10^{-4}$.

The receiver loses a little to its loops. The jitter in Symbol Sync's sampling instant and in the Costas Loop's phase estimate adds about 0.2 dB of loss for QPSK and 0.3 dB for 8PSK at a BER of $10^{-4}$. Differential coding roughly doubles the error rate, which adds another 0.3 to 0.4 dB. Lesson 3 allowed 1.4 dB for a real demodulator; the simulation uses less than that, and the L15 Lab measures what the PlutoSDR adds.
::::

::::{frame} Noise Sweep
:class: read-only

We measured the link with its blocks running headless, without the Throttle, between $3 \times 10^5$ and $1.2 \times 10^7$ bits at each point, and compared the received bits with the transmitted ones. "Coherent" has differential coding off and the channel phase at 0°.

| $E_b/N_0$ | QPSK theory | QPSK coherent | QPSK differential | 8PSK theory | 8PSK coherent | 8PSK differential |
| :-: | :-: | :-: | :-: | :-: | :-: | :-: |
| 4 dB | $1.25 \times 10^{-2}$ | $1.6 \times 10^{-2}$ | $3.0 \times 10^{-2}$ | | | |
| 6 dB | $2.39 \times 10^{-3}$ | $3.2 \times 10^{-3}$ | $6.1 \times 10^{-3}$ | | | |
| 8 dB | $1.91 \times 10^{-4}$ | $2.7 \times 10^{-4}$ | $6.2 \times 10^{-4}$ | $6.2 \times 10^{-3}$ | lost lock | $1.6 \times 10^{-2}$ |
| 10 dB | $3.9 \times 10^{-6}$ | $7.8 \times 10^{-6}$ | $1.3 \times 10^{-5}$ | $1.01 \times 10^{-3}$ | $1.4 \times 10^{-3}$ | $2.7 \times 10^{-3}$ |
| 12 dB | | | | $6.3 \times 10^{-5}$ | $1.1 \times 10^{-4}$ | $2.1 \times 10^{-4}$ |
| 14 dB | | | | $8.8 \times 10^{-7}$ | $1.8 \times 10^{-6}$ | $4.2 \times 10^{-6}$ |

The theory columns are Lesson 3's: $Q\left(\sqrt{2E_b/N_0}\right)$ for QPSK, and for 8PSK with Gray coding

$$P_b \approx \frac{2}{3} Q\left(\sqrt{\frac{6E_b}{N_0}} \sin\frac{\pi}{8}\right).$$

Below about 4 dB for QPSK and 10 dB for 8PSK, noise makes the Costas Loop slip to another lock position now and then. Without differential coding a slip turns every later decision, and the coherent 8PSK link at 8 dB lost lock that way, after which a third or more of its bits were wrong; with differential coding a slip corrupts only the symbol where it happens, which is a second reason real mPSK links use it.
::::

::::{frame} mPSK on a Real Radio
:::{present}
- The L15 Lab sends QPSK through one PlutoSDR, TX port to RX port, with a 30 dB attenuator.
- The Pluto blocks and an AGC replace the Channel Model.
- Nothing in L15 transmits over the air.
:::

The L15 Lab moves this link onto a PlutoSDR. The transmit half ends at a PlutoSDR Sink at 915 MHz instead of the Channel Model, and the receive half starts at a PlutoSDR Source, with the same matched filter, Symbol Sync, Costas Loop, decoder, and text search. As in L10 and L12, a Rational Resampler raises the 32 kHz stream by 32, to 1.024 MS/s, on the way out and lowers it again on the way in, and an **AGC** after it holds the received level near amplitude 1 at any attenuation. The radio supplies the phase ambiguity on its own: every time the flowgraph starts, the carrier arrives with a new phase, and differential coding decides whether the text still arrives.

In class we transmit only into a cable, into a shielded enclosure, or at very low power in an ISM band, and only when the lesson says to. Nothing in this lesson transmits; the L15 Lab transmits from the Pluto's TX port through an inline 30 dB attenuator into its own RX port. We have run the PlutoSDR flowgraph only in simulation, with a model of the cable in place of the radio, so the lab is its first run on hardware.
::::

::::{frame} Key Point
:::{present}
:class: callout
mPSK sends $\log_2 M$ bits per symbol on the carrier's phase. Symbol Sync recovers the timing, a Costas Loop removes the frequency and phase error, and differential coding removes the $360°/M$ ambiguity.
:::
::::

::::{frame} Downloads
:class: read-only doc-links

- <a class="doc-link" href="../../grc/L15-psk-tx.grc" download>L15-psk-tx.grc</a>: random BPSK, QPSK, or 8PSK symbols shaped by the RRC filter, with the constellation, I and Q, and the spectrum. No hardware needed.
- <a class="doc-link" href="../../grc/L15-psk-link.grc" download>L15-psk-link.grc</a>: the whole text link, with sliders for $E_b/N_0$, frequency offset, channel phase, and clock error, a variable that turns differential coding on or off, constellations before and after the Costas Loop, its frequency estimate, the received text, and the BER. No hardware needed.
- <a class="doc-link" href="../../legacy/refs/differential-encoding-tutorial.pdf" target="_blank" rel="noopener">Differential encoding tutorial (PDF)</a>

Open a `.grc` file from GRC's File menu, or run `gnuradio-companion L15-psk-link.grc` from the radioconda prompt. To change the constellation in the link, double-click the variable `M`, set it to 2, 4, or 8, and run the flowgraph again; the Costas Loop's order and every table follow it. The variable `diff` works the same way: 1 turns differential coding on and 0 turns it off. The Text Sink is an Embedded Python Block saved inside the `.grc` file. The L15 Lab page has the PlutoSDR version of the link.
::::

::::{frame} Summary
:class: read-only

| Idea | What it is | Number to remember |
| :-- | :-- | :-- |
| mPSK | $M$ phases on a circle | $k = \log_2 M$ bits per symbol |
| Bandwidth | set by the symbol rate, not $M$ | $(1 + \alpha) R_s$ = 5.4 kHz at 4 kbaud |
| Gray map | neighbors differ in one bit | label of index $i$ is $i \oplus (i \gg 1)$ |
| Receiver order | matched filter, Symbol Sync, Costas Loop, decoder | timing before carrier |
| Frequency offset | turns the points $360° \Delta f/R_s$ a symbol | 50 Hz is 4.5° a symbol at 4 kbaud |
| Costas Loop | phase detector of order $M$, loop filter | QPSK pulls in from about 375 Hz at 12 dB |
| Phase ambiguity | the loop can lock in any of $M$ rotations | $360°/M$ apart |
| Differential coding | data on the change of phase | about twice the BER, 0.3 to 0.4 dB |
| BER | Lesson 3's curves | within 0.3 dB at $10^{-4}$ |
::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE448_L15_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE448_L15_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Looking Ahead
:::{present}
- The L15 Lab builds a carrier-recovery loop, measures BER and pull-in, and runs QPSK on a PlutoSDR.
- Lesson 16 hops the carrier itself from channel to channel.
:::

The L15 Lab is the hands-on version of this lesson, and it takes most of the second period. You build an 8PSK carrier-recovery flowgraph from an empty canvas, measure the link's bit error rate against Lesson 3's curves, find the 8PSK loop's pull-in range, map the phase ambiguity with differential coding off, and then send your own text through a PlutoSDR and a cable.

Lesson 16 turns to frequency hopping, where the transmitter moves its carrier from channel to channel many times a second and the receiver has to follow it. Lesson 20 returns to constellations with QAM and OFDM.
::::
