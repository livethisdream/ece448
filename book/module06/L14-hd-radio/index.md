---
frame_view: true
---

# L14 - HD Radio

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">HD Radio</h1>

<div class="title-rule"></div>

We find the digital sidebands beside an FM station, measure them in GNU Radio, and decode them with nrsc5.

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

::::{frame} Two Shelves Beside a Station
:::{present}
<img src="../../viz/img/L14-hd-band.png"
     alt="A frequency sink labeled Simulated: L14 test file, showing 1.49 MHz around 100.3 MHz: a rounded FM station at 100.3 MHz with a flat shelf on each side of it, from about 100.10 to 100.17 MHz and from 100.43 to 100.50 MHz, and an FM station with no shelves at 99.9 MHz"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Each shelf beside 100.3 MHz is a digital signal, about 69 kHz wide.
- The station at 99.9 MHz has none: it is analog only.
:::

In Lesson 7 an FM station was one rounded hump about 200 kHz wide. Many US stations have two flat shelves on either side of that hump, which we can see on any spectrum display, and an ordinary FM receiver ignores them. The shelves are **HD Radio**, a digital broadcast that carries the same program in better quality, and often one or two extra programs, on the same channel as the analog station.

The figure comes from a test file rather than an antenna, so it carries a "Simulated" label. Today we find those shelves, measure how strong they are, and see why they are built from hundreds of narrow carriers. Then we decode a real one with **nrsc5**, an open-source HD Radio receiver for the RTL-SDR.
::::

::::{frame} The Hybrid Signal
:::{present}
<img src="../../viz/img/L14-hybrid.svg"
     alt="The hybrid HD Radio layout: the analog FM host at the channel center, and an OFDM sideband of ten partitions on each side, from 129.4 to 198.4 kHz, marked as subcarriers 356 to 546, each 69 kHz wide"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The analog FM **host** stays in the center, unchanged.
- The digital **sidebands** run from 129.4 to 198.4 kHz on each side.
:::

A station running HD Radio alongside its analog signal transmits the **hybrid** waveform. The analog FM signal is the same one Lesson 7 received, and every FM radio still plays it. The digital signal sits in two **sidebands**, one on each side of the channel center, starting 129.4 kHz out, beyond where nearly all of the FM signal's power lies. The standard that defines the signal is **NRSC-5**, and the iBiquity design it describes is the one US stations use.

The digital signal carries the station's main program, called HD1, as compressed audio, and a station can split its capacity to add HD2 and HD3 programs that have no analog version. A receiver plays the analog program first and blends to the digital program once it has decoded it, which takes a few seconds, so the station delays its analog audio to keep the two aligned. When the digital signal fades, the receiver blends back to analog.
::::

::::{frame} Subcarriers and Partitions
:::{present}
$$\Delta f = \frac{1{,}488{,}375}{4096} = 363.4\ \text{Hz}$$
:::
:::{present}
- Each sideband is 191 **subcarriers**, numbered 356 to 546.
- Subcarrier $k$ sits at $k\,\Delta f$ from the channel center.
- 10 **partitions** of 19 hold 18 data and 1 reference subcarrier each.
:::

Each sideband is not one carrier but 191 narrow ones, called **subcarriers**, spaced 363.4 Hz apart. NRSC-5 numbers them from the channel center, so subcarrier $k$ sits at $k\,\Delta f$, and the upper sideband runs from subcarrier 356 to 546:

$$\begin{aligned}
356 \times 363.4\ \text{Hz} &= 129.4\ \text{kHz} \\
546 \times 363.4\ \text{Hz} &= 198.4\ \text{kHz}
\end{aligned}$$

The lower sideband is the mirror image, $-356$ to $-546$. Subcarriers 356 to 545 form ten **frequency partitions** of 19 subcarriers, each with 18 data subcarriers and one **reference subcarrier** that the receiver uses to find the timing, frequency, and phase, and subcarrier 546 is one more reference at the outer edge. A station can also add one, two, or four partitions inside subcarrier 356 on each side, a mode called **extended hybrid**, which narrows the room left for the analog signal in exchange for more data.
::::

