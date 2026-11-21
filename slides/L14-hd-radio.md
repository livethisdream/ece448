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
Before class, run L14-hd-test-tx.grc once so L14-hd-test.sigmf-data and its .sigmf-meta sit next to L14-hd-find.grc. If the room has a PlutoSDR and an antenna, switch the finder to its PlutoSDR Source and find a local HD station on the waterfall ahead of time.

---

## Today's Plan

1. HD Radio modes and what is in the spectrum
2. The digital sidebands and OFDM
3. Recreating, finding, and measuring the sidebands in GNU Radio
4. Demodulating a real station to QPSK
5. Decoding it with gr-hdradio

Note:
This follows the slides: overview, spectrum, RBDS, sidebands, the OFDM concept and implementation, then tools. The demodulation and decoding at the end run on nrsc5's sample capture of KUT 90.5: before class, download sample.xz and L14-kut.sigmf-meta from the lesson page, unpack sample.xz, and rename it L14-kut.sigmf-data next to L14-hd-demod.grc and L14-hd-rx.grc.

---

## Find the Shelves on the Air

<img src="./img/14-hd-radio/L14-hd-scan.png" alt="Simulated: the finder's spectrum and waterfall on the L14 test file at 100.3 MHz, with a flat shelf on each side of the station on the spectrum and two straight bands on the waterfall; the station at 99.9 MHz has none" style="max-height:400px; display:block; margin:0 auto;">

Run L14-hd-find.grc on the PlutoSDR at an FM station: flat bands beside it are HD Radio.

Note:
Live demo: in L14-hd-find.grc, disable the File Source and the six blocks after it, enable the PlutoSDR Source (1,488,375 samples per second, extended-frequency mode), and type a strong local station into Center. Drag a box across one shelf on the spectrum to zoom in. hdradio.com/stations lists the local HD stations. The figure is the finder playing the simulated test file.

---

## HD Radio Modes

<div class="fig" data-inline-svg="./fig/L14-hybrid.svg" style="max-width:720px; margin:0 auto;"></div>

- Hybrid keeps the analog host and adds a sideband on each side.
- Extended hybrid widens the sidebands inward; all digital drops the host.

Note:
NRSC-5 defines all three. Hybrid keeps about 130 kHz of analog signal on each side; extended hybrid limits it to about 100 kHz. Inside the host is Lesson 7's multiplex, with RBDS: differentially encoded BPSK at 1187.5 bits per second on 57 kHz. Demo if time allows: Lesson 7's L07-rds-rx.grc shows the station name.

---

## The Digital Sidebands

- Subcarriers are 363.4 Hz apart: one FFT bin at `fft_len` 4096.
- Each sideband is many narrow subcarriers, numbered 356 to 546.
- Partitions hold 18 data subcarriers and 1 reference subcarrier, which carries differential BPSK.
- The sidebands are much weaker than the host.

Note:
Subcarrier k sits at k times 363.4 Hz from the center. The reference subcarriers are 356, 375, 394, and every 19th up to 546. The meter's inner and outer Variables use these numbers.

---

## OFDM in GNU Radio

- OFDM subcarriers overlap, but each is zero at its neighbors' centers.
- An inverse FFT of `fft_len` = 4096 builds a symbol; each bin is one subcarrier.
- The cyclic prefix, `cp_len` = 224 samples, goes in front of each symbol.

Note:
Orthogonality is the O in OFDM, and it lets an FFT separate the subcarriers. The blocks are the OFDM Carrier Allocator, an inverse FFT (the FFT block set to Reverse), and the OFDM Cyclic Prefixer, as in the GNU Radio wiki's Basic OFDM Tutorial, which the slides link. The receiver finds where each symbol starts, removes the prefix, takes a forward FFT, and reads each subcarrier's point; the second half of today does this on a real station.

---

## OFDM Explorer

<a href="../viz/ofdm-explorer.html" target="_blank" rel="noopener">Open the OFDM explorer</a> (it is also on the lesson page).

- At spacing 1.00 every neighbor crosses zero at the center subcarrier.
- An echo longer than the cyclic prefix reaches into the next symbol's FFT window.

Note:
Start at HD Radio: the red dots sit on zero. Move the spacing off 1.00 and the neighbors leak in. Drag the echo past the prefix and the red sliver appears inside symbol 2's FFT window.

---

## The Test Signal

<img src="./img/14-hd-radio/L14-grc-test-tx.png" alt="L14-hd-test-tx.grc: two OFDM chains of Random Uniform Source, Chunks to Symbols, Stream to Tagged Stream, OFDM Carrier Allocator, inverse FFT, and OFDM Cyclic Prefixer; an FM host and neighbor; noise; a File Sink of unsigned bytes; and a Python Snippet that writes the SigMF meta file" style="max-height:400px; display:block; margin:0 auto;">

