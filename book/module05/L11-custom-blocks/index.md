---
frame_view: true
---

# L11 - Out-of-Tree Modules and Custom Blocks

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">Out-of-Tree Modules and Custom Blocks</h1>

<div class="title-rule"></div>

A block of our own, packaged with gr_modtool: an Energy Detector that turns a keyed carrier into a key.

Lesson 11 · Module 5: Custom Blocks & Midterm · Dr. Neil Rogers
::::

::::{frame} Slides
:class: read-only

:::{admonition} Slides
:class: slides
<a href="../../slides/L11-custom-blocks.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L11-custom-blocks.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L11-custom-blocks.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '5'">
  <li>I can create a GNU Radio out-of-tree (OOT) module and add a custom Python block to it.</li>
  <li>I can implement a custom signal-processing block from scratch and integrate it into a GNU Radio flowgraph.</li>
</ol>
::::

::::{frame} A Keyed Carrier
:::{present}
<img src="../../viz/img/L11-keyed-clean.png"
     alt="The L11 keyed-carrier flowgraph running at noise amplitude 0.1, threshold minus 10 dB, and hysteresis 3 dB: the Power plot steps between 0 dB and about minus 20 dB in the pattern of Morse ECE, with the on level dashed at minus 10 dB and the off level at minus 13 dB; the Key plot shows the detected key, which follows the keying the flowgraph sent exactly"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- A carrier keyed on and off spells Morse "ECE" in noise.
- Our own block turns it into a key: 1 while the carrier is on.
:::

The figure is today's flowgraph, `L11-keyed-carrier.grc`, running. A 1 kHz tone at 32 kHz sampling switches on and off in the pattern of Morse code for "ECE" at 20 words per minute, so each dit lasts 60 ms, and a Noise Source adds Gaussian noise. The top plot is the signal's average power in dB, and the bottom plot compares the key our block makes with the keying the flowgraph sent, raised by 1.5 so the two traces do not overlap.

No block in GNU Radio's library makes that key directly, so we write one: the **Energy Detector**. It is the first block in a module of our own, `gr-ece448`. Lesson 12 can reuse it to receive CW, and at the end of this lesson the same block keys on the bursts of a 433 MHz remote.
::::

::::{frame} From Embedded Block to Module
:::{present}
| | Embedded Python Block | OOT module |
| :-- | :-- | :-- |
| Code lives in | one `.grc` file | its own directory |
| Reuse | copy and paste | any flowgraph, like a stock block |
| Testing | by eye | a unit test |
:::

Lesson 8's Text Sink is an **Embedded Python Block**: GRC saves its code inside the `.grc` file, and Lesson 10 had to paste the same code into its own flowgraph. That is the right tool for a block one flowgraph needs. A block several flowgraphs need belongs in an **out-of-tree (OOT) module**, a separate package of blocks that installs beside GNU Radio's own. GNU Radio's library is the "tree", so a module we build ourselves is "out of tree". After we install it, the block appears in GRC's library like any other block, every flowgraph uses the same code, and a unit test checks that code each time we build it.
::::

::::{frame} Part 1: Make the Module
:::{present}
```
gr_modtool newmod ece448
cd gr-ece448
gr_modtool add -t decimator -l python energy_detector
```

- `newmod` makes the empty module; `add` makes one block.
:::

**gr_modtool** comes with GNU Radio and writes the files of a module for us. `gr_modtool newmod ece448` makes a directory named `gr-ece448` with the build files and empty folders. Inside it, `gr_modtool add` asks for the block's type and language, which the flags `-t decimator -l python` give on the command line. It then asks for a copyright holder, the constructor's arguments, which we give as `decim=32, threshold_db=-20.0, hysteresis_db=3.0`, and whether to add a Python unit test, which we accept.
::::

