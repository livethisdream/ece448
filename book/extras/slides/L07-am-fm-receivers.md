<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 448

Software Defined Radios

## Lesson 7 — AM and FM Receivers

Spring 2027 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where We Were

- In Lesson 5 an RTL-SDR recorded 2.4 MS/s of the FM band to a file.
- In Lesson 6 we built and received AM, DSB-SC, and SSB in simulation.
- Today the signal comes from a capture or from the air.

Today we build a **broadcast FM receiver** with **RDS** and an **AM receiver** for the aircraft band, and we compare AM and FM in the same noise.

Note:
Before class, run L07-fm-test-tx.grc and L07-am-test-tx.grc once, in the folder that holds the receivers. Each writes 76.8 MB and stops on its own. Have L07-wbfm-rx.grc open with the volume low.

---

## Two Stations in a Capture

<img src="./img/07-am-fm-receivers/L07-fm-band.png" alt="Simulated test file: 2.4 MHz around 100.0 MHz with stations at 99.5 and 100.3 MHz" style="max-height:300px; display:block; margin:0 auto;">

The goal is audio from the station at 100.3 MHz, and its station name.

Note:
This is a test file from a GNU Radio transmitter flowgraph, the same kind of file as their L5 capture. The station at 100.3 carries the L6 two-tone message and RDS; 99.5 carries a 600 Hz tone. The figure carries a Simulated label.

---

## Wideband FM

- The carrier's **frequency** follows the message, up to $\Delta f$ = 75 kHz away.
- Carson's rule gives the bandwidth:

$$B \approx 2(\Delta f + W)$$

- 15 kHz audio needs 180 kHz; US stations sit 200 kHz apart.

Note:
Narrowband FM on two-way radios uses 2.5 or 5 kHz of deviation. AM carrying the same 15 kHz audio would be 30 kHz wide, so broadcast FM is six times wider.

---

## The Receiver Flowgraph

<img src="./img/07-am-fm-receivers/L07-grc-wbfm-rx.png" alt="L07-wbfm-rx.grc: File Source or RTL-SDR, Frequency Xlating FIR Filter, Quadrature Demod, Decimating FIR Filter, FM Deemphasis, Audio Sink" style="max-height:380px; display:block; margin:0 auto;">

A channel filter, a demodulator, an audio filter, and de-emphasis feed the speaker.

Note:
We disabled the RTL-SDR Source; switching to live means disabling the File Source and enabling the SDR. The flowgraph needs no Throttle, because the Audio Sink paces the File Source, as in Lesson 6.

---

## Channel Filter and Decimation

- The **Frequency Xlating FIR Filter** shifts, filters, and decimates in one block.
- It shifts by $f_\text{station} - f_c$ = 300 kHz and passes ±90 kHz.
- Decimating by 10 leaves 240 kS/s.

Note:
The filter has a 105 kHz cutoff and a 30 kHz transition, so it passes 90 kHz and is 28 dB down by 120 kHz, the new Nyquist frequency. The filter removes the station at 99.5. Type 99.5 into Station to tune it instead.

---

## The Quadrature Demodulator

$$\text{gain} = \frac{f_s}{2\pi\Delta f} = \frac{240\ \text{kHz}}{2\pi \cdot 75\ \text{kHz}} = 0.509$$

- The phase step between samples is the frequency.
- With this gain, 75 kHz of deviation gives an output of 1.

Note:
The block ignores amplitude, so an FM receiver needs no AGC.

---

## The Multiplex

<img src="./fig/L07-fm-multiplex.svg" alt="FM baseband: L+R to 15 kHz, pilot at 19, L-R as DSB-SC around 38, RDS at 57 kHz" style="max-height:280px; display:block; margin:0 auto;">

The demodulator's output carries mono audio, the stereo pilot and difference signal, and RDS.

Note:
L-R is DSB-SC on 38 kHz, the Lesson 6 signal that needs carrier recovery; the 19 kHz pilot lets the receiver rebuild 38 kHz by doubling it. RDS sits at 57 kHz, three times the pilot. The test station is mono, so it has no pilot; its RDS stereo flag is only a data bit.

---

## The Multiplex, Measured

<img src="./img/07-am-fm-receivers/L07-mpx.png" alt="Simulated: the test station's multiplex, two tones near 0 Hz, RDS near 57 kHz, and a noise floor rising with frequency" style="max-height:300px; display:block; margin:0 auto;">

The noise floor rises with frequency.

Note:
FM noise at the demodulator output grows with distance from the carrier, so the top of the audio band and RDS receive the most noise. That rising noise is the reason for de-emphasis, on the next slide.

---

## Audio and De-emphasis

- A 15 kHz low-pass filter decimates by 5, from 240 to 48 kS/s.
- **De-emphasis** (75 μs) cuts the treble the transmitter boosted.
- It removes the high-frequency noise along with the boost.

Note:
US pre-emphasis boosts 15 kHz by about 17 dB; the de-emphasis corner is 2.1 kHz. Europe uses 50 microseconds.

---

## Running the Receiver

