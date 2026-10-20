---
frame_view: true
---

# L12 - CW

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">CW</h1>

<div class="title-rule"></div>

Morse code keyed onto a carrier, received through a product detector, and decoded back into text.

Lesson 12 · Module 6: Waveform Applications & RF Reverse Engineering · Dr. Neil Rogers
::::

::::{frame} Slides
:class: read-only

:::{admonition} Slides
:class: slides
<a href="../../slides/L12-cw.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L12-cw.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L12-cw.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '6'">
  <li>I can transmit and receive CW (Morse) using GNU Radio and decode a received CW stream.</li>
</ol>
::::

::::{frame} Morse Code on an SDR
:::{present}
<img src="../../viz/img/L12-link-clean.png"
     alt="The L12 link flowgraph running at noise amplitude 1 with a 200 Hz CW filter and a threshold of 0.3: the waterfall shows the keyed carrier as a broken vertical line at plus 5 kHz, the envelope sits near 0.64 during each mark and near 0.04 between them with the red key trace on top of it, and the Received label reads USAFA ECE 448 three times"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- A carrier switched on and off sends Morse code.
- Today we key it, receive it, and decode it in one flowgraph.
:::

The figure is today's flowgraph, `L12-cw-link.grc`, running. A keyer turns the line `USAFA ECE 448` into Morse code and switches a carrier on and off with it. The carrier sits 5 kHz above the center of a 32 kHz band, and on the waterfall at the left it appears as a broken vertical line: each dash of color is one key-down. The receiver tunes to that carrier, recovers its on-off **envelope**, the blue trace, and decides from it when the key was down, the red trace. A decoder then turns those marks and spaces back into letters, shown in the Received label.

Lesson 11 showed how to write a custom block. The keyer and the decoder in this flowgraph are two Embedded Python Blocks, and everything between them is standard GNU Radio.
::::

::::{frame} CW and On-Off Keying
:::{present}
- **CW** keys a carrier on for a mark and off for a space.
- It is Lesson 6's AM with a message of 0 and 1.
- Its signal is narrow, so it reaches far on little power.
:::

**CW**, for continuous wave, is the oldest radio modulation still in use. The transmitter keys a carrier on and off: on for a **mark**, a dot or a dash, and off for a **space**. In the terms of Lesson 6, it is AM whose message is 0 or 1, so the receiver only has to recover the envelope and decide whether the carrier is there.

Lesson 2 showed that a narrower bandwidth lowers the noise floor, and CW is one of the narrowest signals in use, about 100 Hz wide at ordinary speeds, so a CW receiver can use a narrow filter and copy a weak signal. Amateur operators still use it: most U.S. amateur HF bands set aside their lowest segments, such as 7.000 to 7.125 MHz in the 40 m band, for CW and data, with no voice. Aircraft navigation beacons such as VORs and NDBs still identify themselves with a two- or three-letter Morse code identifier, and pilots check it before they use the beacon.
::::

::::{frame} Morse Timing
:::{present}
<img src="../../viz/img/L12-paris-timing.svg"
     alt="The word PARIS keyed on a grid of Morse units: marks of 1 unit for each dit and 3 units for each dah, gaps of 1 unit inside a letter, 3 units between letters, and 7 units after the word, 50 units in all"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- A dah lasts three dits.
- Gaps: 1 unit in a letter, 3 between letters, 7 between words.
:::

Morse code measures everything in one time **unit**, the length of a dit. A dah lasts 3 units. The key stays up for 1 unit between the marks of one letter, for 3 units between letters, and for 7 units between words. The receiver needs nothing else: it can tell a dit from a dah and a letter gap from a word gap by comparing lengths, without knowing any absolute time.

The figure keys the word PARIS on that grid. Its 14 marks and the gaps between them, including the 7-unit gap that ends the word, add up to exactly 50 units. Operators use PARIS as the standard word for measuring speed, which the next frame turns into a formula.
::::

::::{frame} Words per Minute
:class: read-only

