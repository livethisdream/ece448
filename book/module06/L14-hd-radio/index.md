---
frame_view: true
---

# L14 - HD Radio

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">HD Radio</h1>

<div class="title-rule"></div>

We find and measure the digital sidebands beside an FM station, demodulate them to QPSK, and play the station with gr-hdradio.

Lesson 14 · Module 6: Waveform Applications & RF Reverse Engineering · Dr. Neil Rogers
::::

::::{frame} Slides
:class: read-only

:::{admonition} Slides
:class: slides
<a href="../../slides/L14-hd-radio.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L14-hd-radio.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L14-hd-radio.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '6'; counter-reset: lo 2">
  <li>I can describe how HD Radio works and demodulate an HD Radio signal.</li>
</ol>
::::

::::{frame} Find the Shelves on the Air
:::{present}
<img src="../../viz/img/L14-hd-scan.png"
     alt="The spectrum and waterfall of L14-hd-find.grc, labeled Simulated: L14 test file, centered on 100.3 MHz: the spectrum shows a rounded station at 100.3 MHz with a flat shelf on each side and a second rounded station at 99.9 MHz with none; on the waterfall the shelves are two straight orange bands of constant width beside the host"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Run `L14-hd-find.grc` on the PlutoSDR, centered on a strong FM station.
- Look for flat bands on either side, and zoom in on one.
:::

We start on the air, with the PlutoSDR and the lesson's finder flowgraph:

1. Open `L14-hd-find.grc`. Select the File Source and the six blocks after it, through Float To Complex, and press D; then select the PlutoSDR Source and press E.
2. Run it and type a strong local station's frequency into Center; the station list at hdradio.com shows which local stations carry HD Radio.
3. Watch the waterfall. The station is a rounded band whose width changes with the audio, and a station with HD Radio also shows two flat bands of constant width on either side of it, which an ordinary FM radio ignores.
4. Drag a box across one of those bands on the spectrum to zoom in on it, and right-click to zoom back out.

Those bands are **HD Radio**, a digital broadcast that carries the station's program, and often extra programs, on the same channel. The course Plutos run in extended-frequency mode, 70 MHz to 6 GHz, so the FM band is in range.

The figure is the finder playing the lesson's test file rather than an antenna, so it carries a "Simulated" label: the station at 100.3 MHz has the two bands, and the one at 99.9 MHz has none. The rest of the lesson builds that test signal in GNU Radio, explains the finder, and measures the bands. Then we demodulate a recording of a real station one step at a time and play it with gr-hdradio, the course's HD Radio module for GNU Radio.
::::

::::{frame} HD Radio Modes
:::{present}
<img src="../../viz/img/L14-hybrid.svg"
     alt="The hybrid HD Radio layout: the analog FM host at the channel center, and an OFDM sideband of ten partitions on each side, from 129.4 to 198.4 kHz, marked as subcarriers 356 to 546, each 69 kHz wide"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- **Hybrid:** the analog FM host plus a digital sideband on each side.
- **Extended hybrid** narrows the analog room and widens the sidebands inward.
- **All digital** drops the analog host.
:::

HD Radio carries a station's program digitally alongside, or in place of, the analog signal. A **hybrid** station, the layout in the figure, keeps the analog FM signal Lesson 7 received in the center, about 130 kHz wide on each side, where every FM radio still plays it, and puts the digital signal in two **sidebands**, one on each side, from 129.4 to 198.4 kHz from the channel center. An **extended hybrid** station limits its analog signal to about 100 kHz each side and adds digital carriers on the inside edge of each sideband, and an **all-digital** station drops the analog signal entirely. The standard that defines all three is **NRSC-5**.

The digital signal carries the main program, called HD1, and a station can add HD2, HD3, and more programs that have no analog version.

:::{depth}
| Part | Where | Modulation |
| :-- | :-- | :-- |
| Analog host | within about ±130 kHz | FM |
| Inside the host | 0 to 57 kHz after demodulation | audio, pilot, stereo DSB-SC, RBDS BPSK |
| Digital sidebands | ±129.4 to ±198.4 kHz | OFDM, QPSK on each subcarrier |

