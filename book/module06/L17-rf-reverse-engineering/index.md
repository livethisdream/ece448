---
frame_view: true
---

# L17 - RF Reverse Engineering

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">RF Reverse Engineering</h1>

<div class="title-rule"></div>

Take an unknown signal from spectrum to bits with a PlutoSDR, GNU Radio, and URH.

Lesson 17 · Module 6: Waveform Applications & RF Reverse Engineering · Dr. Neil Rogers
::::

::::{frame} Slides
:class: read-only

:::{admonition} Slides
:class: slides
<a href="../../slides/L17-rf-reverse-engineering.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L17-rf-reverse-engineering.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L17-rf-reverse-engineering.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '6'; counter-reset: lo 5">
  <li>I can perform RF reverse engineering on an unknown signal: identify its modulation, symbol rate, and payload structure.</li>
</ol>
::::

::::{frame} A Remote Nobody Described
:::{present}
<img src="../../viz/img/L17-urh-interp.png"
     alt="URH's Interpretation tab, labeled simulated, with L17-fan-remote.sigmf-data open: Modulation ASK, Samples/Symbol 80, Noise 0.14, Center 0.31; the signal view shows five groups of six bursts, and the text below lists each burst as a line of chips such as 1101001101001001101101001001001001101101101101 followed by a pause of 2560 samples"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- A ceiling-fan remote sends five commands near 350 MHz, and no one gave us its manual.
- Today we go from the recording to the bits, then build a transmitter for it.
:::

Neil's 2025 class reverse-engineered a Hunter ceiling-fan remote, a low-power transmitter near 350 MHz that operates under FCC Part 15. Not every cadet has that fan, so this lesson uses a **Simulated** fan remote of our own with five buttons: Light, Fan Off, Low, Medium, and High. Its recording, `L17-fan-remote.sigmf-data`, holds one press of each button, and the figure is that recording open in the **Universal Radio Hacker** (URH).

The two lines of the objective from 2025 set the plan: reverse engineer a simple RF transmitter, and create a GNU Radio flowgraph that operates the fan. Lesson 11 found the bursts of a 433.92 MHz remote with an energy detector, and Lesson 12 keyed a carrier on and off. Today we read what those bursts say.
::::

::::{frame} The Process
:::{present}
<img src="../../viz/img/L17-process.svg"
     alt="Five boxes joined by arrows: Step 1 find the carrier, with a spectrum and waterfall; Step 2 identify the modulation, OOK, FSK, PSK; Step 3 identify the encoding, bits, fields, rates; Step 4 build an encoder, a GNU Radio flowgraph; Step 5 transmit: cadets into a cable, the instructor demo over the air to the fan. Steps 1 to 3 work from a recording, and steps 4 and 5 build it back"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- These are the five steps of the 2025 slides, in their order.
- Steps 1 to 3 need only the recording.
:::

The process comes from the 2025 slides. First we find the **carrier**, the frequency the transmitter uses. Next we identify the **modulation**, what the transmitter changes to send information. Then we identify the **encoding**: what the commands are, how the bits group into bytes or nibbles, and the bit rate and baud rate. With those three answers we build an **encoder** that produces the same signal, and last we transmit it.

Steps 1 to 3 work entirely from a recording, so they need no radio. Step 5 transmits: a cadet's transmitter goes into a cable with an attenuator, never over the air, and the instructor closes the lesson by operating the real fan over the air. The lesson's tools are the ones Neil used: a GNU Radio capture flowgraph to find the carrier, then URH to take the bursts apart.
::::

::::{frame} The Recording
:class: read-only

A recording a cadet downloads or makes in this course is a **SigMF** pair. The samples are in `L17-fan-remote.sigmf-data`, and `L17-fan-remote.sigmf-meta` is a short text file that says how to read them:

| Field in the meta file | Value | What it sets |
| :-- | :-- | :-- |
| `core:datatype` | `cf32_le` | complex float, 8 bytes a sample: the Output Type of the SigMF Source |
| `core:sample_rate` | 200000 | `samp_rate` in the flowgraph, and the sample rate in URH |
| `core:frequency` | 350000000 | the center of the recording, 350.000 MHz |
| `core:hw` | Simulated in GNU Radio; no radio | where the recording came from |
| `core:description` | the buttons, in the order pressed | which burst is which |

