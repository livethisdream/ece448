---
frame_view: true
---

# L6 - AM Simulation

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">AM Simulation</h1>

<div class="title-rule"></div>

DSB-AM, DSB-SC, and SSB built and demodulated in GNU Radio.

Lesson 6 · Module 3: Analog Modulation · Dr. Neil Rogers
::::

::::{frame} Slides
:class: read-only

:::{admonition} Slides
:class: slides
<a href="../../slides/L06-am-simulation.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L06-am-simulation.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L06-am-simulation.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '3'">
  <li>I can describe DSB-AM, DSB-SC, and SSB and identify each on a spectrum.</li>
  <li>I can implement an AM modulator and demodulator in GNU Radio and verify demodulated audio against the source.</li>
</ol>
::::

::::{frame} A Message on a Carrier
:::{present}
<img src="../../viz/img/L06-am-spectrum.png"
     alt="The L6 DSB-AM flowgraph's frequency sink: a carrier at 10 kHz with a pair of sidebands at 9 and 11 kHz and a smaller pair at 7.5 and 12.5 kHz"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- **Modulation** moves an audio message up to a carrier frequency.
- Today's signal: a two-tone message on a 10 kHz carrier, as DSB-AM.
:::

An antenna cannot radiate audio efficiently, and two stations sending audio directly would land on top of each other. **Modulation** solves both problems: it moves the message up to a **carrier** frequency, so each transmitter gets its own channel. The simplest way to do that is to vary the carrier's amplitude with the message, which is **amplitude modulation** (AM). It is still on the air in AM broadcast, in every aircraft radio, and in HF voice links.

The figure is the spectrum of the first flowgraph of this lesson, running in GNU Radio with no hardware. The message is two tones, 1 kHz and 2.5 kHz, and the carrier is 10 kHz. The tall line in the middle is the carrier, and each tone produces a pair of lines on either side of it. By the end of the lesson we will build this signal, two relatives of it, and a receiver for each, and check the receiver's output against the message.
::::

::::{frame} Part 1: DSB-AM
:::{present}
$$s(t) = A_c\left[1 + m\,x(t)\right]\cos(2\pi f_c t)$$
:::
:::{present}
- $m$ is the **modulation index**; the bracket is the **envelope**.
- A tone at $f$ makes sidebands at $f_c - f$ and $f_c + f$.
- The bandwidth is $2W$: here 7.5 to 12.5 kHz.
:::

**Double-sideband AM** (DSB-AM, or simply AM) multiplies a carrier at frequency $f_c$ by one plus the scaled message. We scale the message $x(t)$ so its largest value is 1, and the **modulation index** $m$, from 0 to 1, sets how far the carrier's amplitude swings: at $m = 0.5$ it swings between 0.5 and 1.5 times $A_c$. The quantity in brackets is the **envelope**, the outline the carrier's peaks trace out, and it is a copy of the message riding on a constant.

Multiplying by the carrier shifts the message's spectrum up to $f_c$. The constant 1 becomes the carrier line, and each message tone at $f$ becomes two lines, one at $f_c + f$ in the **upper sideband** and one at $f_c - f$ in the **lower sideband**, each with amplitude $mA_c/2$ times the tone's. With $m = 0.5$, the 1 kHz pair sits 16.5 dB below the carrier and the 2.5 kHz pair 20 dB below, as the opening figure shows. The signal occupies $f_c - W$ to $f_c + W$, where $W$ is the highest message frequency, so its **bandwidth** is $2W$, 5 kHz for our message. The FCC spaces US AM broadcast stations 10 kHz apart for the same reason: each carries about 5 kHz of audio.
::::

::::{frame} The DSB-AM Flowgraph
:::{present}
<img src="../../viz/img/L06-grc-dsb-am.png"
     alt="GNU Radio Companion with L06-dsb-am.grc open: two Signal Sources added to form the message, Multiply Const by m, Add Const 1, and a Multiply with a 10 kHz carrier source feed a frequency sink and a time sink; below, Abs, a Decimating FIR Filter, and Multiply Const pi over 2 form the envelope detector, followed by a DC Blocker, a volume control, and an Audio Sink"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The top row is the transmitter, and the bottom row is the receiver.
- The **Audio Sink** paces the flowgraph, so there is no Throttle.
:::

