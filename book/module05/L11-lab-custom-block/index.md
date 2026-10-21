---
frame_view: true
---

# L11 Lab — Custom Block

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">Custom Block</h1>

<div class="title-rule"></div>

Build and test the course module, set the Energy Detector for a noisier signal, and write a Key Timer block of your own.

L11 Lab · Module 5: Custom Blocks & Midterm · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '5'">
  <li>I can create a GNU Radio out-of-tree (OOT) module and add a custom Python block to it.</li>
  <li>I can implement a custom signal-processing block from scratch and integrate it into a GNU Radio flowgraph.</li>
</ol>
::::

::::{frame} From Lesson to Bench
:::{present}
- **Pre-Lab:** check your tools and work out the Morse timing at 15 WPM.
- **Bench:** build `gr-ece448`, read the levels off the plot and set them, then write and time your own Key Timer.
- **Writeup:** explain hysteresis and timing, and what a Morse decoder needs.
:::

Lesson 11 packaged the Energy Detector in an out-of-tree module. Today you build and test that module on your own laptop, set the detector's levels for a noisier signal than the lesson used, and then make a module of your own from an empty `gr_modtool` template and write a second block in it, the **Key Timer**, which measures how long each key-down and key-up lasts, the lengths Lesson 12's Morse decoder needs.

The lab packet has three parts, and you turn it in once, complete, before the midterm. **Part 1, the Pre-Lab**, is on your own before the period. **Part 2** is your own work in class, and **Part 3, the Writeup**, explains it. Nothing in this lab transmits: every flowgraph is a simulation on your laptop.
::::

::::{frame} Part 1: Before the Period
:::{present}
- Check that `gr_modtool` and `cmake` run, and choose your route.
- Run `L11-keyed-carrier-epy.grc`, which needs nothing installed.
- Work out the Morse timing at 15 WPM.
:::

At the radioconda prompt, run `gnuradio-config-info --version`, `gr_modtool --help`, and `cmake --version`. If `cmake` is missing, run `conda install -c conda-forge gnuradio-build-deps`; on macOS, also run `xcode-select --install` once. Question 2 asks for the length of each Morse element at 15 words per minute, where one unit lasts $1.2/15$ s, and how many detector outputs a dit spans. You read the Energy Detector's levels off its Power plot at the bench.
::::

::::{frame} Two Routes
:::{present}
| Laptop | Route |
| :-- | :-- |
| Linux | build both modules with CMake |
| macOS | the same, untested on a Mac |
| Windows | WSL2 with Ubuntu 24.04, then build both modules |
| Windows, no WSL2 | Embedded Python Blocks |
:::

A Python-only module still runs CMake, and CMake needs a C++ compiler, which radioconda does not include, and which `gnuradio-build-deps` cannot supply by itself on Windows. On Windows, install WSL2 with Ubuntu 24.04, run `sudo apt install gnuradio-dev cmake g++` inside it, and follow the Ubuntu steps; WSLg opens GRC in a window. Without WSL2, use `L11-keyed-carrier-epy.grc` for the Energy Detector, and write the Key Timer in an Embedded Python Block: GRC's **Python Block**, with the class renamed `blk`. The code is the same in both routes. Questions 3(a) and 5 still need a real module and `ctest`, so as a last resort build those on a teammate's Linux, macOS, or WSL2 laptop.
::::

::::{frame} Part 2: Build and Test gr-ece448
:class: read-only

1. Download `L11-gr-ece448.zip` from the Lesson 11 page and unzip it. At the radioconda prompt, `cd` into `gr-ece448`.
2. Check that the `gr_python_install` line of `python/ece448/CMakeLists.txt` lists `energy_detector.py`.
3. Run `mkdir build`, `cd build`, and `cmake -G Ninja -DCMAKE_INSTALL_PREFIX=${CONDA_PREFIX} -DCMAKE_PREFIX_PATH=${CONDA_PREFIX} ..`. With Ubuntu's own GNU Radio instead of radioconda, run `cmake ..` and use `make` and `sudo make install` below.
4. Run `cmake --build .`, then `ctest --output-on-failure`. Copy its output for Question 3(a).
5. Run `cmake --install .`, then close and restart GRC.
6. Open and run `L11-keyed-carrier.grc`. Double-click the Energy Detector and screenshot its properties dialog for Question 3(b).
::::

::::{frame} Part 2: Set the Levels
:class: read-only

1. In the running flowgraph, set the noise amplitude to 0.5.
2. Stop the flowgraph. Set the variable `wpm` to 15, and set both Time Sinks' Number of Points to one sending of "ECE" at 1 kHz, from your Question 2(b) answer. Run it again.
3. Read the floor and the carrier-on level from the power plot, and note how far the floor wanders, for Question 4(a).
4. Set the threshold to the floor's level and the hysteresis to 0, and watch the key.
5. Choose your own threshold and hysteresis so that the detected key follows the sent keying for at least 20 s. Record them and screenshot the window for Question 4(b). Save this flowgraph under a new name; Question 6 adds to it.
::::

::::{frame} Part 2: Write the Key Timer
:class: read-only

