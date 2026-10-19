---
frame_view: true
---

# L6 Lab — AM Simulation

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">AM Simulation</h1>

<div class="title-rule"></div>

Build an AM modulator and demodulator and check the audio against the source.

L6 Lab · Module 3: Analog Modulation · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '3'">
  <li>I can describe DSB-AM, DSB-SC, and SSB and identify each on a spectrum.</li>
  <li>I can implement an AM modulator and demodulator in GNU Radio and verify demodulated audio against the source.</li>
</ol>
::::

::::{frame} From Lesson to Bench
:::{present}
- **Pre-Lab:** predict every spectral line and receiver effect.
- **Bench:** build DSB-AM yourself, then measure DSB-SC and SSB.
- **Writeup:** compare, and explain the differences.
:::

Lesson 6 showed all three flowgraphs running. Today you build the DSB-AM flowgraph from an empty canvas and measure the other two. The lab packet has three parts, and you turn it in once, complete, before Lesson 7. **Part 1, the Pre-Lab**, is on your own before the period: predict the DSB-AM sideband levels, the lines of each signal, the overmodulation point, and the effect of LO phase and tuning errors. **Part 2** is your own measurements in class. **Part 3, the Writeup**, compares the two.

Every flowgraph in this lab is a simulation, so you need only your laptop. Bring headphones; the receivers play through the Audio Sink, and thirty laptops playing tones at once make the room hard to work in.
::::

::::{frame} Part 1: Before the Period
:::{present}
- Predict each DSB-AM line's frequency and level at $m = 0.5$.
- List the DSB-SC, USB, and LSB lines, and find where this message overmodulates.
- Predict the coherent output against LO phase, and the mistuned USB tones.
:::

Do the Pre-Lab before you arrive; the bench time assumes you already know what each measurement should show. The three items on the slide are the packet's Question 1, worked from the Lesson 6 page and its practice set. The overmodulation point needs care: the rule $m \le 1$ is safe for any message, but this message never reaches $-1$, so it overmodulates only at a slightly larger $m$. Bring questions to EI before the lab rather than to the lab itself.

Part 2 checks each prediction against a measurement, and the Writeup asks you to explain any that disagree.
::::

::::{frame} Expected Numbers
:::{present}
| Check | Expected |
| :-- | :-- |
| DSB-AM sidebands, $m = 0.5$ | $-16.5$ and $-20$ dB |
| Overmodulation starts | $m \approx 1.1$ |
| DSB-SC output at $60°$ | half |
| USB, 200 Hz high | 800 and 2300 Hz |
:::

These are the predictions of Question 1, worked from Lesson 6. Every one is exact, because a simulated signal has no noise and no hardware in the way. If a measurement disagrees by more than about 1 dB, the flowgraph is built differently from the instructions, most often with a different `m`, a different tone amplitude, or a frequency sink reading taken between FFT bins. The SSB suppression and the tuning error you can hear depend on the Hilbert filter and on your ears, so the packet records them rather than predicting them.
::::

::::{frame} Part 2: Build DSB-AM
:class: read-only

1. Start GRC and choose File, New, QT GUI. Do not open `L06-dsb-am.grc`; build it yourself.
2. Set `samp_rate` to 48000 and add a Variable `fc` of 10000.
3. Add a **QT GUI Range** with ID `m`, from 0 to 1.5 in steps of 0.05, default 0.5.
4. Make the message: two float **Signal Sources**, cosine, 1000 Hz at amplitude 0.6 and 2500 Hz at 0.4, into an **Add**.
5. Build the transmitter: **Multiply Const** `m`, **Add Const** 1, and a **Multiply** with a third Signal Source at `fc`. Send it to a float **QT GUI Frequency Sink**.
6. Build the receiver: **Abs**, a **Low-pass Filter Taps** variable `lpf_taps` (cutoff 3000, transition 1000) used by a **Decimating FIR Filter**, and **Multiply Const** `numpy.pi/2` with an **Import** block for `import numpy`.
7. Add a **Delay** of `len(lpf_taps)//2` on the output of the Add Const, and a two-input float **QT GUI Time Sink** comparing it with the receiver's output.
8. Finish with a **DC Blocker**, a volume Multiply Const, and an **Audio Sink** at 48 kHz. Do not add a Throttle.
9. Run it with the volume low. Screenshot the canvas and the time sink for Question 2, and record the line levels.
::::

::::{frame} Part 2: Overmodulation and DSB-SC
:class: read-only

1. With your DSB-AM flowgraph running and the audio on, raise `m` by 0.05 at a time. Record where the detector output first departs from the envelope, and screenshot $m = 1.4$, for Question 3.
2. Close it, then open and run `L06-dsb-sc.grc`. Confirm the four lines and the empty 10 kHz for Question 4(a).
3. Set the LO phase to 0, 45, 60, and 90 degrees. Read the coherent receiver's peak off the time sink at each, for Question 4(b).
4. Return the LO phase to 0. Switch Listen To between Coherent and Envelope and describe what you hear for Question 4(c).
::::

::::{frame} Part 2: SSB
:class: read-only

1. Open and run `L06-ssb.grc`. Read the kept and suppressed lines for USB and for LSB off the frequency sink for Question 5(a).
2. Select USB and set the tuning error to $+200$ Hz. Screenshot the time sink and describe the audio for Question 5(b).
3. Starting from 0, move the tuning error in steps of 10 Hz in each direction until the tones no longer sound like the original. Record the largest error for Question 5(c).
::::

::::{frame} No Audio?
:class: read-only

:::{admonition} If the flowgraph stops with an audio error
:class: tip
An Audio Sink that cannot open your sound card stops the flowgraph with an error such as `audio_alsa_sink` or `audio_portaudio_sink`. Plug in your headphones and run it again, or set the Audio Sink's Device Name to the device your operating system lists. As a last resort, disable the Audio Sink and add a Throttle at `samp_rate` before the time sinks: every measurement in the packet still works, and only the listening steps need a classmate's laptop. Say in the packet which you did.
:::
::::

::::{frame} Part 3: After the Lab
:::{present}
- Explain any line level more than 1 dB from its prediction.
- Explain why an envelope detector recovers DSB-AM but not DSB-SC.
- Explain why operators tune SSB by ear while DSB-SC needs carrier recovery.
:::

The Writeup is three questions. The first checks your DSB-AM measurements against the sideband amplitudes of Lesson 6. The second connects the overmodulation and DSB-SC envelope screenshots: in both, the detector sees the absolute value of something that goes negative. The third compares your LO phase table with your tuning-error measurement, which is the reason the two receivers are built differently on the air.
::::

::::{frame} Lab Packet
:class: read-only doc-links

- <a class="doc-link" href="../../labs/ECE448_Lab_L06_AMSimulation_blank.pdf" target="_blank" rel="noopener">L6 Lab packet (PDF)</a>
- <a class="doc-link" href="../../grc/L06-dsb-am.grc" download>L06-dsb-am.grc</a>, <a class="doc-link" href="../../grc/L06-dsb-sc.grc" download>L06-dsb-sc.grc</a>, and <a class="doc-link" href="../../grc/L06-ssb.grc" download>L06-ssb.grc</a>
::::

::::{frame} Looking Ahead
:::{present}
- Lesson 7 replaces the simulated transmitter with an RTL-SDR.
- The envelope detector becomes one block: Complex to Mag.
:::

Keep your DSB-AM flowgraph. Lesson 7 receives real AM with an RTL-SDR, and its receiver keeps your low-pass filter and DC Blocker but replaces the Abs block with Complex to Mag, because the SDR delivers the signal as complex samples with its carrier already at 0 Hz.
::::
