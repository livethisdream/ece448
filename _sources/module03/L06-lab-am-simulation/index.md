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
- **Pre-Lab:** list the spectral lines and the message settings for the lab's own message.
- **Bench:** build DSB-AM yourself, then turn the sliders on DSB-SC and SSB.
- **Writeup:** explain what changed and why, in words.
:::

Lesson 6 showed all three flowgraphs running. Today you build the DSB-AM flowgraph from an empty canvas and measure the other two. The lab packet has three parts, and you turn it in once, complete, before Lesson 7. The lab uses its own message, not the Lesson 6 one, so your readings are your own. **Part 1, the Pre-Lab**, is on your own before the period: list the lines of each signal and the message settings you will type in. **Part 2** is your own measurements in class: turn each slider and record what you see and hear. **Part 3, the Writeup**, explains what changed and why.

Every flowgraph in this lab is a simulation, so you need only your laptop. Bring headphones; the receivers play through the Audio Sink, and thirty laptops playing tones at once make the room hard to work in.
::::

::::{frame} Part 1: Before the Period
:::{present}
- List the lines of DSB-AM, DSB-SC, USB, and LSB.
- Fill in the message Signal Source settings.
:::

Do the Pre-Lab before you arrive, so the bench time goes to building and watching. Both items on the slide are the packet's Question 1, worked for the lab's message, which the packet describes: the line list is $f_c$ plus and minus each tone, and the settings table is what you will type into the two message Signal Sources, in your build and in each downloaded flowgraph. Bring questions to EI before the lab rather than to the lab itself.

Part 2 is where you turn the sliders: $m$, the LO phase, and the tuning error. Record what you see on the sinks and hear on the audio.
::::

::::{frame} Part 2: Build DSB-AM
:class: read-only

1. Start GRC and choose File, New, QT GUI. Do not open `L06-dsb-am.grc`; build it yourself.
2. Set `samp_rate` to 48000 and add a Variable `fc` of 10000.
3. Add a **QT GUI Range** with ID `m`, from 0 to 1.5 in steps of 0.05, default 0.5.
4. Make the message: two float **Signal Sources**, cosine, with the settings from your Question 1(c), into an **Add**.
5. Build the transmitter: **Multiply Const** `m`, **Add Const** 1, and a **Multiply** with a third Signal Source at `fc`. Send it to a float **QT GUI Frequency Sink**.
6. Build the receiver: **Abs**, a **Low-pass Filter Taps** variable `lpf_taps` (cutoff 3000, transition 1000) used by a **Decimating FIR Filter**, and **Multiply Const** `numpy.pi/2` with an **Import** block for `import numpy`.
7. Add a **Delay** of `len(lpf_taps)//2` on the output of the Add Const, and a two-input float **QT GUI Time Sink** comparing it with the receiver's output.
8. Finish with a **DC Blocker**, a volume Multiply Const, and an **Audio Sink** at 48 kHz. Do not add a Throttle.
9. Run it with the volume low. Screenshot the canvas and the time sink for Question 2, and record the lower tone's upper sideband line against the carrier at each $m$ in the table.
::::

::::{frame} Part 2: Overmodulation and DSB-SC
:class: read-only

1. With your DSB-AM flowgraph running and the audio on, raise `m` by 0.05 at a time. Record where the detector output first departs from the envelope, and screenshot $m = 1.4$, for Question 3.
2. Close it, then open `L06-dsb-sc.grc`, set its two message Signal Sources with the settings from your Question 1(c), and run it. Confirm the four lines and the empty carrier frequency for Question 4(a).
3. Set the LO phase to each value in the packet's table. Read the coherent receiver's peak off the time sink at each, for Question 4(b).
4. Return the LO phase to 0. Switch Listen To between Coherent and Envelope and describe what you hear for Question 4(c).
::::

::::{frame} Part 2: SSB
:class: read-only

1. Open `L06-ssb.grc`, set its two message Signal Sources with the settings from your Question 1(c), and run it. Read the kept and suppressed lines for USB and for LSB off the frequency sink for Question 5(a).
2. Select LSB and set the tuning error to the value in Question 5(b). Screenshot the time sink and describe the audio for Question 5(b).
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
- Describe what $m$ does to the sideband lines and the carrier.
- Explain why an envelope detector recovers DSB-AM but not DSB-SC.
- Explain why operators tune SSB by ear while DSB-SC needs carrier recovery.
:::

The Writeup is three questions. The first explains your $m$ table: which lines moved and which did not. The second connects the overmodulation and DSB-SC envelope screenshots: in both, the detector sees the absolute value of something that goes negative. The third compares your LO phase table with your tuning-error measurement, which is the reason the two receivers are built differently on the air.
::::

::::{frame} Lab Packet
:class: read-only doc-links

- <a class="doc-link" href="../../labs/ECE448_Lab_L06_AMSimulation_blank.pdf" target="_blank" rel="noopener">L6 Lab packet (PDF)</a>
- <a class="doc-link" href="../../grc/L06-dsb-am.grc" download>L06-dsb-am.grc</a>, <a class="doc-link" href="../../grc/L06-dsb-sc.grc" download>L06-dsb-sc.grc</a>, and <a class="doc-link" href="../../grc/L06-ssb.grc" download>L06-ssb.grc</a>
::::

::::{frame} Looking Ahead
:::{present}
- Lesson 7 replaces the simulated transmitter with a PlutoSDR.
- The envelope detector becomes one block: Complex to Mag.
:::

Keep your DSB-AM flowgraph. Lesson 7 receives real AM with a PlutoSDR, and its receiver keeps your low-pass filter and DC Blocker but replaces the Abs block with Complex to Mag, because the SDR delivers the signal as complex samples with its carrier already at 0 Hz.
::::
