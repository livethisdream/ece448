---
frame_view: true
---

# L8 Lab — FSK

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">FSK</h1>

<div class="title-rule"></div>

Build an FSK transmitter, then find how much frequency offset the link takes at two deviations.

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
     alt="The L8 Lab's two blocks as GNU Radio Companion canvases: above, the FSK transmitter you build (Steps 1 to 7); below, L08-fsk-link.grc, the transmitter, Channel Model, and receiver (Steps 8 to 13)."
     style="max-width: 860px; width: 100%; display: block; margin: 0 auto;">
:::

Steps 1 to 7 build the FSK transmitter from an empty canvas and run it at 2 kHz of deviation. Steps 8 to 13 run `L08-fsk-link.grc` at a fixed noise voltage and raise the Frequency offset slider, first at 1 kHz of deviation and then at 2 kHz, watching the eye and the Lines label. Your Part 1 sensitivity goes into Step 5, the three readings go in Table B of the packet, and the screenshots go in Figures 1 to 3. Nothing in this lab transmits.
::::

::::{frame} Predict First
:class: viz-frame

:::{depth}
Choose a deviation and a frequency offset. The dashed blue lines are the eye's two levels with no offset. Before you press **Show the eye**, set the My Prediction slider to where you think the lower level will sit. Changing either setting or your guess hides the answer again, so each guess comes first. The widget's settings are not the lab's, so nothing here is a reading you record.
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

::::{frame} Build the FSK Transmitter
:::{present}
- Start from an empty QT GUI canvas, not `L08-fsk-tx.grc`.
- Set the deviation to 2 kHz and type your Part 1 sensitivity into Frequency Mod.
- Run it; screenshot the canvas and the spectrum.
:::
:::{present}
<img src="../../viz/img/L08-canvas-tx.png"
     alt="The transmitter you build, as GNU Radio Companion shows it: Vector Source, Unpack K Bits, Chunks to Symbols, Repeat, Frequency Mod with its sensitivity left as k_table_a for your Part 1 value, Throttle, and QT GUI Frequency Sink"
     style="max-width: 620px; width: 100%; display: block; margin: 0 auto;">
:::

1. **Start GRC.** Choose File, New, QT GUI, and save the flowgraph in the folder that holds the two Lesson 8 flowgraphs. Do not open `L08-fsk-tx.grc`; build it yourself.
2. **Add the variables.** Set `samp_rate` to 32000. Add a Variable `sps` of 32, a Variable `dev` of 2000, and a Variable `msg` holding a line of text of your own, in quotes.
3. **Add the source.** Add a Vector Source of type byte with vector `list(msg.encode()) + [10]` and Repeat set to Yes.
4. **Turn bytes into symbols.** Add Unpack K Bits with K = 8, then Chunks to Symbols with input byte, output float, and symbol table `[-1, 1]`.
5. **Add the modulator.** Add a float Repeat with interpolation `sps`, then a Frequency Mod with the sensitivity from your Part 1 Table A.
6. **Add the display.** Add a complex Throttle at `samp_rate` and a complex QT GUI Frequency Sink with bandwidth `samp_rate`, and connect the chain. Every arrow must be black.
7. **Run it.** The spectrum should show one peak each side of zero, each `dev` from the center. If the peaks sit somewhere else, check the sensitivity you typed first. Take one screenshot that shows your canvas and the running window side by side, and paste it as Figure 1.
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

8. **Run the link.** Open and run `L08-fsk-link.grc`. Leave **Noise voltage** at 0.5 for the whole lab. The Lines label counts the lines received since a slider last moved, and one line takes about 0.4 s, so 20 s is about 50 lines.
9. **Read the eye at 600 Hz.** Set **Frequency offset (Hz)** to 600 and read the level the lower traces of the eye settle at between crossings. Compare it with your Part 1 prediction, and paste a screenshot of the window as the left pane of Figure 2.

    <div class="rec" data-lab="L08">
    <label>Step 9: Lower eye level at a 600 Hz offset (normalized) <input data-field="b.low600"></label>
    </div>
