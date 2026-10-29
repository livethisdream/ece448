---
frame_view: true
---

# L17 Lab — RF Reverse Engineering

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">RF Reverse Engineering</h1>

<div class="title-rule"></div>

Reverse-engineer an unknown signal from capture to payload.

L17 Lab · Module 6: Waveform Applications & RF Reverse Engineering · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '6'; counter-reset: lo 5">
  <li>I can perform RF reverse engineering on an unknown signal: identify its modulation, symbol rate, and payload structure.</li>
</ol>
::::

::::{frame} From Lesson to Bench
:::{present}
- **Pre-Lab:** read the recording's meta file, set up URH, and work out chip settings.
- **Bench:** take an unknown remote from carrier to fields, build its encoder, then send it through a cable.
- **Writeup:** explain the evidence for each step.
:::

Lesson 17 took the Simulated fan remote through five steps: find the carrier, identify the modulation, identify the encoding, build an encoder, and transmit. Today you take a different device through the same steps. It is a **Simulated remote outlet switch** with six buttons, and nobody will describe it to you: its recording is all you get. The lab packet has three parts, and you turn it in once, complete, before Lesson 18. **Part 1, the Pre-Lab**, is on your own before the period. **Part 2** is what you find, build, and observe in class. **Part 3, the Writeup**, explains it.

Questions 1 to 7 run on your laptop and transmit nothing. Question 8 transmits, into a cable only, as the PlutoSDR frame below describes.
::::

::::{frame} The Recording
:class: read-only doc-links

- <a class="doc-link" href="../../grc/L17-lab-unknown.sigmf-data" download>L17-lab-unknown.sigmf-data</a> and <a class="doc-link" href="../../grc/L17-lab-unknown.sigmf-meta" download>L17-lab-unknown.sigmf-meta</a>: the unknown device, labeled Simulated in its meta file, one press of each of its six buttons. Keep the two files in the same folder.

The recording is a SigMF pair, like the lesson's, but its sample rate and center frequency are its own: read them from the meta file before you open it anywhere. The meta file's description lists the buttons in the order they were pressed, which tells you which burst is which. It does not describe the signal.
::::

::::{frame} Part 1: Before the Period
:::{present}
- Read the meta file and set up `L17-sigmf-view.grc` for this recording.
- Install URH and open the lesson's recording in it.
- Work out samples per chip for a few chip lengths.
:::

Do the Pre-Lab before you arrive. Question 1 asks for the datatype, sample rate, and center frequency from `L17-lab-unknown.sigmf-meta`, and for the values of `rec`, `samp_rate`, and `fc` you set in `L17-sigmf-view.grc` so that it opens this recording. Run it once to check that the spectrum's axis is centered on the recording's center frequency.

Question 2 checks your URH install on the lesson's recording, `L17-fan-remote.sigmf-data`, whose answers the lesson page gives, so you can tell whether URH is working before you meet the unknown. URH's README gives an installer for Windows and `pipx install urh` for Linux and macOS. Question 3 is the arithmetic URH and your encoder need: samples per chip for several chip lengths at this recording's sample rate and at the PlutoSDR flowgraph's 1 MS/s.
::::

::::{frame} Part 2: Find the Carrier
:class: read-only

1. Run `L17-sigmf-view.grc` with your settings from Question 1. Watch the waterfall through at least two loops of the recording.
2. Find every signal on the waterfall. For each, decide whether it bursts when a button is pressed or stays on, and record its frequency for Question 4(a).
3. Move the Carrier offset slider until the envelope plot shows clean pulses, then move it in steps of 1 kHz each way and record the offset where the pulses are tallest. Screenshot the window for Question 4(b).
4. Record the carrier frequency, the center frequency plus your offset, for Question 4(c).
::::

::::{frame} Part 2: Modulation and Encoding in URH
:class: read-only

1. In URH, choose File, New Project, then open `L17-lab-unknown.sigmf-data` with the file filter set to All Files. Set the signal's sample rate to the one in the meta file.
2. Record the Modulation and Samples/Symbol that autodetect chooses, for Question 5(a).
3. Zoom in on one burst. Select the shortest pulse you can find; URH shows the selection's length in samples below the signal. Do the same for the shortest gap. Record both for Question 5(b). If they disagree with autodetect's Samples/Symbol, set Samples/Symbol to your measurement and record what changes in the lines of chips.
4. Compare the chips of several bursts. Decide which chips every burst shares and how the rest group into bits, and record your evidence for Question 5(c).
5. Decode one burst of each button into bits, by hand or with URH's Analysis tab, and fill in Question 6's table. Then compare the buttons and mark which bits never change, which change with the button, and what the rest do.
6. Count the bursts in one press, and measure the pause between bursts, for Question 6(c).
::::

::::{frame} If the Chips Look Wrong
:class: read-only

:::{admonition} If the lines of chips change from burst to burst, or the groups never repeat
:class: tip
Autodetect is a starting point, not an answer. Check the sample rate first: URH does not read the meta file, and a wrong sample rate makes every time in microseconds wrong. Then measure the shortest pulse yourself and set Samples/Symbol to it. If some lines are a chip or two shorter than others, look at what the last bits of each line are: URH counts off chips at the end of a burst as part of the pause. If the Center is so high that short pulses disappear, lower it, or press Autodetect parameters again after you set Samples/Symbol.
:::
::::

::::{frame} Part 2: Build the Encoder
:class: read-only