GNU Radio 3.10 reads and writes this pair with the **SigMF Source (Minimal)** and **SigMF Sink (Minimal)** blocks. The source block is a File Source with SigMF documentation, so we point it at the `.sigmf-data` file and set its Output Type from `core:datatype` by hand. GRC marks both blocks as deprecated, because a fuller SigMF module is planned, but they work in 3.10 and draw no error. PySDR's chapter on IQ files and SigMF describes the format.

The recording is 2.4 s long and 3.9 MB. `L17-fan-remote-gen.grc` made it: it keys a carrier 40 kHz above 350 MHz with each button's frame, adds noise, and adds a weak steady carrier that has nothing to do with the remote.
::::

::::{frame} Step 1: Find the Carrier
:::{present}
<img src="../../viz/img/L17-view-find.png"
     alt="L17-sigmf-view.grc running on the recording, labeled simulated, with the carrier offset at 0: the spectrum from 349.90 to 350.10 MHz shows a narrow steady line near 349.945 MHz and a wider bump near 350.040 MHz; the waterfall shows a solid vertical line at 349.945 MHz and short bursts near 350.040 MHz; the envelope plot is empty"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Run `L17-sigmf-view.grc` and watch the waterfall while the recording loops.
- The steady line never changes; the remote is the one that bursts.
:::

In 2025 the first tool was a GNU Radio capture flowgraph: a PlutoSDR or HackRF source, a **SigMF Sink (Minimal)** to record, and frequency, time, and waterfall sinks. That flowgraph is `L17-capture.grc`, with a PlutoSDR Source. `L17-sigmf-view.grc` is the same flowgraph with a SigMF Source in place of the radio: the recording, a Throttle, and a **Frequency Sink** and **Waterfall Sink** centered at 350 MHz. The recording loops, so the bursts come back every 2.4 s.

Two signals appear. A narrow line near 349.945 MHz stays on the whole time. The bursts near 350.04 MHz come and go five times per loop, once for each button press, and that is the remote. A real band holds many steady carriers, such as another receiver's oscillator or a nearby digital clock, so the waterfall is how we tell them apart: the remote's signal starts and stops when someone presses a button. The bursts are wider on the spectrum than the steady line because switching a carrier on and off spreads it.
::::

::::{frame} Step 1: Shift the Carrier to 0 Hz
:::{present}
<img src="../../viz/img/L17-view-tuned.png"
     alt="L17-sigmf-view.grc running on the recording, labeled simulated, with the carrier offset at 40000 Hz: the spectrum and waterfall are as before, and the envelope plot shows 40 ms of the signal after the shift: a frame of 16 on-off pulses of two widths, about 20 ms long, a quiet gap of about 12 ms, and the start of the next frame"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Set the carrier offset to 40000 Hz; the envelope plot fills with pulses.
- Each frame lasts about 20 ms, and the frames repeat.
:::

The **Frequency Xlating FIR Filter** shifts the frequency set by the Carrier offset slider down to 0 Hz and keeps $\pm 10$ kHz around it, as in the GNU Radio wiki's Frequency Shifting tutorial. A **Complex to Mag** block then gives the signal's envelope, and the time sink triggers on a rising edge at 0.5, so it holds one frame still on screen.

At 40,000 Hz the pulses appear. In the 2025 class the next move was to open URH's Spectrum Analyzer and fine-tune the carrier; with a recording, the slider does the same thing. Move the offset 10 kHz away from 40 kHz and the pulses drop to half their height, because the signal now sits at the edge of the filter; move it 20 kHz away and they disappear. The carrier is at $350.000 + 0.040 = 350.040$ MHz.
::::

::::{frame} Explore: The Live Band on the PlutoSDR
:::{present}
1. Run `L17-explore-pluto.grc` at 433.72 MHz and watch the waterfall.
2. Step the center frequency to find bursts that start and stop.
3. Retune near 315 MHz and look again.
:::