::::{frame} Why OFDM
:::{present}
- One 69 kHz carrier would send a symbol every 15 μs; echoes last longer.
- OFDM sends 191 slow carriers instead, each at 344.5 symbols per second.
- Each symbol lasts 2.9 ms, so an echo blurs only its start.
:::

Many narrow carriers sent side by side is **orthogonal frequency-division multiplexing** (OFDM), and HD Radio uses it because of **multipath**. A car radio receives the transmitter directly and also by reflections from buildings and hills, which arrive tens of microseconds later. If one carrier filled the 69 kHz sideband, each symbol would last about 15 μs, so an echo 50 μs late would land on top of the next three symbols, and the receiver would need a complex equalizer to undo it.

OFDM divides the same sideband among 191 subcarriers, each sending its own QPSK symbols at only 344.5 symbols per second, so each symbol lasts 2.902 ms. An echo 50 μs late now overlaps only the first 2% of a symbol, and each subcarrier is narrow enough that it sees the channel as a single gain and phase rather than a filter. The same reasoning puts OFDM in Wi-Fi, LTE, and digital TV, and Lesson 20 returns to it.
::::

::::{frame} Orthogonal Subcarriers and the Guard
:::{present}
$$\begin{aligned}
\Delta f &= \frac{1}{T_u}, \qquad T_u = 2.752\ \text{ms} \\
T_g &= \tfrac{7}{128}\,T_u = 150.5\ \mu\text{s}
\end{aligned}$$
:::
:::{present}
- Spacing $1/T_u$ makes the subcarriers **orthogonal**: no leakage at the receiver.
- A **guard interval** in front of each symbol absorbs echoes up to 150.5 μs.
:::

Each symbol is a tone that lasts the **useful time** $T_u$, and the spectrum of a tone that lasts $T_u$ is a sinc shape whose nulls are $1/T_u$ apart. With the subcarriers spaced exactly $1/T_u$, every subcarrier's spectrum crosses zero at the center of every other one, so the receiver can separate them perfectly with an FFT even though their spectra overlap. That property is **orthogonality**, and it is the O in OFDM. The transmitter builds all the subcarriers at once with an inverse FFT, and the receiver separates them with a forward FFT.

In front of each symbol the transmitter adds a **guard interval** $T_g$, a copy of the end of the symbol, which makes each symbol 2.902 ms long. The receiver ignores the guard, so an echo that arrives up to 150.5 μs late, about 45 km of extra path, still falls inside the symbol it belongs to. The explorer in the next frame shows both effects.
::::

::::{frame} OFDM Explorer
:class: viz-frame

:::{depth}
The left panel shows the spectra of five neighboring subcarriers with the HD Radio spacing; the red dots on the dashed line are what the four neighbors add at the center subcarrier's frequency. At spacing 1.00 every red dot sits on zero. Move the spacing away from 1.00 and the dots leave zero, and the leakage readout shows how much the neighbors interfere. The right panel shows two symbols with their guards, an echo of them, and the receiver's FFT window. Drag the echo delay past 150 μs and the end of symbol 1's echo enters symbol 2's window, shown in red.
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

::::{frame} How Strong the Sidebands Are
:::{present}
- Both sidebands together carry 1% of the host's power: **−20 dBc**.
- Each sideband is −23 dBc, and each subcarrier is −45.8 dBc.
- Since 2010 the FCC has allowed up to −14 dBc.
:::

The digital signal is much weaker than the analog one, so that it does not disturb analog receivers or the stations on the neighboring channels. NRSC-5 and the FCC specify its power relative to the analog **host**, in **dBc**, decibels relative to the carrier. As first approved, the two sidebands together carry 1% of the host's power, $-20$ dBc. Each sideband carries half of that, and each of the 382 subcarriers an equal share:

$$\begin{aligned}
-20 - 10\log_{10} 2 &= -23.0\ \text{dBc} \\
-20 - 10\log_{10} 382 &= -45.8\ \text{dBc}
\end{aligned}$$

