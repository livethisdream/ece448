---
frame_view: true
---

# L14 Lab — HD Radio

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">HD Radio</h1>

<div class="title-rule"></div>

Build a sideband power meter, identify a station's configuration from a capture, and measure a live station on the PlutoSDR.

L14 Lab · Module 6: Waveform Applications & RF Reverse Engineering · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '6'; counter-reset: lo 2">
  <li>I can describe how HD Radio works and demodulate an HD Radio signal.</li>
</ol>
::::

::::{frame} From Lesson to Bench
:::{present}
- **Pre-Lab:** change one test-file setting and read the finder.
- **Bench:** build a sideband meter, identify a capture's configuration, and measure a live station.
- **Writeup:** explain what you saw and what it tells you about each station.
:::

Lesson 14 found the HD Radio sidebands in a simulated test file and measured them with `L14-hd-find.grc`. Today you build the sideband meter yourself from an empty canvas, use it on a second capture whose configuration you do not know, and then point it at a live station with the PlutoSDR. Last, if you have nrsc5, you can decode a recording of the station; that step is optional. The lab packet has three parts, and you turn it in once, complete, before Lesson 15. You do **Part 1, the Pre-Lab**, on your own before the period, record **Part 2**'s measurements in class, and explain them in **Part 3, the Writeup**.

Nothing in this lab transmits. The PlutoSDR only receives, because your meter has no transmit block, and both captures came from GNU Radio flowgraphs, not from an antenna.
::::

::::{frame} Part 1: Before the Period
:::{present}
- Change one setting in `L14-hd-test-tx.grc`, run it, and read the finder.
- Slide the finder's Inner subcarrier and watch the readings.
:::

Do the Pre-Lab before you arrive. Put both flowgraphs from the Lesson 14 page in one folder. Question 1 has you open `L14-hd-test-tx.grc`, change the Variable `upper_dbc` from −23 to −18, run it once to write `L14-hd-test.cu8`, and then run `L14-hd-find.grc` and record what its three meters read; if GRC reports an error, the L5 lesson page lists the install checks.

Question 2 uses the same run: slide the finder's **Inner subcarrier** from 356 down to 280, one step at a time, and record what the meters do at each step. Part 2 uses the same slider on a capture whose configuration you do not know.
::::

::::{frame} Expected Numbers
:::{present}
| Check | Expected |
| :-- | :-- |
| Your meter on the Question 1 file | matches the lesson's finder |
| Hybrid sideband edges | about 129.4 and 198.4 kHz from the center |
| A sideband on the display | at least 10 dB above the floor |
:::

Your meter should match the finder's readings on the same file within 0.1 dB; a larger difference means a filter setting or a center frequency is off. The lab capture comes from a different station, and you identify its configuration from its spectrum and its meter readings.
::::

::::{frame} Part 2: Build the Meter
:class: read-only