The recording showed one remote; the air around you holds many. `L17-explore-pluto.grc` is `L17-capture.grc` without the SigMF Sink: a **PlutoSDR Source** at 2 MS/s, the same spectrum, waterfall, and envelope displays, and a **Center frequency** control you can change while it runs. It records nothing, so the center frequency does not have to be set before it starts. It opens at 433.72 MHz, 200 kHz below 433.92 MHz, so the Pluto's DC spike at the center stays off the devices.

Look for what Step 1 taught: a steady line is a carrier that never stops, and a remote, a doorbell, or a weather sensor paints short streaks that come and go. Weather sensors send on their own about once a minute, so wait a minute before you move on. If the whole spectrum rises when a strong signal appears, lower the RX gain. Then step the center frequency to 314.8 MHz and look again. The Pluto only receives here.

SDR Flex is an optional quick look at the same band; nothing in this lesson needs it.
::::

::::{frame} Capture a Real Remote
:::{present}
- Record every button of a real 315 or 433.92 MHz key fob, doorbell, or sensor to SigMF.
- Find its carrier with URH's Spectrum Analyzer, as in 2025.
- Your Pluto only receives.
:::

The 2025 class captured a real remote, and every step so far works the same on one. Take a key fob, a wireless doorbell, or a weather sensor that you own; in the U.S. most use 315 MHz or 433.92 MHz, FCC Part 15 frequencies. Find it first with `L17-explore-pluto.grc`, then run `L17-capture.grc` with the variable `fc` set about 200 kHz below the device's frequency, so the Pluto's DC spike stays off the signal. Set it before you start the flowgraph, because the SigMF Sink writes the center frequency into the meta file when the flowgraph starts. Press each button a few times, close the flowgraph, and rename `capture.sigmf-data` and `.sigmf-meta` for that button.

URH's **Spectrum Analyzer**, under File, shows a live spectrum from a PlutoSDR, and in 2025 it was how the class fine-tuned the carrier: hold a button down and read the peak. Then open the recordings in URH as in Step 3. Receiving is always allowed, and your Pluto only receives in this step. A car key fob usually sends a **rolling code**, which changes with every press, so its frames will not repeat from press to press; the L17 Lab asks why.
::::

::::{frame} Step 2: Identify the Modulation
:::{present}
- The envelope switches between two levels, and the carrier's frequency does not move.
- That is on-off keying (OOK), Lesson 12's keyed carrier.
:::

The question for Step 2 is what the transmitter changes. The envelope plot shows the amplitude jumping between zero and one level, with nothing in between. The waterfall shows the bursts in one place; an FSK signal would show two tracks, as in Lesson 8, and a PSK signal would stay on at constant amplitude, as in Lesson 15. A carrier switched fully on and off is **on-off keying** (OOK), the simplest form of amplitude-shift keying (ASK). It is Lesson 12's CW, keyed hundreds of times faster by a circuit instead of a hand.

Most simple remotes, doorbells, and weather sensors use OOK, because the transmitter is one oscillator and one switch, and the receiver needs only an envelope detector like Lesson 11's.
::::

::::{frame} SigID: Name the Signal
:::{present}
<img src="../../viz/img/L17-sigid.png"
     alt="Spectrograms of three Simulated recordings, 0.8 s each, offsets from minus 50 to plus 50 kHz: signal A shows two parallel lines 6 kHz apart near plus 20 kHz, with the energy switching between them; signal B shows one band about 4 kHz wide near minus 15 kHz that stays on; signal C shows a narrow line that jumps to a new frequency every 80 ms among seven positions from minus 30 to plus 30 kHz"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Open `L17-sigid-a`, `-b`, and `-c` in `L17-sigmf-view.grc` and name each modulation.
- Set `samp_rate` to 100000 and `fc` to 915e6 first.
:::

The 2025 class practiced Step 2 on a set of unknown recordings, the **SigID** exercise: open each one in a frequency and waterfall flowgraph with a SigMF Source (Minimal) and say what it is. The three recordings here are Simulated, 0.8 s each at 100 kS/s; set `rec` to each file in turn. The figure shows their spectrograms, time going up.