In 2010 the FCC allowed stations to raise the digital power to as much as $-14$ dBc, and many did, to reach farther. The two sidebands can also differ by up to 10 dB, which a station uses to protect a neighbor on one side. Measuring the sidebands therefore tells us how a station has set up its digital signal.
::::

::::{frame} The Test Signal
:::{present}
<img src="../../viz/img/L14-grc-test-tx.png"
     alt="GNU Radio Companion with L14-hd-test-tx.grc open: for each sideband, a Random Uniform Source, Chunks to Symbols for QPSK, Stream to Tagged Stream, OFDM Carrier Allocator, a reverse FFT, an OFDM Cyclic Prefixer, and a level; an FM host from filtered noise and a 19 kHz pilot; an analog-only neighbor shifted to minus 400 kHz; a Noise Source; an Add, Head, and a conversion to unsigned bytes into a File Sink"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Each sideband is random QPSK on 191 subcarriers, built with an inverse FFT.
- It writes 4 s in the RTL-SDR's format: 11.9 MB.
:::

`L14-hd-test-tx.grc` builds a hybrid station the way the previous two frames describe, with GNU Radio's own OFDM blocks. For each sideband, random QPSK symbols fill the subcarriers that the **OFDM Carrier Allocator** lists, a reverse **FFT** of size 4096 at 1,488,375 samples per second turns them into one OFDM symbol, so each FFT bin is exactly one 363.4 Hz subcarrier, and the **OFDM Cyclic Prefixer** adds the 224-sample guard. The flowgraph sets each sideband to $-23$ dBc. The FM host is filtered noise and a 19 kHz pilot at 75 kHz deviation, and an analog-only station sits 400 kHz below.

The sidebands carry random symbols, not NRSC-5 data, so nrsc5 cannot decode this file; it is a test signal for finding and measuring the sidebands. It writes `L14-hd-test.cu8`, unsigned 8-bit I and Q at 1,488,375 samples per second, which is the format the RTL-SDR and nrsc5 record. Nothing in it transmits: its last block is a File Sink.
::::

::::{frame} The Sideband Finder
:::{present}
<img src="../../viz/img/L14-grc-find.png"
     alt="GNU Radio Companion with L14-hd-find.grc open: a File Source of bytes, a Throttle, UChar To Float, Add Const minus 127.5, Multiply Const 1/128, Deinterleave, and Float To Complex, and a disabled Soapy RTLSDR Source, both feeding a frequency sink, a waterfall sink, and three Frequency Xlating FFT Filters for the host and the two sidebands, each followed by Complex to Mag squared, a Moving Average, Keep 1 in N, and Log10, with two Subtract blocks feeding a number sink"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Five blocks turn unsigned bytes into complex samples.
- A spectrum, a waterfall, and three band-power meters show the sidebands.
:::

`L14-hd-find.grc` plays the test file, any RTL-SDR recording made at 1,488,375 samples per second, or the RTL-SDR live. An RTL-SDR file stores each sample as two unsigned bytes from 0 to 255, so the first five blocks subtract 127.5, scale by 1/128, and pair the bytes into complex samples. The Soapy RTLSDR Source delivers complex samples directly, so it skips those blocks; as in Lesson 7, we switch between the file and the radio by disabling one source and enabling the other.

The **QT GUI Frequency Sink** and **Waterfall Sink** use an FFT of 4096 points, so each bin is one subcarrier wide. The three meters measure the power in a band, which the next frames use.
::::

::::{frame} Finding the Sidebands
:::{present}
<img src="../../viz/img/L14-hd-find.png"
     alt="The L14 sideband finder window labeled Simulated: L14 test file: the number sink reads minus 23.05 dBc for the upper sideband and minus 23.04 dBc for the lower; the frequency sink shows the host at 100.3 MHz peaking near minus 33 dB, flat shelves near minus 58 dB on both sides, a floor near minus 80 dB, and the analog neighbor at 99.9 MHz; the waterfall shows the shelves as two straight bands of constant width beside the host"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The shelves have flat tops and sharp edges, unlike FM.
