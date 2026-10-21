---
frame_view: true
---

# L15 Lab — mPSK

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">mPSK</h1>

<div class="title-rule"></div>

Build a carrier-recovery loop, measure the link against Lesson 3's curves, find the Costas Loop's limits, and send QPSK through a PlutoSDR.

L15 Lab · Module 6: Waveform Applications & RF Reverse Engineering · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '6'; counter-reset: lo 3">
  <li>I can implement an mPSK modulator and demodulator (BPSK, QPSK, 8PSK), recover carrier and symbol timing, and verify constellation behavior against theory.</li>
</ol>
::::

::::{frame} From Lesson to Bench
:::{present}
- **Pre-Lab:** run the link and predict bit rates, bit error rates, and the phase ambiguity.
- **Bench:** build a Costas Loop, measure BER, pull-in, and ambiguity, then use a PlutoSDR.
- **Writeup:** explain the losses, the limits, and differential coding.
:::

Lesson 15 built an mPSK text link with timing and carrier recovery. Today you first build an 8PSK carrier-recovery loop yourself, then measure the link's bit error rate, the Costas Loop's pull-in range, and its phase ambiguity, and then run QPSK on a PlutoSDR. The lab takes most of the lesson's second period. The lab packet has three parts, and you turn it in once, complete, before Lesson 16. **Part 1, the Pre-Lab**, is on your own before the period: run `L15-psk-link.grc` once and make the predictions Part 2 checks. **Part 2** is your own measurements in class. **Part 3, the Writeup**, explains them.

Questions 1 to 6 run on your laptop and transmit nothing. Question 7 transmits, into a cable only, as the PlutoSDR frame below describes.
::::

::::{frame} Part 1: Before the Period
:::{present}
- `L15-psk-link.grc` runs and shows the received line.
- Predict the bit rates, $E_s/N_0$, and Lesson 3's BER at six settings.
- Predict how many channel phases decode without differential coding.
- Estimate the 8PSK loop's pull-in range.
:::

Do the Pre-Lab before you arrive. Question 1 checks that the link flowgraph opens and runs on your laptop, and has you type a 50 Hz frequency offset to see the ring of the lesson's opening figure: if GRC reports an error, the L5 lesson page lists the install checks, and EI before the lab is the place to fix it.

Question 2 asks for predictions from the lesson: the bit rate and $E_s/N_0$ of BPSK, QPSK, and 8PSK at 6,000 symbols per second; Lesson 3's bit error rate at the six settings of Question 4, with and without differential coding; the number of channel phases at which QPSK and 8PSK decode with differential coding off; and an estimate of the 8PSK loop's pull-in range from the lesson's BPSK and QPSK measurements.
::::

::::{frame} Expected Numbers
:::{present}
| Check | Source |
| :-- | :-- |
| Bit rate and $E_s/N_0$ | $k = \log_2 M$; $E_s/N_0 = E_b/N_0 + 10 \log_{10} k$ |
| BER | Lesson 3's formulas; about twice that with differential coding |
| Phases that decode | the loop's lock points, $360°/M$ apart |
| 8PSK pull-in | the trend from BPSK to QPSK |
:::

These follow from Lessons 3 and 15. The bit rates and $E_s/N_0$ are exact, and so is the count of phases that decode, once you know where the loop locks. The measured BER is random and sits a little above theory, which is why the packet records it over 60 s and the number of bits counted, and the pull-in range is an estimate that the bench measures.
::::

::::{frame} Part 2: Build a Carrier-Recovery Loop
:class: read-only

