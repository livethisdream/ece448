---
frame_view: true
---

# L4 - SDR Introduction

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">SDR Introduction</h1>

<div class="title-rule"></div>

One USB radio receives broadcast FM, aircraft, and key fobs, because software decides what to do with its samples.

Lesson 4 · Module 2: SDR & GNU Radio Foundations · Dr. Neil Rogers
::::

::::{frame} Slides
:class: read-only

:::{admonition} Slides
:class: slides
<a href="../../slides/L04-sdr-introduction.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L04-sdr-introduction.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L04-sdr-introduction.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '2'">
  <li>I can describe what a Software Defined Radio is, contrast it with a traditional hardware radio, and identify the SDR platforms used in this course (RTL-SDR, HackRF, PlutoSDR, ADALM-PHASER).</li>
  <li>I can identify the roles of the RF frontend, ADC/DAC, and host in an SDR signal chain and describe sample-rate, bandwidth, and dynamic-range trade-offs.</li>
</ol>
::::

::::{frame} One Radio, Many Signals
:::{present}
<img src="../../viz/img/L04-tuning-ranges.svg"
     alt="Tuning ranges of four SDRs on a log frequency axis from 100 kHz to 30 GHz: the PlutoSDR from 70 MHz to 6 GHz in extended-frequency mode, full duplex; two optional radios, the HackRF One from 1 MHz to 6 GHz and the RTL-SDR Blog V4 from 500 kHz to 1.766 GHz; and the ADALM-PHASER from 10.0 to 10.5 GHz, an 8-element array. Dashed lines mark FM broadcast, AIS, 433.92 MHz, ADS-B, GPS L1, and the 2.4 GHz ISM band"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Each bar is one SDR's tuning range; the PlutoSDR is the course radio.
- The dashed lines are signals this course receives or decodes.
:::

The PlutoSDR in your kit plugs into a USB port and receives broadcast FM at 100 MHz, ship AIS at 162 MHz, key fobs at 433.92 MHz, aircraft ADS-B at 1090 MHz, and Wi-Fi at 2.4 GHz, all with the same hardware, and it transmits too. What changes is the software on the laptop, which decides how to filter, demodulate, and decode the samples the radio delivers.

The figure places the radios on one frequency axis, with the signals we will work with marked. The course Plutos run in **extended-frequency mode**, which tunes 70 MHz to 6 GHz, so the PlutoSDR covers every marked signal. The HackRF and the RTL-SDR are optional extras that cover the same signals below 1.7 GHz, and the ADALM-PHASER works only at X band, 10.0 to 10.5 GHz. Choosing a radio for a task starts with checking that its bar covers the signal.
::::

::::{frame} What Makes a Radio Software Defined
:::{present}
- A hardware radio builds each function as a circuit: one radio, one job.
- An SDR digitizes early and does the rest in software.
- Changing the job means changing the flowgraph, not the hardware.
:::

A traditional analog radio, such as a classic FM receiver, builds each step as a circuit. Its filters pass one channel width, its demodulator handles one modulation, and receiving a different kind of signal means building a different radio. A **software defined radio** (SDR) is a radio in which some or all of the physical layer, the filtering, mixing, demodulation, and decoding, happens in software. The hardware only tunes to a band, filters it, and converts it to numbers.

An SDR still needs analog hardware: an antenna, a filter, an amplifier, and a converter. Everything after the converter is a program, so the same box becomes an FM receiver, an ADS-B decoder, or a spectrum analyzer depending on which flowgraph runs. In this course that program is a GNU Radio flowgraph, which Lesson 5 introduces.
::::

::::{frame} The Course SDRs
:::{present}
| Radio | Tunes | Max rate | Bits | Transmit |
| :-- | :-- | :-- | :-: | :-- |
| PlutoSDR | 70–6000 MHz | 4 MS/s sustained | 12 | full duplex |
| PHASER | 10.0–10.5 GHz | via Pluto | 12 | — |
| HackRF | 1–6000 MHz | 20 MS/s | 8 | half duplex |
| RTL-SDR | 0.5–1766 MHz | 2.56 MS/s | 8 | no |
:::

