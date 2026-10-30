<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 448

Software Defined Radios

## Lesson 20 — QAM and OFDM

Spring 2027 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where We Were

- Lesson 3 drew constellations and decision regions.
- Lesson 14 found HD Radio's OFDM subcarriers and guard interval.
- Lesson 15 built PSK, carrier recovery, and an equalizer for multipath.

Today we add amplitude to the constellation and spread the symbols across many subcarriers.

Note:
Open L20-qam-noise.grc and L20-ofdm-link.grc in GRC before class. L20 has no 2025 slides; it follows GNU Radio's constellation objects and its OFDM examples tx_ofdm.grc and rx_ofdm.grc, then PySDR's Digital Modulation, Multipath Fading, and Channel Coding chapters.

---

## Today's Plan

1. QAM: points on a grid
2. Noise on QPSK, 16-QAM, and 64-QAM
3. OFDM in GNU Radio: the transmitter, the guard, the equalizer
4. Lesson 15's taps and an echo on OFDM
5. Which systems use each one, and how to find them on the air

Note:
Keep GRC open the whole period. Parts 2 and 4 are sliders moved live.

---

## Text over OFDM

<img src="./img/20-qam-ofdm/L20-ofdm-clean.png" alt="L20-ofdm-link.grc, labeled Simulated channel, on a clean channel: a flat-topped spectrum, rings of points before the equalizer, a clean 16-QAM grid after it, and every line of text received" style="max-height:420px; display:block; margin:0 auto;">

48 data subcarriers carry 16-QAM, and the text arrives.

Note:
Run L20-ofdm-link.grc live. The left plot is the spectrum of all 52 subcarriers, 48 for data and 4 pilots. The middle plot is the subcarrier points straight out of the receiver's FFT; the right plot is after the equalizer.

---

## From PSK to QAM

<img src="./img/20-qam-ofdm/L20-qam-low.png" alt="L20-qam-noise.grc, labeled Simulated channel, at noise amplitude 0.05: QPSK, 16-QAM, and 64-QAM constellations with tight points, and one spectrum showing all three in the same band" style="max-height:400px; display:block; margin:0 auto;">

QAM sets amplitude and phase: 16 points carry 4 bits, 64 points carry 6, in the same band.

Note:
Each modulation runs at 8,000 symbols per second through the RRC filter with alpha 0.35, so all three fill 10.8 kHz. 16-QAM carries twice QPSK's bits and 64-QAM three times. On a QAM grid each point's decision region is the square around it.

---

## Bits per Symbol

| | Bits | Bit rate | Point spacing |
| :-- | :-: | :-: | :-: |
| QPSK | 2 | 16 kb/s | 1.41 |
| 16-QAM | 4 | 32 kb/s | 0.63 |
| 64-QAM | 6 | 48 kb/s | 0.31 |
| 256-QAM | 8 | 64 kb/s | 0.15 |

All four run at 8,000 symbols per second in the same 10.8 kHz and at the same average power.

Note:
Each step adds 2 bits per symbol and roughly halves the spacing. The flowgraph's constellation objects are all set to an average power of 1.

---

## The QAM Flowgraph

<img src="./img/20-qam-ofdm/L20-grc-qam.png" alt="L20-qam-noise.grc in GRC: three Constellation Objects and three rows of Random Source, Constellation Modulator, Throttle, Channel Model, matched filter, Symbol Sync, and constellation sink, with one shared noise slider" style="max-height:420px; display:block; margin:0 auto;">

A **Constellation Object** holds the points; the **Constellation Modulator** maps and shapes.

Note:
16-QAM is built in. QPSK and 64-QAM list their points and use power normalization. The receiver is Lesson 15's matched filter and Symbol Sync. One noise slider drives all three Channel Models.

---

## Noise on QAM

<img src="./img/20-qam-ofdm/L20-qam-high.png" alt="L20-qam-noise.grc, labeled Simulated channel, at noise amplitude 0.3: QPSK clouds well apart, 16-QAM clouds still apart with a few stray points, and 64-QAM merged into one square" style="max-height:400px; display:block; margin:0 auto;">