1. Start GRC and choose File, New, QT GUI. Do not open the lesson's flowgraphs; build this one yourself.
2. Set `samp_rate` to 4000, one sample per symbol. Add an **Import** block with `import math, cmath`, a Variable `pts` = `[cmath.exp(1j*(math.pi/8 + math.pi/4*i)) for i in range(8)]`, the 8PSK points, and a **QT GUI Range** `foff`: label Frequency offset (Hz), default 20, start $-200$, stop 200, step 5.
3. Add a **Random Source**: type byte, minimum 0, maximum 8, number of samples 10000, repeat Yes. Then **Chunks to Symbols**: input byte, output complex, symbol table `pts`. Then a **Throttle**: type complex, sample rate `samp_rate`.
4. Add a **Signal Source**: type complex, sample rate `samp_rate`, waveform Cosine, frequency `foff`, amplitude 1. Add a **Multiply** with 2 complex inputs and connect the Throttle and the Signal Source to it. This is the frequency offset.
5. Add a **Noise Source**: type complex, Gaussian, amplitude 0.2, and an **Add** with 2 complex inputs. Connect the Multiply and the Noise Source to the Add.
6. Add a **Costas Loop**: loop bandwidth 0.02, order 8. Connect the Add's output to it.
7. Add a **QT GUI Constellation Sink** with 2 inputs: the Add's output to input 0 and the Costas Loop's first output to input 1. Add a **Multiply Const**: type float, constant `samp_rate/(2*math.pi)`, on the Costas Loop's frequency output, and a **QT GUI Number Sink** on that, with minimum $-200$ and maximum 200. Every arrow must be black.
8. Run it. Screenshot the canvas for Question 3(a) and the window for Question 3(b). Record the frequency reading at 20 Hz, then type $-60$ into the offset box and record it again.
9. Stop the flowgraph, set the Costas Loop's order to 2, run it again, and describe the output for Question 3(c).
::::

::::{frame} Part 2: Bit Error Rate
:class: read-only

<img src="../../viz/img/L15-grc-link.png"
     alt="The L15 link flowgraph in GNU Radio Companion: the variable M and the sliders for Eb/N0, frequency offset, channel phase, and clock error at the top; the packet transmitter, Gray map, differential encoder, Chunks to Symbols, and RRC filter; the Channel Model; and the receiver from the matched filter through Symbol Sync, the Costas Loop, the Constellation Decoder, the differential decoder, and the access-code search to the Text Sink"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto 12px;">

1. Open and run `L15-psk-link.grc` with every slider at its default: no frequency offset, channel phase 0, and `diff` = 1, differential coding on. The Lines label counts the lines received and the bit errors in them since a slider last moved.
2. Type 5 into the $E_b/N_0$ box and press Enter. Wait 60 s, then record the BER and the number of bits counted for Question 4(a).
3. Repeat at 7 and 9 dB.
4. Stop the flowgraph. Double-click the variable `M`, set it to 8, and run it again. Repeat steps 2 and 3 at 9, 11, and 13 dB. Screenshot the window at 11 dB for Question 4(c).
5. Stop it, set `M` back to 4 and the variable `diff` to 0, and run it again with the sliders at their defaults. Set $E_b/N_0$ to 7 dB, wait 60 s, and record the BER for Question 4(b). Set `diff` back to 1 afterward.
::::

::::{frame} Part 2: Carrier Recovery
:class: read-only

1. With `M` = 4 and differential coding on, set $E_b/N_0$ to 12 dB.
2. With the frequency offset at 0 and lines arriving, type 250 into the frequency offset box in one jump. Watch the frequency estimate for up to 15 s, and record whether the loop locks, about how long it takes, and the frequency it settles at, for Question 5(a).
3. Type 0, wait until lines arrive again, and repeat step 2 for 350 and then 425 Hz. At 425 Hz, also count the clusters in the Costas Loop's output.
4. Stop the flowgraph, set `M` to 8, and run it again. Set $E_b/N_0$ to 12 dB and repeat steps 2 and 3 for 100, 150, 200, and 250 Hz, for Question 5(b). At 200 Hz and above, give the loop the full 15 s.
::::

::::{frame} Part 2: Phase Ambiguity
:class: read-only