The **PlutoSDR** (Analog Devices ADALM-PLUTO) is the course radio, and every lab uses it. It has 12-bit converters and one transmitter and one receiver, which can run at the same time (full duplex). Out of the box it tunes 325 MHz to 3.8 GHz; the course Plutos are set to extended-frequency mode, which treats the chip as an AD9364 and tunes 70 MHz to 6 GHz. Its converters sample at up to 61.44 MS/s, but its USB 2.0 link streams only about 4 MS/s without dropped samples, so we keep live flowgraphs at 2 to 4 MS/s and capture anything wider in short bursts. The **ADALM-PHASER** (CN0566) is an 8-element phased array at 10.0 to 10.5 GHz. It converts its signals down to an intermediate frequency of about 2.2 GHz and uses a PlutoSDR to digitize them.

Two other radios are optional extras that no lab requires. The **HackRF One** from Great Scott Gadgets tunes from 1 MHz to 6 GHz and streams up to 20 MS/s of 8-bit samples, half duplex. The **RTL-SDR Blog V4** is a receive-only 8-bit USB dongle whose datasheet gives 2.56 MS/s as its highest rate without dropped samples. The Sources frame below links each manufacturer's numbers.
::::

::::{frame} Sources for the Specifications
:class: read-only doc-links

Every number in the table above comes from the manufacturer's or the driver project's data:

- <a class="doc-link" href="https://www.analog.com/ADALM-PLUTO" target="_blank" rel="noopener">Analog Devices, ADALM-PLUTO</a>: 325 MHz to 3.8 GHz as shipped, up to 20 MHz instantaneous bandwidth, 12-bit ADC and DAC, up to 61.44 MSPS, one transmitter and one receiver, half or full duplex.
- <a class="doc-link" href="https://wiki.analog.com/university/tools/pluto/users/customizing" target="_blank" rel="noopener">Analog Devices wiki, Customizing the Pluto configuration</a>: setting the PlutoSDR to run as an AD9364, 70 MHz to 6 GHz with up to 56 MHz of bandwidth, the extended-frequency mode the course Plutos use.
- <a class="doc-link" href="https://wiki.analog.com/university/tools/pluto/devs/specs" target="_blank" rel="noopener">Analog Devices wiki, ADALM-PLUTO specifications</a>: USB 2.0 streams up to 4 MSPS with no dropped samples.
- <a class="doc-link" href="https://wiki.analog.com/resources/eval/user-guides/circuits-from-the-lab/cn0566/overview_setup" target="_blank" rel="noopener">Analog Devices wiki, CN0566 (ADALM-PHASER)</a>: an 8-element array at 10.0 to 10.5 GHz, an LTC5548 mixer to an IF of about 2.2 GHz, and an ADALM-PLUTO to digitize it.
- <a class="doc-link" href="https://greatscottgadgets.com/hackrf/one/" target="_blank" rel="noopener">Great Scott Gadgets, HackRF One</a> (optional): 1 MHz to 6 GHz, up to 20 million samples per second, 8-bit quadrature samples, half duplex.
- <a class="doc-link" href="https://www.rtl-sdr.com/wp-content/uploads/2024/12/RTLSDR_V4_Datasheet_V_1_0.pdf" target="_blank" rel="noopener">RTL-SDR Blog V4 datasheet</a> (optional): 500 kHz to 1.766 GHz, 2.56 MS/s stable (up to 3.2 MS/s with dropped samples), 8-bit $I/Q$ samples from the RTL2832U.
::::

::::{frame} Part 1: Inside an SDR
:::{present}
<img src="../../viz/img/L04-sdr-chain.svg"
     alt="Block diagram of a direct-conversion SDR receiver: an antenna feeds a filter and an LNA, the RF front end; the signal splits into two mixers driven by an LO, one directly and one through a 90 degree shift; each mixer output passes through a low-pass filter and an ADC, giving I and Q, which travel over USB to the host running GNU Radio"
     style="max-width: 780px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- **Front end**: filter and amplify the band.
- **Mixer and LO**: move it down to 0 Hz.
- **ADCs**: turn $I$ and $Q$ into numbers for the host.
:::

