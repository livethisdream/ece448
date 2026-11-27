---
frame_view: true
---

# L10 Lab — PAM Link

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">PAM Link</h1>

<div class="title-rule"></div>

Build the packet transmitter, find where noise breaks the text with the matched filter on and off, and send your own line through a PlutoSDR.

L10 Lab · Module 4: Digital Modulation · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '4'; counter-reset: lo 3">
  <li>I can implement a PAM link that transmits and receives ASCII text end-to-end.</li>
</ol>
::::

::::{frame} The Big Picture
:::{present}
<img src="../../viz/img/L10-big-picture.png"
     alt="The L10 Lab's three blocks as GNU Radio Companion canvases: the packet transmitter you build (Steps 1 to 7) beside L10-pam-link.grc (Steps 8 to 10), and L10-pam-pluto.grc below (Steps 11 to 15)."
     style="max-width: 900px; width: 100%; display: block; margin: 0 auto;">
:::

Steps 1 to 7 build the packet transmitter from an empty canvas with your own line of text and look at one packet on the time sink. Steps 8 to 10 run `L10-pam-link.grc` and raise the Noise amplitude slider until lines break, first with the matched filter on and then with it off. Steps 11 to 15 send your line through one PlutoSDR, from its TX port to its RX port through a cable and a 30 dB attenuator at 915 MHz, and note which Polarity setting delivers it. Your Part 1 line goes into Steps 1 and 12 and your packet entries into Steps 2 and 7, the three readings go in Table B of the packet, and the screenshots go in Figures 1 to 3.
::::

::::{frame} Predict First
:class: viz-frame

:::{depth}
Choose the matched filter's setting. Before you press **Show the lines**, set the My Prediction slider to the noise amplitude at which you think lines start to break. Changing the setting or your guess hides the answer again, so each guess comes first. The counts come from `L10-pam-link.grc` run with a 3-byte line; today you send the 31-byte default line, so nothing here is a reading you record.
:::

:::{present}
<iframe src="../../viz/pam-mf-predict.html"
        width="100%" height="465"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Choose the matched filter setting, predict the noise amplitude at which the PAM link's text starts to break, then show the lines that arrive intact">
</iframe>
:::
::::

::::{frame} Build the Packet Transmitter
:::{present}
- Start from an empty QT GUI canvas, not `L10-pam-tx.grc`.
- Put your own line in `msg` and your Part 1 packet length in Stream to Tagged Stream.
- Run it; find your length field and first character on the time sink.
:::
:::{present}
<img src="../../viz/img/L10-canvas-tx.png"
     alt="The packet transmitter you build, as GNU Radio Companion shows it: Vector Source, Stream to Tagged Stream with its packet length left as len_table_a for your Part 1 value, Protocol Formatter, Tagged Stream Mux, Unpack K Bits, and Chunks to Symbols, then a Throttle feeding a QT GUI Time Sink and an Interpolating FIR Filter feeding a QT GUI Frequency Sink"
     style="max-width: 600px; width: 100%; display: block; margin: 0 auto;">
:::