<img src="./img/07-am-fm-receivers/L07-wbfm-rx.png" alt="Simulated: the WBFM receiver window, received band, multiplex, and audio with lines at 1 and 2.5 kHz" style="max-height:420px; display:block; margin:0 auto;">

Note:
Play the audio. The audio sink shows exactly the two message tones. Type 99.5 into Station and the 600 Hz tone plays. Then show how to point the File Source at fm_capture.cfile and type its center frequency.

---

## RDS

- The **Radio Data System** sends 1187.5 bit/s on 57 kHz.
- It is BPSK with differential coding and biphase symbols.
- Groups of 104 bits carry the station name, program type, and radiotext.

Note:
1187.5 is 57 kHz divided by 48. A group is four 26-bit blocks, 16 data bits and a 10-bit check word each, so 87.6 ms per group. The PS name is eight characters, two per group. North America calls it RBDS.

---

## Decoding RDS

<img src="./img/07-am-fm-receivers/L07-rds-decoded.png" alt="Simulated: RDS constellation with two clusters, and the gr-rds panel showing ECE 448 and the radiotext" style="max-height:330px; display:block; margin:0 auto;">

Two clusters show BPSK with its carrier recovered, and the panel shows ECE 448.

Note:
Open L07-rds-rx.grc. It shifts 57 kHz to 0 and resamples to 19 kHz, 16 samples per bit. A matched filter and Symbol Sync find the bits, the Constellation Receiver recovers the carrier, and a Differential Decoder feeds the gr-rds blocks. The panel swaps two labels: the PI code, 1093, appears under Program Type.

---

## An AM Receiver

<img src="./img/07-am-fm-receivers/L07-am-rx.png" alt="Simulated: the AM receiver, a narrow station at 126.2 MHz, its carrier and sidebands, and the two-tone audio" style="max-height:360px; display:block; margin:0 auto;">

The filter cuts off at 5 kHz and decimates by 50, and **Complex to Mag** detects the envelope.

Note:
Aircraft and ATIS are AM between 118 and 137 MHz. After Complex to Mag it is the L6 receiver: the 3 kHz low-pass taps and a DC Blocker, plus an AGC because the level depends on distance.

---

## AM and FM in the Same Noise

<img src="./img/07-am-fm-receivers/L07-amfm-30.png" alt="At C/N 30 dB: AM output SNR 29.5 dB, FM 48.4 dB" style="max-height:340px; display:block; margin:0 auto;">

With the same tone, power, and noise, AM in 10 kHz reaches 29.5 dB and FM in 60 kHz reaches 48.4 dB.

Note:
L07-am-vs-fm.grc sends AM at m = 1 and FM at 25 kHz deviation with the same transmitted power and noise density. The FM receiver admits six times the noise, and its output SNR is still about 19 dB higher. Each doubling of deviation adds 5 to 6 dB above threshold.

---

## The FM Threshold

| C/N in 10 kHz (dB) | 30 | 20 | 15 | 10 |
| :-- | :-: | :-: | :-: | :-: |
| AM | 29.5 | 19.4 | 14.4 | 9.2 |
| FM, 5 kHz | 35.5 | 25.5 | 20.5 | 14.2 |
| FM, 25 kHz | 48.5 | 39.2 | 26.1 | 9.3 |
| FM, 50 kHz | 53.2 | 39.5 | 17.3 | 6.4 |

Below about 10 dB in its own bandwidth, FM clicks and its advantage disappears.

Note:
Drag C/N down with the audio on FM and listen for the clicks. At 15 dB the 25 kHz signal is 7 dB above the noise in its 60 kHz band. A wider deviation gives more SNR above threshold and reaches threshold sooner. At 10 dB the 5 kHz signal is the best of the four. Each table entry averages about 12 s of meter readings; near threshold the live meters wander by about 1 dB.

---

<!-- .slide: class="viz-cue-slide" -->

## FM Explorer

- The lines fall off just outside Carson's band.
- At $\Delta f$ = 2.4 kHz on a 1 kHz tone, the carrier vanishes.
- Carson's band holds about 96% of the power or more.

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
The carrier line vanishes when the deviation is 2.4 times the tone frequency, and technicians use that null to calibrate deviation.

---

## Key Point

<div class="callout">FM spreads the message over a wider channel, and above threshold its receiver returns a cleaner output than AM. Below threshold the improvement disappears, and a wider channel reaches threshold sooner.</div>

Note:
Broadcast FM is strong and has a 200 kHz channel. Aircraft use AM: a weak AM signal stays intelligible, and two transmitters at once are both heard.

---

## On the SDR

- Tune a few hundred kHz off the station, away from the DC spike.
- Set RF gain from your L5 gain table.
- Receiving is unrestricted, and the RTL-SDR receives only.

Note:
ATIS frequencies are in the FAA Chart Supplement and on sectional charts. RDS needs a stronger signal than the audio, because 57 kHz sits where the multiplex noise is highest.

---

## Looking Ahead

- The L7 Lab plays your L5 capture, then receives live FM, RDS, and ATIS.
- Lesson 8 sends bits as FSK, which is FM with a two-valued message.

Note:
The pre-lab asks for the decimation chain, the demodulator gain, Carson bandwidths, and RDS timing before the bench.
