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

Lessons 6 and 7 put an analog message on a carrier. From here on the message is data. **Frequency-shift keying** (FSK) is the simplest way to send it: the transmitter shifts its frequency up by the **deviation** $\Delta f$ for each 1 and down by $\Delta f$ for each 0. The receiver only has to decide, once per bit, which of the two frequencies it heard.

The figure is the first flowgraph of this lesson, running. On the left, the blue trace is the message's bits, and the red and green traces are the real and imaginary parts, $I$ and $Q$, of the transmitted complex signal. $I$ is the same 1 kHz cosine during every bit: at $h = 2$ each bit turns the phase through exactly one full circle, forward for a 1 and backward for a 0, and a cosine cannot tell the two directions apart. $Q$ can. It is a sine that changes sign with the direction of rotation, so it flips relative to $I$ at each change of bit. The spectrum on the right shows the same difference as two tones, at $-1$ and $+1$ kHz, as Lesson 5's complex tone did.
::::

::::{frame} Where FSK Is Used
:::{present}
- Pagers, weather balloons, and amateur APRS
- Key fobs and garage-door remotes at 315 and 433.92 MHz
- Bluetooth and many drone links, as Gaussian FSK (GFSK)
:::

FSK is old, and it is everywhere, because the receiver is simple and the transmitter has a constant envelope: the amplitude never changes, so the power amplifier can run at full output without distorting the signal. POCSAG pagers, the radiosondes on weather balloons, and APRS, which sends audio FSK tones over an FM radio, all use it. So do most key fobs and garage-door remotes, which operate at 315 and 433.92 MHz under FCC Part 15, and which Lesson 17 reverse engineers.

Bluetooth, many drone control links, and many 915 MHz sensor networks use **Gaussian FSK** (GFSK), which smooths each frequency step with a Gaussian filter so the signal takes less bandwidth. The flowgraphs below use plain FSK, but a GFSK receiver uses the same blocks.
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

The transmitter is five blocks. A **Vector Source** repeats the bytes of a text message, with a newline at the end. **Unpack K Bits** splits each byte into 8 bits, most significant first, and **Chunks to Symbols** maps each bit to a number: 0 to $-1$ and 1 to $+1$. **Repeat** holds each symbol for `sps` samples, the **samples per symbol**, so the stream now runs at `samp_rate`. Finally, **Frequency Mod** sets the frequency of its output in proportion to its input, so $+1$ becomes a tone at $+\Delta f$ and $-1$ a tone at $-\Delta f$.

Frequency Mod is the same block an FM transmitter uses. The only difference between FM and FSK is the message: audio in FM, a square wave of bits in FSK. The block also keeps the phase continuous from one bit to the next, which keeps the spectrum compact; we call this form **continuous-phase FSK**.
::::

::::{frame} Three Numbers Set the Signal
:::{present}
- **Symbol rate** $R_s = f_s/\text{sps}$: 32 kHz / 32 = 1000 baud.
- **Deviation** $\Delta f$: 1 kHz.
- **Modulation index** $h = 2\Delta f / R_s = 2$.
:::

Three numbers describe an FSK signal. The **symbol rate** is how many symbols the transmitter sends per second, in baud. With one bit per symbol it is also the bit rate, and in a flowgraph the sample rate and the samples per symbol set it:

$$R_s = \frac{f_s}{\text{sps}}$$

The **deviation** is how far each tone sits from the center. Frequency Mod takes it as a **sensitivity**, the phase change per sample for an input of 1:

$$k = \frac{2\pi \Delta f}{f_s}$$

which is $2\pi \times 1000 / 32000 = 0.196$ rad per sample here. The **modulation index** compares the tone spacing $2\Delta f$ with the symbol rate. At $h = 2$ the tones are two symbol rates apart, and their spectral peaks are clearly separate.
::::

::::{frame} Bandwidth
:::{present}
<img src="../../viz/img/L08-tx-3k.png"
     alt="The transmitter with the deviation slider at 3000 Hz: I and Q oscillate at 3 kHz and the spectrum shows the two peaks at minus 3 and plus 3 kHz"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Carson's rule, taking the message bandwidth as $R_s$: $B \approx 2(\Delta f + R_s)$.
- 1 kHz deviation at 1000 baud takes about 4 kHz.
:::

Dragging the deviation slider to 3 kHz moves the two peaks to $\pm 3$ kHz. The signal's bandwidth grows with the deviation, and it also grows with the symbol rate, because faster switching between the tones spreads each one. **Carson's rule**, the standard bandwidth estimate for FM, accounts for both, taking the message bandwidth as the symbol rate, a conservative choice:

$$B \approx 2(\Delta f + R_s)$$