::::{frame} The Module Tree
:::{present}
<img src="../../viz/img/L11-oot-tree.svg"
     alt="The gr-ece448 directory tree: CMakeLists.txt at the top; grc/ece448_energy_detector.block.yml; python/ece448/ with __init__.py, energy_detector.py, qa_energy_detector.py, and a CMakeLists.txt; include, lib, and bindings for C++ only; apps, docs, examples, and cmake. The three block files are highlighted, with a note that gr_modtool add writes them"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The block, its GRC file, and its test are three files.
- The C++ folders hold no block code in a Python-only module.
:::

`gr_modtool add` writes three files and edits three more. `energy_detector.py` is the block, `qa_energy_detector.py` is its unit test, and `ece448_energy_detector.block.yml` tells GRC how to draw it. It adds an import line to `__init__.py`, so `from gnuradio import ece448` finds the block, it lists the test in `python/ece448/CMakeLists.txt`, and it adds the YAML file to `grc/CMakeLists.txt`, which installs it.

On GNU Radio 3.10.9, Ubuntu 24.04's version, `gr_modtool` misses one edit: it does not add `energy_detector.py` to the `gr_python_install(FILES ...)` line in that `CMakeLists.txt`, so the module installs without its block. Radioconda's 3.10.12 makes the edit. On either version, check that the line reads `FILES __init__.py energy_detector.py` before building.
::::

::::{frame} Four Kinds of Block
:::{present}
<img src="../../viz/img/L11-block-types.svg"
     alt="Four block types drawn as input and output samples: a sync block with six in and six out, a decimator with eight in and two out, an interpolator with two in and eight out, and a general block with six in and three out, labeled 1 in : 1 out, N in : 1 out, 1 in : N out, and any ratio"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The type fixes how many outputs each input makes.
- The Energy Detector makes one output per N inputs, so it is a **decimator**.
:::

GNU Radio's scheduler calls a block's `work()` function with a buffer of input samples and room for some output samples, and the block type tells it how the two counts relate. A **sync** block makes one output per input, like Multiply Const. A **decimator** makes one output per $N$ inputs, like a decimating filter, and an **interpolator** makes $N$ outputs per input, like Repeat. A **general** block reports how many inputs it used and how many outputs it made each time, which is the right type when the ratio changes, as in Correlate Access Code, which passes only the bits of a packet. Choosing the most specific type that fits lets GNU Radio manage the buffers, and the block's code stays short.
::::

::::{frame} Part 2: The Energy Detector
:::{present}
<img src="../../viz/img/L11-energy-steps.svg"
     alt="The Energy Detector's steps: N complex samples, then the average of the magnitude squared, then 10 log10, which is the power output in dB; then a comparison with the on and off levels, which gives the key output, 0 or 1. The average and the log make one output per N inputs"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The block takes one complex input and makes two float outputs, power in dB and the key.
- The key turns on above the threshold and off below threshold minus hysteresis.
:::

For each run of $N$ input samples, the block computes the average power

$$P = \frac{1}{N}\sum_{n=1}^{N} \vert x[n]\vert^2,$$

and outputs $10\log_{10} P$ on its first output. A tone of amplitude 1 has power 1, or 0 dB, and GNU Radio's Noise Source with amplitude $\sigma$ has power $\sigma^2$, so with the carrier off the output sits near $20\log_{10}\sigma$ dB. The second output is the key. It switches to 1 when the power rises above the threshold, and back to 0 only when the power falls below the threshold minus the **hysteresis**. With $N = 32$ at 32 kHz, the block makes one output per millisecond.
::::

::::{frame} The work() Function
:::{present}
```python
def work(self, input_items, output_items):
    n = len(output_items[0])
    x = input_items[0][:n * self.decim].reshape(n, self.decim)
    power_db = 10 * np.log10(np.mean(x.real**2 + x.imag**2, axis=1) + 1e-12)
    for i, p in enumerate(power_db):
        if self.key == 0.0 and p > self.threshold_db:
            self.key = 1.0
        elif self.key == 1.0 and p < self.threshold_db - self.hysteresis_db:
            self.key = 0.0
        output_items[1][i] = self.key
    output_items[0][:] = power_db
    return n
```
:::

