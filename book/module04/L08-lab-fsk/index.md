---
frame_view: true
---

# L8 Lab — FSK

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">FSK</h1>

<div class="title-rule"></div>

Decode an FSK recording whose tones and baud you find yourself, then find how much frequency offset the link tolerates.

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
     alt="The L8 Lab's three blocks as GNU Radio Companion canvases: the flowgraph that reads the recording (Steps 1 to 4) beside the decoder you build (Steps 5 to 11), and L08-fsk-link.grc below (Steps 12 to 17)."
     style="max-width: 860px; width: 100%; display: block; margin: 0 auto;">
:::

Steps 1 to 4 play `L08-lab-unknown.sigmf-data`, a recording from a transmitter like your class one with its own baud rate and tones, and read those off a spectrum and a demodulator. Steps 5 to 11 build a decoder from Lesson 8's blocks with those settings and recover the recording's message into a file. Steps 12 to 17 run `L08-fsk-link.grc` at a fixed noise voltage and raise the Frequency offset slider, first at 1 kHz of deviation and then at 2 kHz, watching the eye and the Lines label. Your Part 1 prediction goes with Step 13, the readings and the message go in Tables A and B of the packet, and the screenshots go in Figures 1 to 4. Nothing in this lab transmits.
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

::::{frame} Read the Recording
:::{present}
- Play `L08-lab-unknown.sigmf-data` into a spectrum and a demodulator.
- Read its two tone frequencies and its symbol rate.
- Set `f_center`, `dev`, and `baud` from them.
:::
:::{present}
<img src="../../viz/img/L08-canvas-view.png"
     alt="The flowgraph that reads the recording, in GNU Radio Companion: File Source on L08-lab-unknown.sigmf-data, Throttle, a QT GUI Frequency Sink, and a Quadrature Demod feeding a QT GUI Time Sink"
     style="max-width: 520px; width: 100%; display: block; margin: 0 auto;">
:::

The recording comes from a transmitter like the one you built in class, with the same packets, but with a baud rate and tone frequencies of its own. Your job is to recover its message.

1. **Read the meta file.** Put `L08-lab-unknown.sigmf-data` and `L08-lab-unknown.sigmf-meta` from the Lab Packet frame in one folder, open the `.sigmf-meta` in a text editor, and note `core:sample_rate`. The samples are complex float, the type GNU Radio calls complex.
2. **Find the tones.** In GRC choose File, New, QT GUI, and save the flowgraph as `L08-lab-decoder.grc` in that folder. Set `samp_rate` to the sample rate, and add a complex File Source on the `.sigmf-data` with Repeat set to Yes, a complex Throttle at `samp_rate`, and a complex QT GUI Frequency Sink with bandwidth `samp_rate`. Run it and read the frequencies of the two tones; the two tracks need not sit evenly about 0.

    <div class="rec" data-lab="L08">
    <label>Step 2: The two tone frequencies (Hz) <input data-field="b.tones"></label>
    </div>
3. **Find the symbol rate.** Add a Quadrature Demod with gain 1 on the Throttle's output and a float QT GUI Time Sink on its output, with 2048 points at `samp_rate`. The output jumps between two levels; zoom in with the mouse until you can read the shortest stay at one level, which is one bit, and take the symbol rate as one over its length, as Lesson 8's "FSK on a Real Radio" does.

    <div class="rec" data-lab="L08">
    <label>Step 3: The symbol rate (baud) <input data-field="b.baud"></label>
    </div>
4. **Name the settings.** Add three Variables: `f_center`, the midpoint of the two tones; `dev`, half their spacing; and `baud`, the symbol rate. Every decoder setting below comes from these three, so a mistake here shows up everywhere downstream.
::::

::::{frame} Build the Decoder
:::{present}
- Shift the midpoint to 0 and filter: a Frequency Xlating FIR Filter.
- Then Lesson 8's receiver, with your three Variables in every setting.
- Recover the message; screenshot the canvas and the text.
:::
:::{present}
<img src="../../viz/img/L08-canvas-decoder.png"
     alt="L08-lab-decoder.grc in GNU Radio Companion: File Source, Throttle, Frequency Xlating FIR Filter, Quadrature Demod, Moving Average with a QT GUI Eye Sink, Symbol Sync, Binary Slicer, Correlate Access Code - Tag Stream, Repack Bits, and a File Sink writing rx.txt; the blocks that use f_center, dev, and baud show red until those Variables exist"
     style="max-width: 620px; width: 100%; display: block; margin: 0 auto;">
:::