- On the waterfall they are straight bands that never change width.
:::

On the frequency sink, the shelves begin 129.4 kHz from the station, at 100.1706 and 100.4294 MHz, and end at 100.1016 and 100.4984 MHz. Their tops are flat because every subcarrier carries the same power, and their edges are sharp because the subcarriers stop at 356 and 546. The FM host is rounded, and on the waterfall its width wanders with the audio, while the shelves stay the same width all the time. That difference is how we recognize HD Radio on a live band: look for two straight, flat bands about 130 to 200 kHz either side of a station.

The shelves sit about 25 dB under the top of the host on the display, a little more than the 23 dB between their powers, because the frequency sink shows power per 363.4 Hz bin. The host concentrates its power in fewer bins near the center, and each sideband spreads its power evenly over 191 bins. To read the power ratio itself, we measure total power in each band.
::::

::::{frame} Measuring Sideband Power
:::{present}
<img src="../../viz/img/L14-hd-meters.png"
     alt="The number sink of the L14 sideband finder: Upper sideband minus 23.050537 dBc and Lower sideband minus 23.039446 dBc, each with a bar on a scale from minus 40 to 0"
     style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Each meter shifts a band to 0 Hz, filters it, and averages $\vert x\vert^2$ for 0.2 s.
- The difference of two meters in dB is the sideband's power in dBc.
:::

A band-power meter is four blocks we have used before. A **Frequency Xlating FFT Filter** moves the band's center to 0 Hz and keeps only the band, $\pm 100$ kHz for the host and $\pm 34.7$ kHz around $\pm 163.9$ kHz for each sideband, and decimates by 6. **Complex to Mag^2** gives each sample's power, a **Moving Average** over 0.2 s averages it, **Keep 1 in N** slows the result to 50 readings a second, and **Log10** with a factor of 10 converts each reading to dB. Subtracting the host's meter from a sideband's meter gives that sideband in dBc.

On the test file the meters read $-23.05$ and $-23.04$ dBc, which matches the $-23$ dBc each sideband was built with. The same flowgraph on the real station recorded in the nrsc5 project's sample file reads about $-24.6$ and $-23.7$ dBc, close to the $-20$ dBc total of the original rule. The Variables `inner` and `outer` set the meters' band by subcarrier number, so the same meters work on an extended hybrid station.
::::

::::{frame} Decoding with nrsc5
:::{present}
```
nrsc5 -g 40 100.3 0          # tune 100.3 MHz, play HD1
nrsc5 -w hd.cu8 100.3 0      # also record the IQ
nrsc5 -r hd.cu8 0            # decode a recording
```
:::
:::{present}
- nrsc5 tunes the RTL-SDR, decodes the sidebands, and plays the audio.
- Program 0 is HD1; 1 to 3 are HD2 to HD4.
:::

Finding and measuring the sidebands needs only the spectrum. Decoding them takes the rest of NRSC-5: the receiver synchronizes to the reference subcarriers, demodulates each subcarrier's QPSK, undoes the interleaving and the convolutional code, and decompresses the audio. The open-source **nrsc5** project does all of that from an RTL-SDR or a recording, at 1,488,375 samples per second, the rate of our test file. It plays the chosen program and prints the station's name, the song title and artist, and measures of signal quality as they arrive. A recording that nrsc5 makes with `-w` opens in `L14-hd-find.grc` too.

nrsc5 is a C program, not a GNU Radio block, and it is not part of radioconda, so you install it separately: build it from source on Linux, install it with Homebrew on macOS, or use the project's MSYS2 build on Windows. We have not run it in this course yet, so expect the lab's decode step to need some adjustment. The related project gr-nrsc5 is an HD Radio transmitter, not a receiver, and this course does not transmit on the FM band.
::::

::::{frame} Key Point
:::{present}
:class: callout
HD Radio adds two OFDM sidebands, 129.4 to 198.4 kHz from the station's center and about 20 dB below the analog host. They appear as flat shelves on a spectrum, band-power meters measure them, and nrsc5 decodes them.
:::
::::

