---
frame_view: true
---

# L11 Lab — Custom Block

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">Custom Block</h1>

<div class="title-rule"></div>

Work out a keyed recording's code, write the block that reads it, and send your own line through it.

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
     alt="The L11 Lab's blocks: L11-lab-rx.grc in GNU Radio Companion, with a File Source, Throttle, Energy Detector, two time sinks, and an empty Key Decoder (Steps 1 to 8); the module steps, gr_modtool, the YAML file, a unit test, and ctest (Steps 9 to 14); and L11-lab-link.grc, which makes the same code from your own line in noise (Steps 15 to 17)."
     style="max-width: 860px; width: 100%; display: block; margin: 0 auto;">
:::

Steps 1 to 4 run `L11-lab-rx.grc` on `L11-lab-remote.sigmf-data`, a Simulated on-off keyed transmitter at 915 MHz that sends one line of text four times, and read the code it uses off the Energy Detector's key. The flowgraph's Key Decoder has an empty `work()`, so the Received label stays at "(nothing decoded)". Steps 5 to 8 write that `work()` as an Embedded Python Block until the line comes through. Steps 9 to 14 move the block into a module of your own with a unit test. Steps 15 to 17 put your block in `L11-lab-link.grc`, which sends your own line in the same code through noise, and get the line through. Your Part 1 answers go with Steps 4 to 6, the entries go in Tables A and B of the packet, and the screenshots go in Figures 1 to 4. Nothing in this lab transmits.
::::

::::{frame} Predict First
:class: viz-frame

:::{depth}
Each recording sends two characters in a pulse-width code: every bit is a mark of one of two lengths, then a short space. Choose which mark you think is a 0, then press **Show the bytes**. Changing the recording or your choice hides the answer again. The recordings do not all use the same mark for a 0, and the lab's code is a different one, so the method carries over and the answer does not.
:::

:::{present}
<iframe src="../../viz/key-code-predict.html"
        width="100%" height="380"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="A key in a pulse-width code: choose which mark length is a 0, then show the bits and the text">
</iframe>
:::
::::

::::{frame} Run the Broken Chain
:::{present}
- Run `L11-lab-rx.grc` on the recording: the key comes through, the text does not.
- Zoom in on the key and read the lengths of its marks and spaces.
- Work out which part carries the bits, and which length is a 0.
:::
:::{present}
<img src="../../viz/img/L11-canvas-rx.png"
     alt="L11-lab-rx.grc in GNU Radio Companion: File Source on L11-lab-remote.sigmf-data, Throttle, and the Energy Detector, whose power output goes to a time sink with the on and off levels and whose key output goes to a second time sink and to the Key Decoder"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::

1. **Run the chain.** Put `L11-lab-remote.sigmf-data`, `L11-lab-remote.sigmf-meta`, and `L11-lab-rx.grc` from the Lab Packet frame in one folder, open the flowgraph in GRC, and run it. The Energy Detector is the Lesson 11 block, here as an Embedded Python Block so the flowgraph runs on any laptop, and its key output feeds the **Key Decoder**, whose `work()` returns without doing anything. The Received label stays at "(nothing decoded)".
2. **Check the key.** Every burst on the Power plot should be one mark on the Key plot. If the key stays on or misses bursts, set the **Threshold (dB)** slider halfway between the floor and the bursts, as in Lesson 11's "Setting the Levels".
3. **Read the lengths.** Drag a box on the Key plot to zoom in on a few dozen marks, and read the length of each kind of mark and each kind of space, in milliseconds, including the long silence between two sendings of the line. Paste a screenshot of the zoomed key as Figure 1.

    <div class="rec" data-lab="L11">
    <label>Step 3: Mark lengths you see (ms) <input data-field="a.marks"></label>
    <label>Step 3: Space lengths you see (ms) <input data-field="a.spaces"></label>
    </div>
4. **Work out the code.** Decide which part of the key changes from bit to bit, and use your Part 1 answer about the bit every character starts with to decide which length is a 0. Count where each character starts from the long silence.

    <div class="rec" data-lab="L11">
    <label>Step 4: What carries a 0 (text) <input data-field="a.zero"></label>
    </div>
::::

