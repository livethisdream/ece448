---
frame_view: true
---

# L11 Lab — Custom Block

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">Custom Block</h1>

<div class="title-rule"></div>

Work out a keyed recording's code, write the block that reads it, and write the encoder that sends your own line.

L11 Lab · Module 5: Custom Blocks & Midterm · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '5'">
  <li>I can create a GNU Radio out-of-tree (OOT) module and add a custom Python block to it.</li>
  <li>I can implement a custom signal-processing block from scratch and integrate it into a GNU Radio flowgraph.</li>
</ol>
::::

::::{frame} The Big Picture
:::{present}
<img src="../../viz/img/L11-big-picture.png"
     alt="The L11 Lab's three blocks, top to bottom: L11-lab-rx.grc in GNU Radio Companion, with a File Source, Throttle, Energy Detector, two time sinks, the sliders, and a Key Decoder whose work() is empty (Steps 1 to 8); the gr-l11lab files the module steps edit (Steps 9 to 14); and L11-lab-link.grc, with a Key Encoder whose make_key() is empty, noise, and the same receiver (Steps 15 to 18)."
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::

Steps 1 to 4 run `L11-lab-rx.grc` on `L11-lab-remote.sigmf-data`, a simulated on-off keyed transmitter at 915 MHz that sends one line of text four times, and read the code it uses off the Energy Detector's key. Steps 5 to 8 write the `work()` of the flowgraph's Key Decoder, an Embedded Python Block, until the line comes through. Steps 9 to 14 move the block into a module of your own with a unit test. Steps 15 to 18 write the transmitter's half, a Key Encoder that sends your own line in the same code, and get that line through noise to your block. Your Part 1 answers go with Steps 4 and 6, the entries go in Tables A and B of the packet, and the screenshots go in Figures 1 to 4.
::::

::::{frame} Predict First
:class: viz-frame

:::{depth}
Each key sends two characters after a long silence. In some keys the length of each mark carries the bit and every space is short; in others every mark is short and the length of the space after it carries the bit. Choose where you think the bit is and which length is a 0, then press **Show the bytes**. Changing the key or either choice hides the answer again. Each kind of key appears once with a short 0 and once with a long 0, and the lab's lengths are different, so the same reasoning finds the lab's 0 and the widget does not. A wrong choice reads as characters outside ASCII, the symptom Step 8 names.
:::

:::{present}
<iframe src="../../viz/key-code-predict.html"
        width="100%" height="390"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="A key: choose whether the mark or the space carries the bit and which length is a 0, then show the bits and the text">
</iframe>
:::
::::

::::{frame} Run the Broken Chain
:::{present}
- Run `L11-lab-rx.grc` on the recording: the key comes through, the text does not.
- Freeze and zoom the key, and read the lengths of its marks and spaces.
- Work out which part carries the bits, and which length is a 0.
:::
:::{present}
<img src="../../viz/img/L11-canvas-rx.png"
     alt="L11-lab-rx.grc in GNU Radio Companion: File Source on L11-lab-remote.sigmf-data, Throttle, and the Energy Detector, whose power output goes to a time sink with the on and off levels and whose key output goes to a second time sink and to the Key Decoder"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

1. **Run the chain.** Put `L11-lab-remote.sigmf-data`, `L11-lab-remote.sigmf-meta`, and `L11-lab-rx.grc` from the Lab Packet frame in one folder, open the flowgraph in GRC, and run it. The Energy Detector is the Lesson 11 block, here as an Embedded Python Block so the flowgraph runs on any laptop. The Received label stays at "(nothing decoded)".
2. **Check the key.** Every burst on the Power plot should be one mark on the Key plot. If the key stays on or misses bursts, set the **Threshold (dB)** slider halfway between the floor and the bursts, as in Lesson 11's "Setting the Levels".
3. **Read the lengths.** Middle-click the Key plot and choose **Stop** to freeze it, then drag a box to zoom in on a few dozen marks; the time axis is in milliseconds. Read the length of each kind of mark and each kind of space, including the long silence between two sendings of the line. Paste a screenshot of the zoomed key as Figure 1.

    <div class="rec" data-lab="L11">
    <label>Step 3: Mark lengths you see (ms) <input data-field="a.marks"></label>
    <label>Step 3: Space lengths you see (ms) <input data-field="a.spaces"></label>
    </div>
4. **Work out the code.** Decide whether the mark or the space carries the bit, and use your Part 1 answer about the first bit of every character to decide which length is a 0. Count bits from the end of the long silence, eight per character, to find where each character starts.

    <div class="rec" data-lab="L11">
    <label>Step 4: What carries a 0 (text) <input data-field="a.zero"></label>
    </div>
::::