Each part of the spectrum uses a different modulation. The host is analog FM, and Lesson 7's demodulator turned it into the **multiplex**: mono audio up to 15 kHz, the 19 kHz stereo pilot, the stereo difference signal as DSB-SC around 38 kHz, and **RBDS**, the US name for RDS, as differentially encoded BPSK at 1187.5 bits per second on 57 kHz. To see it on the same station, run Lesson 7's `L07-rds-rx.grc`. The digital sidebands sit outside the host, where an FM demodulator never sees them, and each one is **OFDM**, a block of many narrow carriers, each carrying QPSK.
:::
::::

::::{frame} The Digital Sidebands
:::{present}
- Each sideband is many narrow **subcarriers**, 363.4 Hz apart: one FFT bin at `fft_len` 4096.
- They come in **partitions** of 18 data subcarriers and 1 reference.
- The sidebands are much weaker than the host.
:::

Each sideband is not one carrier but 191 narrow ones, called **subcarriers**, spaced 363.4 Hz apart. NRSC-5 numbers them from the channel center, so subcarrier $k$ sits at $k \times 363.4$ Hz; the upper sideband runs from subcarrier 356, at 129.4 kHz, to 546, at 198.4 kHz, and the lower sideband is its mirror image. We use those numbers as block settings: the sideband meter later in the lesson takes its band from Variables named `inner` and `outer`.

The subcarriers come in **frequency partitions** of 19: 18 carry data, and one **reference subcarrier**, at 356, 375, 394, and every 19th after that up to 546, carries differentially encoded BPSK that the receiver uses to correct the phase of the data subcarriers around it. An extended hybrid station adds partitions inside subcarrier 356. The sidebands are much weaker than the host, so that they do not disturb analog radios or the neighboring stations; the meters in this lesson read each sideband's power relative to the host, in **dBc**.
::::

::::{frame} OFDM in GNU Radio
:::{present}
- **OFDM** subcarriers overlap, but each is zero at its neighbors' centers.
- An inverse FFT builds a symbol, and a forward FFT separates the subcarriers again.
- A **cyclic prefix** of `cp_len` samples goes in front of each symbol.
:::

**Orthogonal frequency-division multiplexing** (OFDM) divides a wide channel among many slow subcarriers instead of one fast carrier. OFDM spaces the subcarriers so closely that their spectra overlap, but each one passes through zero at the center of every other one. That property is **orthogonality**, the O in OFDM, and it lets the receiver separate them with an FFT. The explorer in the next frame shows it.

Each subcarrier carries one constellation point per OFDM symbol, so a symbol is a list of I/Q points, one per subcarrier: QPSK points on HD Radio's data subcarriers. GNU Radio's **OFDM Carrier Allocator** places the points on the subcarriers we list, a reverse **FFT** turns the whole list into one symbol of time samples, and the **OFDM Cyclic Prefixer** copies the end of each symbol in front of it. That copy is the **cyclic prefix**, also called the **guard interval**, and it separates each symbol from the one before it. These are the blocks of the GNU Radio wiki's Basic OFDM Tutorial, which the slides point to.

For HD Radio at 1,488,375 samples per second, `fft_len` = 4096 makes each FFT bin exactly one 363.4 Hz subcarrier, and `cp_len` = 224 samples is NRSC-5's cyclic prefix. Symbols follow one another over time, each 4096 + 224 = 4320 samples long. The receiver runs the same steps backward: find where each symbol starts, drop the prefix, take a forward FFT, and read each subcarrier's point. The second half of the lesson does exactly that.
::::

::::{frame} OFDM Explorer
:class: viz-frame

:::{depth}
Each OFDM symbol is a set of tones that last one FFT length, and the spectrum of a tone that lasts that long is a sinc shape whose nulls fall exactly one subcarrier spacing apart. With the subcarriers at that spacing, every subcarrier's spectrum crosses zero at the center of every other one, which is the orthogonality of the previous frame.

The left panel shows the spectra of five neighboring subcarriers with the HD Radio spacing; the red dots on the dashed line are what the four neighbors add at the center subcarrier's frequency. At spacing 1.00 every red dot sits on zero. Move the spacing away from 1.00 and the dots leave zero, and the readout shows the neighbors leaking in. The right panel shows two symbols with their guards, an echo of them, and the receiver's FFT window. Drag the echo delay past the guard and the end of symbol 1's echo enters symbol 2's window, shown in red.
:::

