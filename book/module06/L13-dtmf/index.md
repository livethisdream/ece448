---
frame_view: true
---

# L13 - DTMF

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">DTMF</h1>

<div class="title-rule"></div>

A phone number as pairs of tones: generate them, capture them, and decode them in GNU Radio with a bank of Goertzel bins.

Lesson 13 · Module 6: Waveform Applications & RF Reverse Engineering · Dr. Neil Rogers
::::

::::{frame} Slides
:class: read-only

:::{admonition} Slides
:class: slides
<a href="../../slides/L13-dtmf.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L13-dtmf.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L13-dtmf.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '6'; counter-reset: lo 1">
  <li>I can decode DTMF tones from a captured audio signal.</li>
</ol>
::::

::::{frame} A Phone Number in Sound
:::{present}
<img src="../../viz/img/L13-rx-capture.png"
     alt="The L13 receiver flowgraph running on the synthetic capture L13-capture.wav, labeled Simulated capture in its corner: the Digits label reads 7195550148; two time sinks show the Goertzel bin outputs over 3 s, row bins on the left and column bins on the right, with one row peak near 0.15 and one column peak near 0.12 for each of the ten digits in each of two dialings; a spectrum plot below shows the current digit's two tones"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Each key sends two tones at once: one row tone and one column tone.
- The receiver measures eight frequencies and reads the digits.
:::

The figure is today's receiver, `L13-dtmf-rx.grc`, decoding a capture of the number 719-555-0148. The two plots in the middle are the receiver's eight detectors, four for the keypad's rows and four for its columns. Each digit raises exactly one row detector and one column detector for 50 ms, and the receiver turns that pair into a digit.

This is **dual-tone multi-frequency** signaling, DTMF, the sound a telephone keypad makes. It still carries phone menus, voicemail codes, and door-entry systems, and two-way radios send it over FM to key repeaters and trigger remote equipment. Lesson 12 decoded one tone switched on and off; DTMF carries a digit in the frequencies of two tones. The capture is synthetic: `L13-dtmf-capture.grc` dialed it and added noise, as a later frame shows.
::::

::::{frame} The Keypad Grid
:::{present}
<img src="../../viz/img/L13-keypad.svg"
     alt="The 4 by 4 DTMF keypad: rows at 697, 770, 852, and 941 Hz, columns at 1209, 1336, 1477, and 1633 Hz; the keys 1 2 3 A, 4 5 6 B, 7 8 9 C, and star 0 pound D; the fourth column, A to D, is drawn dashed"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Four row tones, 697 to 941 Hz, and four column tones, 1209 to 1633 Hz.
- Each key is one row tone plus one column tone.
:::

A key sends the tone of its row and the tone of its column together. The '5' key, for example, sends 770 Hz and 1336 Hz. Eight frequencies give 16 keys. Telephones use the first three columns; the military's AUTOVON network used the fourth column, A to D, to set call precedence, and radio systems still use it for control codes.

The frequencies are not round numbers on purpose. Each tone is about 10.5% above the one before it in its group, so the four tones in each group are spread evenly on a log scale, and no row tone's second harmonic lands on a column tone. The closest pair is 697 and 770 Hz, 73 Hz apart, and that spacing sets how sharp the receiver's filters must be.
::::

::::{frame} One Key in GNU Radio
:::{present}
<img src="../../viz/img/L13-grc-keypad.png"
     alt="The L13 keypad flowgraph in GNU Radio Companion: a QT GUI Chooser for the key and a QT GUI Push Button for Press; variables row_f and col_f pick the two frequencies; two float Signal Sources at 8 kHz add, a Multiply Const by press gates the sum, a Rational Resampler up by 6 feeds an Audio Sink at 48 kHz, and a frequency sink and a time sink show the gated signal"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Two Signal Sources, an Add, and a gate make one key.
- `row_f` and `col_f` look up the key's two frequencies.
:::

`L13-dtmf-keypad.grc` builds one key from stock blocks. The Chooser sets `key` from 0 to 15, and two variables look up its frequencies: `row_f` is `[697, 770, 852, 941][key // 4]` and `col_f` is `[1209, 1336, 1477, 1633][key % 4]`. Two float Signal Sources make the tones at amplitude 0.3 each, an Add sums them, and a Multiply Const by `press` passes the sum only while you hold the Press button.

Everything runs at 8 kHz, the telephone sample rate. Laptop sound cards do not all accept 8 kHz, so a Rational Resampler raises the rate by 6 to 48 kHz for the Audio Sink.
::::

