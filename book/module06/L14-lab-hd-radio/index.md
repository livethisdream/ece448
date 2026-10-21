---
frame_view: true
---

# L14 Lab — HD Radio

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">HD Radio</h1>

<div class="title-rule"></div>

Build a sideband power meter, identify a station's configuration from a capture, measure a live station, and decode it with nrsc5.

L14 Lab · Module 6: Waveform Applications & RF Reverse Engineering · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '6'; counter-reset: lo 2">
  <li>I can describe how HD Radio works and demodulate an HD Radio signal.</li>
</ol>
::::

::::{frame} From Lesson to Bench
:::{present}
- **Pre-Lab:** run the sideband finder and work out two block settings.
- **Bench:** build a sideband meter, identify a capture's configuration, measure a live station, and decode it.
- **Writeup:** explain what you saw and what it tells you about each station.
:::

Lesson 14 found the HD Radio sidebands in a simulated test file and measured them with `L14-hd-find.grc`. Today you build the sideband meter yourself from an empty canvas, use it on a second capture whose configuration you do not know, and then point it at a live station with the RTL-SDR. Last, you decode a live station with nrsc5. The lab packet has three parts, and you turn it in once, complete, before Lesson 15. You do **Part 1, the Pre-Lab**, on your own before the period, record **Part 2**'s measurements in class, and explain them in **Part 3, the Writeup**.

Nothing in this lab transmits. The RTL-SDR receives only, and both captures came from GNU Radio flowgraphs, not from an antenna.
::::

::::{frame} Part 1: Before the Period
:::{present}
- Run `L14-hd-test-tx.grc` once, then `L14-hd-find.grc`.
- Find the meter's `inner` setting for extended hybrid stations.
- Find the FFT size that makes each bin one subcarrier at nrsc5's float rate.
:::

Do the Pre-Lab before you arrive. Put both flowgraphs from the Lesson 14 page in one folder, run `L14-hd-test-tx.grc` once to write `L14-hd-test.cu8`, and then run `L14-hd-find.grc`. Question 1 checks that the meters read what the lesson showed; if GRC reports an error, the L5 lesson page lists the install checks.

Question 2 asks for two block settings: the value of the meter's `inner` Variable for a station that adds one, two, or four partitions, and the frequency sink's FFT size that puts one subcarrier in each bin for a complex float file at 744,187.5 samples per second, a rate nrsc5 reads. Part 2 uses the first one.
::::

::::{frame} Expected Numbers
:::{present}
| Check | Expected |
| :-- | :-- |
| `L14-hd-test.cu8`, both meters | −23.0 dBc, within 0.1 dB |
| Hybrid sideband edges | subcarriers 356 and 546 |
| Partition | 19 subcarriers |
| A sideband on the display | at least 10 dB above the floor |
:::

Your meter should read the lesson's test file within 0.1 dB of the finder's −23.05 and −23.04 dBc; a larger difference means a filter setting or a center frequency is off. The lab capture comes from a different station, and you identify its configuration from its spectrum and its meter readings.
::::

::::{frame} Part 2: Build the Meter
:class: read-only

1. Start GRC and choose File, New, QT GUI. Do not open `L14-hd-find.grc`; build the meter yourself.
2. Set `samp_rate` to 1488375. Add Variables `df` = `1488375 / 4096`, `inner` = `356`, `outer` = `546`, `sb_center` = `(inner + outer) / 2 * df`, `sb_half` = `((outer - inner) / 2 + 0.5) * df`, `decim` = `6`, and `avg_len` = `int(0.2 * samp_rate / decim)`. Add a **QT GUI Entry** with ID `fc`, label Center (Hz), type real, and default value `100.3e6`, and a **QT GUI Range** with ID `rf_gain`, label RF gain (dB), from 0 to 49.6 in steps of 0.1, default 30.
3. Read the file: a **File Source** (type byte, file `'L14-hd-test.cu8'` with the quotes, repeat Yes), a **Throttle** (byte, `2 * samp_rate`), **UChar To Float**, **Add Const** (float, −127.5), **Multiply Const** (float, `1 / 128`), **Deinterleave** (float, 2 streams), and **Float To Complex**.
4. On the Float To Complex output, add a **QT GUI Frequency Sink**: complex, FFT size 4096, center frequency `fc`, bandwidth `samp_rate`, average Medium, Y axis from −110 to −10.
5. Add two **Low-pass Filter Taps** variables at `samp_rate`: `host_taps` with cutoff `100e3` and transition `10e3`, and `sb_taps` with cutoff `sb_half` and transition `2e3`.
6. Add three **Frequency Xlating FFT Filters**, each with decimation `decim` and sample rate `samp_rate`: the host with taps `host_taps` and center 0, the upper sideband with `sb_taps` and center `sb_center`, and the lower sideband with `sb_taps` and center `-sb_center`. Connect Float To Complex to all three.
7. After each filter add **Complex to Mag^2**, a **Moving Average** (float, length `avg_len`, scale `1 / avg_len`), **Keep 1 in N** (float, N `avg_len // 10`), and **Log10** (n = 10).
8. Add two **Subtract** blocks (float): upper minus host, and lower minus host. Connect them to a **QT GUI Number Sink** with 2 inputs, minimum −40, maximum 0, and labels Upper and Lower in dBc. Every arrow must be black.
9. Run it, wait 5 s, and record both readings and a screenshot for Question 3.
::::