1. In a new directory, run `gr_modtool newmod l11lab`, then `cd gr-l11lab`.
2. Run `gr_modtool add -t sink -l python key_timer`. Give your name as the copyright holder, `rate=1000.0` as the argument list, and answer yes to the Python QA code.
3. In `python/l11lab/key_timer.py`, set `in_sig=[numpy.float32]` (the template imports `numpy`), and write `__init__()`, `work()`, `last_mark()`, `last_space()`, and `mark_count()` to the specification in the packet's Question 5.
4. In `python/l11lab/qa_key_timer.py`, replace the template's test with one that feeds a known key from a Vector Source and checks all three methods.
5. Fill in `grc/l11lab_key_timer.block.yml`: a label, the `make` template, one `real` parameter `rate`, and one `float` input.
6. Check the `gr_python_install` line lists `key_timer.py`. Then build, run `ctest`, and install, as for `gr-ece448`, and restart GRC.
::::

::::{frame} The Key Timer
:::{present}
| Part | What it is |
| :-- | :-- |
| Type | sink: one float input, no outputs |
| Parameter | `rate`, the key's sample rate |
| Methods | `last_mark()`, `last_space()` in ms; `mark_count()` |
:::

The Key Timer reads the Energy Detector's key, a stream of 0s and 1s, and counts how many samples each run of 1s, a **mark**, and each run of 0s, a **space**, lasts. When the key changes, it converts the count to milliseconds with `rate` and keeps it as the last mark or the last space. Like the Energy Detector's key state, the count must survive from one call of `work()` to the next, because a dah can span many calls.
::::

::::{frame} Part 2: Time the Morse
:class: read-only

1. Open your flowgraph from the Set the Levels steps. Add your **Key Timer** from the block library and connect the Energy Detector's `key` output to it. Set `rate` to `samp_rate / decim`.
2. Add three **Function Probes**, with Block ID your Key Timer's ID, Function Names `last_mark`, `last_space`, and `mark_count`, and a poll rate of 4 Hz.
3. Add three **QT GUI Labels** that show the three probes, with GUI hints `3,0,1,1`, `3,1,1,1`, and `3,2,1,1`.
4. Run it. Watch the labels through several sendings and record the lengths you see for each element for Question 6(a). Screenshot the canvas and the window for Question 6(b).
::::

::::{frame} Part 2: A Noisier Signal
:class: read-only

1. Set the noise amplitude to 0.8. With 32 samples averaged, find the best threshold and hysteresis you can.
2. Stop the flowgraph, run it again, and record the Marks label after 30 s for Question 7(a).
3. Stop it, set the variable `decim` to 128, and run it again. Watch how the floor on the power plot changes. Find your best settings again, and record the Marks label after 30 s and the dit length for Question 7(b).
::::

::::{frame} If the Block Does Not Appear
:class: read-only

:::{admonition} Troubleshooting a Missing Block
:class: tip
CMake prints several warnings marked "for project developers" about policies and an old minimum version; they come from `gr_modtool`'s template and do not stop the build. Restart GRC after every install; it reads its block library only when it starts. Check that you ran CMake with `-DCMAKE_INSTALL_PREFIX=${CONDA_PREFIX}` from the same radioconda prompt that runs GRC. A `ModuleNotFoundError` for your block means the `gr_python_install` line does not list its `.py` file; add it, then build and install again. A flowgraph with red arrows usually has a type mismatch: the Key Timer's input must be `float`, to match the Energy Detector's `key` output.
:::
::::

::::{frame} Part 3: After the Lab
:::{present}
- Explain why hysteresis can lengthen a mark, and how a larger $N$ smooths the floor but coarsens the timing.
- Decide which blocks belong in a module.
- Propose a rule that tells a dit from a dah at any speed.
:::

The Writeup is three questions. The first explains why some marks read a millisecond or two long with hysteresis, and what the noisier signal showed about choosing the number of samples averaged. The second decides whether the Energy Detector and the Key Timer belong in a module or in Embedded Python Blocks for Lesson 12's decoder, and what the unit test checks that the flowgraph cannot. The third proposes the timing rules a Morse decoder needs, which Lesson 12 builds.
::::

::::{frame} Lab Packet
:class: read-only doc-links

- <a class="doc-link" href="../../labs/ECE448_Lab_L11_CustomBlock_blank.pdf" target="_blank" rel="noopener">L11 Lab packet (PDF)</a>
- <a class="doc-link" href="../../grc/L11-gr-ece448.zip" download>L11-gr-ece448.zip</a>: the `gr-ece448` module with the Energy Detector and its unit test.
- <a class="doc-link" href="../../grc/L11-keyed-carrier.grc" download>L11-keyed-carrier.grc</a>: the keyed carrier through the installed Energy Detector. No hardware needed.
- <a class="doc-link" href="../../grc/L11-keyed-carrier-epy.grc" download>L11-keyed-carrier-epy.grc</a>: the same flowgraph with the Energy Detector in an Embedded Python Block. Needs nothing installed.
::::

::::{frame} Looking Ahead
:::{present}
- Keep both modules installed and your flowgraph saved.
- Lesson 12 decodes Morse from the key and its timing.
:::

Keep `gr-ece448`, your own `gr-l11lab`, and your timed flowgraph. Lesson 12, on CW, receives Morse code: its receiver uses the Energy Detector to make the key and timing like the Key Timer's to tell each dit from each dah.
::::
