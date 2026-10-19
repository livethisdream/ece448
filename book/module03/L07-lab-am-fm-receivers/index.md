---
frame_view: true
---

# L7 Lab — AM and FM Receivers

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">AM and FM Receivers</h1>

<div class="title-rule"></div>

Receive a live FM broadcast and decode its RDS data.

L7 Lab · Module 3: Analog Modulation · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '3'; counter-reset: lo 2">
  <li>I can implement an FM receiver in GNU Radio, demodulate a live broadcast FM signal, and decode its RDS data.</li>
  <li>I can explain and demonstrate the trade-off between bandwidth and noise performance for AM vs. FM.</li>
</ol>
::::

::::{frame} From Lesson to Bench
:::{present}
- **Pre-Lab:** predict the receiver settings, RDS timing, and the FM threshold.
- **Bench:** build the WBFM receiver, then receive your L5 capture, live FM with RDS, and ATIS, and compare AM with FM.
- **Writeup:** compare, and explain the differences.
:::

Lesson 7 ran every receiver on simulated test files. Today you build the WBFM receiver yourself, then run the receivers on your own L5 capture and on the air. The lab packet has three parts, and you turn it in once, complete, before Lesson 8. **Part 1, the Pre-Lab**, is on your own before the period: the receiver settings for the test file, your capture, and a local ATIS, plus the RDS timing and the FM threshold. **Part 2** is your own measurements in class. **Part 3, the Writeup**, compares the two.

Bring your RTL-SDR, its antenna, your `fm_capture.cfile` from the L5 Lab, and headphones.
::::

::::{frame} Part 1: Before the Period
:::{present}
- Predict the receiver settings and rates, and the audio line levels.
- Find the fastest time to an RDS station name.
- Plan a local ATIS receiver, and predict the FM threshold.
:::

Do the Pre-Lab before you arrive. Question 1 asks for the shift and rates of the FM receiver, the Quadrature Demod gain, the levels of the test file's audio lines, the fastest time to an RDS station name, the AM receiver's settings for a local ATIS, and the C/N at which the 25 kHz FM signal reaches threshold.

The setup also takes a few minutes, and some of it needs a network connection, which the lab room may not have. Put the six flowgraphs from the Lesson 7 page in one folder with `fm_capture.cfile`. Open `L07-rds-rx.grc` first and check that GRC reports no missing blocks: gr-rds comes with radioconda; if GRC reports the RDS blocks missing, run `mamba install gnuradio-rds` from the radioconda prompt. Then run `L07-fm-test-tx.grc`, which also uses an RDS block, and `L07-am-test-tx.grc` once each; they write the two test files, 76.8 MB each, into that folder and stop on their own. For Question 1(e), the FAA Chart Supplement and every sectional chart list an airport's ATIS frequency.
::::

::::{frame} Expected Numbers
:::{present}
| Check | Expected |
| :-- | :-- |
| Test file shift | +300 kHz |
| FM rates | 240, then 48 kS/s |
| 2.5 kHz line | 3.5 dB below 1 kHz |
| Station name, fastest | 350 ms |
| FM threshold, 25 kHz | 17.8 dB in 10 kHz |
:::

These are the predictions of Question 1 for the parts that do not depend on your location. The test file has no hardware in the way, so its measurements should match within about 1 dB, or within a frequency sink bin. Question 4(c) asks you to time the station name and explain the difference from 350 ms. Your capture, the live station, and the ATIS depend on your antenna and location, so the packet records them rather than predicting them.
::::

::::{frame} Part 2: Build the WBFM Receiver
:class: read-only

1. Start GRC and choose File, New, QT GUI. Do not open `L07-wbfm-rx.grc`; build it yourself.
2. Set `samp_rate` to 2.4e6. Add QT GUI Entries `fc_mhz` (100.0) and `station_mhz` (100.3), and a QT GUI Range `vol` from 0 to 1.
3. Add a **File Source** on `L07-fm-test.cfile` with Repeat on.
4. Add a **Low-pass Filter Taps** variable `chan_taps`: cutoff 105 kHz, transition 30 kHz, at `samp_rate`. Use it in a **Frequency Xlating FIR Filter** with decimation 10 and center frequency `(station_mhz - fc_mhz) * 1e6`.
5. Add a **Quadrature Demod** with the gain from Question 1(b).
6. Add a **Decimating FIR Filter**, decimation 5, with taps `firdes.low_pass(1, samp_rate/10, 15e3, 3e3)`.
7. Finish with **FM Deemphasis** at 48 kHz and 75 μs, a Multiply Const `vol`, and an **Audio Sink** at 48 kHz, with a float QT GUI Frequency Sink on the de-emphasis output. Do not add a Throttle.
8. Screenshot the canvas for Question 2(a). Run it with the volume low, and record the audio lines for Question 2(b).
9. Type 99.5 into Station, listen, and answer Question 2(c).
::::

::::{frame} Part 2: Your Capture
:class: read-only

