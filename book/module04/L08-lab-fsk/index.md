---
frame_view: true
---

# L8 Lab — FSK

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">FSK</h1>

<div class="title-rule"></div>

Build a demodulator and decoder that recover the message from your class transmitter, then find the largest frequency offset an FSK link tolerates at two deviations.

L8 Lab · Module 4: Digital Modulation · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '4'">
  <li>I can describe FSK modulation and implement an FSK transmitter and receiver in GNU Radio.</li>
</ol>
::::

::::{frame} The Big Picture
:::{present}
<img src="../../viz/img/L08-big-picture.png"
     alt="The L8 Lab's three blocks as GNU Radio Companion canvases: your class transmitter with packets and a Channel Model (Steps 1 to 3) beside the decoder you add to it (Steps 4 to 10), and L08-fsk-link.grc below (Steps 11 to 16)."
     style="max-width: 860px; width: 100%; display: block; margin: 0 auto;">
:::

Steps 1 to 3 add packets and a Channel Model to the transmitter you built in class, at 1.5 kHz of deviation. Steps 4 to 10 build the demodulator and decoder from Lesson 8's blocks and recover your line of text into a file. Steps 11 to 16 run `L08-fsk-link.grc` at a fixed noise voltage and raise the Frequency offset slider, first at 1 kHz of deviation and then at 2 kHz, watching the eye and the Lines label. Your Part 1 settings go into Steps 4 and 5, the three readings go in Table B of the packet, and the screenshots go in Figures 1 to 4. Nothing in this lab transmits.
::::

::::{frame} Predict First
:class: viz-frame

:::{depth}
Choose a deviation and a frequency offset. The dashed blue lines are the eye's two levels with no offset. Before you press **Show the eye**, set the My Prediction slider to where you think the lower level will sit. Changing either setting or your guess hides the answer again, so each guess comes first. The widget shifts the eye by the offset and leaves out the receive filter, and its settings are not the lab's, so nothing here is a reading you record.
:::

:::{present}
<iframe src="../../viz/fsk-offset-predict.html"
        width="100%" height="466"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Choose an FSK deviation and a frequency offset, predict the lower level of the demodulator's eye, then show the eye">
</iframe>
:::
::::

::::{frame} Frame Your Transmitter
:::{present}
- Open the transmitter you built in class and set its deviation to 1.5 kHz.
- Add the packet front end and a Channel Model.
- Run it: two tones above the noise floor.
:::
:::{present}
<img src="../../viz/img/L08-canvas-tx.png"
     alt="Your class transmitter in GNU Radio Companion with the packet front end and a Channel Model added: Vector Source, Stream to Tagged Stream, Protocol Formatter, Tagged Stream Mux, Unpack K Bits, Chunks to Symbols, Repeat, Frequency Mod, Throttle, Channel Model, and a QT GUI Frequency Sink"
     style="max-width: 620px; width: 100%; display: block; margin: 0 auto;">
:::