Each side carries random QPSK on subcarriers 356 to 546, written as unsigned bytes.

Note:
The FFT has 4096 points at 1,488,375 samples per second, so each bin is one subcarrier, and the cyclic prefix is 224 samples. The symbols are random, not NRSC-5 data, so nrsc5 cannot decode this file. The 4 s file is 11.9 MB, in nrsc5's default format, cu8. The File Sink writes L14-hd-test.sigmf-data, and the write_meta Python Snippet writes the .sigmf-meta, because GNU Radio's SigMF Sink takes no cu8. Nothing transmits.

---

## Finding the Sidebands

<img src="./img/14-hd-radio/L14-hd-find.png" alt="Simulated: the sideband finder with meters at -23.04 and -23.06 dBc and 0.02 dB between them, the spectrum with two flat shelves, and the waterfall with two straight bands" style="max-height:440px; display:block; margin:0 auto;">

The shelves have flat tops and sharp edges, and their width never changes on the waterfall.

Note:
The figure comes from the simulated test file. In L14-hd-find.grc five blocks turn unsigned bytes into complex samples; to go live, select the File Source and the six blocks after it, press D, and enable the PlutoSDR Source. The shelves start at 100.1706 and 100.4294 MHz. The display shows power per bin, so the shelves' height is not the power ratio; the meters measure that.

---

## Measuring Sideband Power

<img src="./img/14-hd-radio/L14-hd-meters.png" alt="Simulated: Upper sideband -23.04 dBc, Lower sideband -23.06 dBc, Upper minus lower 0.02 dB" style="max-height:200px; display:block; margin:0 auto;">

- Each meter shifts its band to 0 Hz, filters it, and averages $\vert x\vert^2$ for 0.2 s.
- The sideband meter minus the host meter gives dBc; a third reading compares the sides.

Note:
The host band is plus or minus 100 kHz, each sideband is plus or minus 34.7 kHz around plus or minus 163.9 kHz, and every filter decimates by 6. The nrsc5 project's real sample file reads about −24.3 and −23.8 dBc in the same flowgraph, close to the test file. On a live station the two meters need not agree.

---

## What Noise Does

<img src="./img/14-hd-radio/L14-hd-noise.png" alt="Simulated: the finder with noise_amp 0.15: the floor near -66 dB, the shelves about 8 dB above it, and the meters reading -22.24 and -22.27 dBc" style="max-height:440px; display:block; margin:0 auto;">

With `noise_amp` raised to 0.15, the shelves sink toward the floor and the meters read high.

Note:
Demo: change noise_amp from 0.03 to 0.15 in L14-hd-test-tx.grc, rerun it, rerun the finder. The floor rises about 14 dB and the meters read about 0.8 dB high, because the noise in each band adds to the sideband's power.

---

## From Sidebands to Symbols

<img src="./img/14-hd-radio/L14-grc-demod.png" alt="L14-hd-demod.grc: the byte conversion or a PlutoSDR, an Added noise source, a band-pass FFT Filter, the cyclic prefix match, and NRSC-5 Symbol Sync, an FFT, and NRSC-5 Subcarriers into a score plot, three constellations, and two number readouts" style="max-height:400px; display:block; margin:0 auto;">

- A band-pass filter keeps the sidebands; the cyclic prefix marks each symbol.
- An FFT gives the subcarriers, and the block equalizes the data against the references.

Note:
L14-hd-demod.grc runs on nrsc5's sample capture of KUT 90.5, L14-kut.sigmf-data, in the same cu8 format at 1,488,375 S/s as the test file. Two steps are Embedded Python Blocks, Lesson 11's tool: double-click them to show the code. Multiply Conjugate, Stream to Vector, and QT GUI Number Sink are new blocks; say what each does as it comes up.

---

## Finding Each Symbol

<img src="./img/14-hd-radio/L14-demod-symbols.png" alt="The recording and its band-passed sidebands, the cyclic prefix match over one 4320-sample symbol with one tall peak, and the tuning error readout near 96 Hz" style="max-height:400px; display:block; margin:0 auto;">

- Delay, Multiply Conjugate, and Moving Average compare each sample with the one `fft_len` later.
- The match peaks once per 4320-sample symbol.

Note:
The prefix is a copy of the symbol's last 224 samples, 4096 samples earlier, so only there do the products line up and add; the lesson page has a to-scale drawing in its depth block. Averaging 16 symbols leaves one clear peak. Without the band-pass filter, the host's products are far larger than the peak, and the page shows that run too. The plot shows the size of the match; Symbol Sync reads its angle, the tuning error within half a subcarrier, ±181.7 Hz, and shows it on the readout: about 90 to 100 Hz on KUT. NRSC-5 fades each symbol in and out over 224 samples, so the block fades it again and adds the last 224 samples onto the first 224, instead of dropping the prefix.

