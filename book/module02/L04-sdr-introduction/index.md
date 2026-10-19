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
     alt="Tuning ranges of the four course SDRs on a log frequency axis from 100 kHz to 30 GHz: RTL-SDR Blog V4 from 500 kHz to 1.766 GHz, receive only; HackRF One from 1 MHz to 6 GHz, half duplex; PlutoSDR from 325 MHz to 3.8 GHz, full duplex; ADALM-PHASER from 10.0 to 10.5 GHz, an 8-element array. Dashed lines mark FM broadcast, AIS, 433.92 MHz, ADS-B, GPS L1, and the 2.4 GHz ISM band"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Each bar is one course SDR's tuning range.
- The dashed lines are signals this course receives or decodes.
:::

The RTL-SDR in your kit plugs into a USB port and receives broadcast FM at 100 MHz, ship AIS at 162 MHz, key fobs at 433.92 MHz, and aircraft ADS-B at 1090 MHz. The hardware is the same for all four. What changes is the software on the laptop, which decides how to filter, demodulate, and decode the samples the radio delivers.

The figure places the four radios of this course on one frequency axis, with the signals we will work with marked. The RTL-SDR and the HackRF cover every marked signal below 1.7 GHz, the HackRF and the PlutoSDR reach the 2.4 GHz ISM band where Wi-Fi and Bluetooth operate, and the ADALM-PHASER works only at X band, 10.0 to 10.5 GHz. Choosing a radio for a task starts with this picture.
::::

::::{frame} What Makes a Radio Software Defined
:::{present}
- A hardware radio builds each function as a circuit: one radio, one job.
- An SDR digitizes early and does the rest in software.
- Changing the job means changing the flowgraph, not the hardware.
:::

A traditional analog radio, such as a classic FM receiver, builds each step as a circuit. Its filters pass one channel width, its demodulator handles one modulation, and receiving a different kind of signal means building a different radio. A **software defined radio** (SDR) is a radio in which some or all of the physical layer, the filtering, mixing, demodulation, and decoding, is done in software. The hardware only tunes to a band, filters it, and converts it to numbers.

An SDR still needs analog hardware: an antenna, a filter, an amplifier, and a converter. Everything after the converter is a program, so the same box becomes an FM receiver, an ADS-B decoder, or a spectrum analyzer depending on which flowgraph runs. In this course that program is a GNU Radio flowgraph, which Lesson 5 introduces.
::::

::::{frame} The Course SDRs
:::{present}
| Radio | Tunes | Max rate | Bits | Transmit |
| :-- | :-- | :-- | :-: | :-- |
| RTL-SDR | 0.5–1766 MHz | 2.56 MS/s | 8 | no |
| HackRF | 1–6000 MHz | 20 MS/s | 8 | half duplex |
| PlutoSDR | 325–3800 MHz | 61.44 MS/s | 12 | full duplex |
| PHASER | 10.0–10.5 GHz | via Pluto | 12 | — |
:::

The **RTL-SDR Blog V4** is a receive-only USB dongle built around the RTL2832U, whose converter delivers 8-bit samples. Its datasheet gives 2.56 MS/s as the highest rate without dropped samples. The **HackRF One** from Great Scott Gadgets tunes from 1 MHz to 6 GHz and samples at up to 20 MS/s with 8-bit $I$ and 8-bit $Q$. It can transmit, but only half duplex: it transmits or receives, not both at once.

The **PlutoSDR** (Analog Devices ADALM-PLUTO) has 12-bit converters and one transmitter and one receiver, which can run at the same time (full duplex). It samples at up to 61.44 MS/s, but its analog bandwidth is at most 20 MHz. The **ADALM-PHASER** (CN0566) is an 8-element phased array at 10.0 to 10.5 GHz. It converts its signals down to an intermediate frequency of about 2.2 GHz and uses a PlutoSDR to digitize them, so its sample rate and bits are the PlutoSDR's. This lesson uses only its receive path. The Sources frame below links each manufacturer's numbers.
::::

::::{frame} Sources for the Specifications
:class: read-only doc-links

Every number in the table above comes from the manufacturer's own data:

- <a class="doc-link" href="https://www.rtl-sdr.com/wp-content/uploads/2024/12/RTLSDR_V4_Datasheet_V_1_0.pdf" target="_blank" rel="noopener">RTL-SDR Blog V4 datasheet</a>: 500 kHz to 1.766 GHz, 2.56 MS/s stable (up to 3.2 MS/s with dropped samples).
- <a class="doc-link" href="https://osmocom.org/projects/rtl-sdr/wiki/Rtl-sdr" target="_blank" rel="noopener">Osmocom rtl-sdr wiki</a>: the RTL2832U delivers 8-bit $I/Q$ samples.
- <a class="doc-link" href="https://greatscottgadgets.com/hackrf/one/" target="_blank" rel="noopener">Great Scott Gadgets, HackRF One</a>: 1 MHz to 6 GHz, up to 20 million samples per second, 8-bit quadrature samples, half duplex.
- <a class="doc-link" href="https://www.analog.com/ADALM-PLUTO" target="_blank" rel="noopener">Analog Devices, ADALM-PLUTO</a>: 325 MHz to 3.8 GHz, up to 20 MHz instantaneous bandwidth, 12-bit ADC and DAC, up to 61.44 MSPS, one transmitter and one receiver, half or full duplex.
- <a class="doc-link" href="https://wiki.analog.com/resources/eval/user-guides/circuits-from-the-lab/cn0566/overview_setup" target="_blank" rel="noopener">Analog Devices wiki, CN0566 (ADALM-PHASER)</a>: an 8-element array at 10.0 to 10.5 GHz, an LTC5548 mixer to an IF of about 2.2 GHz, and an ADALM-PLUTO to digitize it.
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

Every receiver in this course follows the chain in the figure. The **RF front end** comes first. A filter passes the band of interest and rejects strong signals outside it, and a **low-noise amplifier** (LNA) raises the signal above the noise of everything after it. Lesson 2 showed that the first amplifier sets most of a receiver's noise figure, which is why the LNA sits right after the filter. The front end also holds the adjustable gain that GNU Radio's gain setting controls.

The **mixer** and **local oscillator** (LO) shift the band down so the converter can sample it, the **low-pass filters** keep only the shifted band, and the two **analog-to-digital converters** (ADCs) turn it into a stream of numbers. A transmitter runs the same chain in reverse, with **digital-to-analog converters** (DACs) and a mixer that shifts the signal up. The samples travel over USB to the **host**, the laptop running GNU Radio.
::::

::::{frame} The Mixer Moves the Band
:::{present}
<img src="../../viz/img/L04-mixer-shift.svg"
     alt="Two spectra side by side: before the mixer, three stations at 98.4, 100.3, and 101.4 MHz around an LO at 100.0 MHz; after the mixer, the same three stations at minus 1.6, plus 0.3, and plus 1.4 MHz around 0 Hz"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- A mixer multiplies the signal by the LO.
- A signal at $f_{LO} + \Delta$ comes out at $\Delta$.
- Tuning the radio means changing $f_{LO}$.
:::

A **mixer** multiplies the incoming signal by the LO, a sine wave at $f_{LO}$. The product of two cosines is a cosine at their difference frequency plus one at their sum:

$$\begin{aligned}
\cos a \cos b &= \tfrac{1}{2}\cos(a - b) \\
&\quad + \tfrac{1}{2}\cos(a + b)
\end{aligned}$$

with $a = 2\pi f_{RF} t$ for the signal and $b = 2\pi f_{LO} t$ for the LO. The low-pass filter after the mixer removes the sum. A station at 100.3 MHz mixed with an LO at 100.0 MHz comes out at 0.3 MHz, and the 200.3 MHz sum is filtered away. Every station keeps its shape and its spacing; only the frequency axis moves. When we set an SDR's center frequency in GNU Radio, we are setting $f_{LO}$, and the band around it lands at 0 Hz.
::::

::::{frame} I and Q: Two Mixers a Quarter Cycle Apart
:::{present}
- One mixer folds $f_{LO} + \Delta$ and $f_{LO} - \Delta$ onto the same $\Delta$.
- A second mixer, with the LO shifted 90°, tells them apart.
- Each sample is $I + jQ$.
:::

