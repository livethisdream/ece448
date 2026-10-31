---
frame_view: true
---

# L18–L19 Lab — ADS-B and AIS

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">ADS-B and AIS</h1>

<div class="title-rule"></div>

Decode the aircraft overhead with your own PlutoSDR and gr-adsb receiver, and a recording of ships with your own AIS receiver.

L18–L19 Lab · Module 6: Waveform Applications & RF Reverse Engineering · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '6'; counter-reset: lo 6">
  <li>I can receive and decode ADS-B messages from aircraft transponders.</li>
  <li>I can receive and decode AIS messages from marine vessels.</li>
</ol>
::::

::::{frame} From Lesson to Bench
:::{present}
- **Pre-Lab:** fly your own aircraft through the ADS-B generator; work out the AIS settings.
- **Bench:** build both receivers yourself; decode live aircraft on the Pluto and a recording of ships.
- **Writeup:** compare the two receivers and explain what you saw.
:::

Lessons 18 and 19 decoded simulated aircraft and ships with `L18-adsb-rx.grc` and `L19-ais-rx.grc`. Today you build both receivers from an empty canvas. The ADS-B one is a PlutoSDR Source and gr-adsb's blocks listening to the real aircraft over Colorado Springs, so your table is your own and you check it against a public flight tracker. The AIS one decodes the lab's own recording of ships, with a sample rate and center frequency different from the lesson's, so its settings are yours to work out. The lab packet has three parts, and you turn it in once, complete, before Lesson 20. You do **Part 1, the Pre-Lab**, on your own before the period, record **Part 2**'s measurements in class, and explain them in **Part 3, the Writeup**.

The Pluto only receives on 1090 MHz; nothing in this course transmits there. The AIS recording was written by a GNU Radio flowgraph, not captured from an antenna. The one transmission in the lab is optional: your own aircraft, sent at 915 MHz into a cable through a 30 dB attenuator, or, if your instructor says so, over the air at 915 MHz at low power.
::::

::::{frame} Part 1: Before the Period
:::{present}
- Add your own aircraft to the ADS-B generator, decode it, and raise the noise until it leaves.
- Work out the AIS receiver's settings from the lab recording's meta file.
:::

Do the Pre-Lab before you arrive. Question 1 uses the Lesson 18 flowgraphs: put `L18-adsb-tx.grc` and `L18-adsb-rx.grc` in one folder, add an aircraft of your own to the generator's `AIRCRAFT` list as the packet describes, run the generator once, and check that the receiver decodes your aircraft. Then raise the Added noise slider until your aircraft leaves the table. If GRC reports an error, the L5 lesson page lists the install checks.

Question 2 works out the AIS receiver's settings for the lab recording, whose `.sigmf-meta` the packet describes: each channel's offset from the center, the decimation to about 48 kS/s, the samples per bit, and the Quadrature Demod gain. The Lesson 19 page's On the SDR frame describes the same steps for any recording.
::::

::::{frame} Part 2: Build an ADS-B Front End
:class: read-only

1. Start GRC and choose File, New, QT GUI. Do not open `L18-adsb-rx.grc` yet; build the front end yourself.
2. Set `samp_rate` to 2e6, and add a Variable `fc` = 1090e6. Add a **QT GUI Range** with ID `rx_gain`, label Pluto RX gain (dB), from 0 to 70 in steps of 1, default 50.
3. Add a **PlutoSDR Source**: IIO context URI `"ip:192.168.2.1"` with the quotes, LO frequency `int(fc)`, sample rate `int(samp_rate)`, Gain Mode (RX1) Manual, Manual Gain (RX1) `rx_gain`, Filter Configuration Auto (needed below 2.084 MS/s), output type Complex float32.
4. Add an **AGC3** after it: attack rate 1, decay rate 1e-6, reference 1, gain 1, maximum gain 1e9, type complex. It scales the strongest recent pulses to a power near 1, as in `L18-adsb-rx.grc`.
5. Add **Complex to Mag^2** after the AGC.
6. Add a **QT GUI Time Sink**: type float, 120 points, sample rate `samp_rate`, Y axis from 0 to 1.2, grid on. In its Trigger tab set the mode to Normal, the slope to Positive, the level to 1.2, the top of the Y axis, and the delay to 5e-6. Every arrow must be black.
7. Plug in the Pluto, put it and its antenna at a window, and run the flowgraph. Screenshot the canvas for Question 3(a).
8. Watch the time sink. Lower the trigger level a step at a time until it freezes on preambles, four pulses in the first 5 µs, and not on noise. Screenshot one, and record the level, the floor, and the heights of the strongest and weakest messages you see, in power, for Question 3(b).
::::

