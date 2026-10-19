---
frame_view: true
---

# L8 Lab — FSK

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">FSK</h1>

<div class="title-rule"></div>

Build an FSK transmitter from an empty canvas, then find the noise level and frequency offset at which a line of text stops arriving.

L8 Lab · Module 4: Digital Modulation · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '4'">
  <li>I can describe FSK modulation and implement an FSK transmitter and receiver in GNU Radio.</li>
</ol>
::::

::::{frame} From Lesson to Bench
:::{present}
- **Pre-Lab:** run the link flowgraph and predict every setting and limit.
- **Bench:** build the transmitter yourself, then sweep the noise and the offset.
- **Writeup:** explain the limits and choose a deviation.
:::

Lesson 8 showed an FSK link carrying a line of text through noise. Today you build the transmitter from an empty canvas and measure where the link breaks. The lab packet has three parts, and you turn it in once, complete, before Lesson 9. **Part 1, the Pre-Lab**, is on your own before the period: run `L08-fsk-link.grc` once and predict the block settings, the SNR at each noise level, and the demodulator levels at each offset. **Part 2** is your own measurements in class. **Part 3, the Writeup**, explains them.

This lab needs no SDR, and nothing in it transmits. The Channel Model block stands in for the air.
::::

::::{frame} Part 1: Before the Period
:::{present}
- `L08-fsk-link.grc` runs and shows the received line.
- Predict $k$, $g$, $h$, $B$, and the filter cutoff for $\Delta f$ = 1 and 2 kHz.
- Predict the SNR for six noise voltages.
:::

Do the Pre-Lab before you arrive. Question 1 is a check that both flowgraphs open and run on your laptop: if GRC reports an error, the L5 lesson page lists the install checks, and EI before the lab is the place to fix it.

Question 2 asks for predictions from the lesson's formulas: the transmitter's sensitivity and the receiver's gain, modulation index, Carson bandwidth, and filter cutoff for two deviations; the SNR at the demodulator for noise voltages from 0.5 to 2.0; the length and duration of one packet; and the demodulator's two levels at each frequency offset. Part 2 checks each one against a measurement.
::::

::::{frame} Expected Numbers
:::{present}
| Check | Expected |
| :-- | :-- |
| Peaks at $\Delta f$ = 1 kHz | $\pm 1$ kHz |
| SNR at $\sigma$ = 1.0 | 9 dB |
| One packet | 424 bits, 0.424 s |
| Levels at 600 Hz offset | $+1.6$ and $-0.4$ |
:::

These follow from Lesson 8. The block settings and the spectral peaks are exact, because the flowgraph computes them. The SNR comes from the 4 kHz receive bandwidth: noise of voltage $\sigma$ spread over 32 kHz leaves $\sigma^2/8$ in the filter, so the SNR is $8/\sigma^2$. The count of correct lines at each noise voltage is random and changes from run to run, which is why the packet records it over 30 s rather than predicting it.
::::

::::{frame} Part 2: Build the Transmitter
:class: read-only

1. Start GRC and choose File, New, QT GUI. Do not open `L08-fsk-tx.grc`; build it yourself.
2. Set `samp_rate` to 32000. Add a Variable `sps` of 32, a Variable `msg` holding your line of text in quotes, and an **Import** block with `import math`.
3. Add a **QT GUI Range** with ID `dev`, from 250 to 4000 in steps of 250, default 1000.
4. Add a **Vector Source**: type byte, vector `list(msg.encode()) + [10]`, repeat Yes.
5. Add **Unpack K Bits** with K = 8, then **Chunks to Symbols**: input byte, output float, symbol table `[-1, 1]`.
6. Add **Repeat**: type float, interpolation `sps`. Then add **Frequency Mod** with sensitivity `2*math.pi*dev/samp_rate`.
7. Add a **Throttle** (complex, `samp_rate`) and a **QT GUI Frequency Sink** (complex, bandwidth `samp_rate`), and connect the chain. Every arrow must be black.
8. Run it. Screenshot the canvas for Question 3(a), then record the two peaks at a deviation of 1000 and 2000 Hz for Question 3(b).
::::

::::{frame} Part 2: Noise and Offset
:class: read-only

<img src="../../viz/img/L08-grc-link.png"
     alt="The whole L8 link flowgraph in GNU Radio Companion: the transmitter row from Vector Source to Frequency Mod, then Throttle, Channel Model, and the receiver from Low Pass Filter to Text Sink, with the noise and offset sliders and the two labels at the top"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto 12px;">

1. Open and run `L08-fsk-link.grc`. The Lines label counts the lines received since a slider last moved.
2. With the offset at 0, set the noise voltage to 0.5, 0.8, 1.0, 1.2, 1.5, and 2.0 in turn. At each, wait about 30 s and record the time, the lines received, and the lines correct for Question 4(a).
3. At 0.5 and at 1.2, screenshot the eye diagram for Question 4(b).
4. Set the noise back to 0.5. Set the offset to 0, 300, 600, 800, and 1000 Hz in turn. At each, wait about 20 s and record the eye's two levels and the Lines label for Question 5(a).
5. Stop the flowgraph and change the `dev` variable from 1000 to 2000. The transmitter's sensitivity, the receiver's filter, and the demodulator's gain all follow it. Run the two settings of Question 5(b) and record the Lines label for each.
::::

::::{frame} If No Text Arrives
:class: read-only

:::{admonition} If the Received label stays at "(waiting for a packet)"
:class: tip
Close the flowgraph and run it again with the sliders at their defaults, a noise voltage of 0.5 and an offset of 0, where every line should arrive within a second. If it still shows no text, compare `samp_rate`, `sps`, and `dev` with the lesson's values: the transmitter and the receiver share these variables, and a change to `sps` alone breaks the receiver's timing. If you changed the message, keep it on one line, because the newline at its end marks the end of each line of text.
:::
::::

::::{frame} Part 3: After the Lab
:::{present}
- Explain why the link goes from no errors to no packets within about 6 dB.
- Convert the offset limit to ppm at 915 MHz and judge it.
- Choose 1 or 2 kHz of deviation, and justify it.
:::

The Writeup is three questions. The first connects your noise table to Lesson 2's link margin: the change from clean text to no text happens within a few dB, so a link designed right at its threshold fails on the first fade. The second turns your offset limit into parts per million, the unit in which manufacturers specify crystal oscillators, and asks whether this link would work between two real radios. The third asks you to choose a deviation from your own measurements and to say what the choice gives up.
::::

::::{frame} Lab Packet
:class: read-only doc-links

- <a class="doc-link" href="../../labs/ECE448_Lab_L08_FSK_blank.pdf" target="_blank" rel="noopener">L8 Lab packet (PDF)</a>
- <a class="doc-link" href="../../grc/L08-fsk-tx.grc" download>L08-fsk-tx.grc</a> and <a class="doc-link" href="../../grc/L08-fsk-link.grc" download>L08-fsk-link.grc</a>
::::

::::{frame} Looking Ahead
:::{present}
- Lesson 9 sends bits as pulse amplitudes: PAM.
- Lesson 10 sends ASCII over PAM, in packets like today's.
:::

Keep your transmitter flowgraph and your tables. Lesson 9 sends each bit as the height of a pulse instead of a frequency, and Lesson 10 sends ASCII text over PAM. That link needs the same kind of packet as today's, an access code followed by a length, so the receiver can find where each line starts.
::::
