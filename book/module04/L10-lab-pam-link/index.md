---
frame_view: true
---

# L10 Lab — PAM Link

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">PAM Link</h1>

<div class="title-rule"></div>

Build the packet transmitter, find where noise and clock error stop the text, and send your own line through a PlutoSDR.

L10 Lab · Module 4: Digital Modulation · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '4'; counter-reset: lo 3">
  <li>I can implement a PAM link that transmits and receives ASCII text end-to-end.</li>
</ol>
::::

::::{frame} From Lesson to Bench
:::{present}
- **Pre-Lab:** run the link and predict the packet, the SNR, and the lines that arrive.
- **Bench:** build the transmitter, sweep the noise and clock error, then use a PlutoSDR.
- **Writeup:** explain the limits and the polarity.
:::

Lesson 10 sent a line of text over the PAM link of Lesson 9. Today you build the packet transmitter yourself, measure where the simulated link breaks, and then run the same link on a PlutoSDR. The lab packet has three parts, and you turn it in once, complete, before Lesson 11. **Part 1, the Pre-Lab**, is on your own before the period: run `L10-pam-link.grc` once and predict the packet size, the SNR at each noise level, and the share of lines that should arrive. **Part 2** is your own measurements in class. **Part 3, the Writeup**, explains them.

Questions 1 to 5 run on your laptop and transmit nothing. Question 6 transmits, into a cable only, as the PlutoSDR frame below describes.
::::

::::{frame} Part 1: Before the Period
:::{present}
- `L10-pam-link.grc` runs and shows the received line.
- Predict the packet's bits and time, and your own line's length field.
- Predict SNR, BER, and lines intact for six noise amplitudes.
:::

Do the Pre-Lab before you arrive. Question 1 checks that the link flowgraph opens and runs on your laptop: if GRC reports an error, the L5 lesson page lists the install checks, and EI before the lab is the place to fix it.

Question 2 asks for predictions from the lesson's formulas: the bits and time in one packet of the default line, the length field and first character of a line of your own choosing, the SNR at the slicer, the bit error rate, and the share of lines intact at each noise amplitude, and how fast a 10,000 ppm clock error would move a fixed sampling point. Part 2 checks each one.
::::

::::{frame} Expected Numbers
:::{present}
| Check | Expected |
| :-- | :-- |
| One packet | 344 bits, 86 ms |
| SNR at $\sigma$ = 1.0 | 9 dB |
| Lines intact at $\sigma$ = 1.0 | about half |
| Spectrum edges | $\pm 2.7$ kHz |
:::

These follow from Lesson 10. The packet size is exact: 64 bits of access code, 32 of header, and 8 per byte of the line. The SNR at the slicer is $8/\sigma^2$, and a line arrives intact only when all 280 bits of its header and payload are right. The count of correct lines at each setting is random and changes from run to run, which is why the packet records it over 20 to 30 s rather than predicting it exactly.
::::

::::{frame} Part 2: Build the Transmitter
:class: read-only

1. Start GRC and choose File, New, QT GUI. Do not open `L10-pam-tx.grc`; build it yourself.
2. Set `samp_rate` to 32000. Add Variables `sps` = 8, `alpha` = 0.35, `msg` = your line from Question 2(b) in quotes, `hdr` = `digital.header_format_default(digital.packet_utils.default_access_code, 0)`, and `tx_taps` = `firdes.root_raised_cosine(sps, samp_rate, samp_rate/sps, alpha, 11*sps)`.
3. Add a **Vector Source**: type byte, vector `list(msg.encode()) + [10]`, repeat Yes. Then **Stream to Tagged Stream**: type byte, packet length `len(msg) + 1`, length tag key `"packet_len"`.
4. Add a **Protocol Formatter** with format object `hdr` and length tag name `"packet_len"`, and a **Tagged Stream Mux** with 2 inputs and the same tag name. Connect Stream to Tagged Stream to the formatter and to the mux's second input, and the formatter to the mux's first input.
5. Add **Unpack K Bits** with K = 8, then **Chunks to Symbols**: input byte, output float, symbol table `[-1, 1]`.
6. Add a **Throttle** (float, sample rate `samp_rate/sps`) and an **Interpolating FIR Filter** (float in and out, interpolation `sps`, taps `tx_taps`).
7. Add a **QT GUI Time Sink** on the Throttle's output: type float, 112 points, sample rate `samp_rate/sps`, trigger mode Tag, trigger tag key `packet_len`. Add a **QT GUI Frequency Sink** (float, bandwidth `samp_rate`) on the filter's output. Every arrow must be black.
8. Run it. Screenshot the canvas for Question 3(a) and the time sink for Question 3(b), and read the spectrum's edges for Question 3(c).
::::

::::{frame} Part 2: Noise and Clock Error
:class: read-only

<img src="../../viz/img/L10-grc-link.png"
     alt="The whole L10 link flowgraph in GNU Radio Companion: the variables and sliders at the top, the packet transmitter from Vector Source to Chunks to Symbols, then Throttle, the RRC filter, the Fractional Resampler and Noise Source of the channel, and the receiver from the matched filter through Symbol Sync, Binary Slicer, Correlate Access Code - Tag Stream, and Repack Bits to the Text Sink"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto 12px;">