A single mixer has a problem. A station 300 kHz above the LO and another 300 kHz below it both come out at 300 kHz, and nothing in a single real output says which was which. The fix is the second branch of the chain figure. The signal goes to two mixers, one driven by the LO and one by the LO shifted 90°, a quarter cycle. The first output is the **in-phase** component $I$ and the second is the **quadrature** component $Q$.

Together they form one complex sample, $I + jQ$, the point in the plane of Lesson 3. A signal above the LO makes that point rotate one way and a signal below makes it rotate the other way, so the two stations are now distinguishable. Lesson 5 shows what this looks like on GNU Radio's plots, including the negative frequencies it makes possible.
::::

::::{frame} Zero-IF and Superheterodyne
:::{present}
- **Zero-IF**: one quadrature mixer straight to 0 Hz (PlutoSDR).
- **Superheterodyne**: first to a fixed IF, then to 0 Hz (HackRF, ADALM-PHASER).
- **RTL-SDR**: a low IF, then $I/Q$ in the digital chip.
:::

The chain in the figure goes from RF to 0 Hz in one step, which makes it a **direct-conversion**, or **zero-IF**, receiver. The PlutoSDR's AD9363 transceiver works this way. Zero-IF needs few parts, but anything that leaks into the mixer output at 0 Hz lands in the middle of the band, which is the DC spike of Lesson 5.

A **superheterodyne** receiver mixes twice. The first mixer moves the signal to a fixed **intermediate frequency** (IF), where filters and amplifiers can be designed for one frequency, and a second, quadrature mixer moves it to 0 Hz. The HackRF uses a superheterodyne front end. The ADALM-PHASER is one too: its own mixer moves 10.0 to 10.5 GHz down to about 2.2 GHz, and the PlutoSDR performs the second conversion. The RTL-SDR's tuner chip converts to a low IF, and the RTL2832U digitizes that and forms $I$ and $Q$ digitally. GNU Radio receives complex samples from all four, so the flowgraph does not depend on which architecture produced them.
::::

::::{frame} Part 2: Sample Rate and Bandwidth
:::{present}
- Complex samples at $f_s$ show a band $f_s$ wide, centered on $f_{LO}$.
- GNU Radio carries each sample in 8 bytes: $8 f_s$ bytes per second.
- 20 MS/s is 160 MB/s into the flowgraph.
:::

The sample rate $f_s$ sets how much spectrum we see at once. With complex samples, the window is $f_s$ wide, from $f_{LO} - f_s/2$ to $f_{LO} + f_s/2$. Lesson 5 shows why and what happens to signals outside it. An RTL-SDR at 2.4 MS/s sees 2.4 MHz of the FM band, twelve 200 kHz channels, and a HackRF at 20 MS/s sees all 20 MHz of it at once. Near the edges of the window the radio's own filters begin to roll off, so the usable bandwidth is somewhat less than $f_s$.

A higher rate also means more data. Inside GNU Radio each complex sample is two 32-bit floats, 8 bytes, so a flowgraph handles

$$8 f_s \ \text{bytes per second}$$

which is 19.2 MB/s at 2.4 MS/s and 160 MB/s at 20 MS/s. Every block processes every sample, and a laptop that cannot keep up drops samples; most radio drivers print an overflow message in GNU Radio's console when that happens. The right sample rate is a little more than the bandwidth of the signal we want, not the radio's maximum.
::::

::::{frame} SDR Window
:class: viz-frame

:::{depth}
The plot is a simulated band, and the shaded region is the part of it the chosen radio sees at its center frequency and sample rate. Start on the FM band with the RTL-SDR at 2.4 MS/s: three stations fit in the window. Switch to the HackRF and raise the sample rate to 20 MS/s to see the whole band, and watch the data rate into GNU Radio grow to 160 MB/s. Choose the PlutoSDR and note that it cannot tune to 98 MHz at all. On the 2.4 GHz ISM band, find the center frequency that puts one whole 20 MHz Wi-Fi channel in view, and note that the PlutoSDR's window stops growing at 20 MHz however high the sample rate goes.
:::

