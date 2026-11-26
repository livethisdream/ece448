---
frame_view: true
---

# L6 Lab — AM Simulation

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">AM Simulation</h1>

<div class="title-rule"></div>

Build an AM modulator and demodulator and check the audio against the source.

L6 Lab · Module 3: Analog Modulation · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '3'">
  <li>I can describe DSB-AM, DSB-SC, and SSB and identify each on a spectrum.</li>
  <li>I can implement an AM modulator and demodulator in GNU Radio and verify demodulated audio against the source.</li>
</ol>
::::

::::{frame} The Big Picture
:::{present}
<img src="../../viz/img/L06-big-picture.png"
     alt="The L6 Lab's four blocks as a strip, in the lesson's screenshots. Steps 1 to 9: build DSB-AM, shown as the lesson's DSB-AM flowgraph on the GRC canvas. Steps 10 to 12: overmodulate, shown as the detector output leaving the envelope at m = 1.4. Steps 13 to 16: DSB-SC, shown as the coherent receiver and the envelope detector against the message. Steps 17 to 19: SSB, shown as the USB and LSB spectra."
     style="max-width: 980px; width: 100%; display: block; margin: 0 auto;">
:::

Steps 1 to 9 build DSB-AM from an empty canvas with the lab's own message and read its lines. Steps 10 to 12 raise the modulation index $m$ until the detector output leaves the envelope. Steps 13 to 16 run `L06-dsb-sc.grc` with the same message, set the receiver's LO phase, and switch between its two receivers. Steps 17 to 19 run `L06-ssb.grc`, read the LSB lines, and turn the tuning error. The pictures use the lesson's message, not today's. Each reading goes beside your Part 1 prediction in Tables A and B of the packet, and the screenshots go in Figures 1 to 3. Every flowgraph is a simulation, so you need only your laptop and headphones.
::::

::::{frame} Predict First
:class: viz-frame

:::{depth}
Choose a message and read its deepest trough off the top plot. Before you press **Show where it reaches zero**, set the My Prediction slider to the $m$ at which you think the envelope $1 + m\,x(t)$ first touches zero. Changing the message or your prediction hides the answer again, so each guess comes first. The widget offers a single tone and two other pairs, not the lab's 1.5 and 2.25 kHz message, so its answers are not your Part 1 answers.
:::

:::{present}
<iframe src="../../viz/envelope-predict.html"
        width="100%" height="505"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Choose a message, predict the modulation index at which the AM envelope first reaches zero, then show it">
</iframe>
:::
::::

::::{frame} Build DSB-AM
:::{present}
- Start from an empty QT GUI canvas, not `L06-dsb-am.grc`.
- Build the lab's message, the transmitter, and the envelope detector.
- Run it; screenshot the canvas and the window.
- Read the lines on the frequency sink.
:::
:::{present}
<img src="../../viz/img/L06-grc-dsb-am.png"
     alt="The lesson's DSB-AM flowgraph on the GRC canvas: two Signal Sources added into a message, Multiply Const by m, Add Const 1, and a Multiply with a 10 kHz carrier; below, Abs, a Decimating FIR Filter, and Multiply Const pi over 2, then a DC Blocker, a volume control, and an Audio Sink"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

Bring headphones: thirty laptops playing tones at once make the room hard to work in.