1. Open and run `L10-pam-link.grc`. The Lines label counts the lines received since a slider last moved.
2. With the clock error at 500 ppm, set the noise amplitude to 0.5, 0.7, 0.8, 0.9, 1.0, and 1.2 in turn. At each, wait about 30 s and record the time and the Lines label for Question 4(a).
3. At 1.0, wait for a line with a wrong character in the Received label and screenshot it for Question 4(b).
4. Set the noise back to 0.3. Raise the clock error to 0, 10,000, 20,000, 30,000, and 40,000 ppm in that order, without stopping the flowgraph. At each, wait about 20 s and record the Lines label and the eye's appearance for Question 5(a). Screenshot 10,000 ppm for Question 5(b).
5. Stop the flowgraph, run it again, and type 40,000 into the clock-error box right away. Record the Lines label after 20 s in the last column of Question 5(a).
::::

::::{frame} If No Text Arrives
:class: read-only

:::{admonition} If the Received label stays at "(waiting for a packet)"
:class: tip
Close the flowgraph and run it again with the sliders at their defaults, a noise amplitude of 0.3 and a clock error of 500 ppm, where every line should arrive within a second. In your own transmitter, check that the Stream to Tagged Stream packet length is `len(msg) + 1`, so that it counts the newline, and that all three tag names are `"packet_len"`, with the quotes. If you changed the message, keep it on one line.
:::
::::

::::{frame} Part 2: The Link on a PlutoSDR
:::{present}
<img src="../../viz/img/L10-grc-pluto.png"
     alt="The L10 PlutoSDR flowgraph in GNU Radio Companion: the packet transmitter and RRC filter feed Float To Complex, a Multiply Const of 0.5, a Rational Resampler up by 32, and a PlutoSDR Sink at 915 MHz; a PlutoSDR Source feeds a Rational Resampler down by 32, an AGC, the matched filter, Symbol Sync, a Costas Loop, Complex To Real, a polarity Multiply Const, the Binary Slicer, the access-code search, Repack Bits, and the Text Sink, with a frequency sink and a constellation sink"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- One Pluto, TX port cabled to RX port, at 915 MHz.
- The cable goes on before the flowgraph runs; no antennas.
:::

`L10-pam-pluto.grc` is the Lesson 10 link with the simulated channel replaced by a PlutoSDR. The transmit half raises the 32 kHz baseband stream to 1.024 MS/s and sends it from the Pluto's TX port at 915 MHz; the receive half takes it from the RX port, lowers it to 32 kHz, and runs the same matched filter, Symbol Sync, and access-code search. An **AGC** sets the received level, and a **Costas Loop**, which Lesson 15 explains, locks to the carrier's phase.

In class we transmit only into a cable, into a shielded enclosure, or at very low power in an ISM band, and only when the lesson says to. This question transmits only into the cable between the Pluto's own TX and RX ports. The TX attenuation slider starts at 60 dB and stops at 30 dB, which keeps the signal into the RX port at least 30 dB below the transmitter's full power.
::::

::::{frame} PlutoSDR Steps
:class: read-only

1. With the Pluto unplugged, connect a short SMA cable from its TX port to its RX port. Do not connect an antenna.
2. Plug the Pluto into USB and run `iio_info -s` at the radioconda prompt; it should list a PlutoSDR context. The flowgraph uses the Pluto's default address, `ip:192.168.2.1`.
3. Open and run `L10-pam-pluto.grc`. Within a few seconds the constellation should show two clusters on the horizontal axis, one on each side of zero.
4. If no line arrives within 5 s, switch Polarity. If neither setting works, raise the TX attenuation by 10 dB and try both again. Screenshot the window once lines arrive, for Question 6(a).
5. Stop and start the flowgraph three times, and record each time which polarity delivers lines, for Question 6(b).
6. Stop it, put your line from Question 2(b) in `msg`, and run it again for Question 6(c). Stop the flowgraph and unplug the Pluto before you disconnect the cable.
::::

::::{frame} Part 3: After the Lab
:::{present}
- Compare the noise table with your predictions and set a link budget target.
- Compare the clock-error limit with a real crystal.
- Explain why the working polarity changes, and remove the need for the switch.
:::

The Writeup is three questions. The first compares your noise measurements with Question 2(c) and turns them into the SNR a Lesson 2 link budget should deliver at the slicer. The second compares the clock error your link tolerated with the error between two real crystals, and asks what would happen without Symbol Sync. The third asks why the polarity that works on the Pluto changes from run to run, and what change to the receiver would make the switch unnecessary.
::::

::::{frame} Lab Packet
:class: read-only doc-links

- <a class="doc-link" href="../../labs/ECE448_Lab_L10_PAMLink_blank.pdf" target="_blank" rel="noopener">L10 Lab packet (PDF)</a>
- <a class="doc-link" href="../../grc/L10-pam-tx.grc" download>L10-pam-tx.grc</a> and <a class="doc-link" href="../../grc/L10-pam-link.grc" download>L10-pam-link.grc</a>
- <a class="doc-link" href="../../grc/L10-pam-pluto.grc" download>L10-pam-pluto.grc</a>: the link on one PlutoSDR, transmitting at 915 MHz into a cable from its TX port to its RX port. Needs a PlutoSDR.
::::

::::{frame} Looking Ahead
:::{present}
- Lesson 11 writes and packages custom blocks.
- Lesson 15 explains the Costas Loop that locked to the Pluto's carrier.
:::

Keep your transmitter flowgraph and your tables. Lesson 11 starts Module 5 with out-of-tree modules and custom blocks, including Python blocks like the Text Sink that displayed every line today. Lesson 15, on mPSK, explains carrier recovery, the job the Costas Loop did on the Pluto, and why a phase-modulated signal can lock upside down.
::::
