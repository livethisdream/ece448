---
frame_view: true
---

# L8 - FSK

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">FSK</h1>

<div class="title-rule"></div>

Frequency-shift keying sends each bit as one of two tones. Today we send text through an FSK transmitter, a noisy channel, and a receiver.

Lesson 8 · Module 4: Digital Modulation · Dr. Neil Rogers
::::

::::{frame} Slides
:class: read-only

:::{admonition} Slides
:class: slides
<a href="../../slides/L08-fsk.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L08-fsk.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L08-fsk.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '4'">
  <li>I can describe FSK modulation and implement an FSK transmitter and receiver in GNU Radio.</li>
</ol>
::::

::::{frame} A Message on Two Tones
:::{present}
<img src="../../viz/img/L08-tx-1k.png"
     alt="The L8 transmitter flowgraph running: on the left, the bits of the message as a square wave between minus 1 and plus 1, with the transmitted I the same 1 kHz cosine during every bit, and Q a sine that leads or lags I depending on the bit; on the right, the spectrum with two peaks at minus 1 kHz and plus 1 kHz"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- A 1 is a tone at $+\Delta f$ and a 0 is a tone at $-\Delta f$.
- The spectrum shows both tones: $\pm 1$ kHz here.
:::

Lessons 6 and 7 put an analog message on a carrier. From here on the message is data. **Frequency-shift keying** (FSK) sends it by shifting the frequency up by the **deviation** $\Delta f$ for each 1 and down by $\Delta f$ for each 0. The receiver only has to decide, once per bit, which of the two tones it heard.

Run `L08-fsk-tx.grc` and look at the spectrum first: two peaks, at $-1$ and $+1$ kHz, like Lesson 5's complex tone. Then look at the time plot. The blue trace is the bits. The red trace, $I$, is the same 1 kHz cosine during every bit, because a cosine cannot tell which way the phase turns. The green trace, $Q$, can: it flips relative to $I$ each time the bit changes.
::::

::::{frame} Where FSK Is Used
:::{present}
- Pagers, weather balloons, and amateur APRS
- Key fobs and garage-door remotes at 315 and 433.92 MHz
- Bluetooth and many drone links, as Gaussian FSK (GFSK)
:::

FSK is everywhere because the receiver is simple and the amplitude never changes, so the transmitter's power amplifier can run at full output. POCSAG pagers, weather-balloon radiosondes, and APRS use it, and so do most key fobs and garage-door remotes at 315 and 433.92 MHz, which Lesson 17 reverse engineers. Bluetooth and many drone links use **Gaussian FSK** (GFSK), which smooths each frequency step so the signal takes less bandwidth; a GFSK receiver uses the same blocks as today's.
::::

::::{frame} Part 1: The Transmitter
:::{present}
<img src="../../viz/img/L08-grc-tx.png"
     alt="GNU Radio Companion with the L8 transmitter open: a Vector Source of message bytes feeds Unpack K Bits, Chunks to Symbols, Repeat, and Frequency Mod, then a Throttle into a QT GUI Frequency Sink, with Complex To Real and Complex to Imag feeding a QT GUI Time Sink"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Bytes become bits, bits become $\pm 1$, and each symbol repeats `sps` times.
- **Frequency Mod** turns each $\pm 1$ into a frequency of $\pm\Delta f$.
:::

Walk the chain left to right on the canvas:

1. **Vector Source** repeats the bytes of a text message, with a newline at the end.
2. **Unpack K Bits** splits each byte into 8 bits, most significant first.
3. **Chunks to Symbols** maps 0 to $-1$ and 1 to $+1$.
4. **Repeat** holds each symbol for `sps` samples, the **samples per symbol**.
5. **Frequency Mod** turns $+1$ into a tone at $+\Delta f$ and $-1$ into a tone at $-\Delta f$.

Frequency Mod is the FM transmitter block; FSK is FM with a square wave of bits as the message. It keeps the phase continuous from bit to bit, which keeps the spectrum compact.
::::

::::{frame} Three Numbers Set the Signal
:::{present}
- **Symbol rate** $R_s = f_s/\text{sps}$: 32 kHz / 32 = 1000 baud.
- **Deviation** $\Delta f$: 1 kHz.
- **Modulation index** $h = 2\Delta f / R_s = 2$.
:::

Open the Frequency Mod and Variable blocks and read off the three numbers. The **symbol rate**, in baud, is set by the sample rate and the samples per symbol; with one bit per symbol it is also the bit rate:

$$R_s = \frac{f_s}{\text{sps}}$$