:::{present}
<iframe src="../../viz/ofdm-explorer.html"
        width="100%" height="405"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="OFDM explorer: the spectra of five subcarriers against their spacing, and an echo against the guard interval">
</iframe>
:::
::::

::::{frame} The Test Signal
:::{present}
<img src="../../viz/img/L14-grc-test-tx.png"
     alt="GNU Radio Companion with L14-hd-test-tx.grc open: for each sideband, a Random Uniform Source, Chunks to Symbols for QPSK, Stream to Tagged Stream, OFDM Carrier Allocator, a reverse FFT, an OFDM Cyclic Prefixer, and a level; an FM host from filtered noise and a 19 kHz pilot; an analog-only neighbor shifted to minus 400 kHz; a Noise Source; an Add, Head, and a conversion to unsigned bytes into a File Sink; and a Python Snippet that writes the SigMF meta file"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Each sideband is random QPSK on 191 subcarriers, built with an inverse FFT.
- It writes 4 s as unsigned bytes, nrsc5's default format, as a SigMF pair: 11.9 MB.
:::

`L14-hd-test-tx.grc` recreates a hybrid station with the OFDM blocks of the previous frames. For each sideband, random QPSK points fill subcarriers 356 to 546 in the **OFDM Carrier Allocator**, a reverse **FFT** of 4096 points turns them into one symbol, and the **OFDM Cyclic Prefixer** adds the 224-sample guard. A Multiply Const sets each sideband's level, here $-23$ dBc. The FM host is filtered noise and a 19 kHz pilot, frequency modulated with the broadcast 75 kHz deviation setting, and an analog-only station sits 400 kHz below.

The sidebands carry random symbols, not NRSC-5 data, so nrsc5 cannot decode this file; it is a test signal for finding and measuring the sidebands. It writes the SigMF pair `L14-hd-test.sigmf-data` and `L14-hd-test.sigmf-meta`: unsigned 8-bit I and Q at 1,488,375 samples per second, nrsc5's default input format, which the meta file names as datatype `cu8`, with the center frequency, 100.3 MHz. GNU Radio's SigMF Sink takes no 8-bit samples, so a File Sink writes the data file and a **Python Snippet**, `write_meta`, writes the meta file when the flowgraph starts. nrsc5 reads any file without a `.cs16` or `.cf32` ending as `cu8`, so `nrsc5 -r L14-hd-test.sigmf-data 0` reads the data file as it is, though it finds nothing to decode. Nothing in it transmits: its last block is a File Sink.
::::

::::{frame} Finding the Sidebands
:::{present}
<img src="../../viz/img/L14-hd-find.png"
     alt="The L14 sideband finder window labeled Simulated: L14 test file: controls for Center, Pluto RX gain, and Inner subcarrier at 356; the number sink reads minus 23.04 dBc for the upper sideband, minus 23.06 dBc for the lower, and 0.02 dB for upper minus lower; the frequency sink shows the host at 100.3 MHz peaking near minus 33 dB, flat shelves near minus 58 dB on both sides, a floor near minus 80 dB, and the analog neighbor at 99.9 MHz; the waterfall shows the shelves as two straight bands of constant width beside the host"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The shelves have flat tops and sharp edges, unlike FM.
- On the waterfall they are straight bands that never change width.
:::

On the frequency sink, the shelves begin 129.4 kHz from the station, at 100.1706 and 100.4294 MHz, and end at 100.1016 and 100.4984 MHz. Their tops are flat because every subcarrier carries the same power, and their edges are sharp because the subcarriers stop at 356 and 546. The FM host is rounded, and on the waterfall its width changes with the audio, while the shelves stay the same width all the time. That difference is how we recognize HD Radio on a live band: look for two straight, flat bands about 130 to 200 kHz either side of a station.

The shelves sit about 25 dB under the top of the host on the display, but the meters, not the display heights, give the power ratio between the bands.

:::{depth}
<img src="../../viz/img/L14-grc-find.png"
     alt="GNU Radio Companion with L14-hd-find.grc open: a File Source of bytes, a Throttle, UChar To Float, Add Const minus 127.5, Multiply Const 1/128, Deinterleave, and Float To Complex, and a disabled PlutoSDR Source, both feeding a frequency sink, a waterfall sink, and three Frequency Xlating FFT Filters for the host and the two sidebands, each followed by Complex to Mag squared, a Moving Average, Keep 1 in N, and Log10, with three Subtract blocks feeding a number sink; a disabled Rational Resampler and SigMF Sink hang off the PlutoSDR Source"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">