GNU Radio hands `work()` room for `n` outputs on each output port, and because the block is a decimator, exactly `n * decim` inputs. The `reshape` lines the inputs up as `n` rows of `decim` samples, so NumPy averages each row in one call, and the small `1e-12` keeps the log finite when a run is all zeros. The loop runs once per output, not once per input, and `self.key` carries the key's state from one call to the next. The constructor, in the same file, calls `gr.decim_block.__init__` with `in_sig=[np.complex64]`, `out_sig=[np.float32, np.float32]`, and `decim=decim`, and stores the three arguments. Two short methods, `set_threshold_db` and `set_hysteresis_db`, let a slider change the levels while the flowgraph runs.
::::

::::{frame} The Block's YAML File
:::{present}
```yaml
id: ece448_energy_detector
label: Energy Detector
category: '[ECE 448]'
templates:
  imports: from gnuradio import ece448
  make: ece448.energy_detector(${decim}, ${threshold_db}, ${hysteresis_db})
  callbacks:
  - set_threshold_db(${threshold_db})
  - set_hysteresis_db(${hysteresis_db})
```
- The rest of the file has one entry per parameter, input, and output.
:::

GRC never reads the Python file. It reads `grc/ece448_energy_detector.block.yml`, which names the block, puts it in an "ECE 448" category, and gives the line of Python that GRC writes into the flowgraph's generated script: the `make` template, with each `${...}` replaced by the value in the block's properties dialog. The `callbacks` let GRC call the setters when a slider moves. Below this, the file lists the three parameters with their labels, types, and defaults, the complex input, and the two float outputs, `power` and `key`. The template from `gr_modtool` has placeholders for each, and the download has the finished file.
::::

::::{frame} Part 3: Test the Block
:::{present}
```python
def test_002_hysteresis(self):
    p_db = np.array([-30, -19, -21, -22, -24, -21, -19, -25])
    x = (10 ** (p_db / 20)).astype(np.complex64)
    power, key = self.run_detector(x, 1, -20.0, 3.0)
    self.assertFloatTuplesAlmostEqual(power, p_db, 4)
    self.assertFloatTuplesAlmostEqual(key, [0, 1, 1, 1, 0, 0, 1, 0])
```
- The test runs the block on inputs whose answer we know.
:::

`qa_energy_detector.py` builds a small flowgraph, a Vector Source into the block and two Vector Sinks out of it, runs it, and compares the outputs with the expected values. In the test above each output averages one sample, so the powers are the inputs in dB. The key turns on at $-19$ dB, above the $-20$ dB threshold, stays on through $-21$ and $-22$ dB, and turns off at $-24$ dB, below $-23$ dB. The file holds four tests: the block constructs, three amplitudes give 0, $-20$, and $-40$ dB, the hysteresis case above, and a keyed tone in noise 30 dB down that must give a key of exactly 50 outputs on and 50 off, five times.
::::

::::{frame} Build, Test, and Install
:::{present}
```
mkdir build && cd build
cmake -G Ninja -DCMAKE_INSTALL_PREFIX=${CONDA_PREFIX} \
      -DCMAKE_PREFIX_PATH=${CONDA_PREFIX} ..
cmake --build .
ctest --output-on-failure
cmake --install .
```
- `ctest` runs the unit test before we install anything.
:::

A Python-only module has nothing to compile, but **CMake** still copies its files to the right places, and `ctest` runs its tests against the build directory. `CMAKE_PREFIX_PATH` tells CMake to find the radioconda environment's GNU Radio, and `CMAKE_INSTALL_PREFIX` installs into the same environment, so the block goes where that GNU Radio looks: the Python file under its `site-packages/gnuradio/ece448/`, and the YAML file under `share/gnuradio/grc/blocks/`. These steps build, test, and install the module under GNU Radio 3.10.12 from conda-forge on Linux, and under Ubuntu's 3.10.9 with `make` in place of Ninja. A passing `ctest` prints `100% tests passed, 0 tests failed out of 1`: its one entry runs the four test methods in `qa_energy_detector.py`. Restart GRC after installing so it reloads its block library.
::::