::::{frame} Write the Decoder
:::{present}
- Turn the lengths into key samples at the key's own rate.
- Write `work()`: one bit per mark and space, eight bits per character.
- Recover the line; screenshot your code beside the running window.
:::

5. **Choose the limits.** The key runs at `samp_rate / decim` samples per second, your Part 1 rate. Choose a **boundary** in key samples that splits the two lengths of the part that carries the bits, and a **gap** in key samples, longer than any length inside a line and shorter than the silence between lines, that tells your block a line has ended.

    <div class="rec" data-lab="L11">
    <label>Step 5: Boundary and gap (key samples) <input data-field="a.bnd"></label>
    </div>
6. **Write work().** Double-click the Key Decoder and press **Open in Editor**. Add `boundary` and `gap` to `__init__()` as arguments, and write `work()` so it counts how long the key holds each level, decides one bit each time the part that carries a bit ends, builds each character from eight bits, most significant first, and sets `self.line` when a line ends. Keep in `self` everything your Part 1 list says must survive from one call of `work()` to the next. Save; GRC shows the new arguments in the block's properties, where you enter your Step 5 values.
7. **Recover the line.** Run the flowgraph, and the Received label shows the line after its first full sending, about 1.5 s. Record it, and paste a screenshot of your `work()` beside the running window as Figure 2.

    <div class="rec" data-lab="L11">
    <label>Step 7: The recovered line (text) <input data-field="a.msg"></label>
    </div>
8. **If the text is wrong.** The pattern of the error points to the cause. Text that is all `?` points to the bit decision being reversed, a line that is right after its first few characters points to where your block starts a character, and nothing at all points to the gap or to the code that sets `self.line`. A Python error appears in GRC's console at the bottom of the window, with the line number.
::::

::::{frame} Put It in a Module
:::{present}
- Make `gr-l11lab` with `gr_modtool`, and add a sink block, `key_decoder`.
- Move your class in, fill in the YAML file, and write a unit test.
- Build, test, install, and swap your block into the receiver.
:::

9. **Make the module.** In a new folder at the radioconda prompt, run `gr_modtool newmod l11lab`, `cd gr-l11lab`, and `gr_modtool add -t sink -l python key_decoder`. Give your name as the copyright holder, your two arguments with their Step 5 values as the argument list, and answer yes to the Python QA code.
10. **Move the class in.** Copy your class from the Embedded Python Block into `python/l11lab/key_decoder.py`, named `key_decoder` instead of `blk`, and check that the `gr_python_install(FILES ...)` line of `python/l11lab/CMakeLists.txt` lists `key_decoder.py`, as Lesson 11's "The Module Tree" warns.
11. **Fill in the YAML file.** In `grc/l11lab_key_decoder.block.yml`, give the block the label Key Decoder, a `make` template with both arguments, an `int` parameter for each, and one `float` input, as in Lesson 11's "The Block's YAML File".
12. **Write the test.** In `python/l11lab/qa_key_decoder.py`, replace the template's test with one that builds the key for a short word of your own in the lab's code, at the key's own rate, runs it from a Vector Source into your block, and checks `last_line()`.
13. **Build and test.** Build, run `ctest --output-on-failure`, and install, as in Lesson 11's "Build, Test, and Install", then restart GRC. Paste the `ctest` output as Figure 3.
14. **Swap it in.** In `L11-lab-rx.grc`, disable the Embedded Key Decoder, add your **Key Decoder** from the L11 Lab category of the block library with ID `decoder`, connect the key to it, and run. The line arrives as before. On a Windows laptop without WSL2, build Steps 9 to 14 on a teammate's Linux, macOS, or WSL2 laptop and note it on the Documentation line.
::::

::::{frame} Send Your Own Line
:::{present}
- Put your module's block in `L11-lab-link.grc` and type your own line.
- The link adds noise; diagnose from the plots why the line does not arrive.
- Fix it until your line comes through; screenshot before and after.
:::
:::{present}
<img src="../../viz/img/L11-canvas-link.png"
     alt="L11-lab-link.grc in GNU Radio Companion: a Vector Source of key_units, Repeat, Float To Complex, and Multiply with a Signal Source make the keyed carrier; a Noise Source and Add put it in noise; a Throttle feeds the Energy Detector, whose outputs go to the power and key time sinks and to the Key Decoder"
     style="max-width: 620px; width: 100%; display: block; margin: 0 auto;">
