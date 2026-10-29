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
- **Pre-Lab:** read the recording's meta file, read chips in GNU Radio, and work out chip settings.
- **Bench:** take an unknown remote from carrier to fields, build its encoder, send it through a cable, and record a real remote.
- **Writeup:** explain the evidence for each step.
:::

Lesson 17 took the Simulated fan remote through five steps: find the carrier, identify the modulation, identify the encoding, build an encoder, and transmit. Today you take a different device through the same steps. It is a **Simulated remote outlet switch** with six buttons, and nobody will describe it to you: its recording is all you get. The lab packet has three parts, and you turn it in once, complete, before Lesson 18. **Part 1, the Pre-Lab**, is on your own before the period. **Part 2** is what you find, build, and observe in class. **Part 3, the Writeup**, explains it.

Questions 1 to 7 run on your laptop and transmit nothing. Question 8 transmits, into a cable only, as the PlutoSDR frame below describes. Question 9 only receives.
::::

::::{frame} The Recording
:class: read-only doc-links

- <a class="doc-link" href="../../grc/L17-lab-unknown.sigmf-data" download>L17-lab-unknown.sigmf-data</a> and <a class="doc-link" href="../../grc/L17-lab-unknown.sigmf-meta" download>L17-lab-unknown.sigmf-meta</a>: the unknown device, labeled Simulated in its meta file, one press of each of its six buttons. Keep the two files in the same folder.

The recording is a SigMF pair, like the lesson's, but its sample rate and center frequency are its own: read them from the meta file before you open it anywhere. The meta file's description lists the buttons in the order they were pressed, which tells you which burst is which. It does not describe the signal.
::::

::::{frame} Part 1: Before the Period
:::{present}
- Read the meta file and set up `L17-sigmf-view.grc` for this recording.
- Open the lesson's recording in `L17-chips.grc` and read its chips.
- Work out samples per chip for a few chip lengths.
:::

Do the Pre-Lab before you arrive. Question 1 asks for the datatype, sample rate, and center frequency from `L17-lab-unknown.sigmf-meta`, and for the values of `rec`, `samp_rate`, and `fc` you set in `L17-sigmf-view.grc` so that it opens this recording. Run it once to check that the spectrum's axis is centered on the recording's center frequency.

Question 2 checks `L17-chips.grc` on the lesson's recording, `L17-fan-remote.sigmf-data`, whose answers the lesson page gives, so you can tell whether the flowgraph is working before you meet the unknown. Set `samp_rate` to 200000, `fc` to 350e6, and the carrier offset to 40000 Hz, measure the shortest pulse on the envelope, and set the chip length to it. Question 3 is the arithmetic the Chip Reader and your encoder need: samples per chip for several chip lengths at this recording's sample rate and at the PlutoSDR flowgraph's 1 MS/s, so you can convert any length you measure.
::::

::::{frame} Part 2: Find the Carrier
:class: read-only

1. Run `L17-sigmf-view.grc` with your settings from Question 1. Watch the waterfall through at least two loops of the recording.
2. Find every signal on the waterfall. For each, decide whether it bursts when a button is pressed or stays on, and record its frequency for Question 4(a).
3. Read the center of the bursts off the Frequency Sink or the waterfall. To check it, move the Carrier offset slider until the envelope plot shows clean pulses, then find the offset on each side where the pulses drop to half their height and take the midpoint. Record the offset and screenshot the window for Question 4(b).
4. Record the carrier frequency, the center frequency plus your offset, for Question 4(c).
::::

::::{frame} Part 2: Modulation and Encoding in GNU Radio
:class: read-only

1. Open `L17-lab-unknown.sigmf-data` in `L17-chips.grc`. Set `rec`, `samp_rate`, and `fc` as in Question 1, and the carrier offset to your answer to Question 4(b).
2. Set the threshold about halfway between the envelope's off and on levels. On the time sink, find the shortest pulse; the time axis is in milliseconds, so convert it to samples at the recording's rate. Record it for Question 5(a), and set the chip length to it.
3. Find the shortest gap the same way. Record it for Question 5(b), and decide whether it fits your chip length.
4. Read the lines of chips the Chip Reader prints in GRC's console. Compare several bursts, decide how the chips group into bits, and whether each burst holds anything besides data bits, and record your evidence for Question 5(c).
5. Decode one burst of each button into bits by hand, and fill in Question 6's table. Then compare the buttons and mark which bits never change and which change with the button.
6. Count the bursts in one press, and read the pause between bursts from the Chip Reader, for Question 6(c).
::::

::::{frame} If the Chips Look Wrong
:class: read-only