::::{frame} The Block in GRC
:::{present}
<img src="../../viz/img/L11-grc-keyed.png"
     alt="The L11 keyed-carrier flowgraph in GNU Radio Companion: a Vector Source of the Morse pattern, Repeat, Float To Complex, and Multiply with a Signal Source make the keyed tone; a Noise Source and Add put it in noise; a Throttle feeds the Energy Detector block, with Samples Averaged 32, Threshold minus 10 dB, and Hysteresis 3 dB; its power output goes to a time sink with two Constant Sources for the levels, and its key output goes to a second time sink beside the sent keying from Keep 1 in N and Add Const"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The installed block sits in the library under **ECE 448**.
- The block labels its two outputs `power` and `key`.
:::

Once installed, the Energy Detector is an ordinary block: you search for it in GRC's block library, drag it onto the canvas, and set its three parameters in its properties dialog, here with the sliders `threshold` and `hyst` as values. The rest of the flowgraph builds the test signal. A **Vector Source** holds the Morse pattern, one entry per 60 ms unit, and a **Repeat** holds each entry for 1920 samples; multiplying by a 1 kHz **Signal Source** keys the tone. A **Keep 1 in N** with $N = 32$ brings the sent keying down to the detector's 1 kHz output rate for the comparison plot.
::::

::::{frame} Threshold and Hysteresis
:::{present}
<img src="../../viz/img/L11-keyed-chatter.png"
     alt="The L11 flowgraph at noise amplitude 0.3, threshold minus 10 dB, and hysteresis 0: the noise floor of the Power plot sits right on the threshold line near minus 10 dB, and the detected key switches on and off rapidly through every gap in the keying"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- With the threshold on the noise floor, the key **chatters**.
- Hysteresis alone cannot fix a threshold in the wrong place.
:::

At a noise amplitude of 0.3, the noise floor is $20\log_{10} 0.3 = -10.5$ dB, right at the $-10$ dB threshold. With no hysteresis, every averaged output that crosses the line flips the key, so the key **chatters** through every gap, and a Morse decoder downstream would read each flip as a dit. Adding 3 dB of hysteresis with the threshold where it is makes things worse: the key turns on and then rarely falls below $-13$ dB, so it stays on nearly all the time, and the threshold must move up before hysteresis can help.
::::

::::{frame} Setting the Levels
:::{present}
<img src="../../viz/img/L11-keyed-fixed.png"
     alt="The L11 flowgraph at noise amplitude 0.3 with the threshold raised to minus 5 dB and hysteresis 3 dB: the on level at minus 5 dB and the off level at minus 8 dB both sit between the noise floor near minus 10.5 dB and the carrier near 0 dB, and the detected key follows the sent keying exactly"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Put both levels between the floor and the signal.
- Hysteresis then keeps noise near the threshold from switching the key.
:::

With the carrier on, the power is

$$P_\text{on} = 10\log_{10}(1 + \sigma^2)\ \text{dB},$$

which is $+0.4$ dB at $\sigma = 0.3$, and with it off the power is about $-10.5$ dB. Raising the threshold to $-5$ dB puts the on level at $-5$ dB and the off level at $-8$ dB, both well inside that 11 dB gap, and the key follows the keying exactly. A good rule is to set the threshold about halfway between the floor and the signal in dB, and the hysteresis to a few times the spread of the floor, which the frame How Many Samples to Average works out.
::::

::::{frame} Energy Detector Explorer
:class: viz-frame

:::{depth}
The top panel is the detector's power output for one sending of "ECE", and the bottom panel compares the key with the keying the flowgraph sent, shaded red where they differ. It starts where the chatter screenshot did: noise amplitude 0.3, threshold $-10$ dB, no hysteresis. Raise the threshold to $-5$ dB and add 3 dB of hysteresis, and the key changes 11 times, as the keying does. Then change the samples averaged. Averaging 8 samples gives a ragged floor and a 0.25 ms output; averaging 64 gives a smoother floor and a 2 ms output, and a dit is still 30 outputs long.
:::