Follow the figure from left to right. The **RF front end** comes first: a filter passes the band and a **low-noise amplifier** (LNA) raises it, first in line because, from Lesson 2, the first amplifier sets most of the noise figure. The front end also holds the gain that the PlutoSDR Source block's gain setting controls. The optional HackRF and RTL-SDR reach the same $I/Q$ stream by other routes, so GNU Radio sees the same samples from every radio.

The **mixer** and **local oscillator** (LO) shift the band down so the converter can sample it, the **low-pass filters** keep only the shifted band, and the two **analog-to-digital converters** (ADCs) turn it into a stream of numbers. A transmitter runs the same chain in reverse, with **digital-to-analog converters** (DACs) and a mixer that shifts the signal up. The samples travel over USB to the **host**, the laptop running GNU Radio.
::::

::::{frame} The Mixer Moves the Band
:::{present}
<img src="../../viz/img/L04-mixer-shift.svg"
     alt="Two spectra side by side: before the mixer, stations at 100.3 and 101.4 MHz above an LO at 100.0 MHz and one at 98.6 MHz below it, drawn in amber; after one real mixer and a low-pass filter, the stations above the LO sit at 0.3 and 1.4 MHz, and the amber station below the LO has folded to 1.4 MHz, on top of the 101.4 MHz one"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- A mixer multiplies the signal by the LO.
- A signal at $f_{LO} + \Delta$ comes out at $\Delta$.
- One real mixer also puts $f_{LO} - \Delta$ at $\Delta$.
:::

A **mixer** multiplies the incoming signal by the LO, a sine wave at $f_{LO}$. The product of two cosines is a cosine at their difference frequency plus one at their sum:

$$\begin{aligned}
\cos a \cos b &= \tfrac{1}{2}\cos(a - b) \\
&\quad + \tfrac{1}{2}\cos(a + b)
\end{aligned}$$

with $a = 2\pi f_{RF} t$ for the signal and $b = 2\pi f_{LO} t$ for the LO. The low-pass filter after the mixer removes the sum. A station at 100.3 MHz mixed with an LO at 100.0 MHz comes out at 0.3 MHz, and the filter removes the 200.3 MHz sum. When we set an SDR's center frequency in GNU Radio, we are setting $f_{LO}$, and the band around it lands near 0 Hz.

The figure also shows the limit of one real mixer. A cosine cannot tell a positive frequency from a negative one, so the station at 98.6 MHz, 1.4 MHz below the LO, comes out at 1.4 MHz, on top of the 101.4 MHz station.
::::

::::{frame} I and Q: Two Mixers a Quarter Cycle Apart
:::{present}
- One mixer folds $f_{LO} + \Delta$ and $f_{LO} - \Delta$ onto the same $\Delta$.
- A second mixer, with the LO shifted 90°, tells them apart.
- Each sample is $I + jQ$.
:::

Look again at the second branch of the chain figure. The signal goes to two mixers, one driven by the LO and one by the LO shifted 90°, a quarter cycle. The first output is the **in-phase** component $I$ and the second is the **quadrature** component $Q$.

Together they form one complex sample, $I + jQ$, the point in the plane of Lesson 3. A signal above the LO makes that point rotate one way and a signal below makes it rotate the other way, so the 98.6 MHz station of the last figure comes out at $-1.4$ MHz, clear of the one at $+1.4$ MHz. Lesson 5 shows what this looks like on GNU Radio's plots, including the negative frequencies it makes possible.
::::

::::{frame} Zero-IF and Superheterodyne
:::{present}
- **Zero-IF**: one quadrature mixer straight to 0 Hz.
- **Superheterodyne**: first to a fixed IF, then to 0 Hz.
- The ADALM-PHASER: 10.0–10.5 GHz to about 2.2 GHz, then a PlutoSDR.
:::

The chain in the figure goes from RF to 0 Hz in one step, which makes it a **direct-conversion**, or **zero-IF**, receiver; the PlutoSDR is one. Zero-IF needs few parts, but anything that leaks into the mixer output at 0 Hz lands in the middle of the band, which is one source of the DC spike that Lesson 5 shows.