::::{frame} Write the Decoder
:::{present}
- Turn the lengths into key samples at the key's own rate.
- Write `work()`: a bit from each length, eight bits per character.
- Recover the line; screenshot your code beside the running window.
:::
:::{present}
<img src="../../viz/img/L11-decoder-props.png"
     alt="The Key Decoder's properties dialog in GNU Radio Companion once boundary and gap are arguments of __init__(): an Open in Editor button and Boundary and Gap fields, here holding placeholder zeros"
     style="max-width: 480px; width: 100%; display: block; margin: 0 auto;">
:::

5. **Choose the limits.** The key runs at `samp_rate / decim` samples per second, so convert your Step 3 lengths to key samples. Choose a **boundary** that splits the two lengths of the part that carries the bit, and a **gap**, longer than any length inside a line and shorter than the silence between lines, that tells your block a line has ended.

    <div class="rec" data-lab="L11">
    <label>Step 5: Boundary and gap (key samples) <input data-field="a.bnd"></label>
    </div>
6. **Write work().** Double-click the Key Decoder and press **Open in Editor**. Add `boundary` and `gap` to `__init__()` as arguments. Write `work()` so it counts how long the key holds each level, decides one bit each time the part that carries a bit ends, builds each character from eight bits, most significant first, and sets `self.line` when a line ends. Keep in `self` everything your Part 1 list says must survive from one call of `work()` to the next. Save, and enter your Step 5 values in the block's properties, where GRC now shows the two arguments.
7. **Recover the line.** Run the flowgraph. The Received label shows the line once the first sending ends, about 1.4 s in; the line ends with a newline, byte 10, as in Lesson 10. Record the line, and paste a screenshot of your `work()` beside the running window as Figure 2.

    <div class="rec" data-lab="L11">
    <label>Step 7: The recovered line (text) <input data-field="a.msg"></label>
    </div>
8. **Fix the decoder if the text is wrong.** Characters that are all outside ASCII point to the bit decision, since a reversed decision puts a 1 first and makes every byte 128 or more. Characters that go wrong from some point on, or one bit too many or too few at the end of a line, point to where your block starts a character or counts bits. Nothing at all points to the gap or to the code that sets `self.line`. A Python error appears in GRC's console at the bottom of the window, with the line number.
::::

::::{frame} Put It in a Module
:::{present}
- Make `gr-l11lab` with `gr_modtool`, and add a sink block, `key_decoder`.
- Move your class in, fill in the YAML file, and write a unit test.
- Build, test, install, and swap your block into the receiver.
:::
:::{present}
<img src="../../viz/img/L11-lab-tree.svg"
     alt="The gr-l11lab files the steps edit: grc/l11lab_key_decoder.block.yml in Step 11; python/l11lab/key_decoder.py in Step 10; qa_key_decoder.py in Step 12; python/l11lab/CMakeLists.txt, whose gr_python_install line must list key_decoder.py, in Step 10; and build/ for cmake, ctest, and install in Step 13"
     style="max-width: 640px; width: 100%; display: block; margin: 0 auto;">
:::

9. **Make the module.** On a Windows laptop without WSL2, do Steps 9 to 14 on another cadet's Linux, macOS, or WSL2 laptop and note it on the Documentation line. In a new folder at the radioconda prompt, run `gr_modtool newmod l11lab`, `cd gr-l11lab`, and `gr_modtool add -t sink -l python key_decoder`. Give your name as the copyright holder and your two arguments with their Step 5 values as the argument list, and answer yes when `gr_modtool` asks whether to add Python QA code.
10. **Move the class in.** Copy your class from the Embedded Python Block into `python/l11lab/key_decoder.py`, named `key_decoder` instead of `blk`, and check that the `gr_python_install(FILES ...)` line of `python/l11lab/CMakeLists.txt` lists `key_decoder.py`, as Lesson 11's "The Module Tree" warns. Without it, the module installs without your block and Python reports a `ModuleNotFoundError`.
11. **Fill in the YAML file.** In `grc/l11lab_key_decoder.block.yml`, give the block the label Key Decoder, a `make` template with both arguments, an `int` parameter for each, and one `float` input, as in Lesson 11's "The Block's YAML File".
12. **Write the test.** In `python/l11lab/qa_key_decoder.py`, replace the template's test with one that builds the key for a short word of your own in the lab's code, at the key's own rate, runs it from a Vector Source into your block, and checks `last_line()`. End the key with a silence longer than your gap, so your block knows the line has ended.
13. **Build and test.** Build, run `ctest --output-on-failure`, and install, as in Lesson 11's "Build, Test, and Install", then restart GRC, which reads its block library only when it starts. Paste your test's key lines and the `ctest` output as Figure 3.
14. **Swap it in.** In `L11-lab-rx.grc`, disable the Embedded Key Decoder, add your **Key Decoder** from the L11 Lab category of the block library, and set its ID to `decoder`: the Function Probe behind the Received label reads the block with that ID. Connect the key to it and run, and the line arrives as before. If the block is missing from the library, check that you installed from the same radioconda prompt that runs GRC.
::::