At 1 kHz and 1000 baud that is 4 kHz, and at 3 kHz it is 8 kHz. Other references take the message bandwidth as half the symbol rate and write $2\Delta f + R_s$, which gives 3 kHz here; the larger estimate leaves the receiver filter some room. The rule sets the receiver's first filter, which should pass this band and reject everything else. Wider deviation makes the tones easier to tell apart, but every extra hertz of bandwidth also lets in more noise, so the choice of deviation balances the two.
::::

::::{frame} FSK Explorer
:class: viz-frame

:::{depth}
The left panel is the spectrum of the received signal, with the Carson bandwidth shaded and the two tone frequencies dashed. The right panel is the receiver's output for 16 bits, with the transmitted levels in gray and a dot where the receiver decides each bit; a red dot is a wrong decision. Start at the defaults and raise the deviation: the tones move apart and the shaded band widens. Then set the deviation back to 1000 Hz and raise the noise voltage until red dots appear, near an SNR of 9 dB in the Carson bandwidth. Try a symbol rate of 2000: the signal widens, so the same noise gives a lower SNR and more errors.
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

::::{frame} Part 2: The Receiver
:::{present}
<img src="../../viz/img/L08-grc-rx.png"
     alt="The receiver half of the L8 link flowgraph in GNU Radio Companion: a Throttle and a Channel Model feed a Low Pass Filter, Quadrature Demod, Moving Average, Symbol Sync, and Binary Slicer, then Correlate Access Code - Tag Stream, Repack Bits, and a Text Sink; a QT GUI Frequency Sink and a QT GUI Eye Sink display the signal"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Filter to the signal, turn frequency into a number, and decide each bit.
- The **Channel Model** adds the noise and the frequency offset.
:::

The second flowgraph, `L08-fsk-link.grc`, puts the transmitter, a channel, and a receiver in one file. The **Channel Model** block stands in for the air: it adds complex Gaussian noise of a chosen voltage and shifts the signal by a chosen frequency offset, both on sliders. The receiver then works in three steps. A **Low Pass Filter** with a cutoff of $\Delta f + R_s = 2$ kHz keeps the Carson bandwidth and removes the noise outside it. A **Quadrature Demod** turns the frequency of each sample into a number. The last three blocks find each bit's sampling instant and decide whether it is a 0 or a 1.
::::

::::{frame} The Quadrature Demodulator
:::{present}
- It measures the phase step from one sample to the next.
- A phase step is a frequency: $\pm\Delta f$ gives $\pm 1$ with gain $f_s/(2\pi\Delta f)$.
:::

The **Quadrature Demod** block is the FM demodulator from Lesson 7, set here for FSK. A tone at frequency $f$ advances its phase by $2\pi f / f_s$ every sample, so the block multiplies each sample by the conjugate of the one before it and takes the angle of the result, which is that phase step. It then multiplies by its gain. Setting the gain to

$$g = \frac{f_s}{2\pi \Delta f}$$

which is $32000 / (2\pi \times 1000) = 5.09$ here, makes the tone at $+\Delta f$ come out as $+1$ and the tone at $-\Delta f$ as $-1$. This gain is the reciprocal of the transmitter's sensitivity, so the demodulator undoes the modulator. The output is the transmitted square wave, with noise on it and with its edges rounded by the low-pass filter.
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

A **Moving Average** over `sps` samples averages each bit's demodulator output, which reduces the noise on it. **Symbol Sync** then finds the instant where the moving average's output peaks, at the end of each bit, and outputs one sample there; it adjusts its own timing continuously, because the receiver's clock never quite matches the transmitter's. The **Binary Slicer** decides: a sample above 0 is a 1 and below 0 is a 0.

The **eye diagram** on the right overlays many two-bit stretches of the moving average's output. Where the traces cross are the bit edges, and the wide gap between $+1$ and $-1$ between the crossings is the **eye opening**. A wide-open eye means every decision is easy. With the noise voltage at 0.5, all 21 lines in the first 10 s arrive intact.
::::

::::{frame} Part 3: Packets
:::{present}
- The transmitter adds a 64-bit **access code** and a length header to each line.
- The receiver searches for the access code to find where each line starts.
:::

The slicer outputs a stream of bits, but nothing in that stream says where one byte ends and the next begins. The transmitter solves this by sending each line of text as a **packet**. A **Protocol Formatter** builds a header for each line: a 64-bit **access code**, a fixed pattern the receiver knows in advance, then the line's length. A **Tagged Stream Mux** puts the header in front of the line.

At the receiver, **Correlate Access Code - Tag Stream** compares the incoming bits with the access code and, when at most 2 bits differ, reads the 32-bit header, which holds the line's length in bytes twice, and passes that many bytes on as bits. **Repack Bits** packs them back into bytes, and a small Python block, the **Text Sink**, shows the latest line and counts how many matched the message since a slider last moved. Lesson 10 needs the same framing to send ASCII over PAM.
::::