1. **Start GRC.** Choose File, New, QT GUI, and save the flowgraph in the folder that holds the Lesson 10 flowgraphs. Set `samp_rate` to 32000, and add Variables `sps` = 8, `alpha` = 0.35, `msg` = your line from Part 1 Table A in quotes, `hdr` = `digital.header_format_default(digital.packet_utils.default_access_code, 0)`, and `tx_taps` = `firdes.root_raised_cosine(sps, samp_rate, samp_rate/sps, alpha, 11*sps)`.
2. **Add the source.** Add a Vector Source of type byte with vector `list(msg.encode()) + [10]` and Repeat set to Yes, then a byte Stream to Tagged Stream with the packet length from your Part 1 Table A and length tag key `"packet_len"`.
3. **Build the packet.** Add a Protocol Formatter with format object `hdr` and length tag name `"packet_len"`, and a Tagged Stream Mux with 2 inputs and the same tag name. Connect Stream to Tagged Stream to the formatter and to the mux's second input, and the formatter to the mux's first input.
4. **Turn bytes into symbols.** Add Unpack K Bits with K = 8, then Chunks to Symbols with input byte, output float, and symbol table `[-1, 1]`.
5. **Shape the pulses.** Add a float Throttle at `samp_rate/sps`, then an Interpolating FIR Filter, float in and out, with interpolation `sps` and taps `tx_taps`, and a float QT GUI Frequency Sink with bandwidth `samp_rate` on the filter's output.
6. **Add the time sink.** Put a float QT GUI Time Sink on the Throttle's output with 112 points, sample rate `samp_rate/sps`, trigger mode Tag, and trigger tag key `"packet_len"`, so every sweep starts at the first bit of a packet. Every arrow must be black: a red arrow joins two ports of different types, so match that block's type to its neighbor's.
7. **Run it.** Find the header's length field and the first character of your line on the time sink, and compare both with your Part 1 Table A. If the sweep does not hold still, check that all four tag names, in Stream to Tagged Stream, Protocol Formatter, Tagged Stream Mux, and the time sink's trigger, are `"packet_len"`, with the quotes. Take one screenshot that shows your canvas and the time sink, mark the length field and your first character on it, and paste it as Figure 1.
::::

::::{frame} Noise and the Matched Filter
:::{present}
- Run `L10-pam-link.grc` with the matched filter on.
- Raise the noise until the first line breaks.
- Switch the matched filter off and search again from a low setting.
:::
:::{present}
<img src="../../viz/img/L10-canvas-link.png"
     alt="L10-pam-link.grc in GNU Radio Companion: the packet transmitter and RRC filter, a Fractional Resampler and an Add with a Noise Source for the channel, and the receiver from the matched filter through Symbol Sync, Binary Slicer, Correlate Access Code - Tag Stream, and Repack Bits to the Text Sink, with an eye sink and a time sink"
     style="max-width: 620px; width: 100%; display: block; margin: 0 auto;">
:::

8. **Run the link.** Open and run `L10-pam-link.grc`, and leave **Clock error (ppm)** at 500 for the whole lab. The Lines label counts the lines received since a slider or the switch last moved.
9. **Find the break with the filter on.** With **Matched filter** on, raise **Noise amplitude** from 0.3 by 0.05 at a time, waiting about 20 s at each setting, until a line breaks. The link sends about 11 lines a second, so 20 s is about 230 lines, and a line has broken once the correct count falls behind the received count or the received count stops growing. Record that setting, and paste a screenshot of the window there as the left pane of Figure 2.

    <div class="rec" data-lab="L10">
    <label>Step 9: Noise amplitude at which lines start to break, matched filter on <input data-field="b.mfon"></label>
    </div>
10. **Find the break with the filter off.** Set **Noise amplitude** to 0.1 and switch **Matched filter** off, then raise the noise by 0.05 at a time in the same way until a line breaks. Record that setting, and paste a screenshot of the window there as the right pane of Figure 2.

    <div class="rec" data-lab="L10">
    <label>Step 10: Noise amplitude at which lines start to break, matched filter off <input data-field="b.mfoff"></label>
    </div>
::::

::::{frame} The Link on a PlutoSDR
:::{present}
- Cable the Pluto's TX port to its RX port through the 30 dB attenuator first.
- Send your own line with `L10-pam-pluto.grc` at 915 MHz.
- Restart it three times and note which Polarity works.
:::
:::{present}
<img src="../../viz/img/L10-canvas-pluto.png"
     alt="L10-pam-pluto.grc in GNU Radio Companion: the packet transmitter and RRC filter feed Float To Complex, a Multiply Const, a Rational Resampler up by 32, and a PlutoSDR Sink at 915 MHz; a PlutoSDR Source feeds a Rational Resampler down by 32, an AGC, the matched filter, Symbol Sync, a Costas Loop, Complex To Real, a polarity Multiply Const, the Binary Slicer, the access-code search, Repack Bits, and the Text Sink"
     style="max-width: 620px; width: 100%; display: block; margin: 0 auto;">
:::