:::{depth}
Signal A has two lines 6 kHz apart and the energy moves between them: two-level FSK, as in Lesson 8. Signal B is one band that never switches off and does not move: PSK, here QPSK, as in Lesson 15; its envelope stays constant and a constellation plot would show its four phases. Signal C is a narrow tone that jumps to a new frequency every 80 ms: a frequency hopper, as in Lesson 16. The faint horizontal lines in C are FFT frames that straddle a hop.
:::
::::

::::{frame} Step 3: URH
:::{present}
<img src="../../viz/img/L17-urh-frame.png"
     alt="URH's Interpretation tab, labeled simulated, zoomed in on the first frame of the recording: 16 bursts of two widths, a long pause, and the start of the next frame; Modulation ASK, Samples/Symbol 80, and the lines of chips below"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
1. In URH, choose File, New Project, then open the `.sigmf-data` file.
2. Enter 200000 as its sample rate.
3. Autodetect finds ASK and 80 samples a symbol.
:::

The 2025 class worked in a URH project, which keeps every recording and setting together; choose File, New Project and make a folder for it. URH reads a file it does not recognize as complex float, which matches `cf32_le`, so choose File, Open, set the filter to All Files, and open `L17-fan-remote.sigmf-data`. URH does not read the meta file, so enter the sample rate, 200000, in the signal's details.

On opening, URH's autodetect chose **ASK** and **80 samples per symbol**, and it set the Center, the threshold between off and on. At 200 kS/s, 80 samples is 400 µs, the length of the shortest pulse. URH calls each 400 µs slot a symbol; we call it a **chip**, because the next frame shows it takes more than one chip to make a bit. The text area lists one line of chips per burst, and **Pause** is the silence after it.
::::

::::{frame} Step 3: Chips to Bits
:::{present}
<img src="../../viz/img/L17-encodings.svg"
     alt="The bits 1 0 1 1 drawn three ways: pulse width, where every bit starts on and a 1 is a long pulse and a 0 a short one; pulse distance, where every pulse is short and the gap after it is long for a 1 and short for a 0; and Manchester, where a 1 is on then off and a 0 is off then on"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The fan remote's chips come in threes: `110` and `100`.
- Every bit starts on, and a long pulse is a 1: pulse-width coding.
:::

The first line URH lists starts `110 100 110 100 100 110 110 100`. Split into groups of three, every group is `110` or `100`, which is **pulse-width** coding: each bit starts with the carrier on, a 1 stays on for two chips and a 0 for one, and each bit ends off. The figure shows it beside two other common schemes. In **pulse-distance** coding every pulse is short and the length of the gap carries the bit; in **Manchester** coding every bit has a transition in its middle, so the chips come in pairs. The figure draws a 1 as on then off; IEEE 802.3 Ethernet uses the opposite convention, so a Manchester device can use either.

A frame of 16 bits is 48 chips, yet URH lists 46 or 47. The last chip of every bit is off, and a frame ending in a 0 ends in two off chips, so URH counts those chips as part of the pause. We add them back.
::::

::::{frame} Step 3: The Fields
:::{present}
<img src="../../viz/img/L17-frame.svg"
     alt="One frame of the Simulated fan remote's Light button: 48 chips of 400 microseconds, read as 16 bits, 1010 0110 0001 1110; the first 8 bits are the address 0xA6, the next 4 the command 0x1, and the last 4 the check 0xE; the frame lasts 19.2 ms"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Eight bits never change: the **address**.
- Four bits change with the button: the **command**.
- The last four are the command inverted: a **check**.
:::

Reading every press the same way gives one 16-bit word per button:

| Button | Word | Address | Command | Check |
| :-- | :-: | :-: | :-: | :-: |
| Light | 0xA61E | 0xA6 | 0x1 | 0xE |
| Fan Off | 0xA62D | 0xA6 | 0x2 | 0xD |
| Low | 0xA63C | 0xA6 | 0x3 | 0xC |
| Medium | 0xA64B | 0xA6 | 0x4 | 0xB |
| High | 0xA65A | 0xA6 | 0x5 | 0xA |