A **superheterodyne** receiver mixes twice: first to a fixed **intermediate frequency** (IF), then to 0 Hz. The ADALM-PHASER mixes X band to about 2.2 GHz, and the PlutoSDR does the rest. Either way, GNU Radio receives complex samples, so the flowgraph does not depend on how the radio produced them.
::::

::::{frame} Part 2: Sample Rate and Bandwidth
:::{present}
- Complex samples at $f_s$ show a band $f_s$ wide, centered on $f_{LO}$.
- GNU Radio carries each sample in 8 bytes: $8 f_s$ bytes per second.
- 20 MS/s is 160 MB/s into the flowgraph.
:::

The sample rate $f_s$ sets how much spectrum we see at once. With complex samples, the window is $f_s$ wide, from $f_{LO} - f_s/2$ to $f_{LO} + f_s/2$. Lesson 5 shows why and what happens to signals outside it. A PlutoSDR at 2.4 MS/s sees 2.4 MHz of the FM band, twelve 200 kHz channels. Seeing the whole 20 MHz band at once takes 20 MS/s, which the PlutoSDR delivers only in a short burst and the optional HackRF streams. Near the edges of the window the radio's own filters begin to roll off, so the usable bandwidth is somewhat less than $f_s$, and the stations at the very ends of the band sit in that roll-off.

A higher rate also means more data. Inside GNU Radio each complex sample is two 32-bit floats, 8 bytes, so a flowgraph handles

$$8 f_s \ \text{bytes per second}$$

which is 19.2 MB/s at 2.4 MS/s and 160 MB/s at 20 MS/s. Every block processes every sample, and a laptop or a USB link that cannot keep up drops samples, which shows up as gaps in the plots and clicks in the audio. The right sample rate is a little more than the bandwidth of the signal we want, not the radio's maximum.
::::

::::{frame} SDR Window
:class: viz-frame

:::{depth}
The plot is a simulated band, and the shaded region is the part of it the chosen radio sees at its center frequency and sample rate. Start on the FM band with the PlutoSDR at 2.4 MS/s: three stations fit in the window. Raise the sample rate: the slider stops at 4 MS/s, the most the PlutoSDR's USB link streams without dropped samples. On the 2.4 GHz ISM band the PlutoSDR shows only a slice of one 20 MHz Wi-Fi channel. Switch to the optional HackRF, raise the sample rate to 20 MS/s, find the center frequency that puts one whole Wi-Fi channel in view, and watch the data rate into GNU Radio grow to 160 MB/s. The PlutoSDR reaches that view only in short bursts.
:::

:::{present}
<iframe src="../../viz/sdr-window.html"
        width="100%" height="457"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="SDR window: the part of a simulated band that the PlutoSDR, or the optional HackRF or RTL-SDR, can see at a chosen center frequency and sample rate, with the data rate into GNU Radio">
</iframe>
:::
::::

::::{frame} Part 3: Bits and Clipping
:::{present}
- An $N$-bit ADC has $2^N$ levels between $-$full scale and $+$full scale.
- More bits put the converter's own noise floor lower.
- Above full scale, the ADC clips.
:::

An ADC rounds each voltage to the nearest of $2^N$ levels between its negative and positive **full scale**: 4096 for the 12-bit PlutoSDR, 256 for the 8-bit HackRF and RTL-SDR. The rounding error acts like a small noise added to every sample, and finer steps mean less of it, so a radio with more bits has a lower floor. The span from the strongest signal the converter can take to that floor is its **dynamic range**, and it decides how weak a signal can be and still show up next to a strong one.

We measure signal levels against full scale in **dBFS**: 0 dBFS is full scale, and a signal at $-6$ dBFS has half the full-scale amplitude. The ADC cannot represent a signal above 0 dBFS, so it **clips** it. The flowgraph below shows both limits on GNU Radio's plots.
::::

::::{frame} The Quantizer Flowgraph
:::{present}
<img src="../../viz/img/L04-grc-adc.png"
     alt="GNU Radio Companion with the L4 flowgraph open: two Signal Sources, a strong tone at 300.7 kHz with amplitude 0.5 and a weak tone at minus 487.3 kHz, and a Noise Source feed an Add block, then a Multiply Const for the gain, a Throttle, and an embedded Python block named ADC with Bits 8, which feeds a QT GUI Frequency Sink and a QT GUI Time Sink. A QT GUI Chooser selects the bits and two QT GUI Ranges set the gain and the weak signal level"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- A strong tone at $-6$ dBFS and a weak one 64 dB below it.