A speed of one **word per minute** (WPM) sends PARIS, 50 units, once a minute, so one unit lasts $60/50 = 1.2$ s. At $W$ words per minute the unit, the length of one dit, is

$$t_\text{dit} = \frac{1.2\text{ s}}{W}.$$

At 20 WPM a dit lasts 60 ms, a dah 180 ms, and PARIS 3.0 s, which is 20 words in a minute.

| Speed | Dit | Dah | Gap between words | `USAFA ECE 448`, 126 units |
| :-: | :-: | :-: | :-: | :-: |
| 5 WPM | 240 ms | 720 ms | 1.68 s | 30.2 s |
| 10 WPM | 120 ms | 360 ms | 0.84 s | 15.1 s |
| 20 WPM | 60 ms | 180 ms | 0.42 s | 7.56 s |
| 30 WPM | 40 ms | 120 ms | 0.28 s | 5.04 s |
| 40 WPM | 30 ms | 90 ms | 0.21 s | 3.78 s |

Our line, `USAFA ECE 448`, is 126 units long with its final word gap, so the link sends it once every 7.56 s at 20 WPM. A word of real text is not exactly 50 units, since E is 1 unit long and 0 is 19, but PARIS is close to the average word of English text.
::::

::::{frame} The Keyer in GNU Radio
:::{present}
<img src="../../viz/img/L12-grc-tx.png"
     alt="The L12 keyer flowgraph in GNU Radio Companion: two Morse Keyer blocks with the message USAFA ECE 448 at 20 WPM, one with an edge time of 0 ms and one of 5 ms, each followed by a Throttle at 8 kHz, both feeding a QT GUI Time Sink and a QT GUI Frequency Sink with an FFT size of 8192"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The **Morse Keyer** turns text into 0s and 1s at the sample rate.
- One keyer is hard-keyed; the other shapes each edge over 5 ms.
:::

`L12-cw-tx.grc` compares two keyers. The **Morse Keyer** is an Embedded Python Block: it looks up each letter of `msg` in the Morse table, lays out the marks and gaps on the unit grid at the chosen WPM, and outputs one float per sample, 1 while the key is down and 0 while it is up. Multiplied by a carrier, that stream is the CW signal. Here we look at the stream itself, which is the carrier's envelope, at 8 kHz.

The top keyer switches between 0 and 1 in one sample, which is **hard keying**. The bottom one shapes each edge along a raised cosine over the **edge time**, 5 ms by default, and a slider changes it. A dit at 20 WPM lasts 60 ms, so a 5 ms edge changes its shape only slightly.
::::

::::{frame} Key Clicks
:::{present}
<img src="../../viz/img/L12-tx-clicks.png"
     alt="The L12 keyer running at 20 WPM: the time sink shows one key-down edge, the hard-keyed trace jumping from 0 to 1 at once and the shaped trace rising over 5 ms; the frequency sink shows the hard-keyed spectrum falling only to about minus 70 dB at plus and minus 4 kHz while the shaped spectrum falls below minus 120 dB beyond about 2 kHz from the carrier"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Hard keying spreads energy kilohertz away from the carrier.
- A 5 ms edge puts it 40 dB lower 1 kHz away.
:::

The time sink triggers on each key-down and shows 10 ms before it and 30 ms after. Both traces reach 1 within 5 ms and look almost the same in time, but their spectra differ. The hard-keyed spectrum, in blue, falls slowly on both sides of the carrier and is still above $-80$ dB at the edges of the plot, 4 kHz away. The shaped spectrum, in red, falls much faster and is below $-120$ dB beyond about 2 kHz from the carrier.

A receiver tuned to a frequency near a hard-keyed transmitter hears that spread as a click at every edge, and operators call it a **key click**. Shaping the edges removes the clicks without changing what the receiver decodes, so CW transmitters shape their keying, typically with edges of a few milliseconds.
::::

::::{frame} Bandwidth and Edge Time
:class: read-only