The first byte is the same for every button, so it identifies the remote, the way the DIP switches inside a real fan remote pick its code. The third nibble counts up with the buttons. The last nibble is the third one with every bit flipped, so a receiver can reject a frame whose two nibbles disagree.
::::

::::{frame} The 2025 Questions
:class: read-only

The 2025 slides asked five questions about the encoding. For the Simulated fan remote, the answers come from the URH display and the table above.

| Question | What the fan remote shows |
| :-- | :-- |
| What fields would we expect in a simple message? | an address that picks the fan, a command that picks the button, and a check |
| How are 1s and 0s encoded? | pulse width: `110` is a 1 and `100` is a 0, 400 µs a chip |
| Can we identify parts of the message from the captures? | yes, by comparing the five buttons: the bits that never change are the address, and the bits that do are the command |
| Is a command sent just once? | no: each press sends the frame 6 times, with about 12 ms of silence between frames |
| What else do you notice? | the steady carrier at 349.945 MHz is not the remote, and each frame's last off chips run into the pause |

The repeats let a receiver that misses one frame, to noise or to a collision with another remote, act on the next. They also mean that a press lasts about 190 ms, long enough to see on the waterfall.
::::

::::{frame} Bit Rate and Baud Rate
:class: read-only

The chip is the shortest thing the transmitter switches, so the **baud rate**, the symbol rate URH works in, is one chip per symbol. The **bit rate** counts data bits, and each bit takes three chips:

$$\begin{aligned}
\text{chip} &= \frac{80}{200{,}000 \text{ S/s}} \\
&= 400\ \mu\text{s}, \\
\text{baud rate} &= \frac{1}{400\ \mu\text{s}} \\
&= 2500 \text{ baud}, \\
\text{bit rate} &= \frac{2500}{3} \\
&= 833 \text{ bits/s}.
\end{aligned}$$

A frame of 16 bits takes $16 \times 1.2 = 19.2$ ms, and with the 12 ms gap a frame starts every 31.2 ms. These are the numbers the encoder needs: its Repeat block holds each chip for `chip_len` samples, and its Stream Mux inserts the gap.
::::

::::{frame} Pulse Decoder Explorer
:class: viz-frame

:::{depth}
The explorer draws one frame of the Simulated fan remote's envelope and reads it the way URH does: it divides the frame into chips of the chosen length from the first rising edge, compares the middle of each chip with the threshold, and groups the chips in threes. It opens at a chip length of 300 µs, which is wrong. Move the Chip length slider until no group is marked `?`, then pick another button, then raise the noise.
:::

:::{present}
<iframe src="../../viz/pulse-decoder.html"
        width="100%" height="441"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Pulse decoder explorer: the Simulated fan remote's envelope with a threshold and a grid of chips of a chosen length, the chips grouped in threes as pulse-width bits, the address, command, and check fields, and readouts of the chips read, the groups that are neither 110 nor 100, the bit rate, and the frame in hex">
</iframe>
:::
::::

::::{frame} Noise
:::{present}
- Raise the explorer's noise until the frame breaks.
- Frames read cleanly to about 0.4; from about 0.45 the groups break apart.
:::

Raise the Noise amplitude in the explorer a step at a time, and press new noise a few times at each step. Up to about 0.4 the envelope roughens but the frame reads correctly. From about 0.45 chips start to land on the wrong side of the threshold, and most often that breaks a group, so it reads as neither `110` nor `100` and shows `?`; by 0.5 almost every frame has a broken group. Now and then a flipped chip turns one bit into the other instead, and then the frame still reads as 16 bits but the Frame readout says the check fails.

URH shows the same thing on a real recording: as the signal weakens, the lines of chips stop matching from one repeat to the next. A receiver throws away a frame it cannot read. The check catches a frame that reads but has a wrong bit in the command; a flipped address bit passes it, and the frame then reads as another remote's. Remotes repeat each frame so that one of the six tries usually gets through.
::::

