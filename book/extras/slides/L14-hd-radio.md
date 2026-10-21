<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 448

Software Defined Radios

## Lesson 14 — HD Radio

Spring 2027 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where We Were

- Lesson 7 received an FM station and its RDS data.
- Lesson 13 decoded tones in bins, one FFT frequency at a time.
- Today we find a digital signal that sits beside an FM station.

Note:
Before class, run L14-hd-test-tx.grc once so L14-hd-test.cu8 sits next to L14-hd-find.grc. If the room has an RTL-SDR and an antenna, find a local HD station on the waterfall ahead of time.

---

## Today's Plan

1. The hybrid signal and its subcarriers
2. Why OFDM
3. How strong the sidebands are
4. Finding and measuring them in GNU Radio
5. Decoding with nrsc5

Note:
Parts 1 to 3 are the signal; part 4 is the flowgraph we run; part 5 is the decoder the lab uses on a live station.

---

## Two Shelves Beside a Station

<img src="./img/14-hd-radio/L14-hd-band.png" alt="Simulated: an FM station at 100.3 MHz with a flat shelf on each side, and an analog-only station at 99.9 MHz" style="max-height:300px; display:block; margin:0 auto;">

Each shelf is a digital signal about 69 kHz wide. The station at 99.9 MHz has none.

Note:
The figure comes from the simulated test file. The shelves are HD Radio, which carries the same program in better quality and often an HD2 or HD3 as well. An ordinary FM radio ignores them.

---

## The Hybrid Signal

<div class="fig" data-inline-svg="./fig/L14-hybrid.svg" style="max-width:720px; margin:0 auto;"></div>

The analog host stays in the center; the sidebands run 129.4 to 198.4 kHz out.

Note:
NRSC-5 defines the signal. The codec and interleaver make the digital audio arrive several seconds late, so the station delays its analog audio by the same amount. A receiver plays analog first, blends to digital once it decodes it, and blends back to analog when the digital signal fades.

---

## Subcarriers and Partitions

$$\Delta f = \frac{1{,}488{,}375}{4096} = 363.4\ \text{Hz}$$

- Each side has 191 subcarriers, numbered 356 to 546, at $k \Delta f$.
- Ten partitions of 19 hold 18 data and 1 reference subcarrier each.

Note:
356 times 363.4 Hz is 129.4 kHz; 546 times it is 198.4 kHz. Extended hybrid adds one, two, or four partitions inside 356 on each side. The lab asks where those edges fall, so do not work them here.

---

## Why OFDM

- One 69 kHz carrier would send a symbol every 15 μs, shorter than the echoes.
- OFDM sends 191 slow carriers, each with 2.902 ms symbols.
- A 50 μs echo then blurs only the first 2% of a symbol.

Note:
Multipath from buildings and hills arrives tens of microseconds late. With one wide carrier, a 50 microsecond echo overlaps parts of four later symbols, and the receiver needs an equalizer. Each narrow subcarrier sees the channel as one gain and phase. Wi-Fi, LTE, and digital TV use OFDM for the same reason; Lesson 20 returns to it.

---

## OFDM as Block Parameters

$$\begin{aligned}
T_u &= 4096\ \text{samples} = 2.752\ \text{ms} = 1/\Delta f \\
T_g &= 224\ \text{samples} = 150.5\ \mu\text{s}
\end{aligned}$$

- `fft_len` = 4096 at 1,488,375 S/s makes each bin one subcarrier.
- `cp_len` = 224 is the guard, whose edges NRSC-5 tapers, so it absorbs echoes somewhat shorter than 150.5 μs.

Note:
A tone lasting Tu has a sinc spectrum with nulls 1/Tu apart, so subcarriers spaced 1/Tu are orthogonal. The transmitter builds every subcarrier at once with an inverse FFT and the receiver separates them with a forward FFT. The guard is a copy of the end of the symbol, which the receiver discards.

---

## OFDM Explorer

<a href="../viz/ofdm-explorer.html" target="_blank" rel="noopener">Open the OFDM explorer</a> (it is also on the lesson page).

- Spacing 1.00: every neighbor crosses zero at the center subcarrier.
- An echo longer than the guard reaches into the next symbol's FFT window.

Note:
Start at HD Radio: the red dots sit on zero. Move the spacing off 1.00 and the neighbors leak in. Drag the echo past 150 microseconds and the red sliver appears inside symbol 2's FFT window. The explorer draws a plain guard; NRSC-5 tapers the edges, so echoes in the second half of the guard are marginal.

---

## How Strong the Sidebands Are

$$-20 - 10\log_{10} 2 = -23.0\ \text{dBc}, \qquad -20 - 10\log_{10} 382 = -45.8\ \text{dBc}$$

