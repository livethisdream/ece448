<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 448

Software Defined Radios

## Lesson 4 — SDR Introduction

Spring 2027 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where We Were

- Lesson 2: the first amplifier sets the receiver's noise figure
- Lesson 3: a digital signal is points in the I-Q plane
- Today: the hardware that turns a band of spectrum into those points

Note:
Bring the RTL-SDR, HackRF, PlutoSDR, and ADALM-PHASER to the front of the room and pass the first three around while the next slides are up.

---

## Today's Plan

1. What makes a radio software defined
2. The four course SDRs
3. Inside an SDR: front end, mixer and LO, I and Q, ADCs
4. Sample rate and bandwidth
5. Bits and dynamic range, in a flowgraph
6. Choosing the radio and its settings

Note:
Item five runs live from L04-adc-bits.grc, which needs no hardware. If GNU Radio is not yet installed on the projector laptop, use the screenshots on the lesson page.

---

## One Radio, Many Signals

<div class="fig" data-inline-svg="./fig/L04-tuning-ranges.svg" style="max-width:820px; margin:0 auto;"></div>

Each bar is a course SDR's tuning range; the dashed lines are signals this course decodes.

Note:
The RTL-SDR receives FM at 100 MHz, AIS at 162 MHz, key fobs at 433.92 MHz, and ADS-B at 1090 MHz with the same hardware. Only the software changes. Point out that the PlutoSDR cannot reach the FM band and that only the ADALM-PHASER works at X band.

---

## What Makes a Radio Software Defined

- A hardware radio builds each function as a circuit: one radio, one job.
- An SDR digitizes early and does filtering, demodulation, and decoding in software.
- Changing the job means changing the flowgraph, not the hardware.

Note:
An SDR is a radio in which software defines some or all of the physical layer. It still needs an antenna, a filter, an amplifier, and a converter; everything after the converter is a program.

---

## The Course SDRs

| Radio | Tunes | Max rate | Bits | Transmit |
| :-- | :-- | :-- | :-: | :-- |
| RTL-SDR Blog V4 | 0.5–1766 MHz | 2.56 MS/s | 8 | no |
| HackRF One | 1–6000 MHz | 20 MS/s | 8 | half duplex |
| PlutoSDR | 325–3800 MHz | 61.44 MS/s | 12 | full duplex |
| ADALM-PHASER | 10.0–10.5 GHz | via its Pluto | 12 | — |

- The PlutoSDR's instantaneous bandwidth is at most 20 MHz.
- Every number comes from the manufacturer's data, linked on the lesson page.

Note:
The RTL-SDR's 2.56 MS/s is the datasheet's rate without dropped samples. The ADALM-PHASER mixes 10.0 to 10.5 GHz down to about 2.2 GHz and a PlutoSDR digitizes it, so its rate and bits are the PlutoSDR's.

---

## Inside an SDR

<div class="fig" data-inline-svg="./fig/L04-sdr-chain.svg" style="max-width:820px; margin:0 auto;"></div>

- Front end: filter and LNA
- Mixer and LO: down to 0 Hz
- ADCs: \(I\) and \(Q\) to the host

Note:
The LNA comes right after the filter because, from Lesson 2, the first amplifier sets most of the noise figure. A transmitter runs the same chain backward with DACs.

---

## The Mixer Moves the Band

<div class="fig" data-inline-svg="./fig/L04-mixer-shift.svg" style="max-width:780px; margin:0 auto;"></div>

\[\cos a \cos b = \tfrac{1}{2}\cos(a - b) + \tfrac{1}{2}\cos(a + b)\]

A low-pass filter keeps the difference; one real mixer also folds the station below the LO onto the positive axis.

Note:
A station at 100.3 MHz with an LO at 100.0 MHz comes out at 0.3 MHz, and the filter removes the 200.3 MHz sum. Setting the center frequency in GNU Radio sets the LO. Point to the amber station: 98.4 MHz lands at 1.6 MHz, on top of 101.4 MHz. The next slide fixes that.

---

## I and Q

- One mixer folds \(f_{LO} + \Delta\) and \(f_{LO} - \Delta\) onto the same \(\Delta\).
- A second mixer, with the LO shifted 90°, tells them apart.
- Each sample is \(I + jQ\): it rotates one way above the LO and the other way below, so 98.4 MHz lands at \(-1.6\) MHz.

Note:
Lesson 5 shows the negative frequencies this makes possible on GNU Radio's plots. Do not derive it here.

---

## Zero-IF and Superheterodyne

- **Zero-IF**: one quadrature mixer straight to 0 Hz
- **Superheterodyne**: to a fixed IF first, then to 0 Hz
- ADALM-PHASER: 10.0–10.5 GHz to about 2.2 GHz, then a PlutoSDR

GNU Radio receives complex samples whatever the architecture.

