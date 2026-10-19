<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 448

Software Defined Radios

## Lesson 9 — PAM Theory

Spring 2027 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where We Were

- Lesson 3: one clean sample per symbol gives a constellation and a bit error rate
- Lesson 5: a flowgraph is the receiver
- Lesson 8: FSK carried bits as frequency

Today: a PAM link in GNU Radio, from bits to one clean sample per symbol.

Note:
Open both L9 flowgraphs in GRC before class. The pulse-shaping demo runs in the first fifteen minutes.

---

## Today's Plan

1. Bits to levels: symbol rate
2. Pulse shaping: raised cosine and bandwidth
3. The eye diagram
4. Matched filtering
5. Symbol-timing recovery with Symbol Sync

Note:
Every part adds one block to the flowgraph. Items two, four, and five run live.

---

## A PAM Link in One Flowgraph

<img src="./img/09-pam-theory/L09-grc-matched-filter.png" alt="The L9 matched-filter flowgraph in GRC" style="max-height:440px; display:block; margin:0 auto;">

Each block is one idea from this lesson.

Note:
Trace the signal left to right: symbols, transmit filter, channel, matched filter, then Keep 1 in N and Symbol Sync side by side. Lesson 10 puts text in at the left and gets it back out at the right.

---

## Bits to Levels

<div class="fig" data-inline-svg="./fig/L09-pam-levels.svg" style="max-width:720px; margin:0 auto;"></div>

$$R_s = \frac{R_b}{\log_2 M}$$

Note:
Same eight bits both ways. 4-PAM uses half the symbols, each twice as long, Gray coded as in Lesson 3. In GNU Radio the mapping is a Chunks to Symbols block with a table.

---

## Why Not Rectangular Pulses?

- A rectangular pulse has a sinc spectrum.
- Its first sidelobe is only 13 dB down, and the sidelobes fall off slowly.
- The signal spills into neighboring channels.

Note:
The jumps between levels are what spread the spectrum. A licensed transmitter has emission limits outside its channel, and a rectangular pulse fails them.

---

## Raised Cosine and Bandwidth

<div class="fig" data-inline-svg="./fig/L09-rc-spectrum.svg" style="max-width:720px; margin:0 auto;"></div>

$$B = (1+\alpha)R_s$$

Note:
Alpha zero is the minimum bandwidth but an infinitely long pulse. Alpha one doubles the bandwidth. We use 0.35 all lesson.

---

## Zero Intersymbol Interference

<div class="fig" data-inline-svg="./fig/L09-rc-pulses.svg" style="max-width:720px; margin:0 auto;"></div>

Each pulse is zero at every other symbol instant.

Note:
Point at each red dot: the sum passes exactly through the symbol value there. Between the dots it does not, which is why sampling time matters.

---

## Root-Raised Cosine: Half at Each End

- The transmitter and receiver each use a **root-raised cosine** (RRC).
- Together the two filters make one raised cosine.
- The receive half also rejects noise outside the signal band.

Note:
Consequence worth stating: the transmitted signal alone has some ISI. Only the receive filter's output is ISI-free.

---

## Pulse Shaping in GNU Radio

<img src="./img/09-pam-theory/L09-grc-pulse-shaping.png" alt="The L9 pulse-shaping flowgraph in GRC" style="max-height:330px; display:block; margin:0 auto;">

```python
firdes.root_raised_cosine(sps, samp_rate, samp_rate/sps, alpha, 11*sps)
```

Note:
Gain sps, sample rate, symbol rate, alpha, number of taps. The Interpolating FIR Filter inserts sps minus one zeros per symbol and filters. 32 kHz over 8 samples per symbol is 4 kbaud.

---

## Rectangular and RRC Spectra

<img src="./img/09-pam-theory/L09-pulse-shaping.png" alt="Rectangular and RRC spectra, and the RRC eye with no receive filter" style="max-height:400px; display:block; margin:0 auto;">