We measured the keyer's spectrum at the flowgraph's 8 kHz rate, over about 700 characters of random five-letter groups at 20 WPM. The **99% bandwidth** holds 99% of the signal's power, including the carrier. The last two columns compare the spectrum's level with hard keying at the same distance from the carrier.

| Edge time | 99% bandwidth | 99.9% bandwidth | 1 kHz away, vs hard | 2 kHz away, vs hard |
| :-: | :-: | :-: | :-: | :-: |
| 0 (hard) | 183 Hz | 1.7 kHz | 0 dB | 0 dB |
| 1 ms | 150 Hz | 676 Hz | $-10$ dB | $-25$ dB |
| 2 ms | 121 Hz | 450 Hz | $-24$ dB | $-37$ dB |
| 5 ms | 87 Hz | 247 Hz | $-40$ dB | $-53$ dB |
| 10 ms | 64 Hz | 150 Hz | $-52$ dB | $-65$ dB |

Each doubling of the edge time cuts the energy far from the carrier by roughly another 12 dB, and the 99.9% bandwidth shrinks from 1.7 kHz to 247 Hz with 5 ms edges. The edge time has a limit, though: it has to stay well under a dit, or the dits lose their flat tops and the receiver cannot tell them apart. At 40 WPM a dit lasts 30 ms, and 5 ms edges still leave 25 ms of it at full power.
::::

::::{frame} CW Keyer Explorer
:class: viz-frame

:::{depth}
The left panel shows the whole message as marks and spaces, and below it the first key-down edge enlarged, hard keying in gray and the shaped edge in blue. The right panel shows the spectrum within 1 kHz of the carrier. Start with PARIS at 20 WPM: the readouts give a 60 ms dit and a 3.00 s message. Drag the edge time from 5 ms to 0 and watch the blue spectrum rise until it overlaps the gray one, with the skirts rising 40 dB at 1 kHz. Then raise the speed: the dits get shorter, the spectrum widens, and the 99% bandwidth grows. It grows almost in proportion to the WPM with hard keying, and more slowly with a fixed 5 ms edge, which limits how far the energy spreads.
:::

:::{present}
<iframe src="../../viz/cw-keyer.html"
        width="100%" height="427"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="CW keyer explorer: a message keyed as Morse code at a chosen speed and edge time, its envelope, its first edge enlarged, and its spectrum compared with hard keying">
</iframe>
:::
::::

::::{frame} The Receiver
:::{present}
<img src="../../viz/img/L12-grc-link.png"
     alt="The L12 link flowgraph in GNU Radio Companion: the Morse Keyer, Throttle, Float To Complex, and a Multiply by a 5 kHz Signal Source make the CW signal, and an Add with a Noise Source is the channel; the receiver is a Frequency Xlating FIR Filter, a Multiply by a 700 Hz Signal Source, Complex To Real, a band-pass Decimating FIR Filter, Abs, a low-pass Decimating FIR Filter, Threshold, and the CW Decoder, with an audio branch, a waterfall sink, and a time sink"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Tune, then a **product detector** makes a 700 Hz tone.
- A narrow **CW filter**, Abs, and a low-pass recover the envelope.
- **Threshold** and the **CW Decoder** turn it into text.
:::

The top row of the flowgraph is the transmitter and the channel. The Morse Keyer's output becomes a complex carrier at 5 kHz, and a **Noise Source** adds complex Gaussian noise whose amplitude a slider sets. The receiver starts with a **Frequency Xlating FIR Filter**, as in Lesson 7: it moves the 5 kHz carrier to 0 Hz, keeps ±600 Hz around it, and decimates by 4 to 8 kHz.

The rest of the receiver works at audio rates. The product detector makes the carrier audible as a 700 Hz tone, and an **Audio Sink** plays it. A band-pass **CW filter** 200 Hz wide around 700 Hz removes most of the noise. **Abs** and a low-pass filter recover the envelope, as in Lesson 6, and decimate it to 1 kHz. A **Threshold** block turns the envelope into a key, 1 or 0, and the **CW Decoder** turns the key into letters.
::::