1. Stop your receiver. Set the File Source's file to `fm_capture.cfile`.
2. Run it, type the center frequency you recorded at into SDR center, and set Station to the station you centered.
3. Add a float QT GUI Frequency Sink on the Quadrature Demod output at 240 kHz. Screenshot the demodulated multiplex and mark its parts for Question 3(a). Describe the audio for Question 3(b).
::::

::::{frame} Part 2: Live FM and RDS
:class: read-only

1. Connect the antenna and the RTL-SDR. Open `L07-rds-rx.grc`.
2. Right-click the File Source and choose Disable; right-click the RTL-SDR Source and choose Enable.
3. Run it. Type an SDR center about 300 kHz below a strong local station, set Station to the station, and set RF gain from your L5 gain table.
4. Wait for the station name. Fill in the table for Question 4(a); the panel shows the PI code under "Program Type" and the program type under "PI".
5. Screenshot the constellation and the panel for Question 4(b).
6. Stop and restart the flowgraph, and time how long the name takes to appear, for Question 4(c).
::::

::::{frame} Part 2: ATIS
:class: read-only

1. Open `L07-am-rx.grc` and run it on `L07-am-test.cfile`. The audio is the L6 two-tone message.
2. Stop it. Disable the File Source, enable the RTL-SDR Source, and run it again.
3. Enter the SDR center and Station from Question 1(e), and set RF gain to 40 dB to start.
4. Screenshot the receiver and record the information letter and the altimeter setting for Question 5(a).
5. Lower RF gain until the voice is hard to understand, and describe it for Question 5(b).
::::

::::{frame} Part 2: AM and FM in the Same Noise
:class: read-only

1. Open and run `L07-am-vs-fm.grc`. It needs no hardware.
2. With FM deviation at 25 kHz, set C/N to 30, 25, 20, 15, and 10 dB, and record both output SNR meters at each for Question 6(a). Repeat at 5 kHz.
3. Return to 25 kHz, choose FM under Listen To, and lower C/N from 30 to 10 dB. Describe what you hear for Question 6(b).
::::

::::{frame} No Signal?
:class: read-only

:::{admonition} If the station name, the ATIS, or the RTL-SDR does not work
:class: tip
- **No station name:** choose a stronger station, or raise RF gain until the RDS constellation shows two clusters. RDS needs more signal than the audio does.
- **No ATIS:** aircraft band stations need line of sight. Try a window, a higher floor, or the airport's other frequency, and say in the packet what you tried. If none works, answer Question 5 from the test file and say so.
- **No RTL-SDR:** pair with a classmate whose RTL-SDR works for Questions 4 and 5, take turns at their laptop, and record your own numbers. Questions 2, 3, and 6 need no hardware.
- **Audio error:** an Audio Sink that cannot open your sound card stops the flowgraph. Plug in your headphones and run it again, as in the L6 Lab.
:::
::::

::::{frame} Part 3: After the Lab
:::{present}
- Explain why a mono receiver plays a stereo station correctly.
- Explain where FM lost its advantage, and why 5 kHz gives the higher SNR at 10 dB.
- Explain why aircraft use AM and broadcasters use wideband FM.
:::

The Writeup is three questions. The first uses your multiplex screenshot to explain why a mono receiver plays a stereo station correctly. The second compares your AM and FM table with the threshold you predicted in Question 1(f), and asks why the 5 kHz signal has the higher output SNR at 10 dB C/N and the lower one at 30 dB. The third connects your ATIS and FM listening to the reasons each service chose its modulation.
::::

::::{frame} Lab Packet
:class: read-only doc-links

- <a class="doc-link" href="../../labs/ECE448_Lab_L07_AMFMReceivers_blank.pdf" target="_blank" rel="noopener">L7 Lab packet (PDF)</a>
- <a class="doc-link" href="../../grc/L07-wbfm-rx.grc" download>L07-wbfm-rx.grc</a>, <a class="doc-link" href="../../grc/L07-rds-rx.grc" download>L07-rds-rx.grc</a>, <a class="doc-link" href="../../grc/L07-am-rx.grc" download>L07-am-rx.grc</a>, and <a class="doc-link" href="../../grc/L07-am-vs-fm.grc" download>L07-am-vs-fm.grc</a>
- <a class="doc-link" href="../../grc/L07-fm-test-tx.grc" download>L07-fm-test-tx.grc</a> and <a class="doc-link" href="../../grc/L07-am-test-tx.grc" download>L07-am-test-tx.grc</a>, which write the test files
::::

::::{frame} Looking Ahead
:::{present}
- Lesson 8 sends bits as FSK: FM with a two-valued message.
- Keep your WBFM receiver; its Quadrature Demod reappears in the FSK receiver.
:::

Keep your receivers. Lesson 8 moves to digital modulation, starting with frequency-shift keying, which switches the carrier between two frequencies. Its receiver uses the same Quadrature Demod you used today, after a channel filter, and follows it with a decision on each bit instead of a speaker.
::::