1. **Start GRC.** Choose File, New, QT GUI. Do not open `L06-dsb-am.grc`; the lesson's "The DSB-AM Flowgraph" frame shows the flowgraph you build.
2. **Set the variables.** Set `samp_rate` to 48000 and add a Variable `fc` of 10000.
3. **Add the slider.** Add a QT GUI Range with ID `m` and label "Modulation index m", from 0 to 1.5 in steps of 0.05, default 0.5.
4. **Make the message.** Add two float Signal Sources, waveform Cosine, one at 1500 Hz and one at 2250 Hz, each with amplitude 0.5, so that their sum peaks at exactly 1. Feed both into an Add.
5. **Build the transmitter.** Add a Multiply Const of `m`, an Add Const of 1, and a Multiply with a third Signal Source at `fc`. Send the Multiply's output to a float QT GUI Frequency Sink.
6. **Build the receiver.** Add an Abs, a Low-pass Filter Taps variable `lpf_taps` (cutoff 3000, transition 1000) used by a Decimating FIR Filter, and a Multiply Const of `numpy.pi/2` with an Import block for `import numpy`.
7. **Add the check.** Add a Delay of `len(lpf_taps)//2` on the output of the Add Const, and a two-input float QT GUI Time Sink comparing it with the receiver's output.
8. **Add the audio.** Finish with a DC Blocker, a Multiply Const set by a QT GUI Range `vol` from 0 to 1, and an Audio Sink at 48 kHz. Do not add a Throttle: the sound card paces the flowgraph.
9. **Run it and read the lines.** Run it with the volume low. Take one screenshot that shows your canvas and the running window side by side, and paste it as Figure 1. Hover over each line on the frequency sink, read its frequency, and compare with your Part 1 prediction. If a line sits somewhere you did not expect, check the two message Signal Sources first.

   <div class="rec" data-lab="L06">
   <label>Step 9: frequencies of the DSB-AM lines (kHz) <input data-field="a.am"></label>
   </div>
::::

::::{frame} Overmodulate
:::{present}
- Raise $m$ by 0.05 at a time with the audio on.
- Watch the detector output against the delayed envelope.
- Record where they first part; screenshot two views.
:::
:::{present}
<img src="../../viz/img/L06-am-overmod.png"
     alt="The lesson's time sinks at m = 1.4: the envelope dips below zero, and the detector output folds the dips back up, so it no longer matches the envelope"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

10. **Find the point.** With your flowgraph running and the audio on, raise the **Modulation index m** slider by 0.05 at a time from 0.5. On the time sink, find the first value at which the detector output visibly leaves the delayed envelope, and compare with your Part 1 prediction.

    <div class="rec" data-lab="L06">
    <label>Step 10: modulation index at which the detector output first leaves the envelope (unitless) <input data-field="b.mover"></label>
    </div>
11. **Screenshot two views.** Take a screenshot of the time sink at $m = 1.0$ and at $m = 1.5$, and paste them as Figure 2.
12. **Listen.** Sweep $m$ from 0.5 to 1.5 and back, and listen for where the tones change.
::::

::::{frame} Receive DSB-SC
:::{present}
- Run `L06-dsb-sc.grc` with the lab's message.
- Read its lines.
- Set the LO phase to $45°$ and read the coherent output.
- Switch between the coherent and envelope receivers.
:::
:::{present}
<img src="../../viz/img/L06-sc-phi0.png"
     alt="The lesson's DSB-SC time sink with the LO phase at 0 degrees: the coherent receiver's output lies on the message, and the envelope detector's output does not"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

13. **Set the message.** Close your flowgraph. Open `L06-dsb-sc.grc`, set its two message Signal Sources to 1500 Hz and 2250 Hz with amplitude 0.5 each, as in Step 4, and run it.
14. **Read the lines.** Read each line on the transmitted spectrum and compare with your Part 1 prediction.

    <div class="rec" data-lab="L06">
    <label>Step 14: frequencies of the DSB-SC lines (kHz) <input data-field="a.sc"></label>
    </div>
15. **Set the LO phase.** Set the **Receiver LO phase (degrees)** slider to 45. Read the peak of the coherent receiver's trace on the time sink, compare with your Part 1 prediction, and paste a screenshot of the time sink as Figure 3.

    <div class="rec" data-lab="L06">
    <label>Step 15: coherent receiver's peak at an LO phase of 45° (unitless) <input data-field="b.lo45"></label>
    </div>
16. **Listen to both receivers.** Return the LO phase to 0. Switch **Listen to** between Coherent and Envelope, and listen to each.
::::

::::{frame} Receive SSB
:::{present}
- Run `L06-ssb.grc` with the lab's message.
- Select LSB and read its lines.
- Turn the tuning error until you hear the pitch change.
:::
:::{present}
<img src="../../viz/img/L06-ssb-spectra.png"
     alt="The lesson's SSB spectra: with USB selected, the two lines above the carrier remain; with LSB selected, the two lines below it remain"
     style="max-width: 520px; width: 100%; display: block; margin: 0 auto;">
:::