The top row of `L06-dsb-am.grc` is the transmitter, block for block from the equation: two Signal Sources add to make $x(t)$, a Multiply Const applies $m$, an Add Const adds the 1, and a Multiply mixes the result with a third Signal Source at $f_c$. Its output goes to a frequency sink and to a time sink that overlays the modulated signal on its envelope $1 + m\,x(t)$. The bottom row is the receiver, an **envelope detector**, which the next frames take apart. Its output goes to a second time sink for checking and, through a DC Blocker and a volume slider, to an **Audio Sink**, so we can listen to it.

The whole flowgraph runs at 48 kHz, a rate every laptop sound card supports. Lesson 5 said to use a Throttle only when no hardware sets the pace. The sound card is hardware: it takes exactly 48,000 samples per second, so the Audio Sink sets the pace and a Throttle would only cause audio dropouts.
::::

::::{frame} Modulation Index
:::{present}
<img src="../../viz/img/L06-am-envelope.png"
     alt="Two QT GUI time sinks at m = 0.5: on the left the AM signal fills in under a red envelope that swings between about 0.5 and 1.5; on the right the detector output lies on top of the delayed envelope"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Left: the carrier fills in under its envelope, $1 + m\,x(t)$.
- Right: the detector output lies on the envelope.
:::

The left time sink shows 10 ms of the transmitted signal in blue, with the envelope $1 + m\,x(t)$ in red. The carrier is 10 kHz, so 100 cycles fill the window and blur into a solid band, and the red trace outlines its peaks. The pattern repeats every 2 ms because 1 kHz and 2.5 kHz are both multiples of 500 Hz.

The right time sink compares the receiver's output, in red, with the envelope in blue. The two traces lie on top of each other, which is the check the objective asks for: the demodulated signal matches the source. The envelope is delayed by 57 samples before the comparison, because the receiver's low-pass filter delays everything that passes through it by half its length, and the flowgraph's Delay block applies the same delay to the reference.
::::

::::{frame} The Envelope Detector
:::{present}
- **Abs** rectifies: it keeps the carrier's peaks positive.
- A **low-pass filter** at 3 kHz keeps the envelope and removes the carrier.
- Multiply by $\pi/2$ to restore the level.
:::

An AM receiver only has to recover the envelope, and a circuit as simple as a diode and a capacitor does that, which is why AM was the first broadcast standard. The flowgraph does the same thing with blocks. **Abs** is the diode: it flips the negative half-cycles of the carrier up. A **low-pass filter** is the capacitor: it averages the rectified carrier, which keeps the slowly varying envelope and removes everything at the carrier frequency and above. We use a Low-pass Filter Taps variable with a 3 kHz cutoff and a 1 kHz transition, which passes the message and stops the carrier at 10 kHz.

The average of a rectified cosine is $2/\pi$ of its peak, so a Multiply Const of $\pi/2$ restores the envelope's original level. The DC Blocker then removes the constant 1, which carries no information, before the audio reaches the speaker.
::::

::::{frame} Overmodulation
:::{present}
<img src="../../viz/img/L06-am-overmod.png"
     alt="The same time sinks at m = 1.4: the envelope 1 + m x(t) dips below zero, and the detector output folds those dips back up so it no longer matches the envelope"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- At $m > 1$ the envelope goes negative, and the detector folds it up.
- The audio distorts, and the spectrum spreads.
:::

Drag the slider past $m = 1$ and the bracket $1 + m\,x(t)$ goes negative at the message's troughs. The carrier's amplitude cannot be negative, so the envelope the detector sees is $\vert 1 + m\,x(t)\vert$: the dips fold back up, as the red trace shows at $m = 1.4$, and the output no longer matches the message. This is **overmodulation**. It sounds harsh, and it also adds new frequencies that spread the signal outside its channel and into a neighbor's.

AM transmitters therefore keep $m$ at or below 1, usually well below it, with a limiter on the audio. Listen to the flowgraph's audio as you drag $m$ from 0.5 to 1.4 and back; the distortion is easy to hear.
::::

::::{frame} Where the Power Goes
:::{present}
$$\eta = \frac{m^2 P_x}{1 + m^2 P_x}$$
:::
:::{present}
- $\eta$ is the fraction of power in the sidebands; $P_x$ is the message power.
- One tone at $m = 1$: $\eta = 33\%$, the best case.
:::

The carrier carries no information, yet it takes most of the transmitter's power. The **efficiency** $\eta$ is the fraction of the transmitted power that is in the sidebands, where the message is. For a single tone at full modulation, $P_x = 1/2$ and $\eta = 1/3$: two-thirds of the power goes into the carrier even in the best case. Our two-tone message at $m = 0.5$ has $P_x = 0.26$, which gives $\eta = 6\%$.