RRC at $\alpha = 0.35$ fits $4 \times 1.35 = 5.4$ kHz.

Note:
Run it live and drag alpha: the red edge follows one plus alpha times Rs over two. Point out the eye on the right is not clean yet; that is the missing matched filter.

---

## Symbol Rate and Bandwidth

A 12.96 kHz channel at $\alpha = 0.35$ fits 9.6 kbaud.

| Modulation | Bit rate | $E_b/N_0$ at $10^{-5}$ |
| :-- | :-: | :-: |
| 2-PAM | 9.6 kb/s | 9.6 dB |
| 4-PAM | 19.2 kb/s | 13.4 dB |

Note:
4-PAM doubles the bit rate in the same channel and needs 3.8 dB more. Doubling the symbol rate instead doubles the bandwidth and no longer fits.

---

## The Eye Diagram

<div class="fig" data-inline-svg="./fig/L09-eye-anatomy.svg" style="max-width:560px; margin:0 auto;"></div>

Sample where the eye is widest open.

Note:
Height is noise margin, width is timing margin, the center is where to sample. GNU Radio draws it with the QT GUI Eye Sink.

---

<!-- .slide: class="viz-cue-slide" -->

## PAM Eye Explorer

- Lower α: the spectrum narrows and the eye's waist pinches.
- RRC only: the eye picks up ISI.
- Move the sample time or lower Es/N0: symbol errors climb.

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Switch to rectangular to show the spectrum spreading, then back to RRC plus matched filter.

---

## Matched Filtering

<img src="./img/09-pam-theory/L09-matched-filter.png" alt="Eyes before and after the matched filter" style="max-height:400px; display:block; margin:0 auto;">

The same RRC at the receiver removes about 9 dB of noise at 8 sps.

Note:
Turn the noise slider up to 0.6 live. The received eye closes; the matched-filter eye stays open. Noise across 32 kHz down to the signal's 5.4 kHz.

---

## Symbol-Timing Recovery

<img src="./img/09-pam-theory/L09-timing.png" alt="Keep 1 in N drifting through the eye while Symbol Sync stays at plus and minus 1" style="max-height:400px; display:block; margin:0 auto;">

Plain decimation drifts through the eye; Symbol Sync tracks its center.

Note:
The flowgraph exaggerates the error to 500 ppm so the drift shows in seconds. Even 20 ppm at 4 kbaud slips a whole symbol every 12.5 seconds.

---

## The Symbol Sync Block

| Parameter | L9 value |
| :-- | :-- |
| Timing error detector | Gardner |
| Samples per symbol | 8 |
| Loop bandwidth | 0.045 |
| Output samples/symbol | 1 |

Note:
Gardner compares the midpoint sample with the symbol samples on either side; a transition crosses zero exactly halfway when timing is right. Larger loop bandwidth tracks faster but jitters more.

---

## The PAM Receiver in GNU Radio

| Idea | Block |
| :-- | :-- |
| Symbol mapping | Chunks to Symbols |
| Pulse shaping | Interpolating FIR Filter |
| Matched filter | Decimating FIR Filter |
| Eye check | QT GUI Eye Sink |
| Timing recovery | Symbol Sync |

Note:
On an SDR the channel is real: the noise and clock error come from hardware, and this receiver already handles both.

---

## Key Point

<div class="callout">The RRC filter at the transmitter fixes the bandwidth at \((1+\alpha)R_s\). The same RRC filter at the receiver rejects the noise and removes the ISI, and Symbol Sync finds the center of the eye.</div>

Note:
Every PAM, PSK, and QAM link in the rest of the course uses this chain.

---

## Looking Ahead

- Lesson 10: ASCII text over this PAM link
- Bytes to bits, a frame marker, and a slicer back to bits
- L10 Lab: the link over real radios

Note:
Before Lesson 10, run both L9 flowgraphs and be able to find the symbol rate that fits a channel.
