---
frame_view: true
---

# L12 Lab — CW

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">CW</h1>

<div class="title-rule"></div>

Key your initials by hand, find where noise, filter width, speed, and tuning stop the decoder, and send CW through a PlutoSDR.

L12 Lab · Module 6: Waveform Applications & RF Reverse Engineering · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '6'">
  <li>I can transmit and receive CW (Morse) using GNU Radio and decode a received CW stream.</li>
</ol>
::::

::::{frame} From Lesson to Bench
:::{present}
- **Pre-Lab:** run the link and predict timing, SNR, and the decoder's limits.
- **Bench:** build a keyer, sweep noise, speed, and tuning, then use a PlutoSDR.
- **Writeup:** explain the threshold, the filter width, and the speed limits.
:::

Lesson 12 keyed, received, and decoded CW in one flowgraph. Today you first build a keyer yourself from standard blocks and see its key clicks, then measure where the simulated link stops decoding, and then run the same link on a PlutoSDR. The lab packet has three parts, and you turn it in once, complete, before Lesson 13. **Part 1, the Pre-Lab**, is on your own before the period: run `L12-cw-link.grc` once and make the predictions Part 2 checks. **Part 2** is your own measurements in class. **Part 3, the Writeup**, explains them.

Questions 1 to 5 run on your laptop and transmit nothing. Question 6 transmits, into a cable only, as the PlutoSDR frame below describes.
::::

::::{frame} Part 1: Before the Period
:::{present}
- `L12-cw-link.grc` runs and decodes `USAFA ECE 448`.
- Predict the timing at 13 WPM and write your initials as units.
- Predict the SNR at five settings, and the decoder's speed and tuning limits.
:::

Do the Pre-Lab before you arrive. Question 1 checks that the link flowgraph opens and runs on your laptop: if GRC reports an error, the L5 lesson page lists the install checks, and EI before the lab is the place to fix it.

Question 2 asks for predictions from the lesson: the dit, dah, and gap lengths at 13 WPM; your initials in Morse code, written as one 0 or 1 per unit, which is the list you type into your keyer in Question 3; the SNR in the CW filter at the noise and filter settings of Question 4; the slowest and fastest senders a decoder set to 20 WPM should copy; and how far you can mistune the receiver before the tone leaves a 200 Hz filter.
::::

::::{frame} Expected Numbers
:::{present}
| Check | Source |
| :-- | :-- |
| Timing at 13 WPM | dit $1.2/W$; dah and letter gap 3 dits; word gap 7 |
| SNR in the filter | $32{,}000/(\sigma^2 B)$ |
| Speed limits | where a gap meets the 5-unit window |
| Tuning limit | half the filter width |
:::

These follow from Lesson 12. The timing and the SNR are exact, and the speed and tuning limits follow from the decoder's windows and the CW filter's edges. The count of wrong characters at each noise setting is random and changes from run to run, which is why the packet records it over three repeats of the message rather than predicting it exactly.
::::

::::{frame} Part 2: Build a Hand Keyer
:class: read-only

1. Start GRC and choose File, New, QT GUI. Do not open `L12-cw-tx.grc`; build the keyer yourself from standard blocks.
2. Set `samp_rate` to 8000. Add Variables `wpm` = 13 and `spu` = `int(samp_rate*1.2/wpm)`, the samples in one unit.
3. Add a **Vector Source**: type float, vector = your list of 0s and 1s from Question 2(b) in square brackets, repeat Yes.
4. Add a **Repeat** block: type float, interpolation `spu`. It holds each unit for one unit's worth of samples. Then add a **Throttle**: type float, sample rate `samp_rate`. Its output is your hard-keyed envelope.
5. Add a **Moving Average**: type float, length 40, scale `1/40`. It averages the last 5 ms, which turns every edge into a 5 ms ramp. Connect the Throttle's output to its input. Its output is your shaped envelope.
6. Add a **QT GUI Time Sink**: type float, 2 inputs, 32000 points, sample rate `samp_rate`. Connect the Throttle to input 0 and the Moving Average to input 1.
7. Add a **QT GUI Frequency Sink**: type float, 2 inputs, FFT size 8192, bandwidth `samp_rate`, Y min $-140$, and Average left at None. Connect it the same way. Every arrow must be black.
8. Run it. Screenshot the canvas for Question 3(a). Drag a box on the time sink to zoom in on one dit, measure its length, and screenshot it for Question 3(b). Right-click the frequency sink and choose Max Hold, wait a few seconds, and read the highest peak of each spectrum within 100 Hz of 1 kHz and of 2 kHz from 0 Hz, where a carrier would sit, for Question 3(c); the Moving Average has nulls exactly at multiples of 200 Hz.
::::