::::{frame} Part 2: Live Aircraft
:class: read-only

1. Add a **QT GUI Range** with ID `threshold`, label Framer threshold, from 0.0001 to 0.2 in steps of 0.0001, default 0.2.
2. From the ADS-B group of GRC's block list, add gr-adsb's **ADS-B Framer** (sample rate `samp_rate`, detection threshold `threshold`), **ADS-B Demod** (sample rate `samp_rate`), and **ADS-B Decoder** (Extended Squitter Only, Error Correction None, Print Level Verbose). Connect Complex to Mag^2 to the Framer, the Framer to the Demod, the Demod's `out` to a **Null Sink**, and the Demod's `demodulated` to the Decoder's.
3. Open `L18-adsb-rx.grc` in a second GRC tab. Select the **Aircraft Table**, the two **Function Probes** (`stats` and `table`), and the two **QT GUI Labels**, copy them with Ctrl+C, and paste them into your flowgraph with Ctrl+V. If GRC renames the table on pasting, set each Function Probe's Block ID to its new name. Connect the Demod's `demodulated` to the table's `found` and the Decoder's `decoded` to its `decoded`, and set its `settings` to `(rx_gain, threshold)`.
4. Run it. The Framer threshold starts at 0.2; lower it until it sits just above the floor you recorded for Question 3(b), then run for 10 minutes. Each message also prints in the GRC console, which fills quickly on the air, so read the Aircraft Table. The console's Heading is measured counterclockwise from east; the table's track is the compass value a flight tracker shows.
5. Fill in the Question 4 table with up to five aircraft, and look each one up by callsign or ICAO address on a public flight tracker, such as ADS-B Exchange or FlightAware. Screenshot the window for Question 4(b).
6. Set the Pluto RX gain to 70, 60, 50, 40, and 30 dB in turn. At each, wait 60 s and record the Messages label's decoded count, the messages the Decoder turned into an identity, a position, or a velocity, and the number of aircraft, for Question 5.

If no aircraft decode after 10 minutes, move the Pluto to a different window or outside, and raise the gain. If there are still none, or if your instructor chooses, decode your own aircraft instead, and say which you used in your answers. **Your own aircraft at 915 MHz:** copy your Question 1 line into the `AIRCRAFT` list of `L18-adsb-tx-pluto.grc`'s ADS-B Out block, cable the Pluto's TX port through the 30 dB attenuator to an RX port (or, if your instructor says so, send it over the air at 915 MHz at low power), set your `fc` to 915e6, and run both flowgraphs, the transmitter first; never set TX attenuation below 30 dB. With two Plutos on one laptop, give each flowgraph its Pluto's `usb:` URI, as in Lesson 17. On one Pluto, both flowgraphs share one sample-rate clock, so keep both at 2 MS/s and expect a brief glitch when the receiver starts. **The recording:** add a SigMF Source and Throttle as in `L18-adsb-rx.grc` in place of the PlutoSDR Source and play the lesson's recording.
::::

::::{frame} Part 2: Build an AIS Receiver
:class: read-only

1. Put `L18-L19-lab-ais.sigmf-data` and `.sigmf-meta` in a folder, start a new QT GUI flowgraph, and save it there. Do not open `L19-ais-rx.grc` yet.
2. Add Variables `samp_rate`, `decim`, `sps`, `chan_a`, and `chan_b` with your Question 2 values, and `taps` = `firdes.low_pass(1, samp_rate, 7e3, 3e3)`. Add a **QT GUI Range** with ID `squelch`, label Squelch (dB), from −60 to 0 in steps of 1, default −30.
3. Add a **SigMF Source (Minimal)**: file `'L18-L19-lab-ais.sigmf-data'` with the quotes, output type complex float, repeat Yes. Add a **Throttle** at `samp_rate` after it.
4. Build channel A: a **Frequency Xlating FIR Filter** (complex in and out, taps `taps`, center frequency `chan_a`, decimation `decim`, sample rate `samp_rate`), a **Power Squelch** (complex, threshold `squelch`, alpha 0.05, gate No), a **Quadrature Demod** with your Question 2 gain, a **Symbol Sync** (float, Timing Error Detector Zero Crossing, samples per symbol `sps`, loop bandwidth 0.06, damping 1, maximum deviation 1.5, output 1 sample per symbol), and a **Binary Slicer**.
5. Select the five channel A blocks, copy and paste them, connect the copy to the Throttle too, and change its center frequency to `chan_b`.
6. Copy the **AIS Decoder**, its two Function Probes, and its two QT GUI Labels from `L19-ais-rx.grc`, connect channel A's slicer to its first input and channel B's to its second, and set its `settings` to `(squelch,)`. Every arrow must be black.
7. Run it. Screenshot the canvas for Question 6(a), and after one pass through the 5 s recording record the Frames label and the ships for Question 6(b).
::::