::::{frame} The Product Detector
:::{present}
- Multiply by a 700 Hz **BFO** and keep the real part.
- The carrier becomes a 700 Hz tone; a tuning error $\Delta f$ moves it to $700 + \Delta f$.
:::

After the Xlating filter the carrier sits at 0 Hz, which the ear cannot hear. The receiver multiplies it by a complex tone at 700 Hz, the **beat frequency oscillator** (BFO), which moves the carrier up to 700 Hz, and **Complex To Real** keeps the real part. That is the product detector of Lesson 6, used here with an offset so that the output is a tone instead of the envelope. The key-down periods become bursts of a 700 Hz tone, which is the sound most CW operators choose.

A tuning error moves the tone. If the receiver tunes 40 Hz below the carrier, the carrier lands at +40 Hz after the Xlating filter and the tone comes out at 740 Hz. The CW filter is centered on 700 Hz, so the tone has to stay inside it, and a narrower filter leaves less room for a tuning error. The Xlating filter's ±600 Hz passband also matters here, because it removes a signal 1.4 kHz below the carrier that would otherwise come out at the same 700 Hz.
::::

::::{frame} Envelope and Threshold
:::{present}
<img src="../../viz/img/L12-link-thr-low.png"
     alt="The L12 link at noise amplitude 6 with the threshold left at 0.3: the envelope rides near 0.26 between marks and crosses 0.3 often, the red key trace chatters between 0 and 1 during the spaces, and the Received label shows mostly wrong letters and # marks, patterns that are not in the Morse table"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The threshold belongs halfway between the space level and the mark level.
- Noise raises the space level, so the threshold has to rise with it.
:::

After the low-pass filter the envelope sits near 0.64 during a mark, $2/\pi$, the average of a rectified tone of amplitude 1, and near the noise level during a space. The **Threshold** block outputs 1 when the envelope rises above $1.2 \times$ `thr` and 0 when it falls below $0.8 \times$ `thr`. The gap between the two levels, called **hysteresis**, keeps a noisy envelope that hovers near the threshold from flipping the key back and forth.

At a noise amplitude of 1 the space level is about 0.04, and `thr` = 0.3 works. The figure raises the noise to 6. The space level rises to about 0.26, noise peaks cross the fixed threshold, and the decoder reads them as dits. Moving `thr` to 0.47, halfway between the new space level and the 0.68 mark level, fixes it, as the Noise frame below shows. A real decoder tracks the two levels and moves its threshold automatically; in the lab you set it by eye from the envelope plot.
::::

::::{frame} Decoding Marks and Spaces
:::{present}
<img src="../../viz/img/L12-decoder-windows.svg"
     alt="Two number lines in Morse units at the decoder's speed: a mark shorter than 2 units is a dit and a longer one a dah; a space shorter than 2 units stays inside a letter, from 2 to 5 units ends the letter, and 5 or more ends the word; anything under 0.3 unit is ignored as noise; a perfect sender's marks fall at 1 and 3 units and its spaces at 1, 3, and 7"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Marks: under 2 units is a dit, longer is a dah.
- Spaces: 2 units end a letter, and 5 end a word.
:::

The **CW Decoder** measures how long the key stays at each level and converts the length to units at its own WPM setting. Each boundary sits between two values a perfect sender produces: 2 units lies between a 1-unit dit and a 3-unit dah, and between a 1-unit gap inside a letter and a 3-unit gap between letters, and 5 units lies between 3 and 7. When a space reaches 2 units, the decoder looks up the dots and dashes it has collected and adds the letter to the text, or a # if the pattern is not in the table. A change of level that lasts less than 0.3 unit is noise, and the decoder ignores it.

The windows are wide, so the decoder accepts the uneven timing of a human operator. They also let it copy a sender whose speed differs from its own setting, as long as every mark and space still falls in the right window. A sender that is too slow stretches its letter gaps past 5 units, and one that is too fast shrinks its word gaps below 5; the L12 Lab measures both limits.
::::