`L14-hd-find.grc` plays the test file, any SigMF recording of datatype `cu8` at 1,488,375 samples per second, or the PlutoSDR live. A `cu8` file stores each sample as two unsigned bytes from 0 to 255, so the first five blocks subtract 127.5, scale by 1/128, and pair the bytes into complex samples. The PlutoSDR Source delivers complex samples directly, so it skips those blocks. To switch to the radio, select the File Source and the six blocks after it, through Float To Complex, press D to disable all seven, and enable the PlutoSDR Source; GRC will not run with both paths enabled. The **QT GUI Frequency Sink** and **Waterfall Sink** use an FFT of 4096 points, so each bin is one subcarrier wide.
:::
::::

::::{frame} Measuring Sideband Power
:::{present}
<img src="../../viz/img/L14-hd-meters.png"
     alt="The controls and number sink of the L14 sideband finder, labeled Simulated: L14 test file: Center 100.3, Pluto RX gain 30, Inner subcarrier 356; Upper sideband minus 23.04 dBc, Lower sideband minus 23.06 dBc, and Upper minus lower 0.02 dB, each with a bar on a scale from minus 40 to 0"
     style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Each meter shifts a band to 0 Hz, filters it, and averages $\vert x\vert^2$ for 0.2 s.
- A sideband meter minus the host meter is dBc; a third reading compares the sides.
:::

A band-power meter is four blocks we have used before. A **Frequency Xlating FFT Filter** moves the band's center to 0 Hz and keeps only the band, $\pm 100$ kHz for the host and $\pm 34.7$ kHz around $\pm 163.9$ kHz for each sideband, and decimates by 6. **Complex to Mag^2** gives each sample's power, a **Moving Average** over 0.2 s averages it, **Keep 1 in N** slows the result to 50 readings a second, and **Log10** with a factor of 10 converts each reading to dB. Subtracting the host's meter from a sideband's meter gives that sideband in dBc, and a third Subtract shows the upper sideband minus the lower.

On the test file the meters read $-23.04$ and $-23.06$ dBc, the level the test transmitter sets, and the sides differ by 0.02 dB. The same flowgraph on the real station recorded in the nrsc5 project's sample file reads about $-24.3$ and $-23.8$ dBc, close to the test file. On a live station the two meters need not agree, and the lab compares them. The **Inner subcarrier** slider steps the meters' inner edge down one partition at a time, from 356 to 280, so the same meters work on an extended hybrid station: slide it down until the readings stop rising.
::::

::::{frame} What Noise Does
:::{present}
<img src="../../viz/img/L14-hd-noise.png"
     alt="The L14 sideband finder labeled Simulated: test file, noise_amp 0.15: the floor has risen from about minus 80 to minus 66 dB, the shelves stand only about 8 dB above it, and the meters read minus 22.24 and minus 22.27 dBc instead of minus 23"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Raise `noise_amp` in the test transmitter and run the finder again.
- The floor rises, the shelves sink toward it, and the meters read high.
:::

To watch noise at work, open `L14-hd-test-tx.grc`, change the Variable `noise_amp` from 0.03 to 0.15, run it to write a new test file, and run the finder on it. The figure is that run. The floor rises by about 14 dB, the host still stands far above it, and the shelves, which are much weaker, now stand only a few dB above the floor. The meters read about 0.8 dB higher than before, because each one measures all the power in its band and the noise in the band adds to the sideband's. On a live station the same thing happens as the signal weakens, so a meter reading is trustworthy only while the shelves stand well above the floor.
::::

::::{frame} From Sidebands to Symbols
:::{present}
<img src="../../viz/img/L14-grc-demod.png"
     alt="GNU Radio Companion with L14-hd-demod.grc open: the File Source and the five blocks that turn unsigned bytes into complex samples, or a disabled PlutoSDR Source, and a Noise Source, into an Add; an FFT Filter that keeps the sidebands; a QT GUI Frequency Sink; a Delay of fft_len, Multiply Conjugate, Moving Average of cp_len, Stream to Vector, a second Moving Average, and Complex to Mag into a QT GUI Vector Sink; and NRSC-5 Symbol Sync, an FFT, and NRSC-5 Subcarriers into a vector sink and two constellation sinks"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- A band-pass filter keeps only the sidebands.