::::{frame} Two Tones, One Key
:::{present}
<img src="../../viz/img/L13-keypad-run.png"
     alt="The L13 keypad flowgraph running with key 5 pressed: the waveform plot shows 20 ms of a beating two-tone signal between about plus and minus 0.6, the sum of the two 0.3 amplitudes, and the spectrum shows two lines, at 770 Hz and 1336 Hz"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Key '5' puts lines at 770 and 1336 Hz.
- In time, the two tones beat; in frequency, they separate.
:::

With '5' held, the spectrum shows two lines, one in each group. The waveform is hard to read: the two tones add, and the sum rises and falls as they move in and out of phase. In frequency the digit is obvious, so a DTMF receiver works in frequency, and its question for each moment is which row tone and which column tone are present.
::::

::::{frame} The Rules a Receiver Must Meet
:::{present}
| Rule | Accept | Reject |
| :-- | :-- | :-- |
| Tone length | 40 ms or longer | shorter than 23 ms |
| Gap between digits | 40 ms or longer | |
| Frequency error | within ±1.5% | beyond ±3.5% |
| Twist (column minus row) | −8 to +4 dB | |
:::

Telephone standards (ITU-T Q.24 and the Bell System rules it draws on) tell a receiver what it must accept and what it must reject. An auto-dialer typically sends 50 ms of tone and 50 ms of silence, 10 digits a second; the receiver must still catch tones as short as 40 ms and must ignore anything shorter than 23 ms, which is how it avoids taking a burst of speech for a digit. The tones may arrive up to 1.5% off frequency.

**Twist** is the level of the column tone minus the level of the row tone, in dB. A telephone line loses more at high frequencies, so the column tone often arrives weaker, and receivers accept it up to 8 dB below the row tone and up to 4 dB above it. Limits differ a little between countries; these are the common ones.
::::

::::{frame} The Capture
:::{present}
<img src="../../viz/img/L13-capture.svg"
     alt="Spectrogram of L13-capture.wav from 0 to 1.05 s and 500 to 1800 Hz: ten pairs of dark marks, one row tone and one column tone each 50 ms long and 100 ms apart, labeled 7 1 9 5 5 5 0 1 4 8 above, on a lightly speckled noise background; the corner reads Simulated capture"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- `L13-dtmf-capture.grc` dials a number and writes a WAV file.
- Our capture uses 50 ms tones and gaps, −2 dB twist, and 20 dB SNR.
:::

A phone recording would be ideal, but we made the capture instead, so every setting is known. `L13-dtmf-capture.grc` uses an Embedded Python Block, the **DTMF Dialer**, which sends a string of digits with a chosen tone length, gap, and twist. A Noise Source adds Gaussian noise, a Head block stops after one dialing and a 500 ms pause, and a Wav File Sink writes `L13-capture.wav`: 1.5 s at 8 kHz, 16 bits.

The spectrogram shows the result. Each digit is two short marks, one in the row band and one in the column band, and reading the grid by eye already gives 7195550148. The three 5s are three separate digits because a 50 ms gap separates them. The **SNR** setting is the tone power divided by the noise power across the whole 0 to 4 kHz band, during a tone.
::::

::::{frame} Separating Neighboring Tones
:::{present}
- A detector for each tone is a band-pass filter, then an energy measurement.
- Each filter must reject a neighbor 73 Hz away.
- A filter that narrow needs tens of milliseconds of signal.
:::

The direct way to decode DTMF is a bank of eight band-pass filters, one per tone, each followed by an energy detector: square the output and average it. The digit is the strongest row filter and the strongest column filter. The design problem is the filter width. The 697 Hz filter must pass 697 Hz, plus the 1.5% error, and reject 770 Hz, only 73 Hz away.

A filter's bandwidth and the time it needs are tied together: to separate two tones $\Delta f$ apart, a filter must watch the signal for roughly $1/\Delta f$ or longer, about 14 ms for 73 Hz. A 40 ms tone allows a block of about 25 ms, which leaves a margin for the tone's start and end, and practical receivers use that length.
::::

::::{frame} The Goertzel Bin
:::{present}
$$k = \frac{f N}{f_s}, \qquad c = 2\cos\left(\frac{2\pi k}{N}\right)$$

$$q_n = c\,q_{n-1} - q_{n-2} + x_n$$

- One bin measures one tone's energy over a block of $N$ samples.
- With $N = 205$ at 8 kHz, a block lasts 25.6 ms and bins sit 39.0 Hz apart.
:::