5. **Shift and filter.** Disable the Quadrature Demod and the Time Sink from Step 3, and on the Throttle's output add a Frequency Xlating FIR Filter, the block Lesson 7's receiver used, with decimation 1, center frequency `f_center`, and taps `firdes.low_pass(1, samp_rate, dev + baud, 1000)`. It moves the midpoint of the two tones to 0 and keeps the band Lesson 8's receive filter keeps.
6. **Demodulate.** Add a Quadrature Demod whose gain turns a tone at `+dev` into an output of 1, written in terms of `samp_rate` and `dev`, as in Lesson 8's "The Quadrature Demodulator".
7. **Smooth each bit.** One bit lasts `samp_rate/baud` samples, which need not be a whole number. Add a float Moving Average with length `round(samp_rate/baud)` and scale `1/round(samp_rate/baud)`, and put a float QT GUI Eye Sink with `round(samp_rate/baud)` samples per symbol on its output.
8. **Find each bit.** Add a float Symbol Sync with the Gardner timing error detector, `samp_rate/baud` samples per symbol, loop bandwidth 0.045, and 1 output sample per symbol, then a Binary Slicer.
9. **Find each packet.** Add Correlate Access Code - Tag Stream with access code `digital.packet_utils.default_access_code`, threshold 2, and tag name `"packet_len"`, then Repack Bits with 1 bit in, 8 bits out, MSB first, and length tag key `"packet_len"`.
10. **Write the text.** Add a byte File Sink with file `rx.txt` and Unbuffered set to On. Every arrow must be black: a red arrow joins two ports of different types, so match that block's type to its neighbor's.
11. **Recover the message.** Run it for about 10 s with the eye in view, stop it, and open `rx.txt` in a text editor. Record the message, take one screenshot of your canvas and the running window side by side for Figure 1, and paste a screenshot of `rx.txt` as Figure 2. If `rx.txt` is empty, the eye tells you where to look: an eye that never opens points to `f_center`, `dev`, or the gain, an eye that smears points to `baud`, and an open eye with no text points to the access code, the tag names, or the bit order.

    <div class="rec" data-lab="L08">
    <label>Step 11: The recovered message (text) <input data-field="b.msg"></label>
    </div>
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

12. **Run the link.** Open and run `L08-fsk-link.grc`. Leave **Noise voltage** at 0.5 for the whole lab. The Lines label counts the lines received since a slider last moved.
13. **Read the eye at 600 Hz.** Set **Frequency offset (Hz)** to 600 and read the level the lower traces of the eye settle at between crossings. Compare it with your Part 1 prediction, and paste a screenshot of the window as the left pane of Figure 3.

    <div class="rec" data-lab="L08">
    <label>Step 13: Lower eye level, 1 kHz deviation, 600 Hz offset (normalized) <input data-field="b.low600"></label>
    </div>
14. **Find the limit at 1 kHz.** Raise **Frequency offset (Hz)** 50 Hz at a time, waiting about 20 s at each setting; one line takes about 0.4 s, so 20 s is about 50 lines. The link has failed once the correct count falls behind the received count or the received count stops growing. Record the largest offset at which every line arrived correct, and paste a screenshot at the first offset that failed as the right pane of Figure 3.

    <div class="rec" data-lab="L08">
    <label>Step 14: Largest offset with every line correct, 1 kHz deviation (Hz) <input data-field="b.lim1k"></label>
    </div>
15. **Widen the deviation.** Stop the flowgraph and change the `dev` Variable from 1000 to 2000. The flowgraph computes the Frequency Mod sensitivity, the Low Pass Filter cutoff, and the Quadrature Demod gain from `dev`, so all three change with it.
16. **Find the limit at 2 kHz.** Run it, and repeat Step 14's search, starting from your 1 kHz limit. Record the largest offset at which every line arrived correct.

    <div class="rec" data-lab="L08">
    <label>Step 16: Largest offset with every line correct, 2 kHz deviation (Hz) <input data-field="b.lim2k"></label>
    </div>
17. **Screenshot the failure.** Paste a screenshot of the window at the first offset that failed at 2 kHz as Figure 4.
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

1. Part 1, Predict (individual, before the lab period): the shaded eye level in Table B, with your work attached.
2. Part 2, Measure (in class, on your own laptop): the white Measured cells of Tables A and B, and Figures 1 to 4.
3. Part 3, Analyze (individual, after the lab): two prompts, each answered from your own table and figures.

- <a class="doc-link" href="../../labs/ECE448_Lab_L08_FSK_blank.pdf" target="_blank" rel="noopener">L8 Lab packet (PDF)</a>
- <a class="doc-link" href="../../grc/L08-lab-unknown.sigmf-data" download>L08-lab-unknown.sigmf-data</a> and <a class="doc-link" href="../../grc/L08-lab-unknown.sigmf-meta" download>L08-lab-unknown.sigmf-meta</a>, the recording you decode
- <a class="doc-link" href="../../grc/L08-fsk-link.grc" download>L08-fsk-link.grc</a>
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