In return, the carrier makes the receiver simple and inexpensive. That mattered for broadcasting in 1920, and it still matters for aircraft radios, where a receiver that always works is more important than transmitter power. The other two signals of this lesson remove the waste: DSB-SC removes the carrier, and SSB removes half of what is left.
::::

::::{frame} Part 2: DSB-SC
:::{present}
<img src="../../viz/img/L06-sc-spectrum.png"
     alt="The L6 DSB-SC flowgraph's frequency sink: the four sideband lines at 7.5, 9, 11, and 12.5 kHz and no line at the 10 kHz carrier"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
$$s(t) = A_c\,x(t)\cos(2\pi f_c t)$$
:::

**Double-sideband suppressed carrier** (DSB-SC) drops the 1 from the bracket and multiplies the carrier by the message alone. The flowgraph `L06-dsb-sc.grc` is the DSB-AM transmitter with the Multiply Const and Add Const removed. Its spectrum has the same four sideband lines and the same 5 kHz bandwidth, but no carrier line at 10 kHz, so all of the power is in the sidebands and $\eta = 100\%$.

Removing the carrier complicates the receiver. The envelope of $x(t)\cos(2\pi f_c t)$ is $\vert x(t)\vert$, not $x(t)$, because the message itself goes negative. An envelope detector recovers $\vert x(t)\vert$, which is the same folding as overmodulation and sounds just as bad. DSB-SC needs a different receiver.
::::

::::{frame} Coherent Demodulation
:::{present}
<img src="../../viz/img/L06-sc-phi0.png"
     alt="The DSB-SC flowgraph's time sink with the receiver's LO phase at 0 degrees: the coherent receiver's output lies on the message, and the envelope detector's output is a rectified, distorted copy"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Multiply by a local carrier, then low-pass filter.
- Coherent output (red) matches $x(t)$; envelope output (green) does not.
:::

A **coherent receiver**, also called a product detector, multiplies the received signal by its own copy of the carrier, a **local oscillator** (LO), and low-pass filters the product. The product is $x(t)\cos^2(2\pi f_c t)$, and with $\theta = 2\pi f_c t$ the identity

$$\cos^2\theta = \tfrac{1}{2} + \tfrac{1}{2}\cos 2\theta$$

splits it into half the message plus a copy of the message at $2f_c$. The low-pass filter removes the copy at $2f_c = 20$ kHz, and a Multiply Const of 2 restores the level. The flowgraph builds both receivers side by side. The time sink shows the message in blue, the coherent receiver in red on top of it, and the envelope detector in green, which is the rectified $\vert x(t)\vert$ and plainly wrong. The Listen To menu switches the audio between them.
::::

::::{frame} The LO Must Match
:::{present}
<img src="../../viz/img/L06-sc-phi90.png"
     alt="The DSB-SC time sink with the receiver's LO phase at 90 degrees: the coherent receiver's output is a flat line at zero"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- An LO phase error $\phi$ scales the output by $\cos\phi$.
- At $90°$ the output is zero.
:::

The coherent receiver works only if its LO matches the transmitter's carrier in both frequency and phase. With a phase error $\phi$, the output is $x(t)\cos\phi$: a small error lowers the volume, and at $\phi = 90°$ the output vanishes, as the flat red trace shows. A frequency error is worse, because the phase then drifts continuously and the output fades in and out.

In a simulation, both oscillators come from the same `fc` variable, so they match exactly. A real receiver has to recover the carrier's frequency and phase from the signal, and since DSB-SC transmits no carrier, it needs help. FM stereo is a working example: its left-minus-right audio is DSB-SC on a 38 kHz subcarrier, and the station sends a 19 kHz **pilot tone** so receivers can rebuild the 38 kHz LO. Lesson 7 receives it.
::::

::::{frame} Part 3: SSB
:::{present}
<img src="../../viz/img/L06-ssb-spectra.png"
     alt="Two frequency sinks from L06-ssb.grc: with USB selected, lines at 11 and 12.5 kHz and the lower pair suppressed to about minus 80 dB; with LSB selected, lines at 9 and 7.5 kHz and the upper pair suppressed"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The two sidebands carry the same information. **SSB** sends one.
- Its bandwidth is $W$ = 2.5 kHz, half that of DSB.
:::