The same noise makes the same clouds; 64-QAM's points merge first.

Note:
Raise the slider from 0.05 to 0.3 live. More points carry more bits in the same band but need a cleaner signal. PySDR's Digital Modulation chapter runs the same comparison.

---

<!-- .slide: class="viz-cue-slide" -->

## QAM Explorer

- Start with 16-QAM at noise 0.1.
- Raise the noise until the text breaks, then switch to 64-QAM and 256-QAM.

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
The explorer's noise slider matches the flowgraph's. Wrong decisions and wrong characters are red.

---

## Setting the Level

<img src="./img/20-qam-ofdm/L20-qam-gain.png" alt="L20-qam-noise.grc, labeled Simulated channel, with the Receiver gain at 0.6: all three grids shrunk toward the center" style="max-height:400px; display:block; margin:0 auto;">

At a gain of 0.6, 16-QAM's outer points sit where its inner points belong; an **AGC** holds the level.

Note:
Move the Receiver gain slider live. QPSK still decodes by quadrant. 16-QAM's outer points move from 0.95 to about 0.57, inside the 0.63 lines between outer and inner points. Amplifiers must stay out of compression, which squeezes the outer points. Carrier recovery for QAM uses the Constellation Receiver block instead of the Costas Loop.

---

## From One Carrier to Many

- **OFDM** sends many slow subcarriers instead of one fast carrier.
- Each carries one point per OFDM symbol.
- An inverse FFT builds the symbol; an FFT separates the subcarriers.

Note:
Lesson 14 met these blocks in HD Radio: OFDM Carrier Allocator, FFT, OFDM Cyclic Prefixer. Long symbols mean an echo smears only a small part of each one, and the guard absorbs that part.

---

## The OFDM Flowgraph

<img src="./img/20-qam-ofdm/L20-grc-ofdm.png" alt="L20-ofdm-link.grc in GRC: the tx_ofdm.grc transmitter on top, the channel in the middle, and the rx_ofdm.grc receiver below with synchronization, channel estimation, equalizers, decoders, and the Text Sink" style="max-height:420px; display:block; margin:0 auto;">

The link uses a 64-point FFT and a 16-sample guard, with 48 data and 4 pilot subcarriers 1,562.5 Hz apart.

Note:
The transmitter is tx_ofdm.grc with 16-QAM; the receiver is rx_ofdm.grc. Schmidl and Cox finds each packet from the first preamble symbol; the second preamble gives the channel estimate; the Frame Equalizer divides each subcarrier by its gain and turns it back by its phase.

---

## The Guard

<div class="fig" data-inline-svg="./fig/L20-guard.svg" style="max-width:760px; margin:0 auto;"></div>

The guard copies the end of each symbol, so an echo shorter than the guard keeps symbol 1 out of symbol 2's FFT window.

Note:
The window holds symbol 2 from both paths; on each subcarrier that sum is one point with a new gain and phase. An echo longer than the guard puts part of symbol 1 in symbol 2's window, and nothing removes that. The flowgraph's guard is 16 samples, 160 microseconds.

---

## Lesson 15's Taps on OFDM

<img src="./img/20-qam-ofdm/L20-ofdm-taps.png" alt="The OFDM link, labeled Simulated channel, with Lesson 15's taps at 0.25, 0.5, 0.6, and 0.6: a tilted spectrum, a jumble before the equalizer, a clean grid after it, and the text arriving" style="max-height:400px; display:block; margin:0 auto;">

The spectrum tilts; one gain and phase per subcarrier restores the grid.

Note:
At 100 kS/s Tap 1 now sets the lower edge, at minus 40 kHz, so the tilt is steeper than in Lesson 15, which needed an adaptive filter for the same tap settings on one carrier. The weakest subcarriers come out noisier, because the equalizer amplifies their noise too; at noise 0.05 the weak edge corrupts about half the lines.

---

## An Echo Inside the Guard