:::{present}
<iframe src="../../viz/energy-detector.html"
        width="100%" height="510"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Energy detector explorer: the power output and the key for Morse ECE in noise, as the noise amplitude, the threshold, the hysteresis, and the number of samples averaged change">
</iframe>
:::
::::

::::{frame} How Many Samples to Average
:class: read-only

The noise power in one sample varies as much as its mean, so a single sample of noise tells us little. Averaging $N$ samples divides that spread by $\sqrt N$, so the average has a mean of $\sigma^2$ and a standard deviation of

$$\sigma_P = \frac{\sigma^2}{\sqrt N}.$$

In dB, one standard deviation above and below the mean is

$$10\log_{10}\left(1 \pm \frac{1}{\sqrt N}\right)\ \text{dB},$$

which for $N = 8$ is $+1.3$ dB and $-1.9$ dB. Four times as many samples halves the spread.

Averaging more samples takes more time: each output covers $N/f_s$ seconds, and an edge in the keying can land anywhere inside one output. At 32 kHz, $N = 32$ gives 1 ms outputs. A dit at 20 words per minute is 60 ms, so it spans 60 outputs, and even $N = 64$, 2 ms, leaves 30 outputs per dit. A faster signal needs a shorter average: the 433 MHz remotes below send pulses a few hundred microseconds long, so their flowgraph averages 4 samples at 128 kHz, about 31 $\mu$s per output.
::::

::::{frame} On Your Laptop
:::{present}
- Every radioconda install has `gr_modtool`.
- CMake needs a C++ compiler, even for a Python-only module.
- On Windows, the fallbacks are WSL2 with Ubuntu, then an Embedded Python Block.
:::

Radioconda installs GNU Radio from conda-forge, and its `gnuradio-core` package includes `gr_modtool` on Linux, macOS, and Windows, where it is `gr_modtool.exe`. Radioconda has no CMake and no compiler, and the `project()` line of a module's top-level `CMakeLists.txt` declares C and C++, so CMake stops at that line without a compiler, even when the module has no C++. The package `gnuradio-build-deps`, installed with `conda install -c conda-forge gnuradio-build-deps`, adds CMake, Ninja, and a compiler. On Linux that compiler is complete. On macOS the conda compiler does not include Apple's SDK, which `xcode-select --install` provides; we have not tested this route on a Mac. On Windows, conda-forge's `gnuradio-build-deps` pulls in `vs2022_win-64`, which only locates an existing Visual Studio 2022 installation, so a Windows laptop also needs Microsoft's Visual Studio 2022 Build Tools, a large separate install; we have not tested this route either.

A Windows laptop without them has two other routes. The first is WSL2 with Ubuntu 24.04: inside it, `sudo apt install gnuradio-dev cmake g++` installs GNU Radio 3.10.9 and a compiler, the module builds exactly as on Ubuntu, and WSLg runs GRC in a window; we have tested the Ubuntu 24.04 route but not WSL itself. The second needs nothing installed: `L11-keyed-carrier-epy.grc` has the same `energy_detector` class pasted into an Embedded Python Block, renamed `blk`, and runs identically. The block's code, its tests, and its YAML file move into a module unchanged on any Linux or macOS machine, such as a teammate's in the lab.
::::

::::{frame} OOK on an RTL-SDR
:::{present}
<img src="../../viz/img/L11-grc-ook.png"
     alt="The L11 RTL-SDR flowgraph in GNU Radio Companion: a Soapy RTLSDR Source at 1.024 MS/s tuned to 433.72 MHz, a Frequency Xlating FIR Filter that shifts 200 kHz and decimates by 8 to 128 kHz, the Energy Detector averaging 4 samples, a Multiply Const of 20 and an Add Const of minus 60 that draw the key at minus 60 dB when off and minus 40 dB when on, a time sink of power, key, and threshold, and a frequency sink"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Many 433.92 MHz remotes and sensors use on-off keying (OOK).