The **Goertzel algorithm** builds exactly that filter. It computes one bin of a DFT of an $N$-sample block, at bin number $k$, with the recursion above: one multiply and two adds per sample. After the last sample, the bin's power is

$$\begin{aligned}
|X(k)|^2 = {}& q_{N-1}^2 + q_{N-2}^2 \\
&- c\,q_{N-1}\,q_{N-2}.
\end{aligned}$$

Eight bins need far fewer operations than an FFT of the whole band. The classic choice is $N = 205$ at $f_s = 8$ kHz, which puts the bins for 697 Hz and 1209 Hz at

$$\begin{aligned}
k_{697} &= \frac{697 \times 205}{8000} = 17.86, \\
k_{1209} &= \frac{1209 \times 205}{8000} = 30.98.
\end{aligned}$$

The bins of a 205-sample DFT sit $f_s/N = 39.0$ Hz apart, and the block lasts $N/f_s = 25.6$ ms.
::::

::::{frame} Bins Against Tone Spacing
:::{present}
<img src="../../viz/img/L13-goertzel.svg"
     alt="Response of the four row bins of a 205-sample Goertzel decoder at 8 kHz, in dB, from 620 to 1010 Hz: each bin peaks at 0 dB at its tone, falls to nulls 39 Hz either side, so its main lobe is 78 Hz wide, and has sidelobes below minus 13 dB; dashed lines at 697, 770, 852, and 941 Hz show each neighbor tone falling at least 19 dB down the other bins' responses; the 73 Hz spacing of 697 and 770 is marked"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Each bin is a band-pass filter with nulls 39 Hz either side.
- A neighbor tone lands at least 19 dB down.
:::

Each Goertzel bin is a band-pass filter read once per block. Its response falls to its first nulls $f_s/N = 39$ Hz either side of the tone, so the main lobe is 78 Hz wide, about as wide as the 73 Hz spacing. A neighboring row tone falls on the far side of a bin's first null, 19 to 26 dB below the bin's own tone, so the correct bin always measures the higher power.

A longer block narrows the bins but needs a longer tone. A shorter block responds faster, so it accepts shorter bursts, and its wider bins accept tones farther off frequency. The L13 Lab measures both. The classic integer-bin decoder also rounds $k$ to the nearest whole number, which moves the 697 Hz bin to 702.4 Hz; our decoder uses $k$ unrounded, and a later frame shows why.
::::

::::{frame} The Receiver in GNU Radio
:::{present}
<img src="../../viz/img/L13-grc-rx.png"
     alt="The L13 receiver flowgraph in GNU Radio Companion: a Wav File Source and a Throttle at 8 kHz feed eight stock Goertzel blocks of length N = 205 at the eight DTMF frequencies, each followed by Complex to Mag into one of two four-input QT GUI Time Sinks; the Throttle also feeds a QT GUI Frequency Sink and the DTMF Decoder Embedded Python Block, whose digits and stats functions two Function Probes read for two QT GUI Labels"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Eight stock **Goertzel** blocks show the bins.
- The **DTMF Decoder** block makes the decisions.
:::

`L13-dtmf-rx.grc` reads a WAV file at 8 kHz. Eight stock **Goertzel** blocks, one per tone with length 205, each output one complex value per block, the bin divided by $N$; a **Complex to Mag** turns it into half the tone's amplitude, which is why the row bins in the opening figure peak at 0.15 for a 0.3 tone.

The **DTMF Decoder** is an Embedded Python Block that runs the same eight Goertzel bins itself, on a block of 205 samples every 102 samples, so the blocks overlap by half. It applies the decision rules on the next frame and reports each number it hears to the Digits and Numbers labels.
::::

::::{frame} The Decision Rules
:::{present}
1. The best row and column bins hold 35% of the block's energy.
2. Each beats its group's other bins by 6 dB.
3. Twist is within −10 to +6 dB.
4. Three blocks in a row agree.
:::

For each block, the decoder scales each bin's power so that a lone tone gives 1, and picks the strongest row bin and strongest column bin. Test 1 rejects noise and speech, where the energy is spread out. Test 2 rejects a signal with two tones in one group. Test 3 applies the twist limits, set 2 dB outside the standard's −8 and +4 dB, because block-to-block variation in the measured powers is about a decibel.

A digit counts once three overlapping blocks in a row agree on it. The blocks start 102 samples apart, so the tone must last longer than about one 25.6 ms block, which rejects bursts shorter than the standard's 23 ms. The same digit counts again only after a block that does not show it, which is how 555 reads as three digits. A pause of 200 ms ends the number.
::::