<img src="./img/20-qam-ofdm/L20-ofdm-echo-in.png" alt="The OFDM link, labeled Simulated channel, with an echo 8 samples late at level 0.5: a rippled spectrum, points on separate arcs before the equalizer, a clean grid after it, and every line received" style="max-height:400px; display:block; margin:0 auto;">

An echo 8 samples late ripples the spectrum, and every line still arrives.

Note:
The ripple repeats every 12.5 kHz, eight times across the window. Each subcarrier sees a fixed gain and phase, which the equalizer removes.

---

## An Echo Past the Guard

<img src="./img/20-qam-ofdm/L20-ofdm-echo-out.png" alt="The OFDM link, labeled Simulated channel, with an echo 20 samples late: the grid after the equalizer scatters and no line arrives intact" style="max-height:400px; display:block; margin:0 auto;">

At 20 samples the echo reaches into the next symbol's FFT window, and the grid scatters.

Note:
The text survives echoes up to about 9 samples and fails by about 12, not 16, because the receiver starts its FFT window about 7 samples before the end of the guard as a margin for its own timing. Step the delay up from 8 one sample at a time.

---

## Systems That Use Each One

| System | Subcarriers carry | Guard |
| :-- | :-- | :-- |
| Wi-Fi | BPSK to 4096-QAM | 0.4 to 3.2 µs |
| LTE downlink | QPSK to 256-QAM | 4.7 µs |
| DVB-T TV | QPSK to 64-QAM | up to 224 µs |
| HD Radio | QPSK | 0.15 ms |

Cable TV, cable modems, and microwave links use single-carrier QAM.

Note:
802.11a/g Wi-Fi uses today's subcarrier layout at 20 MS/s: 312.5 kHz apart. LTE uses 15 kHz, and 5G NR uses 15 kHz or a multiple of it. ATSC 3.0, the newer US TV standard, is OFDM too. Cable carries 64- and 256-QAM in 6 MHz channels, and DOCSIS 3.1 moved to OFDM.

---

## Choosing a Scheme

<img src="./img/20-qam-ofdm/L20-ofdm-noise.png" alt="The OFDM link, labeled Simulated channel, at noise amplitude 0.15: the 16-QAM clouds touch and most lines arrive with errors" style="max-height:380px; display:block; margin:0 auto;">

Echoes choose OFDM; noise chooses how many points.

Note:
Wi-Fi and LTE step from 64-QAM down to 16-QAM and QPSK as the signal weakens, adding error-correcting code: PySDR calls these modulation and coding schemes. HD Radio stays with QPSK to reach the edge of coverage.

---

## On the SDR

- `L20-band-pluto.grc` at 2 MS/s near 100 MHz: an FM station with Lesson 14's HD Radio shelves.
- At 20 MS/s on 2.437 GHz: Wi-Fi as flat-topped bursts about 17 MHz wide.
- At 20 MS/s between 729 and 756 MHz: LTE as a flat band about 9 MHz wide that stays on.

Note:
The flowgraph is a PlutoSDR Source with a center frequency control and a 2 or 20 MS/s choice. A Pluto streams about 4 MS/s continuously over USB 2.0; at 20 MS/s each 131,072-sample buffer, 6.5 ms, is unbroken, with samples lost between buffers, and that is enough for the spectrum's shape. At 2 MS/s LTE shows only a flat slice; step 2 MHz to find its edges. Some beacons use the older 802.11b format and look rounded. Look at the spectrum only; nothing here transmits.

---

## Key Point

<div class="callout">More QAM points carry more bits but need a cleaner signal. OFDM splits a channel into slow subcarriers with a guard, so an echo shorter than the guard becomes one gain and phase per subcarrier.</div>

Note:
This is the last lesson; the rest of Module 7 is the final project.

---

## Looking Ahead

- The final project: pick a signal, write success criteria, build it.
- Today's flowgraphs are starting points for a QAM or OFDM project.

Note:
Ideas: send a file over the OFDM link through a PlutoSDR and a cable with an inline 30 dB attenuator and an AGC, add a 64-QAM payload with the qam64 object from L20-qam-noise.grc, or survey the Wi-Fi and LTE bands.