1. Stop the flowgraph, set `M` to 4 and `diff` to 0, and run it again, so the loop locks with no frequency offset and the channel phase at 0. Do not move the frequency offset in this part. Set $E_b/N_0$ to 12 dB. Lines should keep arriving.
2. Type 20 into the channel phase box. Record whether lines still arrive after about 5 s. Then type 0, wait until lines arrive again, and type the next phase.
3. Repeat for every phase from 20 to 340 in steps of 20, returning to 0 between them, for Question 6(a).
4. Stop the flowgraph, set `M` to 8, keep `diff` at 0, and run it again. Set $E_b/N_0$ to 12 dB and repeat steps 2 and 3.
5. Stop the flowgraph, set `diff` to 1, run it again, and repeat three of the phases that failed, for Question 6(b).
6. Stop the flowgraph, set `M` to 4 and `diff` to 0, and run it again. Step the phase from 0 to 100 by 20 at a time without returning to 0, and record what happens. Set `diff` back to 1 when you finish.
::::

::::{frame} If No Text Arrives
:class: read-only

:::{admonition} If the Received label stays at "(waiting for a packet)"
:class: tip
Close the flowgraph and run it again with the sliders at their defaults, where every line should arrive within a second. With `diff` = 0, text arrives only when the loop has locked in the right rotation, and any frequency offset or phase jump you applied during the run can leave it locked in another one; run the flowgraph again with the sliders at their defaults. If the Costas Loop's output keeps turning, the frequency offset is beyond its pull-in range: type 0 and wait. If you changed `M`, check that it is 2, 4, or 8 and that you ran the flowgraph again. In your own carrier-recovery flowgraph, check that the Costas Loop's order is 8 and that the Signal Source's sample rate is `samp_rate`.
:::
::::

::::{frame} Part 2: QPSK on a PlutoSDR
:::{present}
<img src="../../viz/img/L15-grc-pluto.png"
     alt="The L15 PlutoSDR flowgraph in GNU Radio Companion: sliders for TX attenuation and RX gain and the variables M and diff; the packet transmitter, Gray map, differential encoder, Chunks to Symbols, and RRC filter feed a Multiply Const of 0.5, a Rational Resampler up by 32, and a PlutoSDR Sink at 915 MHz; a PlutoSDR Source feeds a Rational Resampler down by 32, an AGC3, and the L15 receiver from the matched filter to the Text Sink"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- You cable one Pluto's TX port to its RX port through a 30 dB attenuator, at 915 MHz.
- Connect the cable before the flowgraph runs, and never connect an antenna.
:::

`L15-psk-pluto.grc` is the Lesson 15 link with the Channel Model replaced by a PlutoSDR. The transmit half raises the 32 kHz stream to 1.024 MS/s and sends it from the Pluto's TX port at 915 MHz; the receive half takes it from the RX port, lowers it to 32 kHz, and runs the same matched filter, Symbol Sync, Costas Loop, and decoder. The received level depends on the cable, the attenuator, and the gain, and it is far weaker than in the simulated link, so an **AGC** after the resampler holds it near amplitude 1. The Pluto's transmitter and receiver share one reference oscillator, so the frequency offset is close to zero, but the carrier's phase at the receiver changes every time the flowgraph starts. We have run this flowgraph only in simulation, with a model of the cable in place of the radio, so your bench is its first run on hardware.

In class we transmit only into a cable, into a shielded enclosure, or at very low power in an ISM band, and only when the lesson says to. This question transmits only into the cable between the Pluto's own TX and RX ports, through an inline 30 dB SMA attenuator. The TX attenuation slider opens at 60 dB and cannot go below 30 dB. Never set TX attenuation below 30 dB or change the slider's range; the RX input is rated to only a few dBm, and the transmitter can put out more than that.
::::

::::{frame} What Success Looks Like
:class: read-only

<img src="../../viz/img/L15-pluto-sim.png"
     alt="L15-psk-pluto.grc run in simulation, labeled SIMULATED on the figure, with a model of the cable and of the Pluto's estimated levels and noise in place of the PlutoSDR: at 60 dB TX attenuation and 40 dB RX gain the Symbol Sync output shows four tight clusters turned by the cable's phase, the Costas Loop output shows them at 45 degrees plus multiples of 90, the frequency estimate sits at 0 Hz, and the Lines label reads 328 correct of 328 received in 15 s with no bit errors"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto 12px;">