::::{frame} Step 4: Build an Encoder
:::{present}
<img src="../../viz/img/L17-grc-tx-sim.png"
     alt="L17-fan-tx-sim.grc in GNU Radio Companion: a QT GUI Chooser of the five buttons sets the variables word and bits; a Vector Source of bits, a Map of 4 and 6, Unpack K Bits with K 3, Char To Float, a Repeat of 80, and a Stream Mux with a Constant Source of 0 make the envelope; Float To Complex and a Multiply with a 40 kHz Signal Source put it on a carrier; a Noise Source, an Add, a Throttle, a waterfall, an envelope time sink, and a SigMF Sink follow"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- **Map** turns a 0 into 4 and a 1 into 6; **Unpack K Bits** with K = 3 gives `100` and `110`.
- **Repeat** and **Stream Mux** set the chip length and the gap.
:::

The encoder is the 2025 hier block laid out flat. A **Vector Source** repeats the 16 bits of the chosen button's word. A **Map** replaces each bit with a number whose binary form is its chip pattern, 0 with 4 (`100`) and 1 with 6 (`110`), and **Unpack K Bits** with $K = 3$ writes those three bits out one at a time, most significant first. **Repeat** holds each chip for `chip_len` = 80 samples, 400 µs at 200 kS/s.

The **Stream Mux** takes $48 \times 80 = 3840$ samples, one frame, from the encoder, then $30 \times 80 = 2400$ samples of zero from a **Constant Source**, the 12 ms gap, and repeats. **Float To Complex** and a **Multiply** with a 40 kHz **Signal Source** put the envelope on the carrier, as Lesson 12's keyer did. `L17-encoder.grc` packs the whole chain, from the Vector Source to the Multiply, into one hier block, as the 2025 class did and as the GNU Radio wiki's Hier Blocks and Parameters tutorial describes. The Map comes before Unpack K Bits because it is the Map that turns each bit into its chip pattern.
::::

::::{frame} Step 4: Check the Encoder
:::{present}
<img src="../../viz/img/L17-tx-sim.png"
     alt="L17-fan-tx-sim.grc running, labeled simulated, with the Light button chosen and noise amplitude 0.05: the waterfall shows a steady signal near 350.04 MHz, and the envelope shows a frame of 16 pulses of two widths, a 12 ms gap, and the next frame, matching the recording"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Run `L17-fan-tx-sim.grc` and choose a button; compare the envelope with the recording.
- Open `my-fan-remote.sigmf-data` in URH: the chips should match.
:::

`L17-fan-tx-sim.grc` runs the encoder with no radio. Its envelope plot should match the recording's frame for the same button, pulse for pulse, and its SigMF Sink writes what it makes to `my-fan-remote.sigmf-data` and `.sigmf-meta` while it runs. Run it for a few seconds, close it, and open the recording in URH beside `L17-fan-remote.sigmf-data`: with the same sample rate and 80 samples per symbol, the lines of chips should be identical.

That comparison is the test of the reverse engineering. If our encoder makes chips the original receiver would accept, we have found the carrier, the modulation, the encoding, and the fields correctly. One difference remains: the encoder repeats its frame for as long as it runs, while the remote stops after six.
::::

::::{frame} The Hier Block
:class: read-only

<img src="../../viz/img/L17-grc-encoder.png"
     alt="L17-encoder.grc in GNU Radio Companion: seven parameters, the bits of one frame, the chip pattern for 0 and 1 (default 4 and 6), chips per bit (3), samples per chip (80), the gap in chips (30), the carrier offset (40 kHz), and the sample rate (200 kHz); a Vector Source of the bits, Map, Unpack K Bits, Char To Float, Repeat, a Stream Mux with a Constant Source, Float To Complex, and a Multiply with a Signal Source, ending in a Pad Sink"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto 12px;">

`L17-encoder.grc` is the encoder as a **hier block**, the form the 2025 class built: Vector Source, Map, Unpack K Bits, Repeat, Stream Mux, and a Multiply with a Signal Source, in one block with no inputs. Its parameters are the frame's bits, the chip patterns, the chips per bit, the samples per chip, the gap, the carrier offset, and the sample rate, so the same block serves any pulse-coded remote of fixed bit length. Open it in GRC and press Generate once; GRC writes `L17_ook_encoder.block.yml` and its Python file to `~/.grc_gnuradio`, and after you press the Reload Blocks button on the toolbar the block, **L17 OOK Encoder**, appears under ECE 448. The lesson's flowgraphs use the same blocks laid out flat, so they open without that step.
::::