::::{frame} Send Your Own Line
:::{present}
- Put your module's block in `L11-lab-link.grc`.
- Write the Key Encoder's `make_key()` to send your own line in the lab's code.
- The link adds noise: diagnose why the line does not arrive, and fix it.
:::
:::{present}
<img src="../../viz/img/L11-canvas-link.png"
     alt="L11-lab-link.grc in GNU Radio Companion: a Key Encoder feeds Float To Complex and a Multiply with a Signal Source to make the keyed carrier; a Noise Source and Add put it in noise; a Throttle feeds the Energy Detector, whose outputs go to the power and key time sinks and to the Key Decoder"
     style="max-width: 620px; width: 100%; display: block; margin: 0 auto;">
:::

15. **Open the link.** Open `L11-lab-link.grc`, disable its Embedded Key Decoder, and add your Key Decoder with ID `decoder` and your Step 5 values, as in Step 14.
16. **Write the encoder.** Double-click the **Key Encoder** and open it in the editor. Write `make_key()` so it returns the key for `msg` and its newline, one entry per unit of your code, 1 for a mark and 0 for a space, ending with the silence between sendings. Set **Samples per unit** to the number of 24 kHz samples in one unit of your code, set the `msg` variable to a line of your own, up to 40 characters, and run it.
17. **Diagnose.** With the **Noise amplitude** slider where it opens, your line does not arrive. Use the Power and Key plots to work out why, and paste a screenshot of the window, with your `make_key()` beside it, as the left pane of Figure 4.
18. **Fix it.** Change what your diagnosis points to, in the sliders or in your block, until the Received label shows your line on every sending you watch for 20 s, with no garbled line between. Record what you changed, and paste a screenshot as the right pane of Figure 4.

    <div class="rec" data-lab="L11">
    <label>Step 18: What brought your line through (text) <input data-field="b.fix"></label>
    </div>
::::

::::{frame} No Hardware?
:class: read-only

:::{admonition} This lab needs no radio
:class: tip
Every flowgraph here runs on your laptop from the recording or from a simulated link, and nothing transmits, so a missing or broken PlutoSDR does not matter today.
:::
::::

::::{frame} Your Part 2 Entries
:class: read-only

This frame collects every box you filled in on this page. Your entries stay in this browser only, saved as you type. **Download my packet** writes them into the Measured cells of the blank packet and saves the PDF. The download locks every field, the Predicted cells included, so type your Part 1 answers into your own copy of the packet first, then use **Fill my own copy** and choose that file: the page keeps your answers and adds your entries beside them. Paste Figures 1 to 4 and write Part 3 in your copy, or on the printout, and upload one PDF to Gradescope. **Export entries** saves a small backup file you can **Import** on another laptop.

<div class="rec-summary" data-lab="L11" data-pdf="../../labs/ECE448_Lab_L11_CustomBlock_blank.pdf" data-file="ECE448_L11_Lab"></div>
::::

::::{frame} Lab Packet
:class: read-only doc-links

The L11 Lab packet is one submission, turned in complete by the Gradescope date, before the midterm:

1. Part 1, Predict (individual, before the lab period): the two shaded entries, with your reasoning.
2. Part 2, Measure (in class, on your own laptop): the white cells of Tables A and B, and Figures 1 to 4.
3. Part 3, Analyze (individual, after the lab): three prompts, each answered from your own tables, code, and figures.

- <a class="doc-link" href="../../labs/ECE448_Lab_L11_CustomBlock_blank.pdf" target="_blank" rel="noopener">L11 Lab packet (PDF)</a>
- <a class="doc-link" href="../../grc/L11-lab-remote.sigmf-data" download>L11-lab-remote.sigmf-data</a> and <a class="doc-link" href="../../grc/L11-lab-remote.sigmf-meta" download>L11-lab-remote.sigmf-meta</a>, the recording you decode
- <a class="doc-link" href="../../grc/L11-lab-rx.grc" download>L11-lab-rx.grc</a>: the receiver, with the Key Decoder's `work()` empty
- <a class="doc-link" href="../../grc/L11-lab-link.grc" download>L11-lab-link.grc</a>: the link, with the Key Encoder's `make_key()` and the Key Decoder's `work()` empty
::::

::::{frame} For Part 3
:class: read-only

Do Part 3 after class, with your tables, code, and figures beside you. It asks about three things:

1. How your block in Figure 2 turns the key in Figure 1 into characters, what it does when a mark or space spans two calls of `work()`, and what your test in Figure 3 leaves unchecked.
2. Whether the receivers of Lessons 8 and 10 could have read the key in Figure 1, and what your block does differently.
3. The two panes of Figure 4: what kept your line from arriving, and where the fix belongs.

I grade each answer on a claim, the evidence from your own tables, code, and figures, the reasoning that connects them, and the uncertainty in your readings.
::::

::::{frame} Looking Ahead
:class: read-only

Lesson 12 receives Morse code, another key whose meaning is in its timing.
::::