The figure is the PlutoSDR flowgraph run in simulation, with the Pluto Sink and Source replaced by a model of the cable that uses our estimate of the Pluto's levels: a signal about 50 dB below full scale at 60 dB TX attenuation and 40 dB RX gain, with receiver noise 13 dB below it across the 1.024 MHz band, and a fixed phase. The real levels can differ, but the AGC should give the same picture. On the bench, look for the same three things: four tight clusters before and after the Costas Loop, a frequency estimate near 0 Hz, and lines arriving in the Lines label.
::::

::::{frame} PlutoSDR Steps
:class: read-only

1. With the Pluto unplugged, connect its TX port to its RX port with a short SMA cable and an inline 30 dB SMA attenuator. Do not connect an antenna, and do not connect the cable without the attenuator.
2. Plug the Pluto into USB and run `iio_info -s` at the radioconda prompt; it should list a PlutoSDR context. The flowgraph uses the Pluto's default address, `ip:192.168.2.1`.
3. Open and run `L15-psk-pluto.grc`. Within a few seconds the Costas Loop's output should show four clusters and lines should arrive. If the clusters do not form, raise the RX gain a few dB at a time. Never set TX attenuation below 30 dB or change the slider's range.
4. Once lines arrive, screenshot the window for Question 7(a).
5. Stop and start the flowgraph three times with `diff` = 1, and record whether text arrives each time. Then set the variable `diff` to 0 and stop and start it eight more times, recording whether text arrives each time, for Question 7(b). Set `diff` back to 1.
6. With `diff` = 1, set the TX attenuation to 60, 70, 80, and 89 dB in turn. At each, wait 30 s and record the BER for Question 7(c). Stop the flowgraph and unplug the Pluto before you disconnect the cable.
::::

::::{frame} Part 3: After the Lab
:::{present}
- Compare the BER with Lesson 3, and separate the loops' loss from differential coding's.
- Compare the 8PSK pull-in range with your estimate and with QPSK.
- Explain the phases that decoded, and the Pluto runs.
:::

The Writeup is Question 8, in three parts. Part (a) compares your BER measurements with Question 2(b), estimates how much $E_b/N_0$ the loops and differential coding each add, and asks what a Lesson 2 link budget should deliver for QPSK. Part (b) compares the 8PSK pull-in range with your estimate and with QPSK, and asks what a link between two different PlutoSDRs would need before its Costas Loop. Part (c) explains which channel phases decoded, why the Pluto runs behaved as they did, and why real mPSK links use differential coding.
::::

::::{frame} Lab Packet
:class: read-only doc-links

- <a class="doc-link" href="../../labs/ECE448_Lab_L15_MPSK_blank.pdf" target="_blank" rel="noopener">L15 Lab packet (PDF)</a>
- <a class="doc-link" href="../../grc/L15-psk-link.grc" download>L15-psk-link.grc</a>: the whole mPSK text link with sliders for $E_b/N_0$, frequency offset, channel phase, and clock error, and a variable that turns differential coding on or off. No hardware needed.
- <a class="doc-link" href="../../grc/L15-psk-pluto.grc" download>L15-psk-pluto.grc</a>: the link on one PlutoSDR, transmitting at 915 MHz into a cable from its TX port to its RX port through a 30 dB attenuator. Needs a PlutoSDR.
::::

::::{frame} Looking Ahead
:::{present}
- Lesson 16 hops the carrier from channel to channel.
- Lesson 20 adds amplitude to the constellation with QAM.
:::

Keep your carrier-recovery flowgraph and your tables. Lesson 16 turns to frequency hopping, where the transmitter moves its carrier many times a second and the receiver has to follow it. Lesson 20 returns to constellations: QAM varies the amplitude as well as the phase, so its receiver needs the same timing and carrier recovery as today's, and an AGC that sets the level exactly.
::::