:::{present}
<iframe src="../../viz/sdr-window.html"
        width="100%" height="457"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="SDR window: the part of a simulated band that the RTL-SDR, HackRF, or PlutoSDR can see at a chosen center frequency and sample rate, with the data rate into GNU Radio">
</iframe>
:::
::::

::::{frame} Part 3: Bits and Dynamic Range
:::{present}
- An $N$-bit ADC has $2^N$ levels between $-$full scale and $+$full scale.
- Each bit adds about 6 dB: 8 bits span about 48 dB, 12 bits about 72 dB.
- Above full scale, the ADC clips.
:::

An ADC rounds each voltage to the nearest of $2^N$ levels between its negative and positive **full scale**. The rounding error acts like a small noise added to every sample, and each extra bit halves the step size, which lowers that noise by 6 dB. The **dynamic range**, the span from the strongest signal the converter can take without clipping to its own noise, is therefore about 6 dB per bit:

$$\text{DR} \approx 6N\ \text{dB}$$

which is 48 dB for the 8-bit RTL-SDR and HackRF and 72 dB for the 12-bit PlutoSDR. The exact figure for a full-scale sine wave is $6.02N + 1.76$ dB, 50 dB and 74 dB, but 6 dB per bit is the number to carry. We measure signal levels against full scale in **dBFS**: 0 dBFS is full scale, and a signal at $-6$ dBFS has half the full-scale amplitude. A signal above 0 dBFS cannot be represented, and the ADC **clips** it.
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

The **ADC** block is an Embedded Python Block, ten lines of code saved inside the `.grc` file. It clips $I$ and $Q$ to full scale, $\pm 1$, and rounds each to one of $2^N$ levels, with $N$ chosen from the bits menu: 8 for the RTL-SDR and HackRF, 12 for the PlutoSDR, and 16 for comparison. The frequency sink shows the spectrum after the ADC, and the time sink shows 64 output samples. The sink's 0 dB line is not full scale, so we read differences between levels on its plot, not absolute values.
::::

::::{frame} 8 Bits
:::{present}
<img src="../../viz/img/L04-adc-8bit.png"
     alt="The L4 flowgraph running with 8 bits and 0 dB gain: the spectrum shows the strong tone near minus 15 dB at plus 0.3 MHz above a ragged floor of quantization noise and spurs between about minus 100 and minus 75 dB, with no visible tone at minus 0.49 MHz; the time sink shows I and Q as sine waves of amplitude 0.5"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The 8-bit floor and spurs reach within about 60 dB of the strong tone.
- The weak tone, 64 dB down, is buried.
:::

With 8 bits and 0 dB gain, the strong tone stands near $-15$ dB on the sink's scale, and the ADC's rounding error fills the rest of the band with a ragged floor between about $-100$ and $-75$ dB. Because the input is a pure tone, much of that error repeats with the tone and shows up as discrete spurs rather than smooth noise. The highest of them come within about 60 dB of the strong tone.

The weak tone at $-0.49$ MHz is 64 dB below the strong one, more than the roughly 48 dB an 8-bit converter spans, and it is not visible. Nothing is wrong with the weak signal; the converter's own error is larger. The time sink shows why the strong tone is safe: its peaks reach 0.5, half of full scale.
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

Switching the menu to 12 bits, the PlutoSDR's resolution, changes nothing about the input. The floor drops to about $-118$ dB and becomes smooth, and the weak tone appears at $-0.49$ MHz near $-79$ dB, about 64 dB below the strong tone and about 40 dB above the floor. Four more bits add about 24 dB of dynamic range. The floor on the plot drops by a little less, about 20 dB, because at 8 bits part of the rounding error sits in the spurs rather than the floor. Either way, the converter now spans both signals.

Lowering the weak-signal slider until the tone disappears measures the span directly. With 16 bits the floor drops only to about $-134$ dB, 16 dB lower rather than 24, because the Noise Source's noise is now larger than the converter's error and sets the floor. That is the situation a well-adjusted receiver aims for: the antenna's noise, amplified by the front end, should sit above the converter's own floor.
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