:::{admonition} If the lines of chips change from burst to burst, or the groups never repeat
:class: tip
Check the sample rate first: a wrong `samp_rate` makes every time on the envelope wrong. Then check the carrier offset: if the pulses are low or ragged, the signal sits at the edge of the filter. If short pulses never cross the threshold, lower it, or raise the Envelope gain. If a line is a chip short or long in the middle, your chip length is a little off; measure the pulse again, over several pulses. If some lines are a chip or two shorter than others at the end, look at what the last bits of each line are: the Chip Reader ends a line at its last on chip, so off chips at the end of a burst count as part of the pause.
:::
::::

::::{frame} Part 2: Build the Encoder
:class: read-only

1. Start GRC and choose File, New, QT GUI. Do not open `L17-fan-tx-sim.grc`; build the encoder yourself from standard blocks, with the settings you found. You may look at the lesson page's Step 4 figure.
2. Set `samp_rate` to the recording's sample rate and `chip_len` to your samples per chip. Add a Variable `bits` that holds one button's bits as a list of 0s and 1s.
3. Build the envelope: a **Vector Source** of `bits`, a **Map** and **Unpack K Bits** that turn each bit into your chip pattern, **Char To Float**, and a **Repeat** of `chip_len`.
4. Add anything your measurements show around the bits, and the pause after each burst, with a **Constant Source** of 0. Join them with a **Stream Mux** whose lengths, in samples, match your measurements.
5. Put the envelope on a carrier at your offset with **Float To Complex**, a **Signal Source**, and a **Multiply**. Add a **Noise Source** of amplitude 0.05 and an **Add**, then a **Throttle**, a **QT GUI Time Sink** of the envelope from **Complex to Mag**, and a **SigMF Sink (Minimal)** with file name `my-unknown`, the recording's sample rate, and its center frequency. Every arrow must be black.
6. Run it for about 5 s and close it. Set `rec` in `L17-chips.grc` to `my-unknown.sigmf-data`, with the same settings as for the original recording, and compare the lines of chips for Question 7(a).
7. Change `bits` to a second button and repeat for Question 7(b). Then run it again and raise the noise amplitude in steps of 0.1 until the Chip Reader's lines of chips no longer match; record where for Question 7(c).
::::

::::{frame} Part 2: Transmit into a Cable
:::{present}
- You send your encoder at 915 MHz from one PlutoSDR through a 30 dB attenuator into a second PlutoSDR.
- Connect the cable before the flowgraph runs; an antenna only if your instructor says so.
:::

Save a copy of your encoder for the radio. Delete the Noise Source, the Add, and the Throttle, set `samp_rate` to 1000000 and `chip_len` to your chip length in samples at 1 MS/s, and add a **PlutoSDR Sink** after a Multiply Const of 0.5, tuned to 915 MHz. A signal the course makes never goes out on the real device's frequency, so your encoder leaves the device's band for 915 MHz, in the 902 to 928 MHz ISM band; keep your carrier offset, so the carrier lands at 915 MHz plus the offset. Copy the `tx_atten` QT GUI Range from `L17-fan-tx-pluto.grc` unchanged, from 30 to 89 dB with a default of 60, and set it as the sink's attenuation. Put "Transmit into the cable unless your instructor says otherwise" in the flowgraph's description. A second PlutoSDR records what arrives with `L17-capture.grc`. Leave its variable `fc` at 915e6, its default, and set it before you run it if you changed it; the SigMF Sink writes the center frequency into the meta file when the flowgraph starts.

In class we transmit only into a cable, into a shielded enclosure, or at very low power in an ISM band, and only when the lesson says to. This device's band is an FCC Part 15 frequency, not a U.S. ISM band, which is why the encoder moves to 915 MHz. By default this question transmits only into the cable between the first Pluto's TX port and the second Pluto's RX port, through an inline 30 dB SMA attenuator, or, if your instructor says so, over the air at 915 MHz at low power. Never set TX attenuation below 30 dB or change the slider's range; a Pluto's input is rated to only a few dBm. We have compiled the Pluto flowgraphs but not run them on a radio, so your bench is their first run on hardware.
::::

::::{frame} PlutoSDR Steps
:class: read-only