1. **Open your transmitter.** Open the FSK transmitter you built in class, or `L08-fsk-tx.grc` if you do not have it, and save it as `L08-lab-link.grc`. Set `dev` to 1500 (the slider's default, if your `dev` is a slider), and put a line of text of your own in `msg`, in quotes; the receiver you build next has to recover it.
2. **Add the packet front end.** Add a Variable `hdr` = `digital.header_format_default(digital.packet_utils.default_access_code, 0)`. Between the Vector Source and Unpack K Bits, add a byte Stream to Tagged Stream with packet length `len(msg) + 1` and length tag key `"packet_len"`, a Protocol Formatter with format object `hdr`, and a Tagged Stream Mux with 2 inputs, all with the tag name `"packet_len"`. Wire them as the Packets frame of Lesson 8 shows: Stream to Tagged Stream to the formatter and to the mux's second input, and the formatter to the mux's first input.
3. **Add the channel.** After the Throttle, add a Channel Model with noise voltage 0.3 and the other settings at their defaults, and move the QT GUI Frequency Sink to its output. Run it: the spectrum shows two tones above the noise floor, each 1.5 kHz from the center. Every arrow must be black: a red arrow joins two ports of different types, so match that block's type to its neighbor's.
::::

::::{frame} Build the Decoder
:::{present}
- After the Channel Model, build the receiver from Lesson 8: filter, demodulate, find each bit.
- Find each packet and write its bytes to a file.
- Recover your line; screenshot the canvas and the text.
:::
:::{present}
<img src="../../viz/img/L08-canvas-rx.png"
     alt="L08-lab-link.grc with the decoder added after the Channel Model: Low Pass Filter with its cutoff left as cutoff_table_a and Quadrature Demod with its gain left as gain_table_a for your Part 1 values, Moving Average with a QT GUI Eye Sink, Symbol Sync, Binary Slicer, Correlate Access Code - Tag Stream, Repack Bits, and a File Sink writing rx.txt"
     style="max-width: 620px; width: 100%; display: block; margin: 0 auto;">
:::

4. **Filter.** On the Channel Model's output, add a Low Pass Filter of type complex to complex with decimation 1, the cutoff from your Part 1 Table A, and a transition width of 1000.
5. **Demodulate.** Add a Quadrature Demod with the gain from your Part 1 Table A.
6. **Smooth each bit.** Add a float Moving Average with length `sps` and scale `1/sps`, and put a float QT GUI Eye Sink with `sps` samples per symbol on its output.
7. **Find each bit.** Add a float Symbol Sync with the Gardner timing error detector, `sps` samples per symbol, loop bandwidth 0.045, and 1 output sample per symbol, then a Binary Slicer.
8. **Find each packet.** Add Correlate Access Code - Tag Stream with access code `digital.packet_utils.default_access_code`, threshold 2, and tag name `"packet_len"`, then Repack Bits with 1 bit in, 8 bits out, MSB first, and length tag key `"packet_len"`.
9. **Write the text.** Add a byte File Sink with file `rx.txt` and Unbuffered set to On.
10. **Recover your line.** Run it for about 10 s with the eye in view, stop it, and open `rx.txt` in a text editor: your line, once per packet. Take one screenshot of your canvas and the running window side by side, and paste it as Figure 1; paste a screenshot of `rx.txt` as Figure 2. If `rx.txt` is empty, the eye tells you where to look: an eye that never opens points to the cutoff or the gain, and an open eye with no text points to the access code, the tag names, or the bit order.
::::

::::{frame} Frequency Offset at Two Deviations
:::{present}
- Run `L08-fsk-link.grc` and set the offset your Part 1 table names.
- Raise the offset until a line fails, at 1 kHz of deviation.
- Change `dev` to 2000 and search again.
:::
:::{present}
<img src="../../viz/img/L08-canvas-link.png"
     alt="L08-fsk-link.grc in GNU Radio Companion: the transmitter row, a Throttle and a Channel Model, then the receiver from Low Pass Filter, Quadrature Demod, Moving Average, Symbol Sync, and Binary Slicer to Correlate Access Code - Tag Stream, Repack Bits, and the Text Sink, with a frequency sink and an eye sink"
     style="max-width: 620px; width: 100%; display: block; margin: 0 auto;">
:::

11. **Run the link.** Open and run `L08-fsk-link.grc`. Leave **Noise voltage** at 0.5 for the whole lab. The Lines label counts the lines received since a slider last moved.
12. **Read the eye at 600 Hz.** Set **Frequency offset (Hz)** to 600 and read the level the lower traces of the eye settle at between crossings. Compare it with your Part 1 prediction, and paste a screenshot of the window as the left pane of Figure 3.

    <div class="rec" data-lab="L08">
    <label>Step 12: Lower eye level, 1 kHz deviation, 600 Hz offset (normalized) <input data-field="b.low600"></label>
    </div>
13. **Find the limit at 1 kHz.** Raise **Frequency offset (Hz)** 50 Hz at a time, waiting about 20 s at each setting; one line takes about 0.4 s, so 20 s is about 50 lines. The link has failed once the correct count falls behind the received count or the received count stops growing. Record the largest offset at which every line arrived correct, and paste a screenshot at the first offset that failed as the right pane of Figure 3.

    <div class="rec" data-lab="L08">
    <label>Step 13: Largest offset with every line correct, 1 kHz deviation (Hz) <input data-field="b.lim1k"></label>
    </div>
14. **Widen the deviation.** Stop the flowgraph and change the `dev` Variable from 1000 to 2000. The flowgraph computes the Frequency Mod sensitivity, the Low Pass Filter cutoff, and the Quadrature Demod gain from `dev`, so all three change with it.
15. **Find the limit at 2 kHz.** Run it, and repeat Step 13's search, starting from your 1 kHz limit. Record the largest offset at which every line arrived correct.

    <div class="rec" data-lab="L08">
    <label>Step 15: Largest offset with every line correct, 2 kHz deviation (Hz) <input data-field="b.lim2k"></label>
    </div>
16. **Screenshot the failure.** Paste a screenshot of the window at the first offset that failed at 2 kHz as Figure 4.
::::

::::{frame} No Hardware?
:class: read-only

:::{admonition} This lab needs no radio
:class: tip
Every flowgraph here runs on your laptop, and the Channel Model block stands in for the air, so a missing or broken PlutoSDR does not matter today.

If the Received label of `L08-fsk-link.grc` stays at "(waiting for a packet)", close the flowgraph and run it again at a noise voltage of 0.5 and an offset of 0, where every line arrives within a second or two. If it still shows no text, check that you changed only `dev`; the flowgraph computes every other block's setting from `samp_rate` and `sps`.
:::
::::

::::{frame} Your Part 2 Entries
:class: read-only

This frame collects every box you filled in on this page. Your entries stay in this browser only, saved as you type. **Download my packet** writes them into the Measured cells of the blank packet and saves the PDF. The download locks every field, the Predicted cells included, so type your predictions into your own copy of the packet first, then use **Fill my own copy** and choose that file: the page keeps your predictions and adds your measurements beside them. Paste Figures 1 to 4 and write Part 3 in your copy, or on the printout, and upload one PDF to Gradescope. **Export entries** saves a small backup file you can **Import** on another laptop.

<div class="rec-summary" data-lab="L08" data-pdf="../../labs/ECE448_Lab_L08_FSK_blank.pdf" data-file="ECE448_L08_Lab"></div>
::::

::::{frame} Lab Packet
:class: read-only doc-links

The L8 Lab packet is one submission, turned in complete before Lesson 9:

1. Part 1, Predict (individual, before the lab period): the two shaded decoder settings in Table A and the shaded eye level in Table B, with your work attached.
2. Part 2, Measure (in class, on your own laptop): the white Measured cells of Table B, and Figures 1 to 4.
3. Part 3, Analyze (individual, after the lab): two prompts, each answered from your own table and figures.

- <a class="doc-link" href="../../labs/ECE448_Lab_L08_FSK_blank.pdf" target="_blank" rel="noopener">L8 Lab packet (PDF)</a>
- <a class="doc-link" href="../../grc/L08-fsk-link.grc" download>L08-fsk-link.grc</a>, and <a class="doc-link" href="../../grc/L08-fsk-tx.grc" download>L08-fsk-tx.grc</a> if you do not have your class transmitter
::::

::::{frame} For Part 3
:class: read-only

Do Part 3 after class, with your table and figures beside you. It asks about two comparisons:

1. Your two offset limits in Table B, against the eye and the spectrum at the first offset that failed, in Figures 3 and 4.
2. Your two limits, against the frequency accuracy of two PlutoSDRs at 915 MHz, and what changes between the two deviations in Figures 3 and 4.

I grade each answer on a claim, the evidence from your own table and figures, the reasoning that connects them, and the uncertainty in your readings.
::::

::::{frame} Looking Ahead
:class: read-only

Lesson 9 sends each bit as the height of a pulse instead of a frequency: PAM.
::::