Every capture in this course starts with the same three choices. For broadcast FM, a station about 200 kHz wide near 100 MHz, the RTL-SDR at 2.4 MS/s is enough, and Lesson 5 does exactly that. A 20 MHz Wi-Fi channel at 2.4 GHz is out of the RTL-SDR's range and too wide for its sample rate, so it needs the HackRF at 20 MS/s or the PlutoSDR. A flowgraph that transmits a test signal into a cable needs the HackRF or the PlutoSDR, and the PlutoSDR if it must receive at the same time. Finding the direction of an X-band source needs the ADALM-PHASER.

The gain comes last, set against the strongest signal in the window, not the one we want. A weak signal next to a strong one is where the extra bits of the PlutoSDR matter, and where an 8-bit radio needs a narrower window or a filter ahead of it to keep the strong signal out.
::::

::::{frame} Other SDR Software
:class: read-only

GNU Radio is the course's tool, but every radio in this course also works with standalone receivers, which are useful for finding a signal before building a flowgraph for it.

| Program | What it is for |
| :-- | :-- |
| GQRX | a spectrum, waterfall, and AM/FM/SSB receiver for Linux and macOS, built on GNU Radio |
| SDR++ | a cross-platform spectrum, waterfall, and receiver |
| SDR# (SDRSharp) | a Windows spectrum, waterfall, and receiver |
| SDRangel | a receiver and transmitter with many built-in demodulators |
| SigDigger | a signal analyzer for measuring unknown signals |
| URH | the Universal Radio Hacker, for recording and decoding short bursts such as remotes; Lesson 17 uses it |
::::

::::{frame} Key Point
:::{present}
:class: callout
An SDR mixes a band to 0 Hz and digitizes $I$ and $Q$. The sample rate sets the visible spectrum; the ADC's bits, about 6 dB each, set how weak a signal can be near a strong one.
:::
::::

::::{frame} Downloads
:class: read-only doc-links

- <a class="doc-link" href="../../grc/L04-adc-bits.grc" download>L04-adc-bits.grc</a>: a strong and a weak tone through a simulated ADC, with menus and sliders for the bits, the gain, and the weak signal's level. No hardware needed.

Open it from GRC's File menu, or run `gnuradio-companion L04-adc-bits.grc` from the radioconda prompt. The ADC block is an Embedded Python Block; GRC saves its code inside the `.grc` file, so it needs no other download. Install radioconda first; Lesson 5 walks through the install.
::::

::::{frame} Summary
:class: read-only

| Idea | What it is | Number to remember |
| :-- | :-- | :-- |
| SDR | filtering, mixing, demodulation, and decoding in software | one radio, many signals |
| RTL-SDR Blog V4 | receive only, 8 bits | 0.5–1766 MHz, 2.56 MS/s |
| HackRF One | half duplex, 8 bits | 1–6000 MHz, 20 MS/s |
| PlutoSDR | full duplex, 12 bits | 325–3800 MHz, 20 MHz bandwidth |
| ADALM-PHASER | 8-element array, digitized by a PlutoSDR | 10.0–10.5 GHz |
| Mixer | $f_{LO} + \Delta$ comes out at $\Delta$ | center frequency = $f_{LO}$ |
| $I$ and $Q$ | two mixers 90° apart | tell $+\Delta$ from $-\Delta$ |
| Sample rate | window $f_s$ wide | $8 f_s$ bytes per second in GNU Radio |
| ADC bits | about 6 dB of dynamic range each | 8 bits: 48 dB; 12 bits: 72 dB |
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
- It shows complex sampling, aliasing, and gain on a live RTL-SDR.
:::

Today we followed a signal from the antenna through the front end, the mixer and LO, and the ADCs to the host, and we saw how the sample rate and the ADC's bits limit what a capture can show. The four course radios differ in tuning range, sample rate, bits, and whether they transmit, and choosing among them is the first step of every lab.

Lesson 5 picks up where the ADC leaves off. It installs radioconda, builds a flowgraph from a signal source and then from a real RTL-SDR, and shows complex sampling, aliasing, the DC spike, and the gain setting on GNU Radio's plots. Before Lesson 5, download `L04-adc-bits.grc` so it is ready to open once GNU Radio is installed.
::::