::::{frame} Noise
:::{present}
<img src="../../viz/img/L12-link-noisy.png"
     alt="The L12 link at noise amplitude 6 with a 200 Hz CW filter and the threshold raised to 0.47: noise fills the waterfall and hides the carrier, the envelope swings widely but stays higher during the marks, the key trace follows the marks with a few extra pulses, and the Received label reads USAFA ECE 448 USAFA ECE 448 USAFS ECE 447, with two wrong characters"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- SNR in the CW filter: $160/\sigma^2$ for 200 Hz.
- At 6.5 dB, about 8 characters in 100 come out wrong.
:::

The keyed carrier has power 1 while the key is down, and the noise amplitude $\sigma$ is the standard deviation of the complex noise per sample, spread evenly over 32 kHz. A CW filter of width $B$ passes only $B/32{,}000$ of the noise power, so the SNR inside the filter is

$$\text{SNR} = \frac{32{,}000}{\sigma^2 B},$$

which is $160/\sigma^2$ for the 200 Hz filter. At $\sigma = 6$ that is 4.4, or 6.5 dB. The noise now reaches the top of the waterfall's color scale and hides the carrier there, but the CW filter still separates the carrier from most of the noise. With the threshold at 0.47, the receiver in the figure copies most of the message, and each wrong letter comes from a dit lost in the noise or a noise burst read as an extra dit. Over four runs of 600 characters at this setting, 8.2% of them were wrong, and single runs ranged from 7% to 10%.
::::

::::{frame} Filter Width
:::{present}
<img src="../../viz/img/L12-link-wide.png"
     alt="The L12 link at noise amplitude 6 with the CW filter widened to 1000 Hz and the threshold at 0.7: the envelope's space level rises to about 0.57 and its mark level to about 0.83, the key trace chatters, and about half the letters in the Received label are wrong"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Widen the filter to 1 kHz and 40% of the characters are wrong.
- Narrow it to 50 Hz and nearly all of them arrive.
- A narrower filter needs more accurate tuning.
:::

The figure keeps the noise amplitude at 6 and widens the CW filter to 1 kHz. Five times as much noise reaches the envelope detector, the space level rises to about 0.57, and even with the threshold moved to 0.70, the gap between the two levels is too small for clean decisions. The signal itself is only about 100 Hz wide, so a 1 kHz filter passes mostly noise. Narrowing the filter to 50 Hz goes the other way: at the same noise amplitude, only 3 characters in 1000 were wrong.

A narrow filter has two limits. The tone must stay inside it, so a narrower filter needs more accurate tuning and a more stable transmitter. And the filter's own response slows the envelope's edges, which matters only at speeds well above ours: at 40 WPM and $\sigma = 5.5$, the 50 Hz filter still got about 99% of the characters right.
::::

::::{frame} Noise Sweep
:class: read-only

We measured the link with the flowgraph's blocks running headless, without the Throttle, decoding four runs of 600 characters of random five-letter groups at 20 WPM at each setting, and the table gives the average; single runs vary by about a quarter of the value. At each one we set the threshold halfway between the measured space and mark levels and counted the wrong characters, including those missing or added.

| $\sigma$ | SNR in 200 Hz | 50 Hz filter | 200 Hz filter | 1 kHz filter |
| :-: | :-: | :-: | :-: | :-: |
| 3 | 12.5 dB | 0% | 0% | 0% |
| 4 | 10.0 dB | 0% | 0% | 1.4% |
| 5 | 8.1 dB | 0% | 1.6% | 15% |
| 6 | 6.5 dB | 0.3% | 8.2% | 40% |
| 7 | 5.1 dB | 1.7% | 24% | 67% |

The 200 Hz filter decodes without errors down to 10 dB in its own bandwidth and loses about a quarter of the characters at 5 dB. Each narrower filter keeps the error rate at zero up to a higher noise amplitude, which is the point of Lesson 2: the noise that reaches the detector is proportional to the bandwidth. The threshold matters as much as the filter. Left at 0.3, the 200 Hz receiver lost about 21% of the characters at $\sigma = 5$ and about 77% at $\sigma = 6$.
::::

