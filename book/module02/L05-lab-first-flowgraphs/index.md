---
frame_view: true
---

# L5 Lab — First Flowgraphs

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">First Flowgraphs</h1>

<div class="title-rule"></div>

Build a tone flowgraph from an empty canvas, then receive, record, and plot the FM band on the PlutoSDR.

L5 Lab · Module 2: SDR & GNU Radio Foundations · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '2'; counter-reset: lo 2">
  <li>I can install GNU Radio and use GNU Radio Companion (GRC) to build, inspect, and run a basic flowgraph.</li>
  <li>I can capture a real RF signal using an SDR and interpret its time- and frequency-domain representations.</li>
</ol>
::::

::::{frame} The Big Picture
:::{present}
| Steps | Set or switched | Read |
| :-- | :-- | :-- |
| 1 to 7 | tone: $+20$, $+30$, $-35$ kHz | spike position |
| 8 to 12 | center 96.5 MHz; gain 0 to 71 dB | band; three views |
| 13 to 17 | SigMF Sink, about 3 s | file size; plot |
:::

Steps 1 to 7 run your own tone flowgraph at a 48 kHz sample rate; Steps 8 to 17 run `L05-fm-spectrum.grc` on the PlutoSDR. Each reading goes beside your Part 1 prediction in Tables A and B of the packet, and the screenshots go in Figures 1 to 3. Nothing in this lab transmits.
::::

::::{frame} Predict First
:class: viz-frame

:::{depth}
Choose a sample rate and set a tone. Before you press **Show where it appears**, mark on the frequency sink where you think the spike will be, by clicking it or with the My Prediction slider. Changing the sample rate, the tone, or your mark hides the answer again, so each guess comes first. The widget offers 32, 40, and 64 kHz, not the 48 kHz of today's flowgraph, so its answers are not your Part 1 answers.
:::

:::{present}
<iframe src="../../viz/alias-predict.html"
        width="100%" height="506"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Choose a sample rate and a tone, mark where the spike will appear on the frequency sink, then show it">
</iframe>
:::
::::

::::{frame} Build the Tone Flowgraph
:::{present}
- Start from an empty QT GUI canvas, not `L05-tone.grc`.
- Set `samp_rate` to 48000; add a slider, source, throttle, and two sinks.
- Run it; screenshot the canvas and the window at $+30$ kHz.
- Read where each tone appears.
:::

This part needs only your laptop.

1. **Start GRC.** Choose File, New, QT GUI. Do not open `L05-tone.grc`; Figure 1 shows the flowgraph you build. If GRC does not open, go back to the lesson's "Verify the Install" frame.
2. **Set the sample rate.** Double-click the `samp_rate` variable and set it to 48000.
3. **Add the slider.** Add a **QT GUI Range** with ID `freq`, from $-72000$ to $72000$ in steps of 250, default 1000.
4. **Add the source.** Add a **Signal Source**: type complex, sample rate `samp_rate`, waveform Cosine, frequency `freq`.
5. **Add the rest and connect.** Add a **Throttle** (complex, `samp_rate`), a **QT GUI Time Sink** (complex), and a **QT GUI Frequency Sink** (complex, bandwidth `samp_rate`). Connect the source to the throttle and the throttle to both sinks. Every connection must be black; a red one is a type mismatch, so check that each block's type is complex.
6. **Run it.** Set the slider to 30 kHz. Take one screenshot that shows your canvas and the running window side by side, and paste it as Figure 1.
7. **Read the tones.** Set the slider to each tone in Table A, read where the spike appears on the frequency sink, and compare with your Part 1 prediction. A computed tone has no noise or hardware in the way, so if a reading disagrees with your prediction, check `samp_rate` and the Signal Source's frequency first.

   <div class="rec" data-lab="L05">
   <label>Step 7: spike frequency for the +20 kHz tone (kHz) <input data-field="a.t20"></label>
   <label>Step 7: spike frequency for the +30 kHz tone (kHz) <input data-field="a.t30"></label>
   <label>Step 7: spike frequency for the −35 kHz tone (kHz) <input data-field="a.tm35"></label>
   </div>
::::

::::{frame} The FM Band and the Gain
:::{present}
- Put the whip on **RX** and run `L05-fm-spectrum.grc`.
- Center on 96.5 MHz and read the band on screen.
- Find the strongest station, off the DC spike.
- Step the RF gain from 0 to 71 dB; screenshot three views.
:::

8. **Connect the PlutoSDR.** Screw the course's broadband whip onto the RX port and plug the Pluto's middle USB port into your laptop. Open and run `L05-fm-spectrum.grc`. The PlutoSDR Source opens the radio at `ip:192.168.2.1`; if you have not switched your Pluto to NCM mode on a Mac, type the `usb:` URI from `iio_info -s` into the PlutoSDR Source instead, as the lesson's "Connect the PlutoSDR" frame shows.
9. **Read the band.** Set the **Center frequency (Hz)** slider to 96.5 MHz, hover the cursor at the left and right ends of the plot to read the lowest and highest frequencies it shows, and compare with your Part 1 prediction.

   <div class="rec" data-lab="L05">
   <label>Step 9: lowest to highest frequency on the display at 96.5 MHz (MHz) <input data-field="b.band"></label>
   </div>