::::{frame} Step 5: Transmit
:::{present}
- `L17-fan-tx-pluto.grc` sends the encoder from a PlutoSDR at 350.04 MHz.
- Cadets: through a 30 dB attenuator into a second PlutoSDR, never an antenna.
- Instructor demo: the real fan, over the air, at very low power.
:::

The last step puts the encoder on a radio. `L17-fan-tx-pluto.grc` is the simulation flowgraph at 1 MS/s, so `chip_len` is 400 samples, with a **PlutoSDR Sink** tuned to 350 MHz in place of the noise and the waterfall; the 40 kHz tone puts the carrier at 350.04 MHz. A short SMA cable with an inline 30 dB attenuator carries it to a second PlutoSDR running `L17-capture.grc`, with `fc` set to 350e6 before it starts, which records what arrives as a SigMF pair. Open that recording in URH as in Step 3: the chips should match `L17-fan-remote.sigmf-data`.

Cadets transmit only into a cable, and only when the lesson says to; 350 MHz is an FCC Part 15 frequency, not an ISM band. The TX attenuation slider opens at 60 dB and cannot go below 30 dB; never connect an antenna to this flowgraph.

The 2025 class ended by operating the fan, and this one does too, as an instructor demo. Dr. Rogers records the classroom's Hunter fan remote, decodes it with the same steps, and sends its Light command from his own encoder flowgraph over the air, a few meters from the fan, at the lowest power that still works it. The fan answers a transmitter it has never seen, which is the point of the lesson: a fixed code has no way to tell the two apart. Both Pluto flowgraphs have been compiled but not run on a radio, so the L17 Lab is their first run on hardware.
::::

::::{frame} Key Point
:::{present}
:class: callout
Reverse engineering runs in five steps: find the carrier, identify the modulation, identify the encoding, build an encoder, and transmit. An encoder whose output decodes the same as the recording confirms the first three.
:::
::::

::::{frame} Downloads
:class: read-only doc-links