::::{frame} On the SDR
:::{present}
- Set the RTL-SDR to 1,488,375 samples per second, centered on the station.
- Look for flat shelves 129 to 198 kHz either side of each station.
- Receiving is unrestricted, and the RTL-SDR receives only.
:::

To look for HD Radio live, disable the File Source in `L14-hd-find.grc`, enable the RTL-SDR Source, and type the station's frequency into Center. Centering on the station puts the RTL-SDR's DC spike on the host, where it does not touch the sidebands or the meters. Set the RF gain from your L5 Lab gain table, and lower it if the floor rises or copies of strong stations appear, because the sidebands are 20 dB or more below the host and an overloaded receiver buries them. Not every station carries HD Radio, so step through the strong stations in the band and watch the waterfall for the two straight bands.

A weak sideband measurement reads high, because the band's noise adds to it. Check the floor beside the shelves: the shelves should stand at least 10 dB above it. As in Lesson 7, receiving is unrestricted and transmitting is not; nothing in this lesson transmits.
::::

::::{frame} Downloads
:class: read-only doc-links

- <a class="doc-link" href="../../grc/L14-hd-test-tx.grc" download>L14-hd-test-tx.grc</a>: writes `L14-hd-test.cu8`, 4 s (11.9 MB) of a simulated hybrid station at 100.3 MHz, with an analog-only neighbor 400 kHz below. Run it once; it stops on its own.
- <a class="doc-link" href="../../grc/L14-hd-find.grc" download>L14-hd-find.grc</a>: the spectrum, waterfall, and sideband power meters, playing the test file, an RTL-SDR recording at 1,488,375 samples per second, or the RTL-SDR live.
- <a class="doc-link" href="../../legacy/refs/nrsc-1011s_hd-radio.pdf" target="_blank" rel="noopener">NRSC-5 Layer 1 FM specification, SY_IDD_1011s (PDF)</a>: Section 3.5 and Table 5-1 list the numbers this lesson uses.
- nrsc5, the receiver, is at <a href="https://github.com/theori-io/nrsc5" target="_blank" rel="noopener">github.com/theori-io/nrsc5</a>, with build instructions for Linux, macOS, and Windows.

Put both flowgraphs in one folder and run the test transmitter first; GRC runs a flowgraph from its own folder, so the finder finds the test file there.
::::

::::{frame} Summary
:class: read-only

| Quantity | Value | Where it comes from |
| :-- | :-- | :-- |
| Subcarrier spacing | $\Delta f$ = 363.4 Hz | 1,488,375 / 4096 |
| Sideband | subcarriers 356 to 546, 129.4 to 198.4 kHz | $k\,\Delta f$ |
| Partition | 19 subcarriers: 18 data, 1 reference | 10 per sideband, plus subcarrier 546 |
| Symbol | $T_u$ = 2.752 ms, $T_g$ = 150.5 μs, 2.902 ms total | $T_u = 1/\Delta f$, $T_g = (7/128)\,T_u$ |
| Power | −20 dBc total, −23 dBc per sideband; up to −14 dBc since 2010 | 382 subcarriers |
| Decoder | nrsc5, RTL-SDR at 1,488,375 samples per second | program 0 is HD1 |
::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE448_L14_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE448_L14_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Looking Ahead
:::{present}
- The L14 Lab builds a sideband meter, identifies a station's mode, and decodes a live station.
- Lesson 15 recovers the carrier and timing of an mPSK signal.
:::

Today we found the HD Radio sidebands beside an FM station, measured their power with meters built from familiar blocks, and saw why HD Radio divides its sidebands into hundreds of orthogonal subcarriers. The L14 Lab is the bench version: build the sideband meter yourself, use it on a capture whose configuration you do not know, measure a live station, and decode it with nrsc5.

Lesson 15 turns to the receiver work that nrsc5 hid from us today. Every QPSK subcarrier here needed its phase and timing recovered before its symbols could be read, and Lesson 15 builds that recovery for a single mPSK carrier in GNU Radio.
::::