Frequency Mod takes the **deviation** as a **sensitivity**, the phase change per sample for an input of 1:

$$k = \frac{2\pi \Delta f}{f_s}$$

which is $2\pi \times 1000 / 32000 = 0.196$ rad per sample here. The **modulation index** $h$ compares the tone spacing with the symbol rate; at $h = 2$ the two peaks are clearly separate.
::::

::::{frame} Bandwidth
:::{present}
<img src="../../viz/img/L08-tx-3k.png"
     alt="The transmitter with the deviation slider at 3000 Hz: I and Q oscillate at 3 kHz and the spectrum shows the two peaks at minus 3 and plus 3 kHz"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The signal takes about $B \approx 2(\Delta f + R_s)$.
- 1 kHz deviation at 1000 baud takes about 4 kHz.
- The receiver's filter is set to pass this band.
:::

Drag the deviation slider to 3 kHz and watch the peaks move to $\pm 3$ kHz and the spectrum widen. A faster symbol rate widens it too. **Carson's rule** from FM adds the two:

$$B \approx 2(\Delta f + R_s)$$

At 1 kHz and 1000 baud that is 4 kHz, and at 3 kHz it is 8 kHz. We use the number for one thing: setting the receiver's first filter. A wider deviation makes the tones easier to tell apart, but the wider filter also lets in more noise.
::::

::::{frame} Part 2: The Channel
:::{present}
- `L08-fsk-link.grc`: transmitter, channel, and receiver in one file.
- The **Channel Model** adds noise and a frequency offset, each on a slider.
:::

Close the transmitter and open `L08-fsk-link.grc`. Its top row is the transmitter you just ran. After the Throttle, a **Channel Model** block stands in for the air: it adds noise of a chosen voltage and shifts the signal by a chosen frequency offset. Run it and drag the noise slider: the tones on the spectrum stay put while the noise floor rises and falls. Leave the noise at 0.5 and the offset at 0 while we walk through the receiver.
::::

::::{frame} Part 3: The Receiver
:::{present}
<img src="../../viz/img/L08-grc-rx.png"
     alt="The receiver half of the L8 link flowgraph in GNU Radio Companion: a Throttle and a Channel Model feed a Low Pass Filter, Quadrature Demod, Moving Average, Symbol Sync, and Binary Slicer, then Correlate Access Code - Tag Stream, Repack Bits, and a Text Sink; a QT GUI Frequency Sink and a QT GUI Eye Sink display the signal"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Filter to the signal, turn frequency into a number, and decide each bit.
:::

The receiver works in three steps. A **Low Pass Filter** with a cutoff of $\Delta f + R_s = 2$ kHz passes the 4 kHz band from $-2$ to $+2$ kHz and removes the noise outside it. A **Quadrature Demod** turns the frequency of each sample into a number. The last three blocks find each bit's sampling instant and decide whether it is a 0 or a 1.
::::

::::{frame} The Quadrature Demodulator
:::{present}
- It measures the phase step from one sample to the next.
- A phase step is a frequency: $\pm\Delta f$ gives $\pm 1$ with gain $f_s/(2\pi\Delta f)$.
:::

**Quadrature Demod** is Lesson 7's FM demodulator. It measures how far the phase turns from one sample to the next, which is the frequency, and multiplies by its gain. Set the gain to

$$g = \frac{f_s}{2\pi \Delta f}$$

which is $32000 / (2\pi \times 1000) = 5.09$ here, and the tone at $+\Delta f$ comes out as $+1$ and the tone at $-\Delta f$ as $-1$. The gain is the reciprocal of the transmitter's sensitivity: the demodulator undoes the modulator, and out comes the square wave of bits, with noise on it.
::::

::::{frame} Finding the Bits
:::{present}
<img src="../../viz/img/L08-link-clean.png"
     alt="The L8 link running at noise voltage 0.5: the received spectrum shows the two tones about 25 dB above the noise floor, the eye diagram of the demodulator output is wide open with traces at plus 1 and minus 1, and the labels read Received: USAFA ECE 448: FSK over a noisy channel, and 21 correct of 21 received in 10 s"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- **Moving Average** over one symbol, then **Symbol Sync** samples each bit at its peak.
- **Binary Slicer**: above 0 is a 1, below 0 is a 0.
:::

A **Moving Average** over `sps` samples smooths each bit. **Symbol Sync** picks one sample per bit, at the peak, and keeps adjusting its timing because the two clocks never quite match. The **Binary Slicer** decides: above 0 is a 1, below 0 is a 0.