- Both sidebands together carry 1% of the host's power, −20 dBc.
- Since 2010 the FCC has allowed −14 dBc, and up to −10 dBc with approval.

Note:
NRSC-5 lets the sidebands differ by up to 10 dB, which protects a neighbor on one side. The lab asks for the −14 dBc numbers, so leave them for the pre-lab.

---

## The Test Signal

<img src="./img/14-hd-radio/L14-grc-test-tx.png" alt="L14-hd-test-tx.grc: two OFDM chains of Random Uniform Source, Chunks to Symbols, Stream to Tagged Stream, OFDM Carrier Allocator, reverse FFT, and OFDM Cyclic Prefixer; an FM host and neighbor; noise; and a File Sink of unsigned bytes" style="max-height:400px; display:block; margin:0 auto;">

Each side carries random QPSK on 191 subcarriers at −23 dBc, written as RTL-SDR bytes.

Note:
The FFT has 4096 points at 1,488,375 samples per second, so each bin is one subcarrier, and the guard is 224 samples. The symbols are random, not NRSC-5 data, so nrsc5 cannot decode this file. The 4 s file is 11.9 MB. Nothing transmits.

---

## The Sideband Finder

<img src="./img/14-hd-radio/L14-grc-find.png" alt="L14-hd-find.grc: a byte File Source through UChar To Float, Add Const, Multiply Const, Deinterleave, and Float To Complex, or an RTL-SDR, into a frequency sink, a waterfall, and three band-power meters" style="max-height:400px; display:block; margin:0 auto;">

Five blocks turn RTL-SDR bytes into complex samples.

Note:
Subtract 127.5, scale by 1/128, pair the bytes. GRC shows the RTL-SDR Source grayed out. To go live, select the File Source and the six blocks after it, press D, and enable the RTL-SDR Source.

---

## Finding the Sidebands

<img src="./img/14-hd-radio/L14-hd-find.png" alt="Simulated: the sideband finder with meters at -23.05 and -23.04 dBc, the spectrum with two flat shelves, and the waterfall with two straight bands" style="max-height:440px; display:block; margin:0 auto;">

The shelves have flat tops and sharp edges, and their width never changes on the waterfall.

Note:
The figure comes from the simulated test file. The shelves start at 100.1706 and 100.4294 MHz. They sit about 25 dB under the host's peak on the display, more than the 23 dB between powers, because the host's power is concentrated in fewer bins.

---

## Measuring Sideband Power

<img src="./img/14-hd-radio/L14-hd-meters.png" alt="Simulated: Upper sideband -23.05 dBc, Lower sideband -23.04 dBc" style="max-height:200px; display:block; margin:0 auto;">

- Each meter shifts its band to 0 Hz, filters it, and averages $\vert x\vert^2$ for 0.2 s.
- The sideband meter minus the host meter gives dBc.

Note:
The host band is plus or minus 100 kHz, each sideband is plus or minus 34.7 kHz around plus or minus 163.9 kHz, and every filter decimates by 6. The nrsc5 project's real sample file reads about −24.3 and −23.7 dBc in the same flowgraph.

---

## Decoding with nrsc5

```
nrsc5 -g 30 100.3 0            # tune 100.3 MHz, play HD1
nrsc5 -g 30 -w hd.cu8 100.3 0  # also record the IQ
nrsc5 -r hd.cu8 0            # decode a recording
```

nrsc5 runs the rest of NRSC-5: sync, QPSK, deinterleaving, decoding, and audio.

The nrsc5 README documents these commands; we have not yet tested them in this course.

Note:
nrsc5 is not part of radioconda; build it from source on Linux, with the project's Homebrew formula on macOS, or with MSYS2 on Windows. We have not yet run it in this course. Program 0 is HD1. A recording made with -w opens in L14-hd-find.grc. gr-nrsc5 is a transmitter, not a receiver.

---

## Key Point

<div class="callout">HD Radio adds two OFDM sidebands, 129.4 to 198.4 kHz from the station's center and about 20 dB below the analog host. They appear as flat shelves on a spectrum, band-power meters measure them, and nrsc5 decodes them.</div>

---

## On the SDR

- Run the RTL-SDR at 1,488,375 samples per second, centered on the station.
- Look for shelves 129 to 198 kHz either side, with gain from your L5 table.
- The shelves should stand 10 dB above the floor.

Note:
Centering puts the DC spike on the host, away from the meters. Overload buries the sidebands, so back off the gain if the floor rises. The RTL-SDR only receives, and nothing transmits.

---

## Looking Ahead

- The L14 Lab builds the meter, identifies a station's mode, and decodes a live station.
- Lesson 15 recovers carrier phase and symbol timing for mPSK.

Note:
nrsc5 performed the carrier and timing recovery for us today; Lesson 15 builds it for a single carrier.