::::{frame} Part 2: The Receiver in Noise
:class: read-only

<img src="../../viz/img/L12-grc-link.png"
     alt="The L12 link flowgraph in GNU Radio Companion: the sliders for noise, CW filter width, threshold, tuning, and both speeds at the top; the Morse Keyer, carrier, and Noise Source; and the receiver from the Frequency Xlating FIR Filter through the BFO, the CW filter, Abs, the low-pass, and Threshold to the CW Decoder"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto 12px;">

1. Open and run `L12-cw-link.grc` with every slider at its default. The Received label shows the last 60 characters, about four repeats of `USAFA ECE 448`.
2. Set the noise amplitude to 4.5. On the envelope plot, read the level between marks (the space level) and the level during marks (the mark level). Set the threshold halfway between them.
3. Wait for three new repeats of the message, about 23 s, and count the wrong, missing, and extra characters in the Received label. Record the levels, the threshold, and the count for Question 4(a).
4. Repeat steps 2 and 3 at noise amplitudes of 5.5 and 6.5. Screenshot the window at 6.5 for Question 4(b).
5. At 6.5, set the CW filter width to 1000 Hz, set the threshold again from the envelope plot, and record the count. Then do the same at 50 Hz.
::::

::::{frame} Part 2: Speed and Tuning
:class: read-only

1. Set the noise amplitude back to 1, the CW filter to 200 Hz, and the threshold to 0.3.
2. Leave the Decoder speed at 20 WPM. Set the Sender speed to 10, 12, 13, 20, 27, 28, and 30 WPM in turn. At each, wait for one full repeat of the message and record for Question 5(a) whether it decodes correctly, and if not, what goes wrong.
3. Set the Sender speed back to 20. Turn up your laptop's volume and listen to the tone.
4. Set the Receiver tuning to 5050, 5080, 5100, and 5150 Hz in turn. At each, record the pitch you hear, higher or lower than at 5000 Hz, and whether the text decodes, for Question 5(b).
::::

::::{frame} If No Text Arrives
:class: read-only

:::{admonition} If the Received label stays at "(listening)" or shows only E and T
:class: tip
Close the flowgraph and run it again with the sliders at their defaults, where every repeat of the message should decode. If the key trace never rises, the threshold is above the mark level; if it chatters between marks, the threshold is too close to the space level. In your own keyer, check that the vector ends with seven 0s, so the pattern repeats with a word gap, and that the Repeat block's interpolation is `spu`, not `wpm`.
:::
::::

::::{frame} Part 2: CW on a PlutoSDR
:::{present}
<img src="../../viz/img/L12-grc-pluto.png"
     alt="The L12 PlutoSDR flowgraph in GNU Radio Companion: a QT GUI Entry for the message and sliders for TX attenuation, RX gain, threshold, speeds, and filter width; the Morse Keyer and a 5 kHz carrier at amplitude 0.5 feed a Rational Resampler up by 32 and a PlutoSDR Sink at 915 MHz; a PlutoSDR Source feeds a Rational Resampler down by 32, the Xlating filter, an AGC3, and the rest of the L12 receiver, whose time sink plots the envelope against a constant threshold line"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- You cable one Pluto's TX port to its RX port through a 30 dB attenuator, at 915 MHz.
- Connect the cable before the flowgraph runs, and never connect an antenna.
:::

`L12-cw-pluto.grc` is the Lesson 12 link with the simulated channel replaced by a PlutoSDR. The transmit half raises the 32 kHz stream to 1.024 MS/s and sends the keyed carrier from the Pluto's TX port at 915 MHz plus 5 kHz; the receive half takes it from the RX port, lowers it to 32 kHz, and runs the same receiver. The received level depends on the cable, the attenuator, and the gain, and it is far weaker than in the simulated link, so an **AGC** after the Xlating filter holds the tuned carrier near amplitude 1. The envelope's mark level should then sit near 0.6 at any attenuation, and the envelope plot shows the threshold as a red line instead of the key. The waterfall's color scale runs from $-120$ to $-40$ dB; if the carrier does not show, right-click the waterfall and choose Auto Scale. You type the message into the Message box. We have run this flowgraph only in simulation, with a model of the cable in place of the radio, so your bench is its first run on hardware.