- **Gain**, then an **ADC** block with 8, 12, or 16 bits.
:::

The flowgraph `L04-adc-bits.grc` builds the receiver's problem from two tones. A strong tone at 300.7 kHz with amplitude 0.5, which is $-6$ dBFS, stands in for a nearby station, and a weak tone at $-487.3$ kHz, at $-70$ dBFS by default, stands in for a distant one. A Noise Source adds a very small noise floor. A **Multiply Const** applies the receiver's gain from a slider, in dB.

The **ADC** block is an Embedded Python Block, about 15 lines of code saved inside the `.grc` file. It clips $I$ and $Q$ to full scale, $\pm 1$, and rounds each to one of $2^N$ levels, with $N$ chosen from the bits menu: 12 for the PlutoSDR, 8 for the HackRF and RTL-SDR, and 16 for comparison. The frequency sink shows the spectrum after the ADC, and the time sink shows 64 output samples. The sink's 0 dB line is not full scale, so we read differences between levels on its plot, not absolute values.
::::

::::{frame} 8 Bits
:::{present}
<img src="../../viz/img/L04-adc-8bit.png"
     alt="The L4 flowgraph running with 8 bits and 0 dB gain: the spectrum shows the strong tone near minus 15 dB at plus 0.3 MHz above a ragged floor of quantization noise and spurs between about minus 100 and minus 75 dB, with no visible tone at minus 0.49 MHz; the time sink shows I and Q as sine waves of amplitude 0.5"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The 8-bit floor and spurs reach within about 60 dB of the strong tone.
- The weak tone, 64 dB down, lies below the spurs.
:::

With 8 bits and 0 dB gain, the strong tone stands near $-15$ dB on the sink's scale, and the ADC's rounding error fills the rest of the band with a ragged floor between about $-100$ and $-75$ dB. Because the input is a pure tone, much of that error repeats with the tone and shows up as discrete spurs rather than smooth noise. The highest of them come within about 60 dB of the strong tone.

The weak tone at $-0.49$ MHz is 64 dB below the strong one, below the spurs, and it is not visible, although nothing about the weak signal has changed. The time sink shows why the strong tone is safe: its peaks reach about 0.5, half of full scale.
::::

::::{frame} 12 Bits
:::{present}
<img src="../../viz/img/L04-adc-12bit.png"
     alt="The same flowgraph with 12 bits: the floor drops to about minus 118 dB and is smooth, the strong tone is unchanged near minus 15 dB, and the weak tone appears at minus 0.49 MHz near minus 79 dB, about 40 dB above the floor"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The floor drops about 20 dB, and the spurs are gone.
- The weak tone appears about 40 dB above the floor.
:::

Switching the menu to 12 bits, the PlutoSDR's resolution, changes nothing about the input. The floor drops to about $-118$ dB and becomes smooth, and the weak tone appears at $-0.49$ MHz near $-79$ dB, about 40 dB above the floor. The extra bits did not make the weak signal stronger; they lowered the floor beneath it.

Lowering the weak-signal slider until the tone disappears shows how far below the strong tone a weak signal can sit on this radio. Switching to 16 bits lowers the floor again, but by less, because the Noise Source's noise now sits above the converter's own error and sets the floor. That is the situation a well-adjusted receiver aims for: the antenna's noise, amplified by the front end, should sit above the converter's own floor.
::::

::::{frame} Too Much Gain
:::{present}
<img src="../../viz/img/L04-adc-clip.png"
     alt="The flowgraph with 8 bits and 12 dB gain: the time sink shows I and Q flat-topped at plus and minus 1, the strong tone has risen only to about minus 8 dB, and a large distortion product near minus 0.9 MHz reaches about minus 20 dB, with smaller spurs across the band"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- 12 dB of gain drives the strong tone 6 dB past full scale.