::::{frame} Noise
:::{present}
<img src="../../viz/img/L08-link-noisy.png"
     alt="The L8 link at noise voltage 1.3: the noise floor is about 8 dB higher, the eye diagram is still mostly open, with a few traces spiking across zero, and the labels show a line with two wrong characters and 7 correct of 29 received in 13 s"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- At 0.5 V: SNR 15 dB in 4 kHz, and every line arrives.
- At 1.3 V: 6.7 dB, and most lines have an error.
:::

The Channel Model's signal has power 1, and noise of voltage $\sigma$ has power $\sigma^2$ spread over the whole 32 kHz. The receiver's filter keeps only 4 kHz of it, an eighth, so the SNR at the demodulator is

$$\text{SNR} = \frac{1}{\sigma^2 \times 4/32} = \frac{8}{\sigma^2}$$

At 0.5 V that is 32, or 15 dB, and every line arrives. At 1.0 V it is 9 dB and an occasional character goes wrong. At 1.3 V it is 6.7 dB. The eye is still mostly open, but now and then the noise swings the phase far enough to make a spike, an FM click, in the demodulator output, and a spike that crosses zero at a sampling instant is a bit error. Only 7 of 29 lines arrive without an error. By 2 V the receiver almost never finds the access code. The change from no errors to no packets happens within about 6 dB, which is typical of an FM-type demodulator, and it is why Lesson 2's link margin matters: a link designed right at 9 dB fails on the first fade.
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

No two radios agree exactly on frequency. Each derives its carrier from a crystal oscillator with an error of a few parts per million, and at 915 MHz an error of 2 ppm is 1.8 kHz. The Channel Model's offset slider imitates this. A 600 Hz offset moves both tones up by 600 Hz, and the demodulator output moves up by $600/1000 = 0.6$: the levels sit at $+1.6$ and $-0.4$. The slicer still decides correctly, because both levels are on the correct side of zero.

Once the offset approaches the deviation, the lower level approaches zero, and the low-pass filter begins to cut off the upper tone. At 800 Hz the lines still arrive but every one has errors, and at 1000 Hz none arrive. Real FSK receivers handle offset in one of two ways: they use a deviation large compared with the expected offset, as most key fobs do, or they measure the offset and remove it before the demodulator. The L8 Lab measures both effects.
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

On a real SDR an FSK signal is easy to recognize on the waterfall: two tracks side by side, with the signal jumping between them. The figure is a simulation of a 433.92 MHz remote, the kind Lesson 17 decodes. The tracks are 40 kHz apart, so $\Delta f = 20$ kHz, and the shortest stay on one track, in the alternating preamble, is 1 ms, so the symbol rate is 1000 baud. A live waterfall row often lasts longer than one bit, so in practice we measure the dwell on a spectrogram in URH or on the Quadrature Demod output. Those two numbers are all we need to set the receiver's filter, gain, and samples per symbol.

The link of this lesson runs over the air by replacing the Throttle and Channel Model with a PlutoSDR or HackRF sink on one side and a source on the other, with a resampler to raise the 32 kHz stream to a rate the radio supports. In class we transmit only into a cable, into a shielded enclosure, or at very low power in an ISM band, and only when the lesson says to. Nothing in this lesson or its lab transmits.
::::

::::{frame} Key Point
:::{present}
:class: callout
FSK sends each bit as one of two tones. The transmitter is a Frequency Mod block; the receiver filters to $2(\Delta f + R_s)$, demodulates frequency into $\pm 1$, samples each bit at its peak, and slices at zero.
:::
::::

::::{frame} Downloads
:class: read-only doc-links

- <a class="doc-link" href="../../grc/L08-fsk-tx.grc" download>L08-fsk-tx.grc</a>: the FSK transmitter alone, with a deviation slider, showing the bits, the transmitted signal, and its spectrum. No hardware needed.
- <a class="doc-link" href="../../grc/L08-fsk-link.grc" download>L08-fsk-link.grc</a>: a line of text through an FSK transmitter, a Channel Model with noise and frequency offset sliders, and an FSK receiver that displays the received text. No hardware needed.

Open a `.grc` file from GRC's File menu, or run `gnuradio-companion L08-fsk-link.grc` from the radioconda prompt. The link flowgraph's Text Sink is an Embedded Python Block; GRC saves its code into the `.grc` file, so it needs no other download.
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
| Carson's rule | $B \approx 2(\Delta f + R_s)$ | 4 kHz |
| Access code | marks the start of each packet | 64 bits, 2 errors allowed |
| Noise threshold | SNR in the Carson bandwidth | errors start near 9 dB |
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