---

## Reference Subcarriers

<img src="./img/14-hd-radio/L14-demod-refs.png" alt="A score against subcarrier with 22 spikes at plus and minus 356 to 546, and the reference points in two clusters at plus and minus 1" style="max-height:400px; display:block; margin:0 auto;">

- The block multiplies each subcarrier by its conjugate one symbol earlier.
- References give $+1$ or $-1$, so 22 spikes mark them.

Note:
The references use differential BPSK, as in Lesson 7's RDS, so the channel's phase cancels between symbols. Data subcarriers change QPSK point every symbol, so their score stays near zero. The plot spans subcarriers −600 to 600, so the 11 spikes on each side can be counted: 10 partitions plus a closing reference at 546. The references carry slowly changing control data, so most points sit at +1. Demo on the Pluto: change Center by 0.0025 MHz; the Whole subcarriers off readout moves about 7 and the plots stay the same.

---

## Equalizing the Data Subcarriers

<img src="./img/14-hd-radio/L14-demod-eq.png" alt="Data subcarriers on the KUT capture: before equalization, smeared around a ring; after, four tight round clusters at plus and minus 0.7 in I and Q" style="max-height:400px; display:block; margin:0 auto;">

- The two references around each partition measure the channel there.
- Dividing each data subcarrier by that measurement leaves QPSK.

Note:
Multipath, echoes off buildings and terrain, turns the phase across the band, which smears the raw points. The receiver knows each reference only up to its sign, so the block squares the two measurements to remove the sign, interpolates between them across the partition, takes the square root, and divides. It rotates the result 45°, because NRSC-5's QPSK points sit at 45° while dividing by a reference on the real axis leaves them on the axes. Each symbol puts 360 points on the plot, 180 from each sideband.

---

## Noise on the Constellation

<img src="./img/14-hd-radio/L14-demod-noise.png" alt="Equalized QPSK at added noise 0, 0.015, and 0.025: tight clusters, wide clouds that nearly touch, then one round cloud" style="max-height:400px; display:block; margin:0 auto;">

- Raise Added noise: the reference spikes shrink and the QPSK clusters spread.
- gr-hdradio still plays the capture at 0.035 and falls silent by 0.05.

Note:
Demo: drag Added noise up slowly. The clusters run together near 0.025. L14-hd-rx.grc has the same slider; its decoder plays at 0.035 and is silent by 0.05, because the error-correcting code adds extra bits that let it fix the bits the noise turned wrong.

---

## Decoding with gr-hdradio

<img src="./img/14-hd-radio/L14-grc-rx.png" alt="L14-hd-rx.grc: the byte conversion or a PlutoSDR into HD Radio Receiver, two Selectors and an Audio Sink, a Message Debug, and an HD File Sink" style="max-height:400px; display:block; margin:0 auto;">

- HD Radio Receiver outputs each program's audio, the station and song, and album art.
- The Program buttons select HD1, HD2, HD3, or HD4.

Note:
gr-hdradio is an out-of-tree module, the kind Lesson 11 built: GNU Radio blocks that call nrsc5's decoder library, which undoes the error-correcting code and the interleaving and decompresses the audio. The Selector passes one of its inputs to its output. Run L14-hd-rx.grc on the KUT capture: the receiver takes about 5 s to lock, then HD1 plays, and the console prints KUT, its slogan, and the program title. The files port saves album art to hd_files; KUT's capture carries none. Install steps are on the lesson page.

---

## Key Point

<div class="callout">HD Radio adds two OFDM sidebands, about 23 dB below the host, 129.4 to 198.4 kHz from its center. The prefix marks each symbol, the receiver equalizes the QPSK data against the references, and gr-hdradio decodes the audio.</div>

---

## On the SDR

- Run the PlutoSDR at 1,488,375 samples per second, centered on the station.
- Look for shelves 129 to 198 kHz either side, with manual gain near 30 dB.
- The shelves should stand well above the floor, or the meters read high.

Note:
Centering puts the Pluto's DC correction on the host, away from the meters. The finder uses manual gain, not the Pluto's AGC, so a reading at a given gain means the same thing every time. In the noise run, shelves 8 dB above the floor read 0.8 dB high. Overload hides the sidebands under the receiver's distortion, so back off the gain if the floor rises. The finder, the demodulator, and the receiver all switch to the Pluto the same way, and nothing transmits.

---

## Looking Ahead

- The L14 Lab builds the meter, identifies a station's mode, and measures a live station.
- Lesson 15 recovers the carrier phase and symbol timing of a single mPSK carrier.

Note:
Today the cyclic prefix gave each symbol's timing and the references gave each subcarrier's phase. A single mPSK carrier has neither, so Lesson 15 recovers both from the signal itself.