Now look at the **eye diagram** on the right, many two-bit stretches of the moving average overlaid. The traces cross at the bit edges; the gap between $+1$ and $-1$ is the **eye opening**. A wide-open eye means every decision is easy. At a noise voltage of 0.5, all 21 lines in the first 10 s arrive intact.
::::

::::{frame} Part 4: Packets
:::{present}
- The transmitter adds a 64-bit **access code** and a length header to each line.
- The receiver searches for the access code to find where each line starts.
:::

The slicer's bits do not say where a byte starts, so the transmitter sends each line as a **packet**. A **Protocol Formatter** builds a header, a 64-bit **access code** the receiver knows in advance followed by the line's length, and a **Tagged Stream Mux** puts it in front of the line.

At the receiver, **Correlate Access Code - Tag Stream** watches for the access code, allowing up to 2 wrong bits, reads the length, and passes that many bytes on. **Repack Bits** packs them back into bytes, and the **Text Sink**, a small Python block, shows the latest line and counts how many matched since a slider last moved. Lesson 10 uses the same framing for ASCII over PAM.
::::

::::{frame} Turn Up the Noise
:::{present}
<img src="../../viz/img/L08-link-noisy.png"
     alt="The L8 link at noise voltage 1.3: the noise floor is about 8 dB higher, the eye diagram is still mostly open, with a few traces spiking across zero, and the labels show a line with two wrong characters and 7 correct of 29 received in 13 s"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- At 0.5 V: a wide-open eye, and every line arrives.
- At 1.3 V: spikes cross zero, and most lines have an error.
:::

Drag the noise slider up slowly and watch three things: the floor on the spectrum, the eye, and the text.

- **0.5 V:** the tones stand about 25 dB above the floor, the eye is wide open, and every line arrives.
- **1.0 V:** the eye's traces thicken, and an occasional character goes wrong.
- **1.3 V:** the floor is about 8 dB higher. Now and then a sharp spike, an FM click, crosses zero; one that lands on a sampling instant is a bit error. Only 7 of 29 lines arrive clean.
- **2 V:** the receiver almost never finds the access code.

The whole change, from clean text to no text, takes a small turn of the slider. That is why Lesson 2's link margin matters: a link that only just works fails on the first fade.
::::

::::{frame} FSK Explorer
:class: viz-frame

:::{depth}
The explorer repeats the noise experiment with the receiver's output in view. The left panel is the spectrum, with the Carson bandwidth shaded and the two tones dashed. The right panel is the receiver's output for 16 bits, with the sent levels in gray and a dot at each decision; a red dot is a wrong bit. Raise the deviation: the tones move apart and the band widens. Set it back to 1000 Hz and raise the noise slowly; note the noise voltage, and the SNR the panel shows, when the first red dot appears. Then try 2000 baud: the band widens, more noise gets through, and red dots appear at a lower noise voltage.
:::

:::{present}
<iframe src="../../viz/fsk-explorer.html"
        width="100%" height="403"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="FSK explorer: the spectrum and demodulator output of a 32 kHz FSK link as the deviation, symbol rate, and noise change, with the bit errors counted">
</iframe>
:::
::::

::::{frame} Frequency Offset
:::{present}
<img src="../../viz/img/L08-link-offset.png"
     alt="The L8 link with a 600 Hz frequency offset: the two tones in the spectrum have moved right, and the eye diagram is still open but shifted up, with levels at about plus 1.6 and minus 0.4"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- An offset shifts both tones, so the demodulator output shifts by $f_\text{off}/\Delta f$.
- This link tolerates about $\pm 600$ Hz, a little over half the deviation.
:::

No two radios agree exactly on frequency: their crystals are off by a few parts per million, and at 915 MHz 2 ppm is 1.8 kHz. Set the noise back to 0.5 and drag the offset slider to 600 Hz. Both tones move right, and the eye moves up to about $+1.6$ and $-0.4$. Both levels are still on the correct side of zero, so the text still arrives.

Keep going. At 800 Hz the lower level is near zero and the filter starts to cut off the upper tone: lines arrive, but every one has errors. At 1000 Hz none arrive. Real receivers either use a deviation much larger than the expected offset, as key fobs do, or measure the offset and remove it before the demodulator. The L8 Lab measures both effects.
::::

::::{frame} FSK on a Real Radio
:::{present}
<img src="../../viz/img/L08-burst-sim.svg"
     alt="Simulated waterfall of an FSK burst near 433.92 MHz: two vertical tracks 40 kHz apart, alternating every millisecond during the preamble, then switching irregularly during the data; one bit lasts 1 ms"
     style="max-width: 680px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Tone spacing gives $2\Delta f$; the shortest dwell gives $1/R_s$.