- <a class="doc-link" href="../../grc/L17-fan-remote.sigmf-data" download>L17-fan-remote.sigmf-data</a> and <a class="doc-link" href="../../grc/L17-fan-remote.sigmf-meta" download>L17-fan-remote.sigmf-meta</a>: the Simulated fan remote, one press of each button, 200 kS/s centered at 350 MHz, 3.9 MB. Keep the two files in the same folder.
- <a class="doc-link" href="../../grc/L17-sigmf-view.grc" download>L17-sigmf-view.grc</a>: a SigMF recording's spectrum and waterfall, a carrier-offset slider, and the envelope after the shift. Set `rec`, `samp_rate`, and `fc` from the meta file. No hardware needed.
- <a class="doc-link" href="../../grc/L17-fan-tx-sim.grc" download>L17-fan-tx-sim.grc</a>: the encoder with a button chooser and a noise slider, recording to `my-fan-remote.sigmf-data`. No hardware needed.
- <a class="doc-link" href="../../grc/L17-encoder.grc" download>L17-encoder.grc</a>: the encoder as a hier block, L17 OOK Encoder. Press Generate once to install it.
- <a class="doc-link" href="../../grc/L17-fan-remote-gen.grc" download>L17-fan-remote-gen.grc</a>: the flowgraph that made the recording. No hardware needed.
- <a class="doc-link" href="../../grc/L17-sigid-a.sigmf-data" download>L17-sigid-a</a>, <a class="doc-link" href="../../grc/L17-sigid-b.sigmf-data" download>-b</a>, and <a class="doc-link" href="../../grc/L17-sigid-c.sigmf-data" download>-c</a> (.sigmf-data), with <a class="doc-link" href="../../grc/L17-sigid-a.sigmf-meta" download>a</a>, <a class="doc-link" href="../../grc/L17-sigid-b.sigmf-meta" download>b</a>, and <a class="doc-link" href="../../grc/L17-sigid-c.sigmf-meta" download>c</a> meta files: three Simulated unknown signals for SigID, 0.8 s each at 100 kS/s, 640 KB each. <a class="doc-link" href="../../grc/L17-sigid-gen.grc" download>L17-sigid-gen.grc</a> made them.
- <a class="doc-link" href="../../grc/L17-explore-pluto.grc" download>L17-explore-pluto.grc</a>: a PlutoSDR Source at 2 MS/s with spectrum, waterfall, and envelope displays and a center frequency you change while it runs. Receive only; records nothing.
- <a class="doc-link" href="../../grc/L17-capture.grc" download>L17-capture.grc</a>: a PlutoSDR Source at 1 MS/s with spectrum, waterfall, and envelope displays, recording to `capture.sigmf-data`. Receive only; needs a PlutoSDR. Set `fc` before you run it.
- <a class="doc-link" href="../../grc/L17-fan-tx-pluto.grc" download>L17-fan-tx-pluto.grc</a>: the encoder on a PlutoSDR at 350.04 MHz. Transmit only into the cable, through a 30 dB attenuator, to a second PlutoSDR.
- Optional: <a class="doc-link" href="../../grc/L17-capture-rtl.grc" download>L17-capture-rtl.grc</a> is `L17-capture.grc` with a Soapy RTL-SDR Source at 1.024 MS/s, if you own an RTL-SDR. Nothing in the lesson or lab needs it.
- <a class="doc-link" href="https://github.com/jopohl/urh" target="_blank" rel="noopener">Universal Radio Hacker (URH)</a>: its README gives an installer for Windows and `pipx install urh` for Linux and macOS.
- <a class="doc-link" href="https://wiki.gnuradio.org/index.php/Frequency_Shifting" target="_blank" rel="noopener">GNU Radio wiki: Frequency Shifting</a> and <a class="doc-link" href="https://wiki.gnuradio.org/index.php/Hier_Blocks_and_Parameters" target="_blank" rel="noopener">Hier Blocks and Parameters</a>: the tutorials behind Steps 1 and 4.
- <a class="doc-link" href="https://pysdr.org/content/iq_files.html" target="_blank" rel="noopener">PySDR: IQ Files and SigMF</a>: the recording format.
- <a class="doc-link" href="https://livethisdream.github.io/sdr-flex/" target="_blank" rel="noopener">SDR Flex</a>: an optional quick look at a band.

Open a `.grc` file from GRC's File menu, or run `gnuradio-companion L17-sigmf-view.grc` from the radioconda prompt, in the folder that holds the recording.
::::

::::{frame} Summary
:class: read-only

| Step | What we did | The fan remote |
| :-- | :-- | :-- |
| 1. Carrier | spectrum and waterfall, then shift to 0 Hz | 350.040 MHz; the steady line is not the remote |
| 2. Modulation | what the envelope and the waterfall do | OOK |
| 3. Encoding | URH: chips, then bits, then fields | 400 µs chips, 3-chip pulse width, 16 bits: address, command, check |
| Rates | chips and bits per second | 2500 baud, 833 bits/s, 6 frames a press |
| 4. Encoder | Map, Unpack K Bits, Repeat, Stream Mux, carrier | chips match the recording in URH |
| 5. Transmit | PlutoSDR into a cable with a 30 dB attenuator | a second PlutoSDR records it as SigMF |
| Noise | watch the chips and the check | bad frames fail the check |
::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE448_L17_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE448_L17_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Looking Ahead
:::{present}
- The L17 Lab hands you a different remote's recording and no description.
- Lessons 18 and 19 decode signals whose formats are published: ADS-B and AIS.
:::

The L17 Lab is today's process on a device you have not seen. You get a SigMF recording of a Simulated remote with several buttons, with settings of its own, and you find its carrier, modulation, encoding, and fields, build an encoder for it from an empty canvas, check your encoder against the recording in URH, and then send it through a PlutoSDR and a cable to a second PlutoSDR.

Lessons 18 and 19 receive aircraft and ship transponders. Their formats are public standards, so there the work is building and running the receiver rather than discovering the format.
::::