- Clipping creates false signals; the largest is near $-0.9$ MHz.
:::

Raising the gain is the usual way to lift a weak signal out of the converter's floor, and it works only until the strongest signal reaches full scale. At 12 dB of gain the strong tone's amplitude would be 2, 6 dB above full scale. The time sink shows $I$ and $Q$ flattened at $\pm 1$, and the strong tone rises only about 7 dB on the spectrum instead of 12.

The clipping distorts the waveform, and the distortion appears as new signals. The largest, near $-0.9$ MHz, is about 12 dB below the strong tone, and smaller spurs spread across the band. On a real SDR these false signals look exactly like transmissions, which is how an overloaded receiver shows stations at frequencies where nothing transmits. The gain setting is a balance: high enough to lift weak signals above the converter's floor, and low enough to keep the strongest signal below full scale.
::::

::::{frame} Choosing the Radio and Its Settings
:::{present}
1. **Radio**: its tuning range covers the signal, and it transmits if the task does.
2. **Sample rate**: a little more than the signal's bandwidth.
3. **Gain**: the strongest signal in the window stays below full scale.
:::

Every capture in this course starts with the same three choices, and for every lab the radio is the PlutoSDR. For broadcast FM, a station about 200 kHz wide near 100 MHz, the PlutoSDR at 2.4 MS/s is enough, and Lesson 5 does exactly that. A 20 MHz Wi-Fi channel at 2.4 GHz is within its tuning range but wider than the 4 MS/s it streams, so the PlutoSDR captures it in a short burst at 20 MS/s or more; the optional HackRF streams it at 20 MS/s. A flowgraph that transmits a test signal into a cable through the 30 dB attenuator uses the PlutoSDR, which can receive at the same time. Finding the direction of an X-band source needs the ADALM-PHASER.

The gain comes last, set against the strongest signal in the window, not the one we want. A weak signal next to a strong one is where the PlutoSDR's 12 bits matter, and where an 8-bit radio needs a narrower window or a filter ahead of it to keep the strong signal out. Lesson 5 gives the procedure for setting the gain on a live PlutoSDR.
::::

::::{frame} Demo: Explore a Band on the PlutoSDR
:::{present}
1. Run `L05-fm-spectrum.grc` on the PlutoSDR at 98 MHz.
2. Read the spectrum and the waterfall.
3. Drag the center frequency across the band.
4. Raise the gain until false stations appear; back off.
:::

Before building a receiver for a signal, we find it with a flowgraph that only looks. This is an instructor demo with the Lesson 5 flowgraph, which cadets run themselves once GNU Radio is installed. A PlutoSDR Source at 2.4 MS/s feeds a spectrum and a waterfall, with sliders for the center frequency and the gain.

The top plot is the spectrum, 2.4 MHz wide around the center frequency, and the waterfall below it scrolls the same spectrum through time, so a station that stays on the air draws a steady vertical stripe. Each FM station is a stripe about 200 kHz wide. Drag the center frequency slider and the stripes slide across the display. Now raise the gain slider in steps and watch the noise floor and the strongest stations. At first the weak stations rise above the floor; past some setting, new stripes appear where nothing transmits, the clipping of the Too Much Gain frame on a real radio. Back the gain off until they disappear. Lesson 7 adds the demodulator that plays a station, and the same look-first steps find a signal before every lab.
::::

::::{frame} Other SDR Software
:class: read-only

GNU Radio is the course's tool, and every lab step is a GNU Radio flowgraph. Standalone receivers are optional extras for a quick look on your own time; no lab depends on them.

| Program | What it is for |
| :-- | :-- |
| SDR Flex | Dr. Rogers's explore tool: spectrum, waterfall, demodulators, and decoders; runs in a browser |
| GQRX | a spectrum, waterfall, and AM/FM/SSB receiver built on GNU Radio |
| SDR++ | a cross-platform spectrum, waterfall, and receiver |
| SDR# (SDRSharp) | a Windows spectrum, waterfall, and receiver |
| SDRangel | a receiver and transmitter with many built-in demodulators |
| SigDigger | a signal analyzer for measuring unknown signals |
| URH | the Universal Radio Hacker, for recording and decoding short bursts such as remotes; Lesson 17 uses it |
::::