1. Start GRC and choose File, New, QT GUI, and save the new flowgraph in the folder that holds `L14-hd-test.cu8`. Do not open `L14-hd-find.grc`; build the meter yourself.
2. Set `samp_rate` to 1488375. Add Variables `df` = `1488375 / 4096`, `outer` = `546`, `sb_center` = `(inner + outer) / 2 * df`, `sb_half` = `((outer - inner) / 2 + 0.5) * df`, `decim` = `6`, and `avg_len` = `int(0.2 * samp_rate / decim)`. Add a **QT GUI Entry** with ID `fc`, label Center (Hz), type real, and default value `100.3e6`, a **QT GUI Range** with ID `rx_gain`, label Pluto RX gain (dB), from 0 to 70 in steps of 1, default 30, and a **QT GUI Range** with ID `inner`, label Inner subcarrier, type int, from 280 to 356 in steps of 19, default 356.
3. Read the file: a **File Source** (type byte, file `'L14-hd-test.cu8'` with the quotes, repeat Yes), a **Throttle** (byte, `2 * samp_rate`), **UChar To Float**, **Add Const** (float, −127.5), **Multiply Const** (float, `1 / 128`), **Deinterleave** (float, 2 streams), and **Float To Complex**.
4. On the Float To Complex output, add a **QT GUI Frequency Sink**: complex, FFT size 4096, center frequency `fc`, bandwidth `samp_rate`, average Medium, Y axis from −110 to −10.
5. Add two **Low-pass Filter Taps** variables at `samp_rate`: `host_taps` with cutoff `100e3` and transition `10e3`, and `sb_taps` with cutoff `sb_half` and transition `2e3`.
6. Add three **Frequency Xlating FFT Filters**, each with decimation `decim` and sample rate `samp_rate`: the host with taps `host_taps` and center 0, the upper sideband with `sb_taps` and center `sb_center`, and the lower sideband with `sb_taps` and center `-sb_center`. Connect Float To Complex to all three.
7. After each filter add **Complex to Mag^2**, a **Moving Average** (float, length `avg_len`, scale `1 / avg_len`), **Keep 1 in N** (float, N `avg_len // 10`), and **Log10** (n = 10).
8. Add three **Subtract** blocks (float): upper minus host, lower minus host, and upper minus lower, each taking the Log10 outputs. Connect them to a **QT GUI Number Sink** with 3 inputs, minimum −40, maximum 0, and labels Upper and Lower in dBc and Upper minus lower in dB. Every arrow must be black.
9. Run it on the file you wrote in Question 1, wait 5 s, and record the three readings and a screenshot for Question 3.
::::

::::{frame} Part 2: The Lab Capture
:class: read-only

1. Stop your meter and change the File Source's file to `'L14-lab-capture.cu8'`. The File Source reads the file only when the flowgraph starts.
2. Change the frequency sink's FFT size to 8192 and run it. Drag a box around one edge of a sideband on the frequency sink to zoom in, read the edge's frequency in MHz, and right-click to zoom back out. Do the same for the inner and outer edge of each sideband, for Question 4(a).
3. Record the meter readings with Inner subcarrier at 356 for Question 4(b).
4. If the inner edges sit closer to the host than 129.4 kHz, slide Inner subcarrier down one step at a time until the readings stop rising, and record the setting and the readings there.
5. Read the Upper minus lower meter for Question 4(c).
6. Find the other station in the capture, give its offset from the center, and say whether it carries HD Radio, for Question 4(d).
::::

::::{frame} Part 2: A Live Station
:class: read-only

<img src="../../viz/img/L14-hd-find.png"
     alt="The L14 sideband finder on the lesson's test file, labeled Simulated: L14 test file, for comparison: meters at minus 23.02 and minus 23.05 dBc and 0.02 dB upper minus lower, two flat shelves beside the host on the spectrum, and two straight bands on the waterfall"
     style="max-width: 640px; width: 100%; display: block; margin: 0 auto 12px;">

The figure shows the lesson's simulated test file; a live station's host is rougher, and its shelves may stand closer to the floor. We have compiled this step but not yet tested it on a live station, so expect to adjust the gain.

1. Add a **PlutoSDR Source** to your meter: IIO context URI `ip:192.168.2.1`, LO frequency `int(fc)`, sample rate `samp_rate`, RF bandwidth `samp_rate`, gain mode Manual, and manual gain `rx_gain`, with the rest at their defaults. Connect it to the frequency sink and the three filters. Then select the File Source and the six blocks after it, through Float To Complex, and press D to disable all seven; GRC will not run with both sources connected.
2. Plug in the PlutoSDR with an antenna on its RX port; the course Plutos run in extended-frequency mode, so the FM band is in range. Run your meter and type each strong station's frequency in hertz into Center in turn, using the station list at hdradio.com, and stop at one with two flat shelves beside it.
3. Raise the gain until the shelves stand at least 10 dB above the floor, but lower it if the floor rises everywhere or copies of other stations appear.
4. Record the station, its sideband edges, and both meter readings, with a screenshot, for Question 5. If its inner edges sit closer to the host than 129.4 kHz, slide Inner subcarrier down until the readings stop rising before you record them.
5. Lower the Pluto RX gain slider in steps and watch the shelves and the readings as the floor rises toward them, for Question 5(c).
::::