11. **Cable the Pluto.** With the Pluto unplugged, connect its TX port to its RX port with a short SMA cable and the inline 30 dB SMA attenuator. Never connect an antenna in this lab, since the cable keeps the 915 MHz signal off the air, and never connect the cable without the attenuator: the RX input survives only a few dBm, and the transmitter can put out more than that.
12. **Send your line.** Plug in the Pluto, open `L10-pam-pluto.grc`, put your line from Part 1 Table A in `msg`, and run it. **Pluto TX attenuation (dB)** opens at 60 and stops at 30; never set it lower or change the slider's range, because the 30 dB floor and the attenuator together keep the RX input below its limit.
13. **Lock the polarity.** If no line arrives within 5 s, switch **Polarity**. If neither setting works, raise the TX attenuation by 10 dB and try both again: too strong a signal overloads the receiver and flattens the two levels. Once your line arrives, paste a screenshot of the window as Figure 3.
14. **Restart it three times.** Stop and start the flowgraph three times, repeat Step 13's search on each run, and note each time which **Polarity** setting delivers lines.

    <div class="rec" data-lab="L10">
    <label>Step 14: Runs that needed Polarity set to inverted (of 3) <input data-field="b.inv"></label>
    </div>
15. **Disconnect.** Stop the flowgraph and unplug the Pluto before you disconnect the cable.
::::

::::{frame} No Hardware?
:class: read-only

:::{admonition} If the PlutoSDR or the text does not work
:class: tip
Steps 1 to 10 need no radio. If your PlutoSDR is missing or will not open, do Steps 11 to 15 at the laptop of a classmate whose PlutoSDR works, taking turns, with your own line and your own screenshots, and note whose PlutoSDR you used on the packet's Documentation line. Bring the failed Pluto to EI.

If the Received label stays at "(waiting for a packet)" on `L10-pam-link.grc`, close it and run it again at a noise amplitude of 0.3 with the matched filter on, where every line arrives within about a second. If you changed the message, keep it on one line.
:::
::::

::::{frame} Your Part 2 Entries
:class: read-only

This frame collects every box you filled in on this page. Your entries stay in this browser only, saved as you type. **Download my packet** writes them into the Measured cells of the blank packet and saves the PDF. The download locks every field, the Predicted cells included, so type your predictions into your own copy of the packet first, then use **Fill my own copy** and choose that file: the page keeps your predictions and adds your measurements beside them. Paste Figures 1 to 3 and write Part 3 in your copy, or on the printout, and upload one PDF to Gradescope. **Export entries** saves a small backup file you can **Import** on another laptop.

<div class="rec-summary" data-lab="L10" data-pdf="../../labs/ECE448_Lab_L10_PAMLink_blank.pdf" data-file="ECE448_L10_Lab"></div>
::::

::::{frame} Lab Packet
:class: read-only doc-links

The L10 Lab packet is one submission, turned in complete before Lesson 11:

1. Part 1, Predict (individual, before the lab period): your line of text and the three shaded entries in Table A, with your work attached.
2. Part 2, Measure (in class, on your own laptop and PlutoSDR): the white Measured cells of Table B, and Figures 1 to 3.
3. Part 3, Analyze (individual, after the lab): two prompts, each answered from your own table and figures.

- <a class="doc-link" href="../../labs/ECE448_Lab_L10_PAMLink_blank.pdf" target="_blank" rel="noopener">L10 Lab packet (PDF)</a>
- <a class="doc-link" href="../../grc/L10-pam-link.grc" download>L10-pam-link.grc</a>
- <a class="doc-link" href="../../grc/L10-pam-pluto.grc" download>L10-pam-pluto.grc</a>: the link on one PlutoSDR, transmitting at 915 MHz into a cable from its TX port to its RX port.
::::

::::{frame} For Part 3
:class: read-only

Do Part 3 after class, with your table and figures beside you. It asks about two comparisons:

1. Your two break settings in Table B, against the two windows in Figure 2.
2. Your three PlutoSDR runs in Table B and Figure 3, against the simulated link, which has no Polarity switch.

I grade each answer on a claim, the evidence from your own table and figures, the reasoning that connects them, and the uncertainty in your readings.
::::

::::{frame} Looking Ahead
:class: read-only

Lesson 11 writes and packages a custom block like the Text Sink that showed every line today.
::::