::::{frame} DTMF Explorer
:class: viz-frame

:::{depth}
The left panel shows the response of all eight Goertzel bins for the block length N, main lobes bold, with the two tones sent marked in amber. The right panel shows the share of one noisy block's energy in each bin, with the decoder's choice in navy, or red when a test fails. Press keys, then lower the SNR until "too little energy" appears. Move the frequency error until a tone leaves its bin's main lobe. Lower N until the main lobes overlap and "no clear winner" appears, and raise the twist past +6 dB. The explorer tests one block; the flowgraph also needs three blocks in a row to agree.
:::

:::{present}
<iframe src="../../viz/dtmf-explorer.html"
        width="100%" height="444"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="DTMF explorer: the eight Goertzel bin responses for a chosen block length, and the share of one noisy block's energy in each bin, with the decoder's decision, as the key, SNR, twist, and frequency error change">
</iframe>
:::
::::

::::{frame} Decoder Performance in Noise
:::{present}
<img src="../../viz/img/L13-link-noisy.png"
     alt="The L13 link flowgraph at an SNR of 1 dB, twist 0 dB, 50 ms tones and gaps, and no frequency error: the Numbers label reads 15 correct of 26 decoded in 40 s, and the spectrum shows noise across 0 to 4 kHz"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Every number arrives down to 2 dB SNR.
- At 1 dB, about 60% arrive; at 0 dB, almost none.
:::

`L13-dtmf-link.grc` puts the dialer, a noise source, and the decoder in one flowgraph, with sliders for the SNR, twist, tone and gap lengths, and frequency error, and it counts the numbers decoded correctly since a setting last changed. At 1 dB SNR the screenshot shows 15 of 26 correct.

The decoder tolerates low SNR because each bin is only 39 Hz wide, so it sees about a hundredth of the noise in the 4 kHz band, 20 dB less. The limit near 1 dB comes from test 1: at 0 dB half of each block's energy is noise, so the two tones cannot hold much more than half of it, and the blocks at a tone's start and end hold less, below 35%.
::::

::::{frame} Noise and Frequency-Error Sweeps
:class: read-only

We ran the dialer and decoder blocks headless with `L13-dtmf-sweep.py`, 40 dialings per setting, and counted the dialings decoded exactly. The noise sweep dials 719-555-0148 with 50 ms tones and gaps; the frequency-error sweep dials all 16 keys.

| SNR | 6 dB | 3 dB | 2 dB | 1 dB | 0 dB | −1 dB |
| :-- | :-: | :-: | :-: | :-: | :-: | :-: |
| Numbers correct | 40/40 | 40/40 | 40/40 | 25/40 | 5/40 | 0/40 |

| Frequency error | ±1.0% | ±1.5% | ±2.0% | ±2.5% | ±3.5% |
| :-- | :-: | :-: | :-: | :-: | :-: |
| $k$ unrounded | 40/40 | 40/40 | 0/40 | 0/40 | 0/40 |
| $k$ rounded | 40/40 | 0/40 | | | |

With $k$ unrounded, the decoder meets both frequency rules: it accepts every tone within ±1.5% and rejects every tone 2% or more off, which the standard permits, since it requires acceptance only within 1.5% and rejection at 3.5%. The two frequency sweeps use no noise. The noise sweep shows no false digits either; ten minutes of noise alone at three levels produced none.
::::

::::{frame} Frequency Error and Rounding k
:::{present}
<img src="../../viz/img/L13-link-roundk.png"
     alt="The L13 link flowgraph with Round k to an integer checked and a frequency error of 1.5% at an SNR of 20 dB: the Digits label shows only 71914, and the Numbers label reads 0 correct of 15 decoded in 25 s"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Rounded $k$ fails at 1.5% error; unrounded $k$ passes.
- Rounding moves some bins by up to 10 Hz.
:::

The link has a check box that rounds $k$ to an integer, as the classic decoder does. Rounding moves the 697 Hz bin to 702.4 Hz, 5.4 Hz high, and moves some other bins by as much as 10 Hz. A tone 1.5% off moves another 10 to 25 Hz, and when the two errors add, the tone sits halfway down its bin's main lobe. Its energy then fails test 1 or its twist fails test 3, and the screenshot shows 0 of 15 numbers correct.

The Goertzel recursion does not need an integer $k$; the power formula still gives the energy at exactly $f$. Using the tone's own frequency removes the rounding error and leaves the whole main lobe for the tone's real error.
::::