::::{frame} Part 2: Decoding with nrsc5 (Optional)
:class: read-only

This part is optional, and Question 6 does not count toward the grade. nrsc5 is not part of radioconda, and it has no PlutoSDR driver, so it decodes a recording you make in GRC. Use a laptop that has a recent nrsc5 installed, your own or one your instructor provides. These steps follow the nrsc5 project's documentation; we have not yet tested them in this course.

1. Open `L14-hd-find.grc` and switch it to the PlutoSDR as the lesson describes, then also enable its Rational Resampler and SigMF Sink. Type your station's frequency in MHz into the finder's Center (MHz) and set the gain you used before you run it, because the SigMF Sink records the center frequency when the flowgraph starts.
2. Run it for about 10 s and stop it. It writes `hd.sigmf-data`, about 60 MB, at 744,188 samples per second, and `hd.sigmf-meta`.
3. Run `nrsc5 --iq-input-format cf32 -r hd.sigmf-data 0`. It takes a few seconds to synchronize. Record the station name, the song title and artist, and any HD2 or HD3 program it reports, for Question 6(a). Try program 1 for HD2.
4. Record and decode again at lower gains, a few dB at a time, until nrsc5 stops playing audio. Record the lowest gain at which it plays, and how high the shelves stand above the floor in your meter at that gain, for Question 6(b).
::::

::::{frame} No Shelves?
:class: read-only

:::{admonition} If the meters read below −40 dBc or the shelves never appear
:class: tip
For a file, check that the file name in the File Source is in quotes, that the file sits in the same folder as the flowgraph, and that the File Source's type is byte, not complex. If the shelves appear but a meter reads wrong, check the sign of each filter's center frequency, that the two dBc Subtract blocks take the host on their second input, and that the third takes the lower sideband on its second input. For a live station, check that the PlutoSDR Source's sample rate is `samp_rate`, its LO frequency is `int(fc)`, and its gain mode is Manual, that you have centered on the station, and that the station carries HD Radio at all; many do not. Shelves of unequal height can mean the station runs one sideband weaker than the other; a missing shelf usually means a weak signal or a neighbor covering it.
:::
::::

::::{frame} Part 3: After the Lab
:::{present}
- Compare the live station with the test file and say what each difference means.
- Explain how the capture's spectrum identified its configuration.
- Explain why nrsc5 cannot decode the lesson's test file.
:::

The Writeup is three questions. The first compares the live station with the lesson's test file, its edges, the height of its shelves, and whether its two sides match, and says what each difference tells you about the station. The second explains how the lab capture's edges and meter readings identified its configuration, and why a station would choose it. The third lists what nrsc5 needs from a signal that the lesson's test file does not provide.
::::

::::{frame} Lab Packet
:class: read-only doc-links

- <a class="doc-link" href="../../labs/ECE448_Lab_L14_HDRadio_blank.pdf" target="_blank" rel="noopener">L14 Lab packet (PDF)</a>
- `L14-lab-capture.cu8`, the lab's simulated capture for Question 4: your instructor posts it here before the lab.
- The Lesson 14 page has `L14-hd-test-tx.grc`, which writes the lesson's test file, and `L14-hd-find.grc`, to check your meter against after Question 3.
- nrsc5, for the optional Question 6, is at <a href="https://github.com/theori-io/nrsc5" target="_blank" rel="noopener">github.com/theori-io/nrsc5</a>.
::::

::::{frame} Looking Ahead
:::{present}
- Lesson 15 recovers the carrier phase and symbol timing of mPSK.
- Lesson 20 returns to OFDM, with QAM on each subcarrier.
:::

Keep your meter. Lesson 15 builds the carrier and timing recovery that nrsc5 performs on every HD Radio subcarrier, for a single mPSK carrier. Lesson 20 returns to OFDM, with QAM in place of QPSK on each subcarrier.
::::