::::{frame} Key Point
:::{present}
:class: callout
An SDR mixes a band to 0 Hz and digitizes $I$ and $Q$. The sample rate sets the visible spectrum; the ADC's bits and the gain set how weak a signal can be near a strong one.
:::
::::

::::{frame} Downloads and Sources
:class: read-only doc-links

- <a class="doc-link" href="../../grc/L04-adc-bits.grc" download>L04-adc-bits.grc</a>: a strong and a weak tone through a simulated ADC, with menus and sliders for the bits, the gain, and the weak signal's level. No hardware needed.

Open it from GRC's File menu, or run `gnuradio-companion L04-adc-bits.grc` from the radioconda prompt. The ADC block is an Embedded Python Block; GRC saves its code inside the `.grc` file, so it needs no other download. Install radioconda first; Lesson 5 walks through the install and hands out `L05-fm-spectrum.grc`, the PlutoSDR flowgraph of the demo.

This lesson follows Dr. Rogers's 2025 slides and these pages:

- <a class="doc-link" href="https://wiki.gnuradio.org/index.php?title=What_Is_GNU_Radio" target="_blank" rel="noopener">GNU Radio wiki, What Is GNU Radio</a>
- <a class="doc-link" href="https://wiki.gnuradio.org/index.php?title=InstallingGR" target="_blank" rel="noopener">GNU Radio wiki, Installing GNU Radio</a>
- <a class="doc-link" href="https://pysdr.org/content/hardware.html" target="_blank" rel="noopener">PySDR, SDR Hardware</a>
- <a class="doc-link" href="https://pysdr.org/content/sampling.html" target="_blank" rel="noopener">PySDR, IQ Sampling</a>
- <a class="doc-link" href="https://pysdr.org/content/frequency_domain.html" target="_blank" rel="noopener">PySDR, Frequency Domain</a>
- <a class="doc-link" href="https://pysdr.org/content/pluto.html" target="_blank" rel="noopener">PySDR, PlutoSDR in Python</a>
::::

::::{frame} Summary
:class: read-only

| Idea | What it is | Number to remember |
| :-- | :-- | :-- |
| SDR | filtering, mixing, demodulation, and decoding in software | one radio, many signals |
| PlutoSDR | the course radio: full duplex, 12 bits | 70–6000 MHz (extended mode), 4 MS/s sustained |
| ADALM-PHASER | 8-element array, digitized by a PlutoSDR | 10.0–10.5 GHz |
| HackRF One | optional: half duplex, 8 bits | 1–6000 MHz, 20 MS/s |
| RTL-SDR Blog V4 | optional: receive only, 8 bits | 0.5–1766 MHz, 2.56 MS/s |
| Mixer | $f_{LO} + \Delta$ comes out at $\Delta$ | center frequency = $f_{LO}$ |
| $I$ and $Q$ | two mixers 90° apart | tell $+\Delta$ from $-\Delta$ |
| Sample rate | window $f_s$ wide | $8 f_s$ bytes per second in GNU Radio |
| ADC bits | more bits, lower floor | 8 bits: 256 levels; 12 bits: 4096 |
| Clipping | strongest signal above 0 dBFS | false signals across the band |
::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE448_L04_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE448_L04_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Looking Ahead
:::{present}
- Lesson 5 installs GNU Radio and builds the first flowgraphs.
- It shows complex sampling, aliasing, and gain on a live PlutoSDR.
:::

Today we followed a signal from the antenna through the front end, the mixer and LO, and the ADCs to the host, and we saw how the sample rate and the ADC's bits limit what a capture can show. The radios differ in tuning range, sample rate, bits, and whether they transmit; the PlutoSDR covers every lab, and checking its range, rate, and gain against the signal is the first step of each one.

Lesson 5 picks up where the ADC leaves off. It installs radioconda, builds a flowgraph from a signal source and then from a real PlutoSDR, and shows complex sampling, aliasing, the DC spike, and the gain setting on GNU Radio's plots. Before Lesson 5, download `L04-adc-bits.grc` so it is ready to open once you install GNU Radio.
::::
