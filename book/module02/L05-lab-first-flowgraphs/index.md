---
frame_view: true
---

# L5 Lab — First Flowgraphs

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">First Flowgraphs</h1>

<div class="title-rule"></div>

Build a flowgraph from an empty canvas, measure aliasing, then find an FM station in GQRX and record the band in GNU Radio.

L5 Lab · Module 2: SDR & GNU Radio Foundations · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '2'; counter-reset: lo 2">
  <li>I can install GNU Radio and use GNU Radio Companion (GRC) to build, inspect, and run a basic flowgraph.</li>
  <li>I can capture a real RF signal using an SDR and interpret its time- and frequency-domain representations.</li>
</ol>
::::

::::{frame} From Lesson to Bench
:::{present}
- **Pre-Lab:** install radioconda and work out the numbers your settings fix.
- **Bench:** build the tone flowgraph yourself, find an FM station in GQRX, then receive and record the band in GNU Radio.
- **Writeup:** compare, and explain the differences.
:::

Lesson 5 showed both flowgraphs running. Today you build one from an empty canvas and run the other against real signals. The lab packet has three parts, and you turn it in once, complete, before Lesson 6. **Part 1, the Pre-Lab**, is on your own before the period: install radioconda, confirm it sees your RTL-SDR, and work out where the tones will appear, the band the display shows, and the file size. **Part 2** is your own measurements and observations in class. **Part 3, the Writeup**, explains what you saw.

Nothing in this lab transmits. The RTL-SDR is receive-only, and the tone flowgraph never leaves your laptop.
::::

::::{frame} Part 1: Before the Period
:::{present}
- `gnuradio-config-info --version` reports 3.10.
- `rtl_test` finds your RTL-SDR and names its tuner.
- `L05-tone.grc` runs and shows one spike at $+1$ kHz.
:::

Do the Pre-Lab before you arrive; the bench time assumes a working install. The three checks on the slide are the packet's Question 1. If any fails, the L5 lesson page lists the fixes, and the most common one on Windows is the Zadig driver step for the RTL-SDR. Bring the problem to EI before the lab rather than to the lab itself.

Question 2 is quick arithmetic from your block settings: where five tones appear at a 32 kHz sample rate, the band the FM display shows, and the size of a 2 s recording. Part 2 checks each one on the screen.
::::

::::{frame} Expected Numbers
:::{present}
| Check | Expected |
| :-- | :-- |
| 20 kHz tone at 32 kHz | appears at $-12$ kHz |
| FM display at 100.1 MHz | 98.9 to 101.3 MHz |
| 2 s recording | 38.4 MB |
:::

These are the answers to Question 2, worked from Lesson 5. The tone aliases are exact, because a computed tone has no noise or hardware in the way; if a measurement disagrees, the flowgraph is built differently from the instructions, most often with a different `samp_rate`. The FM numbers depend only on the center frequency and sample rate you set. Station levels, the noise floor, and the gain where overload starts depend on your antenna and location, so the packet has you watch and record them instead.
::::

::::{frame} Part 2: Build the Tone Flowgraph
:class: read-only

1. Start GRC and choose File, New, QT GUI. Do not open `L05-tone.grc`; build it yourself.
2. Set the `samp_rate` variable to 32000.
3. Add a **QT GUI Range** with ID `freq`, from $-48000$ to $48000$ in steps of 250, default 1000.
4. Add a **Signal Source**: type complex, sample rate `samp_rate`, waveform cosine, frequency `freq`.
5. Add a **Throttle** (complex, `samp_rate`), a **QT GUI Time Sink** (complex), and a **QT GUI Frequency Sink** (complex, bandwidth `samp_rate`).
6. Connect source to throttle and throttle to both sinks. Every arrow must be black; a red arrow is a type mismatch.
7. Run it. Screenshot the canvas for Question 3(a).
8. Set the slider to 1, 12, 20, 30, and $-25$ kHz in turn and record where the spike appears for Question 3(b).
::::

::::{frame} Part 2: The FM Band
:class: read-only

1. Connect the antenna to the RTL-SDR and plug it in. Run `gqrx`, choose the RTL-SDR, set the mode to WFM (stereo), and press the power button. GQRX comes with radioconda; if GQRX does not start on your laptop, SDR++ has the same controls.
2. Click across the FM band until you hear a station clearly. Record its frequency for Question 4(a), then quit GQRX; only one program can open the RTL-SDR at a time.
3. Open `L05-fm-spectrum.grc`, set the center frequency to the station you found, and run it. Drag the center frequency across 88 to 108 MHz. Record the three strongest stations' frequencies, peak levels, and widths for Question 4(b).
4. Center a station exactly on the spike in the middle of the display, then tune 300 kHz away. Note what moves for Question 4(c).
5. With the strongest station on screen, set the gain to 0, 20, 30, 40, and 49 dB. At each, record the noise floor away from any station, and whether new signals appear between stations, for Question 4(d).
::::

::::{frame} Part 2: Record and Plot
:class: read-only

1. Stop the flowgraph. Right-click the gray File Sink and choose Enable. Set its file name to `fm_capture.cfile` in a folder you can find.
2. Center the strongest station slightly off the DC spike and set the highest gain in your 4(d) table at which no spurs appeared.
3. Run the flowgraph for about 2 s and stop it. Record the file size for Question 5(a).
4. Disable the File Sink again so the next run does not overwrite the capture.
5. From the radioconda prompt, run `python L05-psd.py fm_capture.cfile --fs 2.4e6 --fc` followed by your center frequency in hertz. Paste the plot for Question 5(b).
::::

::::{frame} No Hardware?
:class: read-only

:::{admonition} If your RTL-SDR is missing or will not open
:class: tip
Do Question 3 on your laptop as written; it needs no hardware. For Questions 4 and 5, pair with a classmate whose RTL-SDR works, take turns at their laptop, and record your own numbers and your own capture. Say in the packet whose hardware you used. Bring the failed dongle to EI so it is working before the L6 Lab.
:::
::::

::::{frame} Part 3: After the Lab
:::{present}
- Explain why 20 kHz and $-12$ kHz give identical samples at 32 kHz.
- Describe, in words, what raising the gain did to the floor and the stations.
- Choose and justify a gain for weak stations.
:::

The Writeup is three questions. The first connects your alias table to the sampling wheel of Lesson 5: adding $f_s$ to a tone's frequency adds a whole turn to every sample. The second asks what you watched happen as the gain went up: when the floor moved, when the stations stood out more, and when false signals appeared. The third asks you to defend a gain setting from your own gain table.
::::

::::{frame} Lab Packet
:class: read-only doc-links

- <a class="doc-link" href="../../labs/ECE448_Lab_L05_FirstFlowgraphs_blank.pdf" target="_blank" rel="noopener">L5 Lab packet (PDF)</a>
- <a class="doc-link" href="../../grc/L05-tone.grc" download>L05-tone.grc</a>, <a class="doc-link" href="../../grc/L05-fm-spectrum.grc" download>L05-fm-spectrum.grc</a>, and <a class="doc-link" href="../../grc/L05-psd.py" download>L05-psd.py</a>
::::

::::{frame} Looking Ahead
:::{present}
- Lesson 6 adds the first processing blocks: AM modulation and demodulation.
- Lesson 7 turns today's FM capture into audio and decodes its RDS data.
:::

Keep your `fm_capture.cfile` and the center frequency you recorded it at. Lesson 7 builds an FM receiver, and the first test of that receiver is the capture you made today, played back through a File Source before you point it at the live band.
::::