17. **Set the message.** Close the DSB-SC flowgraph. Open `L06-ssb.grc`, set its two message Signal Sources as in Step 13, and run it.
18. **Read the LSB lines.** Choose LSB on the **Sideband** menu. Read the lines that remain and compare with your Part 1 prediction.

    <div class="rec" data-lab="L06">
    <label>Step 18: frequencies of the LSB lines (kHz) <input data-field="a.lsb"></label>
    </div>
19. **Turn the tuning error.** Starting from 0, move the **Receiver tuning error (Hz)** slider one 10 Hz step at a time in each direction, listening after each step. Record the largest error, of either sign, at which the pitch still sounds the same as at 0 Hz; the next step out is the first one where you hear a shift. This is a pitch change, not the point where the tones stop sounding like the message.

    <div class="rec" data-lab="L06">
    <label>Step 19: largest tuning error with no pitch change you can hear (Hz) <input data-field="b.df"></label>
    </div>
::::

::::{frame} No Hardware?
:class: read-only

:::{admonition} If the flowgraph stops with an audio error
:class: tip
Every flowgraph in this lab is a simulation, so the only hardware it needs is your laptop's sound card. An Audio Sink that cannot open it stops the flowgraph with an error such as `audio_alsa_sink` or `audio_portaudio_sink`. Plug in your headphones and run it again, or set the Audio Sink's Device Name to the device your operating system lists. If neither works, disable the Audio Sink and add a Throttle at `samp_rate` before the sinks: every reading still works. For the listening in Steps 12, 16, and 19, work at the laptop of a classmate whose audio works, taking turns, and note whose laptop you used on the packet's Documentation line.
:::
::::

::::{frame} Your Part 2 Entries
:class: read-only

This frame collects every box you filled in on this page. Your entries stay in this browser only, saved as you type. **Download my packet** writes them into the Measured cells of the blank packet and saves the PDF. The download locks every field, the Predicted cells included, so type your predictions into your own copy of the packet first, then use **Fill my own copy** and choose that file: the page keeps your predictions and adds your measurements beside them. Paste Figures 1 to 3 and write Part 3 in your copy, or on the printout, and upload one PDF to Gradescope. **Export entries** saves a small backup file you can **Import** on another laptop.

<div class="rec-summary" data-lab="L06" data-pdf="../../labs/ECE448_Lab_L06_AMSimulation_blank.pdf" data-file="ECE448_L06_Lab"></div>
::::

::::{frame} Lab Packet
:class: read-only doc-links

The L6 Lab packet is one submission, turned in complete before Lesson 7:

1. Part 1, Predict (individual, before the lab period): the shaded Predicted cells of Tables A and B, with your work for one row of each attached.
2. Part 2, Measure (in class, on your own laptop): the white Measured cells of the same tables, and Figures 1 to 3.
3. Part 3, Analyze (individual, after the lab): three prompts, each answered from your own tables and figures.

- <a class="doc-link" href="../../labs/ECE448_Lab_L06_AMSimulation_blank.pdf" target="_blank" rel="noopener">L6 Lab packet (PDF)</a>
- <a class="doc-link" href="../../grc/L06-dsb-sc.grc" download>L06-dsb-sc.grc</a> and <a class="doc-link" href="../../grc/L06-ssb.grc" download>L06-ssb.grc</a>
::::

::::{frame} For Part 3
:class: read-only

Do Part 3 after class, with your tables and figures beside you. It asks about three comparisons:

1. Table A: your predicted and measured lines for DSB-AM, DSB-SC, and LSB.
2. Table B and Figure 2: your predicted and measured overmodulation point, with what you heard on the Envelope setting in Step 16.
3. Table B and Figure 3: the LO phase reading, against the tuning error you could not hear in Step 19.

I grade each answer on a claim, the evidence from your own tables and figures, the reasoning that connects them, and the uncertainty in your readings.
::::

::::{frame} Looking Ahead
:class: read-only

Keep your DSB-AM flowgraph: Lesson 7's AM receiver keeps its low-pass filter and DC Blocker and replaces the Abs with Complex to Mag, because a PlutoSDR delivers complex samples with the carrier already at 0 Hz.
::::