:::

15. **Run the link.** Open `L11-lab-link.grc`, disable its Embedded Key Decoder, and add your Key Decoder with ID `decoder`, as in Step 14. Set the `msg` variable to a line of your own, up to 40 characters, and run it. The flowgraph sends your line in the lab's code, over and over, with the **Noise amplitude** slider's noise added.
16. **Diagnose.** Your line does not arrive. Use the Power and Key plots to work out why, and paste a screenshot of the window as the left pane of Figure 4.
17. **Fix it.** Change what your diagnosis points to, in the sliders or in your block, until your line arrives on every sending for 20 s. Record what you changed, and paste a screenshot as the right pane of Figure 4.

    <div class="rec" data-lab="L11">
    <label>Step 17: What brought your line through (text) <input data-field="b.fix"></label>
    </div>
::::

::::{frame} No Hardware?
:class: read-only

:::{admonition} This lab needs no radio
:class: tip
Every flowgraph here runs on your laptop from the recording or from a simulated link, so a missing or broken PlutoSDR does not matter today.

If a flowgraph shows red blocks after Step 14 or 15, the Key Decoder from your module is missing from GRC's library: restart GRC, and check that you installed from the same radioconda prompt that runs it. A `ModuleNotFoundError` for `key_decoder` means the `gr_python_install` line does not list `key_decoder.py`. If the Received label never changes, check that the Key Decoder's ID is exactly `decoder`, the block the Function Probe reads.
:::
::::

::::{frame} Your Part 2 Entries
:class: read-only

This frame collects every box you filled in on this page. Your entries stay in this browser only, saved as you type. **Download my packet** writes them into the Measured cells of the blank packet and saves the PDF. The download locks every field, the Predicted cells included, so type your Part 1 answers into your own copy of the packet first, then use **Fill my own copy** and choose that file: the page keeps your answers and adds your entries beside them. Paste Figures 1 to 4 and write Part 3 in your copy, or on the printout, and upload one PDF to Gradescope. **Export entries** saves a small backup file you can **Import** on another laptop.

<div class="rec-summary" data-lab="L11" data-pdf="../../labs/ECE448_Lab_L11_CustomBlock_blank.pdf" data-file="ECE448_L11_Lab"></div>
::::

::::{frame} Lab Packet
:class: read-only doc-links

The L11 Lab packet is one submission, turned in complete before the midterm:

1. Part 1, Predict (individual, before the lab period): the three shaded entries, with your reasoning.
2. Part 2, Measure (in class, on your own laptop): the white cells of Tables A and B, and Figures 1 to 4.
3. Part 3, Analyze (individual, after the lab): three prompts, each answered from your own tables, code, and figures.

- <a class="doc-link" href="../../labs/ECE448_Lab_L11_CustomBlock_blank.pdf" target="_blank" rel="noopener">L11 Lab packet (PDF)</a>
- <a class="doc-link" href="../../grc/L11-lab-remote.sigmf-data" download>L11-lab-remote.sigmf-data</a> and <a class="doc-link" href="../../grc/L11-lab-remote.sigmf-meta" download>L11-lab-remote.sigmf-meta</a>, the recording you decode
- <a class="doc-link" href="../../grc/L11-lab-rx.grc" download>L11-lab-rx.grc</a>: the receiver, with the Key Decoder's `work()` empty
- <a class="doc-link" href="../../grc/L11-lab-link.grc" download>L11-lab-link.grc</a>: your own line in the same code, in noise
::::

::::{frame} For Part 3
:class: read-only

Do Part 3 after class, with your tables, code, and figures beside you. It asks about three things:

1. How your block in Figure 2 turns the key in Figure 1 into characters, and what it does when a mark or space spans two calls of `work()`.
2. Why the chain needed a block of your own, from the key in Figure 1 and the receivers of Lessons 8 and 10.
3. The two panes of Figure 4: what kept your line from arriving, and where the fix belongs.

I grade each answer on a claim, the evidence from your own tables, code, and figures, the reasoning that connects them, and the uncertainty in your readings.
::::

::::{frame} Looking Ahead
:class: read-only

Keep `gr-l11lab` installed. Lesson 12 receives Morse code, another key whose meaning is in its timing.
::::