1. With both radios unplugged, connect the first Pluto's TX port to the second Pluto's RX port with a short SMA cable and an inline 30 dB SMA attenuator. Do not connect an antenna, and do not connect the cable without the attenuator.
2. Plug in both radios. Run `iio_info -s` at the radioconda prompt; it should list both PlutoSDRs, each with a `usb:` address such as `usb:1.5.5`. Every Pluto has the same default address, `ip:192.168.2.1`, so on one laptop copy each Pluto's `usb:` address into the `uri` of its flowgraph's PlutoSDR block, or run each Pluto from its own laptop.
3. Run `L17-capture.grc` on the second Pluto, with `fc` already set, then run your Pluto encoder. Find your signal on the capture flowgraph's waterfall, and screenshot both windows for Question 8(a). If the signal is weak, raise the capture flowgraph's RX gain a few dB at a time. Never set TX attenuation below 30 dB.
4. Close the capture flowgraph after about 5 s. Open `capture.sigmf-data` in `L17-chips.grc` with `samp_rate` 1000000, `fc` 915e6, your carrier offset, and your chip length at 1 MS/s. Raise the Envelope gain until the pulses reach about 1, and compare its chips with the original recording's for Question 8(b).
5. Set the TX attenuation to 60, 70, 80, and 89 dB in turn, recording 5 s at each, and record whether the Chip Reader's chips still match, for Question 8(c). Stop both flowgraphs and unplug the radios before you disconnect the cable.
::::

::::{frame} Part 2: A Real Remote
:class: read-only

In Question 9 your Pluto only receives, and receiving is always allowed.

1. Choose a real device that you own: a key fob, a wireless doorbell, or a weather sensor. Its label or manual usually gives its frequency.
2. Run `L17-explore-pluto.grc`, set its center frequency about 200 kHz below the device's frequency, hold a button down, and read the carrier off the spectrum's peak. The 2025 class read it off a live spectrum the same way. Record it for Question 9(a).
3. Set `fc` in the capture flowgraph about 200 kHz below the carrier, so the Pluto's DC spike stays off the signal, and run it. Press one button a few times and close the flowgraph; rename `capture.sigmf-data` and `.sigmf-meta` for that button. Repeat for every button.
4. Open the recordings in `L17-chips.grc` and take the device as far through Steps 2 and 3 as you can: the modulation, the chip length, the encoding, and which bits change with the button. Record it for Question 9(b) and (c).
::::

::::{frame} Part 3: After the Lab
:::{present}
- Give the evidence for the carrier, the modulation, the encoding, and each field.
- Explain how a receiver could reject a damaged frame, and what it could miss.
- Explain why a fixed code can be replayed, and what would stop it.
:::

The Writeup is Question 10, in three parts. Part (a) lists, step by step, the observation that settled each answer: what you saw on the waterfall, the envelope, and the lines of chips, and which comparison between buttons identified each field. Part (b) explains, from your Question 6 table and your noise run in Question 7(c), how a receiver of this device could tell a frame damaged by noise from a good one, and what damage it could miss. Part (c) explains why your encoder from Question 7 would operate a device that matched this recording, and describes in words how a rolling code, as in a car key fob, would stop a recording from being reused.
::::

::::{frame} Lab Packet
:class: read-only doc-links

- <a class="doc-link" href="../../labs/ECE448_Lab_L17_RFReverseEngineering_blank.pdf" target="_blank" rel="noopener">L17 Lab packet (PDF)</a>
- <a class="doc-link" href="../../grc/L17-sigmf-view.grc" download>L17-sigmf-view.grc</a>: the viewer for Questions 1 and 4. No hardware needed.
- <a class="doc-link" href="../../grc/L17-chips.grc" download>L17-chips.grc</a>: the envelope, threshold, and Chip Reader for Questions 2, 5 to 9. No hardware needed.
- <a class="doc-link" href="../../grc/L17-capture.grc" download>L17-capture.grc</a>: the receiving PlutoSDR for Questions 8 and 9, recording to SigMF. Receive only; set `fc` before you run it.
- <a class="doc-link" href="../../grc/L17-explore-pluto.grc" download>L17-explore-pluto.grc</a>: a live PlutoSDR spectrum and waterfall with a center frequency you change while it runs, for Question 9(a). Receive only.
- Optional: an RTL-SDR also works for Question 9 with <a class="doc-link" href="../../grc/L17-capture-rtl.grc" download>L17-capture-rtl.grc</a>, a Soapy RTL-SDR Source at 1.024 MS/s; nothing in the lab needs one.
- <a class="doc-link" href="../../grc/L17-fan-tx-pluto.grc" download>L17-fan-tx-pluto.grc</a>: the lesson's Pluto encoder, for its TX attenuation slider. Transmit into the cable unless your instructor says otherwise.
::::

::::{frame} Looking Ahead
:::{present}
- Lesson 18 receives ADS-B from aircraft at 1090 MHz.
- Its format is a public standard, so the work is the receiver.
:::

Keep your encoder and your Question 6 table. Lessons 18 and 19 decode aircraft and ship transponders, whose formats are published, and the L18–L19 Lab decodes live traffic. The same first steps apply there: find the carrier on a waterfall, and identify the modulation before you build anything.
::::