- To transmit, use a cable, a shielded box, or low power in an ISM band, and only when the lesson says to; nothing in L8 transmits.
:::

On a waterfall, FSK is two tracks side by side with the signal jumping between them. The figure simulates a 433.92 MHz remote, the kind Lesson 17 decodes. Read two numbers off it: the tracks are 40 kHz apart, so $\Delta f = 20$ kHz, and the shortest stay on one track, in the preamble, is 1 ms, so the symbol rate is 1000 baud. A live waterfall row often lasts longer than one bit, so measure the dwell in URH or on the Quadrature Demod output. Those two numbers set the receiver's filter, gain, and samples per symbol.

To run this link over the air, replace the Throttle and Channel Model with a PlutoSDR or HackRF sink on one side and a source on the other, with a resampler to raise the 32 kHz stream to a rate the radio supports. In class we transmit only into a cable, into a shielded enclosure, or at very low power in an ISM band, and only when the lesson says to. Nothing in this lesson or its lab transmits.
::::

::::{frame} Key Point
:::{present}
:class: callout
FSK sends each bit as one of two tones. The transmitter is a Frequency Mod block; the receiver filters to $2(\Delta f + R_s)$, demodulates frequency into $\pm 1$, samples each bit at its peak, and slices at zero.
:::
::::

::::{frame} Downloads and Sources
:class: read-only doc-links

- <a class="doc-link" href="../../grc/L08-fsk-tx.grc" download>L08-fsk-tx.grc</a>: the FSK transmitter alone, with a deviation slider, showing the bits, the transmitted signal, and its spectrum. No hardware needed.
- <a class="doc-link" href="../../grc/L08-fsk-link.grc" download>L08-fsk-link.grc</a>: a line of text through an FSK transmitter, a Channel Model with noise and frequency offset sliders, and an FSK receiver that displays the received text. No hardware needed.

Open a `.grc` file from GRC's File menu, or run `gnuradio-companion L08-fsk-link.grc` from the radioconda prompt. The link flowgraph's Text Sink is an Embedded Python Block; GRC saves its code into the `.grc` file, so it needs no other download.

This lesson follows:

- <a class="doc-link" href="https://wiki.gnuradio.org/index.php?title=Simulation_example:_FSK" target="_blank" rel="noopener">GNU Radio wiki, Simulation example: FSK</a>
- <a class="doc-link" href="https://pysdr.org/content/digital_modulation.html" target="_blank" rel="noopener">PySDR, Digital Modulation</a>, the FSK section.
::::

::::{frame} Summary
:class: read-only

| Idea | What it is | Number to remember |
| :-- | :-- | :-- |
| FSK | a 1 at $+\Delta f$, a 0 at $-\Delta f$ | course link: $\Delta f$ = 1 kHz |
| Symbol rate | $R_s = f_s/\text{sps}$ | 32 kHz / 32 = 1000 baud |
| Modulation index | $h = 2\Delta f/R_s$ | $h = 2$ |
| Frequency Mod | sensitivity $2\pi\Delta f/f_s$ | 0.196 rad per sample |
| Quadrature Demod | gain $f_s/(2\pi\Delta f)$ | 5.09 |
| Bandwidth | $B \approx 2(\Delta f + R_s)$, sets the filter | 4 kHz |
| Access code | marks the start of each packet | 64 bits, 2 errors allowed |
| Noise | the eye thickens, then FM clicks cross zero | errors start near 1.0 V on the slider |
| Offset tolerance | levels shift by $f_\text{off}/\Delta f$ | about 600 Hz at $\Delta f$ = 1 kHz |
::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE448_L08_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE448_L08_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Looking Ahead
:::{present}
- The L8 Lab builds the transmitter and measures the link's noise and offset limits.
- Lesson 9 sends bits as amplitudes instead of frequencies: PAM.
:::

Today we built an FSK transmitter from a Frequency Mod block, a receiver from a filter, a quadrature demodulator, and a slicer, and a packet format that lets the receiver find each line of text. The L8 Lab is the hands-on version: build the transmitter from an empty canvas, then use the link flowgraph to find the noise level and the frequency offset at which the text stops arriving, and test whether a wider deviation helps.

Lesson 9 changes what carries the bits. Pulse-amplitude modulation (PAM) sends each symbol as a pulse of a chosen height, and Lesson 10 sends ASCII text over it. Its receiver ends the same way as today's, with symbol timing and a slicer.
::::