- The cyclic prefix marks where each symbol starts.
- An FFT gives the subcarriers, and the references equalize the data.
:::

`L14-hd-demod.grc` runs the receiver's first steps on a real station, one plot per step. Its default recording is the sample capture that ships with the nrsc5 project: 17 s of KUT 90.5 in Austin, in the same `cu8` format at 1,488,375 samples per second as the lesson's test file. The Downloads frame has it and a SigMF meta file for it: unpack `sample.xz`, rename the result `L14-kut.sigmf-data` beside `L14-kut.sigmf-meta`, and run. The same five blocks as the finder's turn the bytes into complex samples, and the PlutoSDR path is there to run it live.

Most of the chain is blocks we have used before. Two steps have no stock block, so they are **Embedded Python Blocks**, Lesson 11's tool for a block one flowgraph needs: **NRSC-5 Symbol Sync** cuts out each symbol, and **NRSC-5 Subcarriers** reads the subcarriers after the FFT. Double-click either one to read its code. The next four frames take the plots in order.
::::

::::{frame} Finding Each Symbol
:::{present}
<img src="../../viz/img/L14-demod-symbols.png"
     alt="Two plots from L14-hd-demod.grc on the KUT capture: on the left, the spectrum of the recording in blue with the host at the center and a shelf on each side, and the band-pass output in red with only the two shelves left; on the right, the cyclic prefix match against the sample within one 4320-sample symbol, with one tall peak near sample 450 and low ripple everywhere else"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Delay, Multiply Conjugate, and Moving Average compare each sample with the one `fft_len` later.
- The match peaks once per 4320-sample symbol, where the symbol starts.
:::

The cyclic prefix is a copy of the last 224 samples of each symbol, placed 4096 samples earlier. A **Delay** of `fft_len` and a **Multiply Conjugate** multiply each sample by the conjugate of the sample 4096 later, and a **Moving Average** of `cp_len` adds up 224 of those products. Over the prefix the two samples are copies, the products all point the same way, and the sum grows; everywhere else they point in random directions and cancel. One symbol's match is noisy, so **Stream to Vector** cuts the stream into 4320-sample pieces and a second Moving Average stacks 16 of them, which leaves one clear peak where each symbol starts.

The band-pass filter in front has to be there. The analog host carries most of the power and has no prefix, and without the filter its products bury the peak. The angle of the match at the peak is the phase that the radio's tuning error adds over 4096 samples, so it measures that error to within half a subcarrier, $\pm 181.7$ Hz. NRSC-5 Symbol Sync does the same matching in Python, cuts out each symbol, removes the tuning error, and hands 4096 samples to the FFT. On the KUT capture it measures about 90 Hz, close to the 99 Hz that nrsc5 reports on the same recording.
::::

::::{frame} Reference Subcarriers
:::{present}
<img src="../../viz/img/L14-demod-refs.png"
     alt="Two plots from L14-hd-demod.grc on the KUT capture: on the left, a score against subcarrier from minus 2048 to 2047, flat near zero except two groups of tall spikes near plus and minus 356 to 546; on the right, the reference subcarrier points in two clusters, a large one at plus 1 and a smaller one at minus 1"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The block compares each subcarrier with its value one symbol earlier.
- References give $+1$ or $-1$, so 22 spikes mark them.
- Their points form two BPSK clusters.
:::

The references carry BPSK with the same differential coding as Lesson 7's RDS, so the receiver needs only the change from one symbol to the next. NRSC-5 Subcarriers multiplies each FFT output by the conjugate of the same subcarrier one symbol earlier. The channel turns a subcarrier by nearly the same phase in both symbols, so that phase cancels, and a reference subcarrier lands on $+1$ or $-1$. A data subcarrier carries a new QPSK point every symbol, so its product lands anywhere. The **score** plot averages how close each subcarrier's product stays to the real axis, and 22 spikes stand out, at every 19th subcarrier from 356 to 546 on each side. The constellation shows the references' points: most sit at $+1$, because most reference bits repeat from one symbol to the next.