10. **Find the strongest station.** Drag the center frequency slowly from 88 to 108 MHz and stop on the tallest station. Uncheck **DC tracking** and find the spike at the center of the display: it is the receiver's own DC offset, not a station. Check the box again, then tune so that the station sits a little to one side of center, because DC tracking can subtract part of a signal centered at 0 Hz.
11. **Step the gain.** With the station on screen, set the **RF gain (dB)** slider to 0, 20, 40, 60, and 71 dB in turn, and watch the noise floor, the station, and the space between stations at each.
12. **Screenshot three views.** Choose the gain you would use to receive weak stations in this room. Take a screenshot of the display at 0 dB, at your gain, and at 71 dB, with the same station on screen in all three, and paste them as Figure 2.

    <div class="rec" data-lab="L05">
    <label>Step 12: RF gain you chose for weak stations (dB) <input data-field="b.gain"></label>
    </div>
::::

::::{frame} Record and Plot
:::{present}
- Type the center and your gain in as the sliders' defaults.
- Enable the SigMF Sink, run about 3 s, and compare the file size.
- Plot the file with `L05-psd.py`.
:::

13. **Set the defaults.** Stop the flowgraph. Double-click the **Center frequency (Hz)** slider block and type the center frequency of your Figure 2 views as its Default Value, then do the same for the **RF gain (dB)** slider with your gain from Step 12. The SigMF Sink writes the center frequency to the meta file when the run starts, so it has to be right before you press Run.
14. **Enable the SigMF Sink.** Right-click the gray SigMF Sink and choose Enable. Its file name, `fm_capture`, makes `fm_capture.sigmf-data` and `fm_capture.sigmf-meta` in the flowgraph's folder. GRC outlines the block in orange because GNU Radio 3.10 marks it deprecated, but the block records correctly.
15. **Record.** Run the flowgraph for about 3 s and stop it. Read the size of `fm_capture.sigmf-data` in bytes from its file properties, divide by $10^6$ to get MB, and compare with your Part 1 prediction. A file browser's own "MB" may be $2^{20}$ bytes, about 5% larger, so use the byte count. Open `fm_capture.sigmf-meta` in a text editor and check that its center frequency is the one you set.

    <div class="rec" data-lab="L05">
    <label>Step 15: size of fm_capture.sigmf-data (MB) <input data-field="b.size"></label>
    </div>
16. **Disable the sink.** Right-click the SigMF Sink and choose Disable, so the next run does not overwrite the capture.
17. **Plot it.** From the radioconda prompt, in the flowgraph's folder, run `python L05-psd.py fm_capture.sigmf-data`. It reads the sample rate and center frequency from the meta file. Paste the plot as Figure 3.
::::

::::{frame} No Hardware?
:class: read-only

:::{admonition} If your PlutoSDR is missing or will not open
:class: tip
Steps 1 to 7 need no radio. For Steps 8 to 17, work at the laptop of a classmate whose PlutoSDR works, taking turns, and take your own readings, your own screenshots, and your own capture; note whose PlutoSDR you used on the packet's Documentation line. Bring the failed Pluto to EI so it works before the L7 Lab.
:::
::::

::::{frame} Your Part 2 Entries
:class: read-only

This frame collects every box you filled in on this page. Your entries stay in this browser only, saved as you type. **Download my packet** writes them into the Measured cells of the blank packet and saves the PDF. The download locks every field, the Predicted cells included, so type your predictions into your own copy of the packet first, then use **Fill my own copy** and choose that file: the page keeps your predictions and adds your measurements beside them. Paste Figures 1 to 3 and write Part 3 in your copy, or on the printout, and upload one PDF to Gradescope. **Export entries** saves a small backup file you can **Import** on another laptop.

<div class="rec-summary" data-lab="L05" data-pdf="../../labs/ECE448_Lab_L05_FirstFlowgraphs_blank.pdf" data-file="ECE448_L05_Lab"></div>
::::

::::{frame} Lab Packet
:class: read-only doc-links

The L5 Lab packet is one submission, turned in complete before Lesson 6:

1. Part 1, Predict (individual, before the lab period): the shaded Predicted cells of Tables A and B, with your work for one row of each attached.
2. Part 2, Measure (in class, on your own laptop and PlutoSDR): the white Measured cells of the same tables, and Figures 1 to 3.
3. Part 3, Analyze (individual, after the lab): three prompts, each answered from your own tables and figures.

- <a class="doc-link" href="../../labs/ECE448_Lab_L05_FirstFlowgraphs_blank.pdf" target="_blank" rel="noopener">L5 Lab packet (PDF)</a>
- <a class="doc-link" href="../../grc/L05-fm-spectrum.grc" download>L05-fm-spectrum.grc</a> and <a class="doc-link" href="../../grc/L05-psd.py" download>L05-psd.py</a>
::::

::::{frame} For Part 3
:class: read-only

Do Part 3 after class, with your tables and figures beside you. It asks about three comparisons:

1. Table A and Figure 1: your predicted and measured tone positions at 48 kHz.
2. Figure 2: the three gain views, and the gain you chose.
3. Your recording against the live display: the file size against your prediction, and Figure 3 against Figure 2.

I grade each answer on a claim, the evidence from your own tables and figures, the reasoning that connects them, and the uncertainty in your readings.
::::

::::{frame} Looking Ahead
:class: read-only

Keep both capture files: Lesson 7's FM receiver plays `fm_capture.sigmf-data` back through a SigMF Source before it receives the live band.
::::