The upper and lower sidebands of a DSB signal are mirror images, so either one alone carries the whole message. **Single sideband** (SSB) sends one of them: the **upper sideband** (USB) or the **lower sideband** (LSB). An SSB signal has no carrier, needs half the bandwidth of DSB, and puts all of its power into the one sideband it sends, which is why it is the standard for long-range HF voice in military, maritime, and amateur radio.

The figure shows `L06-ssb.grc` with each setting of its Sideband menu. With USB selected, the lines at 11 and 12.5 kHz remain and the lower pair is about 60 dB down. With LSB selected, only the lines at 9 and 7.5 kHz remain. Note that the LSB reverses the message's spectrum: the higher tone is the line farther below the carrier.
::::

::::{frame} The Phasing Method
:::{present}
<img src="../../viz/img/L06-grc-ssb.png"
     alt="GNU Radio Companion with L06-ssb.grc open: the message feeds a Hilbert block, whose complex output multiplies a complex 10 kHz Signal Source; Complex To Real gives the SSB signal, which feeds a frequency sink and a product detector made of a Multiply with a real 10 kHz source, a Decimating FIR Filter, and a Multiply Const of 2"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
$$\begin{aligned}
z(t) &= x(t) + j\hat{x}(t) \\
s(t) &= \mathrm{Re}\left\{z(t)\,e^{\pm j2\pi f_c t}\right\}
\end{aligned}$$
:::

The flowgraph makes SSB by the **phasing method**. The **Hilbert** block shifts the phase of every frequency in the message by $90°$, which turns each cosine into a sine, and outputs the complex signal $z(t) = x(t) + j\hat{x}(t)$. That signal has only positive frequencies: it is the message with its negative-frequency half removed, the same idea as the complex tone of Lesson 5 that turned in only one direction.

Multiplying by a complex carrier $e^{+j2\pi f_c t}$ moves those positive frequencies up to just above $f_c$, and taking the real part gives the USB. Using $e^{-j2\pi f_c t}$ instead gives the LSB, so the Sideband menu changes only the sign of the carrier's frequency. The Hilbert block is an FIR filter with 129 taps, and its imperfection is what leaves the unwanted sideband 60 dB down instead of gone.
::::

::::{frame} Receiving SSB
:::{present}
<img src="../../viz/img/L06-ssb-mistuned.png"
     alt="The SSB flowgraph's time sink with a receiver tuning error of 200 Hz: the product detector's output no longer lies on the delayed message because each tone has shifted in frequency"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- A product detector at $f_c$ recovers $x(t)$ from either sideband.
- A tuning error $\Delta f$ shifts every audio tone by $\Delta f$.
:::

The SSB receiver is the same product detector as DSB-SC: multiply by a cosine at $f_c$, low-pass filter, and multiply by 2. With the receiver tuned exactly, its output lies on the message, for USB and LSB alike. The figure shows what happens with the receiver 200 Hz off: every tone in the output moves by 200 Hz, so 1 kHz becomes 800 Hz and 2.5 kHz becomes 2.3 kHz, and the traces drift apart.

A frequency error in SSB shifts the audio rather than fading it, and a voice stays intelligible within about 100 Hz of the right frequency, although it sounds high or low pitched. Phase does not matter to the ear. That is why an SSB receiver needs no carrier recovery: the operator turns the tuning knob until the voice sounds natural. Drag the tuning slider and listen.
::::

::::{frame} AM Explorer
:class: viz-frame

:::{depth}
The left panel plots 2 ms of the signal, its envelope in red, and the message in dashed amber; the right panel shows the spectral lines around the 10 kHz carrier. Start with DSB-AM at $m = 0.5$ and notice the envelope follow the message. Raise $m$ past 1 and watch the envelope fold. Switch to DSB-SC and the carrier line disappears, while the envelope becomes $\vert x(t)\vert$. Switch to USB or LSB and notice the bandwidth halve, and that the envelope of the two-tone SSB signal is not the message at all, which is why SSB needs a product detector.
:::

:::{present}
<iframe src="../../viz/am-explorer.html"
        width="100%" height="427"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="AM explorer: DSB-AM, DSB-SC, USB, and LSB in time and frequency, with the modulation index, bandwidth, sideband power, and whether an envelope detector recovers the message">
</iframe>
:::
::::

::::{frame} Identifying Each on a Spectrum
:::{present}
| Signal | Carrier line | Sidebands | Bandwidth | Receiver |
| :-- | :-: | :-: | :-: | :-- |
| DSB-AM | yes | two | $2W$ | envelope |
| DSB-SC | no | two | $2W$ | coherent |
| SSB | no | one | $W$ | product |
:::