A tuning error larger than half a subcarrier moves the whole spike pattern. The block searches 40 subcarriers either way for the pattern and corrects the shift, so a radio tuned 2.5 kHz off, about 7 subcarriers, still decodes. On the PlutoSDR, change Center by 0.0025 MHz and watch the block find the references again.
::::

::::{frame} Equalizing the Data Subcarriers
:::{present}
<img src="../../viz/img/L14-demod-qpsk.png"
     alt="The data subcarrier constellation from L14-hd-demod.grc on the KUT capture: four tight round clusters at plus and minus 0.7 in I and Q"
     style="max-width: 420px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The two references around each partition measure the channel there.
- Dividing each data subcarrier by that measurement leaves QPSK.
:::

Multipath and the leftover timing error change the channel's gain and phase from one subcarrier to the next, but slowly, so the two references at the edges of each partition measure it well for the 18 data subcarriers between them. NRSC-5 Subcarriers blends the two measurements according to where each data subcarrier sits, divides the subcarrier by the result, and rotates it by 45° to the usual QPSK positions. That is **equalization**: undoing what the channel did, using signals whose value the receiver already knows. Each symbol puts 360 points on the plot, 180 from each sideband, and on the KUT capture they form four tight clusters.
::::

::::{frame} Noise on the Constellation
:::{present}
<img src="../../viz/img/L14-demod-noise.png"
     alt="L14-hd-demod.grc on the KUT capture with added noise 0.015: the reference score spikes still stand out but lower, near 0.7, over a busier floor, and the four QPSK clusters have spread into wide clouds that nearly touch"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Raise **Added noise** and every plot loses contrast.
- At 0.015 the QPSK clusters spread until they nearly touch.
- gr-hdradio still plays the capture at 0.035 and falls silent by 0.05.
:::

The **Added noise** slider adds a Noise Source to the recording, as a weaker station would. Move it up and watch the plots: the spikes shrink toward the floor, and the four clusters grow until they run together near 0.025. The decoder keeps playing past that point, because NRSC-5 adds an error-correcting code to the bits before they go on the subcarriers, and the decoder uses it to repair the points that land in the wrong cluster. On this recording gr-hdradio plays through 0.035 and is silent by 0.05.
::::

::::{frame} Decoding with gr-hdradio
:::{present}
<img src="../../viz/img/L14-grc-rx.png"
     alt="GNU Radio Companion with L14-hd-rx.grc open: the File Source and the five blocks that turn unsigned bytes into complex samples, or a disabled PlutoSDR Source, into an HD Radio Receiver block with eight audio outputs and the message ports status, station, services, id3, files, data, and hdc; two Selectors controlled by a Program chooser pick one program's left and right audio for an Audio Sink at 44.1 kHz; station and id3 go to a Message Debug, and files go to an HD File Sink writing to hd_files"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- **HD Radio Receiver** takes the recording or the PlutoSDR at 1,488,375 S/s.
- It outputs each program's audio, the station and song, and album art.
- The Program buttons switch between HD1 and HD4.
:::

Past the constellation, the receiver still has to undo the error-correcting code, put the bits back in order, and decompress the audio. **gr-hdradio** is the course's out-of-tree module for that, in the sense of Lesson 11: GNU Radio blocks built on the decoder library of the nrsc5 project. Open `L14-hd-rx.grc` in the folder with the KUT capture and run it. After about 5 s, while the receiver locks, HD1 plays, and the console prints the station's name, its slogan, and the program's title as message dictionaries:

```
((event . station_name) (name . KUT ))
((event . station_slogan) (slogan . The University of Texas at Austin))
((event . id3) ... (title . You're Listening to Q with Jian Ghomeshi) (program . 0))
```

The receiver decodes all four programs at once, and the two **Selectors** pass the one the Program buttons pick to the Audio Sink; KUT's capture carries HD1 and HD2. Its **files** port sends each file the station transmits, such as album art and logos, to the **HD File Sink**, which saves them in the `hd_files` folder; the KUT capture carries none, but most live stations send album art. To decode a live station, disable the File Source and the six blocks after it, enable the PlutoSDR Source, and type the station into Center.
::::

::::{frame} Setting Up gr-hdradio
:class: read-only

gr-hdradio is not part of radioconda, and neither is nrsc5, which it needs. Install both once, from the radioconda prompt, following the gr-hdradio README:

1. Download gr-hdradio from <a href="https://github.com/livethisdream/gr-hdradio" target="_blank" rel="noopener">github.com/livethisdream/gr-hdradio</a> and open a radioconda prompt in its folder.
2. **Linux or macOS:** install the build tools the README lists with `conda install`, then run `scripts/install_nrsc5.sh`, which builds nrsc5 into radioconda.
3. **Windows:** download the `nrsc5-win64` build from the repository's Actions page and copy `libnrsc5.dll` where the README says.
4. Install the blocks with `cmake -S . -B build` and `cmake --install build`, using the install prefix the README gives for your system, and restart GRC.

The blocks appear under **[HD Radio]** in GRC's block list. If GRC reports that it cannot find libnrsc5, nrsc5 is not installed where Python looks for it; the README lists the places it searches.
::::

::::{frame} Key Point
:::{present}
:class: callout
HD Radio adds two weak OFDM sidebands, 129.4 to 198.4 kHz from the station's center. The cyclic prefix marks each symbol, the references equalize the QPSK data, and gr-hdradio decodes it into audio.
:::
::::

::::{frame} On the SDR
:::{present}
- Run the PlutoSDR at 1,488,375 samples per second, centered on the station.
- The finder, the demodulator, and the receiver all switch to the Pluto the same way.
- Receiving is unrestricted, and nothing here transmits.
:::

To work live, disable the File Source and the six blocks after it, enable the PlutoSDR Source, and type the station's frequency into Center; `L14-hd-find.grc`, `L14-hd-demod.grc`, and `L14-hd-rx.grc` all switch the same way. About 1.5 MS/s streams continuously over the Pluto's USB 2.0 link. Centering on the station puts the Pluto's DC correction on the host, where it does not touch the sidebands or the meters.

The finder sets the Pluto's gain by hand, from the Pluto RX gain slider, rather than with its automatic gain, so a reading at a given gain means the same thing every time. Start near 30 dB, and lower it if the floor rises or copies of strong stations appear, because the sidebands are far weaker than the host and an overloaded receiver buries them. Not every station carries HD Radio, so check the station list at hdradio.com, and then type its frequency into the finder.

A weak station reads high, as the noise frame showed. As in Lesson 7, receiving is unrestricted and transmitting is not; nothing in this lesson transmits.
::::

::::{frame} Downloads
:class: read-only doc-links

- <a class="doc-link" href="../../grc/L14-hd-test-tx.grc" download>L14-hd-test-tx.grc</a>: writes `L14-hd-test.sigmf-data` and `.sigmf-meta`, 4 s (11.9 MB) of a simulated hybrid station at 100.3 MHz, with an analog-only neighbor 400 kHz below. Run it once; it stops on its own.
- <a class="doc-link" href="../../grc/L14-hd-find.grc" download>L14-hd-find.grc</a>: the spectrum, waterfall, and sideband power meters, playing the test file, or any SigMF recording of datatype `cu8` at 1,488,375 samples per second, or the PlutoSDR live, and recording the Pluto as SigMF for nrsc5.
- <a class="doc-link" href="../../grc/L14-hd-demod.grc" download>L14-hd-demod.grc</a>: the sidebands, the cyclic prefix match, the reference subcarriers, and the equalized QPSK, from the KUT capture or the PlutoSDR live, with an Added noise slider.
- <a class="doc-link" href="../../grc/L14-hd-rx.grc" download>L14-hd-rx.grc</a>: plays HD1 to HD4 with gr-hdradio, prints the station and song, and saves album art to `hd_files`, from the KUT capture or the PlutoSDR live. It needs gr-hdradio and nrsc5; see Setting Up gr-hdradio.
- <a class="doc-link" href="https://github.com/theori-io/nrsc5/raw/master/support/sample.xz" download>sample.xz</a> and <a class="doc-link" href="../../grc/L14-kut.sigmf-meta" download>L14-kut.sigmf-meta</a>: nrsc5's capture of KUT 90.5, 23 MB, and its SigMF meta file. Unpack `sample.xz` with `xz -d` or 7-Zip and rename the 50 MB result `L14-kut.sigmf-data`, beside the meta file.

Put the flowgraphs and the KUT pair in one folder and run the test transmitter first; GRC runs a flowgraph from its own folder, so the finder finds the test file there, and the demodulator and the receiver find `L14-kut.sigmf-data`.