::::{frame} Part 2: The Ships and the Squelch
:class: read-only

1. With the squelch at −30 dB, read the decoder's printout in the GRC console and the Ships label, and fill in the Question 7 table. Look up each MMSI's first three digits in the ITU's table of Maritime Identification Digits for the flag.
2. Copy one complete `!AIVDM` sentence from the console into `pyais` (`pyais.decode('...')` in Python) or an online AIVDM decoder, for Question 7(b). A message 5 needs both of its sentences.
3. Set the Squelch slider to −40, −30, −20, −15, −10, −5, and 0 dB in turn. At each, wait for two passes through the recording, about 10 s, and mark which ships are in the table, for Question 8. The table starts over each time the slider moves.
4. At −40 dB, add a **QT GUI Time Sink** on the two Quadrature Demod outputs if you do not have one, and describe the plot and the Frames label for Question 8(a).
::::

::::{frame} Nothing Decodes?
:class: read-only

:::{admonition} If the table stays empty
:class: tip
For ADS-B, check that the PlutoSDR Source's URI is `"ip:192.168.2.1"`, its LO frequency `int(fc)` with `fc` at 1090e6, and its sample rate 2e6, that the AGC sits between it and Complex to Mag^2, that the ADS-B Framer's input comes from Complex to Mag^2, that the Demod's `demodulated` port goes to the Decoder, and that the antenna can see the sky; inside a building with no window, few aircraft decode. If bursts are found but few decode, raise the Framer threshold above the floor. If GRC marks the ADS-B blocks red, gr-adsb is missing: run `mamba install gnuradio-adsb` in the radioconda prompt and restart GRC. For AIS, check that the file name is in quotes and the SigMF Source's type is complex float, that `chan_a` and `chan_b` match the recording's center frequency, that each Frequency Xlating FIR Filter decimates by `decim`, that the Quadrature Demod gain uses the rate after decimation, and that Symbol Sync's samples per symbol is `sps`. If frames fail the CRC at every squelch, check `sps` and the loop bandwidth first; the sign of the Quadrature Demod gain does not matter, because NRZI ignores which level is which.
:::
::::

::::{frame} Part 3: After the Lab
:::{present}
- Explain why ADS-B needs only the power and AIS needs FM and timing recovery.
- Rank the ships you decoded by strength from your squelch table.
- Compare your aircraft with the flight tracker.
:::

The Writeup is Question 9, in three parts. Part (a) compares your two receivers and explains why each needs the blocks it has. Part (b) ranks the ships you decoded by received strength from your squelch table, explains what each step told you, and says how you would choose a squelch for a real recording. Part (c) compares your live aircraft with the flight tracker and explains any aircraft the tracker showed that you did not decode.
::::

::::{frame} Lab Packet
:class: read-only doc-links

- <a class="doc-link" href="../../labs/ECE448_Lab_L18_ADSBAIS_blank.pdf" target="_blank" rel="noopener">L18–L19 Lab packet (PDF)</a>
- <a class="doc-link" href="../../grc/L18-L19-lab-ais.sigmf-data" download>L18-L19-lab-ais.sigmf-data</a> and <a class="doc-link" href="../../grc/L18-L19-lab-ais.sigmf-meta" download>L18-L19-lab-ais.sigmf-meta</a>: the lab's simulated AIS recording for Questions 2 and 6 to 8, 7.7 MB. GRC 3.10 marks the SigMF Source (Minimal) and SigMF Sink (Minimal) blocks as deprecated and shows a warning when the flowgraph loads; the warning is expected and harmless, and both blocks work.
- The Lesson 18 page has `L18-adsb-tx.grc`, `L18-adsb-tx-pluto.grc`, and `L18-adsb-rx.grc`, whose Aircraft Table you copy, and the Lesson 19 page has `L19-ais-rx.grc`, whose AIS Decoder you copy.
- <a href="https://www.itu.int/en/ITU-R/terrestrial/fmd/Pages/mid.aspx" target="_blank" rel="noopener">ITU table of Maritime Identification Digits</a>, for the ships' flags.
::::

::::{frame} Looking Ahead
:::{present}
- Lesson 20 turns to QAM and OFDM.
- The final project is an SDR application of your own.
:::

Keep both flowgraphs. Lesson 20 turns to QAM and OFDM, which carry many bits per symbol. Either receiver can also start a final project, such as a live map of local aircraft or a decoder for another pulse or FSK signal.
::::