We can identify every signal in this lesson on a spectrum display by asking two questions. Is there a steady line at the center of the signal? Only DSB-AM has one. Is the signal symmetric about its center? DSB-AM and DSB-SC are, because they carry both sidebands, while SSB sits entirely on one side of its carrier frequency, above it for USB and below it for LSB. With a voice message, an SSB signal on a waterfall is a band about 3 kHz wide that comes and goes with speech, with no line beside it.

The table also says what to build to receive each one. An envelope detector is enough for DSB-AM, DSB-SC needs a coherent receiver with carrier recovery, and SSB needs a product detector tuned by ear.
::::

::::{frame} On the SDR
:::{present}
- AM broadcast uses 540 to 1700 kHz, and aircraft use AM from 118 to 137 MHz.
- Long-range HF voice uses SSB.
- On an SDR, the envelope detector is one block: **Complex to Mag**.
:::

Each of today's signals is on the air. AM broadcast fills 540 to 1700 kHz, and every aircraft and control tower talks in AM between 118 and 137 MHz, including the recorded airport weather broadcasts (ATIS), which make a good first target for Lesson 7's AM receiver. SSB carries long-range HF voice: military and maritime stations use USB, and amateurs use LSB below 10 MHz and USB above it. DSB-SC rides inside every FM stereo broadcast.

An SDR delivers complex samples centered on its tuned frequency, so a signal arrives with its carrier already at 0 Hz. The envelope is then the magnitude of each sample, and the whole envelope detector is one **Complex to Mag** block, which is what GNU Radio's AM Demod block contains. An SSB receiver on an SDR keeps the real part after a frequency shift. Lesson 7 builds both receivers around an RTL-SDR.
::::

::::{frame} Downloads
:class: read-only doc-links

- <a class="doc-link" href="../../grc/L06-dsb-am.grc" download>L06-dsb-am.grc</a>: a two-tone message as DSB-AM on a 10 kHz carrier, with an envelope detector, a modulation-index slider, and audio out. No hardware needed.
- <a class="doc-link" href="../../grc/L06-dsb-sc.grc" download>L06-dsb-sc.grc</a>: the same message as DSB-SC, with a coherent receiver and an envelope detector side by side and an LO phase slider.
- <a class="doc-link" href="../../grc/L06-ssb.grc" download>L06-ssb.grc</a>: the same message as USB or LSB by the phasing method, with a product detector and a tuning-error slider.

Each flowgraph plays its receiver's output through your laptop's speakers; start with the volume low. Open a `.grc` file from GRC's File menu, or run `gnuradio-companion L06-dsb-am.grc` from the radioconda prompt.
::::

::::{frame} Summary
:class: read-only

| Signal | Transmitter | Spectrum | Receiver | Number to remember |
| :-- | :-- | :-- | :-- | :-- |
| DSB-AM | $[1 + m\,x(t)]\cos(2\pi f_c t)$ | carrier and two sidebands, $2W$ | Abs, low-pass, $\times\pi/2$ | $m \le 1$; $\eta \le 33\%$ |
| DSB-SC | $x(t)\cos(2\pi f_c t)$ | two sidebands, $2W$ | multiply by LO, low-pass, $\times 2$ | output $\propto \cos\phi$ |
| SSB | $\mathrm{Re}\{z(t)\,e^{\pm j2\pi f_c t}\}$ | one sideband, $W$ | product detector at $f_c$ | $\Delta f$ shifts the audio |
::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE448_L06_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE448_L06_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Key Point
:::{present}
:class: callout
DSB-AM puts most of its power in a carrier so the receiver can be an envelope detector. DSB-SC and SSB drop the carrier, and the receiver has to supply its own.
:::
::::

::::{frame} Looking Ahead
:::{present}
- The L6 Lab builds each modulator and receiver from an empty canvas.
- Lesson 7 receives real AM and FM with an RTL-SDR.
:::

Today we built DSB-AM, DSB-SC, and SSB transmitters in GNU Radio, received each one, and compared the output with the message on a time sink and by ear. The L6 Lab is the hands-on version: predict each spectrum, build the DSB-AM flowgraph yourself, measure its sidebands and its overmodulation point, and then measure what LO phase and tuning errors do to the DSB-SC and SSB receivers.

Lesson 7 replaces the simulated transmitter with the air. An RTL-SDR delivers complex samples, the envelope detector becomes a Complex to Mag block, and we receive an aircraft band AM station, then a broadcast FM station with its stereo and RDS data.
::::