10. **Find the limit at 1 kHz.** Raise **Frequency offset (Hz)** 50 Hz at a time, waiting about 20 s at each step. The link has failed once the correct count falls behind the received count or the received count stops growing. Record the largest offset at which every line arrived correct, and paste a screenshot at the first offset that failed as the right pane of Figure 2.

    <div class="rec" data-lab="L08">
    <label>Step 10: Largest offset with every line correct, 1 kHz deviation (Hz) <input data-field="b.lim1k"></label>
    </div>
11. **Widen the deviation.** Stop the flowgraph and change the `dev` Variable from 1000 to 2000. The Frequency Mod sensitivity, the Low Pass Filter cutoff, and the Quadrature Demod gain are all written in terms of `dev`, so all three follow it.
12. **Find the limit at 2 kHz.** Run it, and repeat Step 10's search from an offset of 0. Record the largest offset at which every line arrived correct.

    <div class="rec" data-lab="L08">
    <label>Step 12: Largest offset with every line correct, 2 kHz deviation (Hz) <input data-field="b.lim2k"></label>
    </div>
13. **Screenshot the failure.** Paste a screenshot of the window at the first offset that failed at 2 kHz as Figure 3.
::::

::::{frame} No Hardware?
:class: read-only

:::{admonition} This lab needs no radio
:class: tip
Every flowgraph here runs on your laptop, and the Channel Model block stands in for the air, so a missing or broken PlutoSDR does not matter today.

If the Received label stays at "(waiting for a packet)", close the flowgraph and run it again at a noise voltage of 0.5 and an offset of 0, where every line arrives within a second or two. If it still shows no text, check that you changed only `dev`: the transmitter and the receiver share `samp_rate`, `sps`, and `dev`, and a change to `sps` alone breaks the receiver's timing.
:::
::::

::::{frame} Your Part 2 Entries
:class: read-only

This frame collects every box you filled in on this page. Your entries stay in this browser only, saved as you type. **Download my packet** writes them into the Measured cells of the blank packet and saves the PDF. The download locks every field, the Predicted cells included, so type your predictions into your own copy of the packet first, then use **Fill my own copy** and choose that file: the page keeps your predictions and adds your measurements beside them. Paste Figures 1 to 3 and write Part 3 in your copy, or on the printout, and upload one PDF to Gradescope. **Export entries** saves a small backup file you can **Import** on another laptop.

<div class="rec-summary" data-lab="L08" data-pdf="../../labs/ECE448_Lab_L08_FSK_blank.pdf" data-file="ECE448_L08_Lab"></div>
::::

::::{frame} Lab Packet
:class: read-only doc-links

The L8 Lab packet is one submission, turned in complete before Lesson 9:

1. Part 1, Predict (individual, before the lab period): the shaded sensitivity in Table A and the shaded eye level in Table B, with your work attached.
2. Part 2, Measure (in class, on your own laptop): the white Measured cells of Table B, and Figures 1 to 3.
3. Part 3, Analyze (individual, after the lab): two prompts, each answered from your own table and figures.

- <a class="doc-link" href="../../labs/ECE448_Lab_L08_FSK_blank.pdf" target="_blank" rel="noopener">L8 Lab packet (PDF)</a>
- <a class="doc-link" href="../../grc/L08-fsk-link.grc" download>L08-fsk-link.grc</a>
::::

::::{frame} For Part 3
:class: read-only

Do Part 3 after class, with your table and figures beside you. It asks about two comparisons:

1. Your two offset limits in Table B, against the eye and the spectrum at each limit in Figures 2 and 3.
2. Your two limits, against the frequency accuracy of two PlutoSDRs at 915 MHz, and the band each deviation takes in Figures 1 and 2.

I grade each answer on a claim, the evidence from your own table and figures, the reasoning that connects them, and the uncertainty in your readings.
::::

::::{frame} Looking Ahead
:class: read-only

Lesson 9 sends each bit as the height of a pulse instead of a frequency: PAM.
::::