1. Start GRC and choose File, New, QT GUI. Do not open `L17-fan-tx-sim.grc`; build the encoder yourself from standard blocks, with the settings you found. You may look at the lesson page's Step 4 figure.
2. Set `samp_rate` to the recording's sample rate and `chip_len` to your samples per chip. Add a Variable `bits` that holds one button's bits as a list of 0s and 1s.
3. Build the envelope: a **Vector Source** of `bits`, a **Map** and **Unpack K Bits** that turn each bit into your chip pattern, **Char To Float**, and a **Repeat** of `chip_len`.
4. Add anything your measurements show around the bits, with a second Vector Source of chips and a Repeat where you need one, and the pause after each burst, with a **Constant Source** of 0. Join them with a **Stream Mux** whose lengths, in samples, match your measurements.
5. Put the envelope on a carrier at your offset with **Float To Complex**, a **Signal Source**, and a **Multiply**. Add a **Noise Source** of amplitude 0.05 and an **Add**, then a **Throttle**, a **QT GUI Time Sink** of the envelope from **Complex to Mag**, and a **SigMF Sink (Minimal)** with file name `my-unknown`, the recording's sample rate, and its center frequency. Every arrow must be black.
6. Run it for about 5 s and close it. Open `my-unknown.sigmf-data` in URH beside the original recording, with the same sample rate and Samples/Symbol, and compare the lines of chips for Question 7(a).
7. Change `bits` to a second button and repeat for Question 7(b). Then run it again and raise the noise amplitude in steps of 0.1 until URH's lines of chips no longer match; record where for Question 7(c).
::::

::::{frame} Part 2: Transmit into a Cable
:::{present}
- You send your encoder from one PlutoSDR through a 30 dB attenuator into a second SDR.
- Connect the cable before the flowgraph runs, and never connect an antenna.
:::

Save a copy of your encoder for the radio. Delete the Noise Source, the Add, and the Throttle, set `samp_rate` to 1000000 and `chip_len` to your Question 3 value at 1 MS/s, and add a **PlutoSDR Sink** after a Multiply Const of 0.5, tuned to the recording's center frequency. Copy the `tx_atten` QT GUI Range from `L17-fan-tx-pluto.grc` unchanged, from 30 to 89 dB with a default of 60, and set it as the sink's attenuation. Put "Transmit only into the cable" in the flowgraph's description. The second SDR, a PlutoSDR or an RTL-SDR, runs `L17-capture.grc` with its center frequency set to the recording's and records what arrives.

In class we transmit only into a cable, into a shielded enclosure, or at very low power in an ISM band, and only when the lesson says to. This question transmits only into the cable between the first Pluto's TX port and the second SDR's input, through an inline 30 dB SMA attenuator. Never set TX attenuation below 30 dB or change the slider's range; an SDR's input is rated to only a few dBm. We have compiled the Pluto flowgraphs but not run them on a radio, so your bench is their first run on hardware.
::::

::::{frame} PlutoSDR Steps
:class: read-only

1. With both radios unplugged, connect the first Pluto's TX port to the second SDR's RX input with a short SMA cable and an inline 30 dB SMA attenuator. Do not connect an antenna, and do not connect the cable without the attenuator.
2. Plug in both radios. Run `iio_info -s` at the radioconda prompt; it should list each PlutoSDR. If you use two Plutos, give each flowgraph its own Pluto's address.
3. Run `L17-capture.grc` on the second SDR, then run your Pluto encoder. Find your signal on the capture flowgraph's waterfall, and screenshot both windows for Question 8(a). If the signal is weak, raise the capture flowgraph's RX gain a few dB at a time. Never set TX attenuation below 30 dB.
4. Close the capture flowgraph after about 5 s. Open `capture.sigmf-data` in URH at 1 MS/s and compare its chips with the original recording's for Question 8(b).
5. Set the TX attenuation to 60, 70, 80, and 89 dB in turn, recording 5 s at each, and record whether URH's chips still match, for Question 8(c). Stop both flowgraphs and unplug the radios before you disconnect the cable.
::::

::::{frame} Part 3: After the Lab
:::{present}
- Give the evidence for the carrier, the modulation, the encoding, and each field.
- Explain what the check field lets a receiver do, and what it cannot.
- Explain why a fixed code can be replayed, and what would stop it.
:::

The Writeup is Question 9, in three parts. Part (a) lists, step by step, the observation that settled each answer: what you saw on the waterfall, the envelope, and the lines of chips, and which comparison between buttons identified each field. Part (b) explains, from your Question 6 table and your noise run in Question 7(c), what the device's check lets a receiver reject, and why a frame with two flipped bits might still pass. Part (c) explains why your encoder from Question 7 would operate the real device, and describes in words how a rolling code, as in a car key fob, would stop a recording from being reused.
::::

::::{frame} Lab Packet
:class: read-only doc-links

- <a class="doc-link" href="../../labs/ECE448_Lab_L17_RFReverseEngineering_blank.pdf" target="_blank" rel="noopener">L17 Lab packet (PDF)</a>
- <a class="doc-link" href="../../grc/L17-sigmf-view.grc" download>L17-sigmf-view.grc</a>: the viewer for Questions 1 and 4. No hardware needed.
- <a class="doc-link" href="../../grc/L17-capture.grc" download>L17-capture.grc</a>: the receiving SDR for Question 8, recording to SigMF. Receive only.
- <a class="doc-link" href="../../grc/L17-fan-tx-pluto.grc" download>L17-fan-tx-pluto.grc</a>: the lesson's Pluto encoder, for its TX attenuation slider. Transmit only into the cable.
::::

::::{frame} Looking Ahead
:::{present}
- Lesson 18 receives ADS-B from aircraft at 1090 MHz.
- Its format is a public standard, so the work is the receiver.
:::

Keep your encoder and your Question 6 table. Lessons 18 and 19 decode aircraft and ship transponders, whose formats are published, and the L18–L19 Lab decodes live traffic. The same first steps apply there: find the carrier on a waterfall, and identify the modulation before you build anything.
::::