Note:
Zero-IF puts anything that leaks into the mixer output at 0 Hz in the middle of the band, which is Lesson 5's DC spike. The ADALM-PHASER's mixer moves X band to about 2.2 GHz and the PlutoSDR does the second conversion. A superheterodyne's first mixer also passes an image at the LO plus the IF, which a filter ahead of it removes.

---

## Sample Rate and Bandwidth

- Complex samples at \(f_s\) show a band \(f_s\) wide, centered on \(f_{LO}\).
- GNU Radio carries each sample in 8 bytes: \(8 f_s\) bytes per second.
- 2.4 MS/s is 19.2 MB/s; 20 MS/s is 160 MB/s.

Choose a little more than the signal's bandwidth, not the radio's maximum.

Note:
A laptop that cannot keep up drops samples, and most drivers print an overflow message in the console. The radio's own filters roll off near the window's edges. Demo the SDR Window widget from the lesson page here: FM on the RTL-SDR at 2.4 MS/s, then the HackRF at 20 MS/s, then the PlutoSDR, which cannot tune to 98 MHz.

---


## Bits and Dynamic Range

- An \(N\)-bit ADC has \(2^N\) levels between \(-\)full scale and \(+\)full scale.
- Each bit adds about 6 dB: 8 bits span about 48 dB, 12 bits about 72 dB.
- 0 dBFS is full scale; above it, the ADC clips.

Note:
The exact figure for a full-scale sine is 6.02 N plus 1.76 dB, 50 and 74 dB, but six dB per bit is accurate enough for this course.

---

## The Quantizer Flowgraph

<img src="./img/04-sdr-introduction/L04-grc-adc.png" alt="The L4 flowgraph in GNU Radio Companion: two Signal Sources and a Noise Source into an Add block, a Multiply Const for gain, a Throttle, an ADC block, and two QT GUI sinks" style="max-height:400px; display:block; margin:0 auto;">

- A strong tone at \(-6\) dBFS and a weak one 64 dB below it
- Then a gain and an ADC block with 8, 12, or 16 bits

Note:
The ADC block is an Embedded Python Block: it clips I and Q to plus and minus one and rounds to 2 to the N levels. The sink's 0 dB is not full scale, so read differences.

---

## 8 Bits

<img src="./img/04-sdr-introduction/L04-adc-8bit.png" alt="8 bits, 0 dB gain: the strong tone near minus 15 dB above a ragged floor of spurs between minus 100 and minus 75 dB; no weak tone visible" style="max-height:380px; display:block; margin:0 auto;">

The floor and spurs reach within about 60 dB of the strong tone; the weak tone lies below them.

Note:
Point to minus 0.49 MHz, where the weak tone should be. It sits below the spurs. The smooth floor is deeper than six dB per bit suggests because the 4096-point FFT spreads the noise over 4096 bins; the spurs do not spread.

---

## 12 Bits

<img src="./img/04-sdr-introduction/L04-adc-12bit.png" alt="12 bits: a smooth floor near minus 118 dB and the weak tone near minus 79 dB at minus 0.49 MHz" style="max-height:380px; display:block; margin:0 auto;">

The floor drops about 20 dB and the spurs are gone; the weak tone sits about 40 dB above the floor.

Note:
Switch the menu live. Then drag the weak-signal slider down until the tone disappears to measure the span.

---

## Too Much Gain

<img src="./img/04-sdr-introduction/L04-adc-clip.png" alt="8 bits, 12 dB gain: I and Q flat-topped at plus and minus 1, and a distortion product near minus 0.9 MHz about 12 dB below the strong tone" style="max-height:380px; display:block; margin:0 auto;">

The strong tone rises only 7 dB, and clipping creates a false signal near \(-0.9\) MHz.

Note:
On a real SDR these false signals look exactly like transmissions. Set the gain against the strongest signal in the window.

---

## Choosing the Radio and Its Settings

1. **Radio**: its tuning range covers the signal, and it transmits if the task does.
2. **Sample rate**: a little more than the signal's bandwidth.
3. **Gain**: the strongest signal in the window stays below full scale.

Note:
Broadcast FM: RTL-SDR at 2.4 MS/s. A 20 MHz Wi-Fi channel: HackRF at its 20 MS/s maximum or PlutoSDR at its 20 MHz bandwidth, with no margin at the edges. Transmit into a cable: HackRF or PlutoSDR. Direction of an X-band source: ADALM-PHASER.

---

## Key Point

<div class="callout">An SDR mixes a band to 0 Hz and digitizes \(I\) and \(Q\). The sample rate sets the visible spectrum; the ADC's bits, about 6 dB each, set how weak a signal can be near a strong one.</div>

---

## Looking Ahead

- Lesson 5: install GNU Radio and build the first flowgraphs
- Complex sampling, aliasing, the DC spike, and gain on a live RTL-SDR
- Download L04-adc-bits.grc before then

Note:
Remind cadets that Lesson 5 walks through the radioconda install, which they need before the L5 Lab; its pre-lab checks the install.