- The same block keys on their bursts.
:::

On-off keying sends a 1 as a burst of carrier and a 0 as silence, the same signal as today's keyed tone, only faster. Weather sensors, doorbells, and some remotes in the US use on-off keying at 433.92 MHz, as low-power unlicensed devices under FCC Part 15. `L11-ook-rtlsdr.grc` tunes an RTL-SDR 200 kHz below 433.92 MHz to keep the radio's DC spike off the signal, shifts the signal to 0 Hz and decimates to 128 kHz, and runs the Energy Detector with $N = 4$. The time sink draws the key at $-60$ dB when it is off and $-40$ dB when it is on, so it shares the power plot's axis. Set the threshold halfway between the floor and the burst level on the power plot, press a remote nearby, and the key traces its bursts. The flowgraph only receives. This page has not run it, because it needs an RTL-SDR and a remote, so the figure shows the flowgraph in GRC, not a capture.
::::

::::{frame} Key Point
:::{present}
:class: callout
A block several flowgraphs need belongs in an out-of-tree module: gr_modtool writes the files, we write work(), the YAML file, and a unit test, and CMake builds, tests, and installs it.
:::
::::

::::{frame} Downloads
:class: read-only doc-links

- <a class="doc-link" href="../../grc/L11-gr-ece448.zip" download>L11-gr-ece448.zip</a>: the `gr-ece448` module, with the Energy Detector, its YAML file, and its unit test. Its `README.md` lists the build steps.
- <a class="doc-link" href="../../grc/L11-keyed-carrier.grc" download>L11-keyed-carrier.grc</a>: Morse "ECE" as a keyed carrier in noise, through the installed Energy Detector, with noise, threshold, and hysteresis sliders. Needs `gr-ece448` installed; no hardware.
- <a class="doc-link" href="../../grc/L11-keyed-carrier-epy.grc" download>L11-keyed-carrier-epy.grc</a>: the same flowgraph with the Energy Detector in an Embedded Python Block. Needs nothing installed.
- <a class="doc-link" href="../../grc/L11-ook-rtlsdr.grc" download>L11-ook-rtlsdr.grc</a>: the Energy Detector on an RTL-SDR at 433.92 MHz, for OOK remotes. Needs `gr-ece448` and an RTL-SDR; receive only.

Unzip the module, then follow its `README.md` from the radioconda prompt. Open a `.grc` file from GRC's File menu, or run `gnuradio-companion L11-keyed-carrier.grc`.
::::

::::{frame} Summary
:class: read-only

| Idea | What it is | Detail to remember |
| :-- | :-- | :-- |
| Embedded Python Block | a block saved inside one `.grc` | right for one flowgraph |
| OOT module | a package of blocks installed beside GNU Radio | `gr_modtool newmod`, then `add` |
| Block types | sync, decimator, interpolator, general | 1:1, $N$:1, 1:$N$, any ratio |
| Block files | `.py`, `.block.yml`, `qa_*.py` | check `gr_python_install` on 3.10.9 |
| Build | CMake, `ctest`, install | install into the radioconda environment |
| Energy Detector | average power in dB, keyed with hysteresis | floor near $20\log_{10}\sigma$ dB |
| Levels | threshold halfway, hysteresis above the spread | spread shrinks as $\sqrt N$ |
| Windows | CMake needs Visual Studio 2022 Build Tools | fallbacks: WSL2 Ubuntu, then an Embedded Python Block |
::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE448_L11_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE448_L11_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Looking Ahead
:::{present}
- The L11 Lab builds the module and adds a block you write yourself.
- Lesson 12 turns the key into Morse letters.
:::

The L11 Lab is the hands-on version of this lesson. You build and test `gr-ece448` on your laptop, set the detector's levels for a noisier signal, and then make a module of your own and write a Key Timer block in it, which measures how long each key-down and key-up lasts.

Lesson 12, on CW, receives Morse code. Its receiver uses the Energy Detector to make the key and the timing of the key to tell a dit from a dah, which is the job the Key Timer starts.
::::