::::{frame} DTMF on a Real Radio
:::{present}
- DTMF also travels over FM two-way radio, to control repeaters and remote sites.
- An RTL-SDR, an FM receiver, and this decoder can read it.
- The L13 Lab decodes a phone keypad through the laptop's microphone.
:::

On the air, radios send DTMF over narrowband FM. Amateur repeaters accept DTMF commands, and many handheld radios have a DTMF keypad. To decode it from an SDR, tune an RTL-SDR to the channel, demodulate it with an FM receiver like Lesson 7's, with its channel filter narrowed to the 12.5 kHz channel, resample the audio to 8 kHz, and connect the audio to the DTMF Decoder block in place of the Wav File Source.

Nothing in this lesson transmits, and decoding is receive-only. In class we transmit only into a cable, into a shielded enclosure, or at very low power in an ISM band, and only when the lesson says to. The L13 Lab uses a real acoustic signal instead: `L13-dtmf-mic.grc` decodes a phone's keypad tones from the laptop's microphone. It is compiled only and not yet tested with a real microphone.
::::

::::{frame} Key Point
:::{present}
:class: callout
Each DTMF key is one row tone plus one column tone. Goertzel bins of 205 samples at 8 kHz separate tones 73 Hz apart, and a digit counts when one row bin and one column bin dominate for three blocks.
:::
::::

::::{frame} Downloads
:class: read-only doc-links

- <a class="doc-link" href="../../grc/L13-dtmf-keypad.grc" download>L13-dtmf-keypad.grc</a>: one DTMF key, played on the laptop's speaker and shown in time and frequency. No hardware needed.
- <a class="doc-link" href="../../grc/L13-dtmf-capture.grc" download>L13-dtmf-capture.grc</a>: dials a number, adds noise, writes `L13-capture.wav`, and stops. No hardware needed.
- <a class="doc-link" href="../../grc/L13-capture.wav" download>L13-capture.wav</a>: the synthetic capture of 719-555-0148, 1.5 s at 8 kHz.
- <a class="doc-link" href="../../grc/L13-dtmf-rx.grc" download>L13-dtmf-rx.grc</a>: the receiver, with the eight Goertzel bins and the DTMF Decoder. No hardware needed.
- <a class="doc-link" href="../../grc/L13-dtmf-link.grc" download>L13-dtmf-link.grc</a>: dialer, noisy channel, and decoder, with sliders. No hardware needed.
- <a class="doc-link" href="../../grc/L13-dtmf-sweep.py" download>L13-dtmf-sweep.py</a>: the noise and frequency-error sweeps on this page, run headless. Put it beside `L13-dtmf-link.grc`.

Put the files in one folder; the receiver opens the WAV file by name from that folder. Open a `.grc` file from GRC's File menu, or run `gnuradio-companion L13-dtmf-rx.grc` from the radioconda prompt. The DTMF Dialer and DTMF Decoder are Embedded Python Blocks, saved inside the `.grc` files.
::::

::::{frame} Summary
:class: read-only

| Idea | What it is | Number to remember |
| :-- | :-- | :-- |
| DTMF key | one row tone plus one column tone | rows 697-941 Hz, columns 1209-1633 Hz |
| Tone spacing | about 10.5% between neighbors | closest pair 73 Hz apart |
| Timing | accept 40 ms tones and gaps | reject tones under 23 ms |
| Frequency error | accept ±1.5% | reject beyond ±3.5% |
| Twist | column level minus row level | accept −8 to +4 dB |
| Goertzel bin | one DFT bin, $k = fN/f_s$ | $N = 205$: 25.6 ms, bins 39.0 Hz apart |
| Decoder | share, 6 dB winner, twist, three blocks | every number to 2 dB SNR |
| Rounded $k$ | the classic integer bin | fails at 1.5% error |
::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE448_L13_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE448_L13_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Looking Ahead
:::{present}
- The L13 Lab builds the keypad, decodes a capture, finds the decoder's limits, and decodes a real phone.
- Lesson 14 receives HD Radio, a digital signal beside an FM station.
:::

The L13 Lab is the hands-on version of this lesson. You build the keypad from an empty canvas, decode a second capture whose number you do not know, measure the decoder's twist and timing limits and how they change with the block length, and decode the keypad tones of a real phone through the laptop's microphone.

Lesson 14 moves from audio back to RF with HD Radio, the digital broadcast that sits on either side of many FM stations.
::::