**What this lesson follows.** The topics and their order come from the slides. The hands-on steps follow the pages those slides link and the documentation of the tools:

- <a class="doc-link" href="../../legacy/L24-hd-radio.pdf" target="_blank" rel="noopener">HD Radio slides (PDF)</a>
- <a href="https://wiki.gnuradio.org/index.php/Basic_OFDM_Tutorial" target="_blank" rel="noopener">GNU Radio wiki, Basic OFDM Tutorial</a>: the OFDM Carrier Allocator, FFT, and OFDM Cyclic Prefixer of the test transmitter. The other blocks are in the <a href="https://wiki.gnuradio.org/index.php/Tutorials" target="_blank" rel="noopener">GNU Radio tutorials</a>, and each block's wiki page has the same name as the block.
- <a href="https://github.com/livethisdream/gr-hdradio" target="_blank" rel="noopener">gr-hdradio and its README</a>: the HD Radio Receiver, HD Radio Decoder, and HD File Sink blocks, and how to install them and nrsc5.
- <a href="https://github.com/theori-io/nrsc5" target="_blank" rel="noopener">nrsc5</a>, the decoder library under gr-hdradio and the source of the KUT sample capture, and <a href="https://github.com/markjfine/nrsc5-dui" target="_blank" rel="noopener">NRSC5-DUI</a>, the graphical front end the slides list.
- <a href="https://pysdr.org/content/rds.html" target="_blank" rel="noopener">PySDR, RDS</a>, the slides' activity for decoding RBDS in Python, and <a href="https://github.com/bastibl/gr-rds" target="_blank" rel="noopener">gr-rds</a>, the RDS blocks of Lesson 7.
- <a href="https://hdradio.com/stations/" target="_blank" rel="noopener">hdradio.com station list</a>, to find local HD Radio stations.
- <a class="doc-link" href="../../legacy/refs/nrsc-1011s_hd-radio.pdf" target="_blank" rel="noopener">NRSC-5 Layer 1 FM specification, SY_IDD_1011s (PDF)</a>: Section 3.5 and Table 5-1 give the spacing and subcarriers.
- For more practice, the slides point to the GRCon 2023 CTF challenge "Not Really Superior Clatter-V", built on an HD Radio signal.
::::

::::{frame} Summary
:class: read-only

| Part | What to know | In GNU Radio |
| :-- | :-- | :-- |
| Modes | hybrid, extended hybrid, all digital | the shelves on the finder's waterfall |
| Host | analog FM, about ±130 kHz, with mono, pilot, stereo, RBDS | Lesson 7's receiver and gr-rds |
| Sidebands | ±129.4 to ±198.4 kHz, subcarriers 356 to 546 | the meter's `inner` and `outer` |
| Subcarriers | 363.4 Hz apart, partitions of 18 data and 1 reference | `fft_len` = 4096 at 1,488,375 S/s |
| Cyclic prefix | a copy of each symbol's end | `cp_len` = 224 |
| Symbol timing | the prefix matches its copy `fft_len` samples later | Delay, Multiply Conjugate, Moving Average |
| References | differential BPSK on every 19th subcarrier | NRSC-5 Subcarriers' score and BPSK plots |
| Data | QPSK, equalized by the references | NRSC-5 Subcarriers' QPSK plot |
| Decoder | audio, station, song, and album art | gr-hdradio's HD Radio Receiver and HD File Sink |
::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE448_L14_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE448_L14_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Looking Ahead
:::{present}
- The L14 Lab builds a sideband meter, identifies a station's mode, and measures a live station.
- Lesson 15 recovers the carrier and timing of a single mPSK carrier.
:::

Today we found the HD Radio sidebands beside an FM station, measured their power with meters built from familiar blocks, built an OFDM signal from GNU Radio's own blocks, demodulated a real station to QPSK, and played it with gr-hdradio. The L14 Lab is the bench version: build the sideband meter yourself, use it on a capture whose configuration you do not know, and measure a live station on the PlutoSDR, with an optional nrsc5 decode.

Today the cyclic prefix gave us each symbol's timing and the reference subcarriers gave us each subcarrier's phase. A single mPSK carrier has neither, so Lesson 15 recovers its carrier and timing from the signal itself, in GNU Radio.
::::