::::{frame} CW on a Real Radio
:::{present}
- The L12 Lab sends CW through one PlutoSDR, TX port to RX port, with a 30 dB attenuator.
- Only the Pluto blocks change; you set the threshold from the envelope plot.
- Nothing in L12 transmits over the air.
:::

The L12 Lab moves this link onto a PlutoSDR. The transmit half ends at a PlutoSDR Sink at 915 MHz instead of the Noise Source, and the receive half starts at a PlutoSDR Source, with the same Xlating filter, product detector, CW filter, envelope detector, threshold, and decoder. As in L10, a Rational Resampler raises the 32 kHz stream by 32, to 1.024 MS/s, on the way out and lowers it again on the way in. The received level depends on the cable, the attenuator, and the Pluto's gain, so the lab flowgraph plots the threshold on the envelope plot, and you set it halfway between the space and mark levels.

In class we transmit only into a cable, into a shielded enclosure, or at very low power in an ISM band, and only when the lesson says to. Nothing in this lesson transmits; the L12 Lab transmits from the Pluto's TX port through an inline 30 dB attenuator into its own RX port. We have run the PlutoSDR flowgraph only in simulation, with a model of the cable in place of the radio, so the lab is its first run on hardware.
::::

::::{frame} Key Point
:::{present}
:class: callout
CW keys a carrier on and off, and a dit lasts $1.2/W$ s at $W$ WPM. Shaped edges keep it narrow. A narrow filter rejects the noise, and a threshold midway between the envelope's two levels recovers the text.
:::
::::

::::{frame} Downloads
:class: read-only doc-links

- <a class="doc-link" href="../../grc/L12-cw-tx.grc" download>L12-cw-tx.grc</a>: a hard-keyed and a shaped Morse keyer side by side, in time and in frequency. No hardware needed.
- <a class="doc-link" href="../../grc/L12-cw-link.grc" download>L12-cw-link.grc</a>: the whole CW link, with sliders for the noise, the CW filter, the threshold, the tuning, and both speeds, a waterfall, the envelope, the audio, and the decoded text. No hardware needed.

Open a `.grc` file from GRC's File menu, or run `gnuradio-companion L12-cw-link.grc` from the radioconda prompt. The Morse Keyer and the CW Decoder are Embedded Python Blocks, saved inside the `.grc` file; double-click one and choose Open in Editor to read its code. The L12 Lab page has the PlutoSDR version of the link.
::::

::::{frame} Summary
:class: read-only

| Idea | What it is | Number to remember |
| :-- | :-- | :-- |
| CW | a carrier keyed on and off | AM with a 0 or 1 message |
| Morse timing | dit 1, dah 3; gaps 1, 3, 7 | PARIS = 50 units |
| Speed | $t_\text{dit} = 1.2/W$ s | 60 ms at 20 WPM |
| Key clicks | hard edges spread energy far from the carrier | 5 ms edges: 40 dB lower 1 kHz away |
| Product detector | multiply by a BFO, keep the real part | tone at $700 + \Delta f$ Hz |
| CW filter | band-pass around the tone | SNR $= 32{,}000/(\sigma^2 B)$ |
| Threshold | halfway between space and mark levels | rises with the noise |
| Decoder | marks: 2 units; spaces: 2 and 5 units | ignores changes under 0.3 unit |
::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE448_L12_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE448_L12_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Looking Ahead
:::{present}
- The L12 Lab keys your initials by hand, sweeps the noise, and sends CW through a PlutoSDR.
- Lesson 13 decodes DTMF, a signal made of two tones at once.
:::

The L12 Lab is the hands-on version of this lesson. You build a keyer from standard blocks on an empty canvas and see its key clicks, measure how the noise, the filter width, the decoder's speed, and the tuning limit the link, and then send a message of your own through a PlutoSDR and a cable and decode it.

Lesson 13 turns to DTMF, the tones a telephone keypad sends. Each key sends two tones at once, so where today's receiver asked whether one tone was present, the DTMF receiver asks which two of eight tones are present.
::::