In class we transmit only into a cable, into a shielded enclosure, or at very low power in an ISM band, and only when the lesson says to. This question transmits only into the cable between the Pluto's own TX and RX ports, through an inline 30 dB SMA attenuator. The TX attenuation slider opens at 60 dB and cannot go below 30 dB. Never set TX attenuation below 30 dB or change the slider's range; the RX input is rated to only a few dBm, and the transmitter can put out more than that.
::::

::::{frame} What Success Looks Like
:class: read-only

<img src="../../viz/img/L12-pluto-sim.png"
     alt="L12-cw-pluto.grc run in simulation, labeled SIMULATED on the figure, with a model of the cable and of the Pluto's estimated levels and noise in place of the PlutoSDR: at 60 dB TX attenuation and 40 dB RX gain the waterfall shows the keyed carrier at plus 5 kHz, the AGC holds the envelope near 0.64 during marks and near 0.01 between them, the red threshold line sits halfway at 0.33, and the Received label reads USAFA ECE 448 repeatedly"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto 12px;">

The figure is the PlutoSDR flowgraph run in simulation, with the Pluto Sink and Source replaced by a model of the cable that uses our estimate of the Pluto's levels: about $-90$ dBm at the RX port and a carrier about $-50$ dB below full scale at 40 dB gain, with receiver noise. The real levels can differ, but the AGC should give the same picture. On the bench, look for the same three things: the keyed carrier on the waterfall at +5 kHz, the red threshold line halfway between the envelope's space and mark levels, and the message in the Received label.
::::

::::{frame} PlutoSDR Steps
:class: read-only

1. With the Pluto unplugged, connect its TX port to its RX port with a short SMA cable and an inline 30 dB SMA attenuator. Do not connect an antenna, and do not connect the cable without the attenuator.
2. Plug the Pluto into USB and run `iio_info -s` at the radioconda prompt; it should list a PlutoSDR context. The flowgraph uses the Pluto's default address, `ip:192.168.2.1`.
3. Open and run `L12-cw-pluto.grc`. Find the keyed carrier on the waterfall at +5 kHz. On the envelope plot, read the space and mark levels and set the threshold halfway between them; the default of 0.3 should be close. If no marks appear, raise the RX gain a few dB at a time. Never set TX attenuation below 30 dB or change the slider's range.
4. Once `USAFA ECE 448` decodes, screenshot the window for Question 6(a).
5. Have a teammate type a short message of their own into the Message box, without telling you what it is, and press Enter. Decode it and record it for Question 6(b).
6. Set the TX attenuation to 60, 70, 80, and 89 dB in turn. At each, read the mark and space levels, set the threshold halfway again, and record both levels and whether the text decodes for Question 6(c). Stop the flowgraph and unplug the Pluto before you disconnect the cable.
::::

::::{frame} Part 3: After the Lab
:::{present}
- Compare the noise table with your predictions, and explain the threshold.
- Compare the 50 Hz, 200 Hz, and 1 kHz filters, and the tuning each requires.
- Compare the speed limits with your prediction, and propose a better decoder.
:::

The Writeup is Question 7, in three parts. Part (a) compares your noise measurements with Question 2(c), explains why the threshold had to move, and asks what SNR a Lesson 2 link budget should deliver in the CW filter. Part (b) compares the three filter widths and connects your tuning measurement to the narrowest one. Part (c) compares the speeds that decoded with your prediction from the decoder's windows, says which window failed at each end, and proposes a change that would let the decoder follow any sender's speed.
::::

::::{frame} Lab Packet
:class: read-only doc-links

- <a class="doc-link" href="../../labs/ECE448_Lab_L12_CW_blank.pdf" target="_blank" rel="noopener">L12 Lab packet (PDF)</a>
- <a class="doc-link" href="../../grc/L12-cw-link.grc" download>L12-cw-link.grc</a>: the whole CW link with sliders for the noise, filter, threshold, tuning, and both speeds. No hardware needed.
- <a class="doc-link" href="../../grc/L12-cw-pluto.grc" download>L12-cw-pluto.grc</a>: the link on one PlutoSDR, transmitting at 915 MHz into a cable from its TX port to its RX port through a 30 dB attenuator. Needs a PlutoSDR.
::::

::::{frame} Looking Ahead
:::{present}
- Lesson 13 decodes DTMF, two tones at a time.
- Lesson 17 receives other on-off keyed signals: remotes.
:::

Keep your keyer flowgraph and your tables. Lesson 13 decodes DTMF, the tones of a telephone keypad, where the receiver has to find which two of eight tones are present instead of whether one carrier is on. Lesson 17, on RF reverse engineering, returns to on-off keying: many of the remotes it captures key a carrier the same way, and the same envelope and threshold recover their bits.
::::