::::{frame} Part 2: The Lab Capture
:class: read-only

1. Stop your meter and change the File Source's file to `'L14-lab-capture.cu8'`. The File Source reads the file only when the flowgraph starts.
2. Change the frequency sink's FFT size to 8192 and run it. Drag a box around one edge of a sideband on the frequency sink to zoom in, read the edge's frequency in MHz, and right-click to zoom back out. Do the same for the inner and outer edge of each sideband, and convert each edge to a subcarrier number for Question 4(a).
3. Record both meter readings with `inner` at 356 for Question 4(b).
4. Stop it, change `inner` to the subcarrier number you found for the inner edge, run it again, and record both readings.
5. Find the other station in the capture, give its offset from the center, and say whether it carries HD Radio, for Question 4(d).
::::

::::{frame} Part 2: A Live Station
:class: read-only

<img src="../../viz/img/L14-hd-find.png"
     alt="The L14 sideband finder on the lesson's test file, labeled Simulated: L14 test file, for comparison: meters at minus 23.05 and minus 23.04 dBc, two flat shelves beside the host on the spectrum, and two straight bands on the waterfall"
     style="max-width: 640px; width: 100%; display: block; margin: 0 auto 12px;">

The figure shows the lesson's simulated test file; a live station's host is rougher, and its shelves may stand closer to the floor. We have compiled this step but not yet tested it on a live station, so expect to adjust the gain.

1. Add a **Soapy RTLSDR Source** to your meter: sample rate `samp_rate`, center frequency `fc`, gain `rf_gain`. Connect it to the frequency sink and the three filters. Then select the File Source and the six blocks after it, through Float To Complex, and press D to disable all seven; GRC will not run with both sources connected.
2. Plug in the RTL-SDR and antenna. If you have SDR Flex or GQRX, find a station with two flat shelves there first, and close it before you run your meter, because only one program can hold the RTL-SDR; otherwise run your meter and type each strong station's frequency in hertz into Center in turn, and stop at one with two flat shelves beside it.
3. Raise the gain until the shelves stand at least 10 dB above the floor, but lower it if the floor rises everywhere or copies of other stations appear.
4. Record the station, its sideband edges, and both meter readings, with a screenshot, for Question 5. If its inner edge is inside 129.4 kHz, set `inner` to match before you read the meters.
5. Lower the RF gain slider in steps and watch the shelves and the readings as the floor rises toward them, for Question 5(c).
::::

::::{frame} Part 2: Decoding with nrsc5
:class: read-only

nrsc5 is not part of radioconda. Use a laptop that has nrsc5 installed, your own or one your instructor provides, with your RTL-SDR. The RTL-SDR can serve only one program at a time, so stop GRC first. These steps follow the nrsc5 project's documentation; we have not yet tested them in this course.

1. Tune and play the station you measured, with the gain you used in GRC: `nrsc5 -g 30 100.3 0`, with your station's frequency in place of 100.3. It takes a few seconds to synchronize.
2. Record the station name, the song title and artist, and any HD2 or HD3 program it reports, for Question 6(a). Try program 1 for HD2.
3. Lower the gain until the audio drops out, and record the gain at which it stops, for Question 6(b).
4. Record 10 s with `nrsc5 -g 30 -w hd.cu8 <station> 0`, with the same gain as step 1, open `hd.cu8` in your meter with the center frequency set to the station, and record both meter readings for Question 6(c).
::::

::::{frame} No Shelves?
:class: read-only

:::{admonition} If the meters read below −40 dBc or the shelves never appear
:class: tip
For a file, check that the file name in the File Source is in quotes, that the file sits in the same folder as the flowgraph, and that the File Source's type is byte, not complex. If the shelves appear but a meter reads wrong, check the sign of each filter's center frequency and that both Subtract blocks take the host on their second input. For a live station, check that the RTL-SDR Source's sample rate is `samp_rate`, that you have centered on the station, and that the station carries HD Radio at all; many do not. Shelves of unequal height can mean the station runs one sideband weaker than the other; a missing shelf usually means a weak signal or a neighbor covering it.
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
- nrsc5 is at <a href="https://github.com/theori-io/nrsc5" target="_blank" rel="noopener">github.com/theori-io/nrsc5</a>.
::::

::::{frame} Looking Ahead
:::{present}
- Lesson 15 recovers the carrier phase and symbol timing of mPSK.
- Lesson 20 returns to OFDM, with QAM on each subcarrier.
:::

Keep your meter. Lesson 15 builds the carrier and timing recovery that nrsc5 performed on every HD Radio subcarrier today, for a single mPSK carrier. Lesson 20 returns to OFDM, with QAM in place of QPSK on each subcarrier.
::::
