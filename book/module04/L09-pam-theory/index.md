---
frame_view: true
---

# L9 - PAM Theory

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">PAM Theory</h1>

<div class="title-rule"></div>

A PAM transmitter and receiver in GNU Radio: pulse shaping, bandwidth, the eye diagram, matched filtering, and symbol-timing recovery.

Lesson 9 · Module 4: Digital Modulation · Dr. Neil Rogers
::::

::::{frame} Slides
:class: read-only

:::{admonition} Slides
:class: slides
<a href="../../slides/L09-pam-theory.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L09-pam-theory.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L09-pam-theory.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '4'; counter-reset: lo 1">
  <li>I can describe PAM theory and identify the pulse-shaping, symbol-rate, and bandwidth trade-offs.</li>
  <li>I can apply matched filtering and symbol-timing recovery to a received PAM signal.</li>
</ol>
::::

::::{frame} A PAM Link in One Flowgraph
:::{present}
<img src="../../viz/img/L09-grc-matched-filter.png"
     alt="GNU Radio Companion with the L9 matched-filter flowgraph open: a Random Source, Chunks to Symbols, and a Throttle feed an Interpolating FIR Filter with RRC taps; a Fractional Resampler and a Noise Source model the channel; a Decimating FIR Filter is the matched filter, feeding a Keep 1 in N, a Symbol Sync, two eye sinks, and a time sink"
     style="max-width: 690px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Today's flowgraph sends random bits as PAM through noise and a clock error.
- Each block is one idea from this lesson.
:::

Lesson 10 sends text over a PAM link. Before that works, the link has to carry random bits reliably, and the figure is the flowgraph that does it. Bits become **symbols**, a filter shapes each symbol into a pulse that fits a fixed bandwidth, the channel adds noise and a clock error, and the receiver filters, finds the right instant to sample, and recovers one number per symbol.

Lesson 3 covered what happens at that last step: once we have one clean sample per symbol, the constellation and the bit error rate follow. This lesson covers everything before it. Each part below adds one block to the flowgraph, and every block has a parameter we have to choose.
::::

::::{frame} Part 1: Bits to Levels
:::{present}
<img src="../../viz/img/L09-pam-levels.svg"
     alt="Eight bits, 1 0 1 1 0 0 1 0, as 2-PAM: eight rectangular pulses at plus or minus 1. The same bits as Gray-coded 4-PAM: four pulses, each two bit periods long, at levels plus 3, plus 1, minus 3, and plus 3"
     style="max-width: 720px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- **PAM** sends each symbol as a pulse whose amplitude carries the bits.
- $M$ levels carry $\log_2 M$ bits, so $R_s = R_b/\log_2 M$.
:::

**Pulse amplitude modulation** (PAM) is the simplest digital signal: each symbol is a pulse, and its height carries the data. 2-PAM uses two levels, $\pm 1$, and carries one bit per symbol. 4-PAM uses four, $\pm 1$ and $\pm 3$, and carries two bits per symbol, Gray coded as in Lesson 3 so that neighboring levels differ in one bit. In general, $M$ levels carry $\log_2 M$ bits, so the **symbol rate** $R_s$, in symbols per second or **baud**, is

$$R_s = \frac{R_b}{\log_2 M}$$

where $R_b$ is the bit rate. The figure sends the same eight bits both ways: 4-PAM takes half as many symbols, each twice as long. In GNU Radio, a **Chunks to Symbols** block makes this mapping: it reads a number from 0 to $M-1$ and outputs the matching level from a table, such as `[-1, 1]`.
::::

::::{frame} Part 2: Why Not Rectangular Pulses?
:::{present}
- A rectangular pulse has a sinc spectrum.
- Its first sidelobe is only 13 dB down, and the sidelobes fall off slowly.
- The signal spills into neighboring channels.
:::

The waveforms in the last figure use **rectangular pulses**: each level holds for one symbol period $T = 1/R_s$, then jumps. The jumps are the problem. The spectrum of a rectangular pulse is a sinc, with its first nulls at $\pm R_s$ and sidelobes that continue far beyond. The first sidelobe is only 13 dB below the peak, and the sidelobes decay slowly with frequency.

A radio channel has a fixed width, set by a regulator or by the neighbors on either side. A rectangular-pulse transmitter puts power well outside its own channel, which interferes with other users and fails the emission limits on any license. The fix is to round off the pulse so that its spectrum ends, and the shape we use for that is the raised cosine.
::::

::::{frame} Raised Cosine and Bandwidth
:::{present}
<img src="../../viz/img/L09-rc-spectrum.svg"
     alt="Raised-cosine spectra plotted against frequency in multiples of the symbol rate: alpha 0 is a rectangle from minus 0.5 to plus 0.5; alpha 0.35 is flat to 0.325 and rolls off to zero at 0.675; alpha 1 is a cosine bump reaching zero at plus and minus 1"
     style="max-width: 720px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
$$B = (1+\alpha)R_s$$

- The roll-off $\alpha$ runs from 0 to 1; 0.35 is common.
:::

The **raised-cosine** pulse has a spectrum that is flat in the middle and rolls off smoothly to exactly zero. The **roll-off factor** $\alpha$, between 0 and 1, sets how gradual the edge is. The spectrum spans $-(1+\alpha)R_s/2$ to $+(1+\alpha)R_s/2$, so on GNU Radio's complex baseband display, and on the air after upconversion, the signal occupies

$$B = (1+\alpha)R_s.$$

At $\alpha = 0$ the bandwidth is the minimum possible, $R_s$, but that pulse is impractical: its spectrum has a brick-wall edge, so its pulse lasts forever. At $\alpha = 1$ the bandwidth doubles, but the pulse is short and forgiving of timing errors. Most real systems sit between 0.2 and 0.5; 0.35 is a common default and the value used throughout this lesson.
::::

::::{frame} Zero Intersymbol Interference
:::{present}
<img src="../../viz/img/L09-rc-pulses.svg"
     alt="Three raised-cosine pulses with alpha 0.35, one symbol period apart, for symbols plus 1, minus 1, plus 1, drawn dashed, and their sum in red. At each symbol instant the sum passes exactly through that symbol's value, because every other pulse is zero there"
     style="max-width: 720px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Each pulse is zero at every other symbol instant.
- Sampled at the right instants, the sum gives back each symbol exactly.
:::

A smooth pulse lasts longer than one symbol, so neighboring pulses overlap. Overlap that corrupts a sample is **intersymbol interference** (ISI). The raised cosine avoids it by design: each pulse passes through zero at every symbol instant except its own. In the figure, three overlapping pulses add to the red waveform, and at each symbol instant the waveform equals that symbol's value exactly, because the other two pulses are zero there.

That property holds only at the symbol instants. Between them, the pulses add to values that depend on the neighbors, so a receiver that samples at the wrong time sees interference. Finding the right time is Part 5.
::::

::::{frame} Root-Raised Cosine: Half at Each End
:::{present}
- The transmitter and receiver each use a **root-raised cosine** (RRC).
- Together the two filters make one raised cosine.
- The receive half also rejects noise outside the signal band.
:::

In practice we split the raised cosine into two equal halves. The transmitter shapes each symbol with a **root-raised-cosine** (RRC) filter, whose spectrum is the square root of the raised cosine's, so the transmitted bandwidth is still $(1+\alpha)R_s$. The receiver applies the same RRC filter again, and the two in cascade multiply to one raised cosine, with its zero-ISI property, at the receiver's output.

The split serves a second purpose. The receive filter passes the signal's band and rejects the noise everywhere else, and the same RRC is the filter that does this best, as Part 4 shows. A consequence is that the transmitted signal alone does not have zero ISI; only the output of the receive filter does.
::::

::::{frame} Pulse Shaping in GNU Radio
:::{present}
<img src="../../viz/img/L09-grc-pulse-shaping.png"
     alt="GNU Radio Companion with the L9 pulse-shaping flowgraph open: a Random Source, Chunks to Symbols, and Throttle split into a Repeat block, which makes rectangular pulses, and an Interpolating FIR Filter with rrc_taps; both feed a QT GUI Frequency Sink, and the RRC branch also feeds a QT GUI Eye Sink. An alpha slider sets the roll-off"
     style="max-width: 690px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
```python
firdes.root_raised_cosine(sps, samp_rate, samp_rate/sps, alpha, 11*sps)
```
:::

The pulse-shaping flowgraph makes 2-PAM symbols at $R_s = 4$ kbaud and shapes them two ways. The **Repeat** block holds each symbol for `sps` samples, which is a rectangular pulse. The **Interpolating FIR Filter** does the RRC shaping: it inserts `sps` $- 1$ zeros after each symbol to raise the sample rate, then filters with RRC taps, so each symbol becomes one smooth pulse.

The taps come from `firdes.root_raised_cosine`, whose five arguments are the gain, the sample rate, the symbol rate, $\alpha$, and the number of taps. We set the gain to `sps` so the interpolated pulse keeps the symbol's amplitude, and the length to `11*sps`, which makes the pulse 11 symbols long; a shorter filter truncates the pulse and raises its sidelobes. The **samples per symbol**, `sps` = 8 here, must be an integer, and it ties the rates together: $R_s = $ `samp_rate/sps` $= 32\text{ kHz}/8 = 4$ kbaud.
::::

::::{frame} Rectangular and RRC Spectra
:::{present}
<img src="../../viz/img/L09-pulse-shaping.png"
     alt="The L9 pulse-shaping flowgraph running with alpha 0.35: the frequency sink shows the rectangular signal in blue with sidelobes across the whole 32 kHz span only 20 to 30 dB below its peak, and the RRC signal in red confined to about plus and minus 2.7 kHz; the eye sink shows the RRC signal alone, with an eye that is open but crossed by traces between the levels"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- RRC at $\alpha = 0.35$ fits $4 \times 1.35 = 5.4$ kHz.
- The rectangular sidelobes fill the whole 32 kHz span.
:::

With the flowgraph running, the frequency sink shows what pulse shaping does. The rectangular signal (blue) has its main lobe between $\pm 4$ kHz, the first nulls at $\pm R_s$, and sidelobes only 20 to 30 dB below its peak across the entire 32 kHz the samples can show. The RRC signal (red) ends near $\pm 2.7$ kHz, half of $B = 1.35 \times 4 = 5.4$ kHz, and falls 50 dB or more below its peak outside that. Drag the $\alpha$ slider and the red edge moves with $(1+\alpha)R_s/2$.

The eye sink on the right shows the RRC signal before any receive filter. The traces cluster near $\pm 1$ but do not pass cleanly through them, because one RRC alone has some ISI. The receive filter of Part 4 removes it.
::::

::::{frame} Symbol Rate and Bandwidth
:class: read-only

A link must fit a 12.96 kHz channel. With $\alpha = 0.35$, the largest symbol rate that fits is

$$\begin{aligned}
R_s &= \frac{B}{1+\alpha} \\
    &= \frac{12.96\ \text{kHz}}{1.35} = 9.6\ \text{kbaud}.
\end{aligned}$$

The number of levels sets the bit rate in that bandwidth, and more levels need more signal power. The $E_b/N_0$ column is the value for a bit error rate of $10^{-5}$ from Lesson 3's curves.

| Modulation | Bits per symbol | Bit rate at 9.6 kbaud | Bandwidth | $E_b/N_0$ at $10^{-5}$ |
| :-- | :-: | :-: | :-: | :-: |
| 2-PAM | 1 | 9.6 kb/s | 12.96 kHz | 9.6 dB |
| 4-PAM | 2 | 19.2 kb/s | 12.96 kHz | 13.4 dB |

4-PAM doubles the bit rate in the same channel, and it needs 3.8 dB more $E_b/N_0$ to keep the same error rate, because its four levels sit closer together. The other way to double the bit rate is to double the symbol rate, which doubles the bandwidth to 25.92 kHz and no longer fits the channel. Lowering $\alpha$ to 0.25 instead would fit 10.4 kbaud, but with a longer pulse that tolerates less timing error.
::::

::::{frame} Part 3: The Eye Diagram
:::{present}
<img src="../../viz/img/L09-eye-anatomy.svg"
     alt="A noiseless raised-cosine 2-PAM eye diagram two symbol periods wide: traces from many symbols overlaid, converging on plus 1 and minus 1 at time 0 and at plus and minus T, with a dashed sample-here line at time 0 and an arrow marking the eye opening between the two levels"
     style="max-width: 560px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- An **eye diagram** overlays the waveform, a few symbols at a time.
- Sample where the eye is widest open.
:::

An **eye diagram** cuts the received waveform into pieces two symbols long and draws them all on top of each other. For a raised-cosine signal with no noise, every trace passes exactly through $\pm 1$ at the symbol instant, and the gap between the levels there, the **eye opening**, is as large as it can be. Away from the symbol instant the traces spread out, and they cross zero halfway between symbols.

The eye shows three things at a glance. The height of the opening is the margin against noise, the width is the margin against timing error, and the center is where the receiver should sample. Noise fills in the eye from above and below, ISI makes the traces miss the levels, and a timing error moves the sampling instant off center. GNU Radio draws eyes with the **QT GUI Eye Sink**, which needs only the samples per symbol.
::::

::::{frame} PAM Eye Explorer
:class: viz-frame

:::{depth}
The left panel is the eye of the received signal and the right panel is the transmitted spectrum, with a rectangular pulse in gray for comparison. Start with "RRC + matched" at $\alpha = 0.35$: the eye is open and the spectrum ends at $(1+\alpha)R_s/2$. Lower $\alpha$ and the spectrum narrows while the eye's waist pinches, so timing error matters more. Switch to "rectangular" and watch the spectrum spread. Switch to "RRC only" and the eye picks up ISI, because the matched filter is missing. Then lower $E_s/N_0$, move the sample time off center, and switch to 4-PAM, and watch the symbol errors climb.
:::

:::{present}
<iframe src="../../viz/pam-eye.html"
        width="100%" height="447"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="PAM eye explorer: a 2-PAM or 4-PAM signal with rectangular, RRC, or RRC plus matched-filter pulses, showing the eye diagram, the transmitted spectrum, the eye opening, and the symbol errors as roll-off, noise, and sample time change">
</iframe>
:::
::::

::::{frame} Part 4: Matched Filtering
:::{present}
<img src="../../viz/img/L09-matched-filter.png"
     alt="The L9 matched-filter flowgraph running with noise amplitude 0.6 and no clock error: the eye of the received signal is closed by noise, and the eye after the matched filter is open, with traces converging near plus and minus 1"
     style="max-width: 600px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The **matched filter** is the transmit pulse, reused at the receiver.
- At 8 samples per symbol it removes about 9 dB of noise.
:::

The receiver's job at each symbol is to decide which level was sent, and the best it can do is make the signal as large as possible relative to the noise at the sampling instant. The filter that does this is the **matched filter**: a filter whose impulse response is the transmitted pulse, reversed in time. An RRC pulse is symmetric, so the matched filter for RRC shaping is the same RRC filter, which is why the split of the last part works.

The screenshot shows the effect with the noise turned up. Before the filter, the noise occupies the full 32 kHz the samples represent, and the eye is closed. The matched filter keeps only the signal's 5.4 kHz, which removes about 9 dB of noise at 8 samples per symbol, and the eye opens. In GNU Radio the matched filter is a **Decimating FIR Filter** with `rx_taps` from the same `firdes.root_raised_cosine` call, with a gain of 1 and a decimation of 1, so it keeps all 8 samples per symbol for the timing recovery that follows.
::::

::::{frame} Part 5: Symbol-Timing Recovery
:::{present}
<img src="../../viz/img/L09-timing.png"
     alt="The L9 matched-filter flowgraph running with noise amplitude 0.3 and a 500 ppm clock error: the matched-filter eye is smeared as the sampling point drifts; the symbols plot shows Keep 1 in N samples in blue scattered between plus and minus 1, and Symbol Sync samples in red clustered tightly at plus and minus 1"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The receiver's clock never matches the transmitter's exactly.
- Plain decimation drifts through the eye; **Symbol Sync** tracks its center.
:::

After the matched filter, the receiver keeps one sample per symbol. The simplest way is to keep every eighth sample, which is what **Keep 1 in N** does, but it only works if the receiver knows where the eye's center falls and that point stays fixed, and neither is true. The receiver's sample clock and the transmitter's symbol clock come from different oscillators, so they start at an arbitrary offset and drift apart. A clock error of 500 ppm, set on the slider, slips the sampling point by one sample every 2000 samples.

The right-hand plot shows the result. The blue samples from Keep 1 in N land wherever the drift has carried them, often near the zero crossings, where the receiver would decide many of them wrong. The red samples from the **Symbol Sync** block stay clustered at $\pm 1$, because the block measures where the eye's center is and keeps adjusting its sampling instant to follow it. Real oscillators are accurate to tens of ppm, not 500; the flowgraph exaggerates the error so the drift shows in seconds. At 20 ppm and 4 kbaud the sampling point still slips a whole symbol every 12.5 s, so no receiver of a long message can do without timing recovery.
::::

::::{frame} The Symbol Sync Block
:::{present}
| Parameter | L9 value | What it sets |
| :-- | :-- | :-- |
| Timing error detector | Gardner | how the block measures the error |
| Samples per symbol | `sps` = 8 | the nominal spacing |
| Loop bandwidth | 0.045 | tracking speed against jitter |
| Output samples/symbol | 1 | one sample per symbol out |
:::

**Symbol Sync** is a feedback loop. A **timing error detector** (TED) estimates, from the samples around each symbol, whether the current sampling instant is early or late; a loop filter smooths that estimate; and an interpolator computes the signal's value at the corrected instant, which is usually between two input samples. The **Gardner** TED we use compares the sample halfway between two symbols with the two symbol samples on either side: when the timing is right, a transition crosses zero exactly halfway. It needs at least 2 samples per symbol, and it does not need to know which symbols were sent, so it works before any decisions are made.

The **loop bandwidth** is the main setting. A larger value tracks a drifting clock faster but lets noise jitter the sampling instant; a smaller value is steadier but slower to lock and to follow a drift. The default of 0.045 works for the flowgraph's 500 ppm error. The block can also apply the matched filter itself, with its "Polyphase Filterbank, Matched Filter" interpolator, but we keep the matched filter as its own block in this lesson so that each idea has its own block.
::::

::::{frame} The PAM Receiver in GNU Radio
:::{present}
| Idea | Block | Parameter |
| :-- | :-- | :-- |
| Symbol mapping | Chunks to Symbols | level table |
| Pulse shaping | Interpolating FIR Filter | RRC taps, `sps` |
| Matched filter | Decimating FIR Filter | the same RRC |
| Eye check | QT GUI Eye Sink | `sps` |
| Timing recovery | Symbol Sync | TED, loop bandwidth |
:::

Every idea in this lesson became one block and one or two parameters. Choosing them for a real link starts from the channel: its width and $\alpha$ fix the symbol rate, the symbol rate and the radio's sample rate fix `sps`, and `sps` and $\alpha$ fix both RRC filters. The eye sink is the check at each stage, before and after the matched filter and after timing recovery.

On an SDR, the transmit half of this flowgraph ends at the radio's sink block and the receive half starts at its source block, with the channel replaced by a real one. The noise and the clock error then come from the hardware rather than from a slider, which is why the receiver we built today already handles both.
::::

::::{frame} Key Point
:::{present}
:class: callout
The RRC filter at the transmitter fixes the bandwidth at $(1+\alpha)R_s$. The same RRC filter at the receiver rejects the noise and removes the ISI, and Symbol Sync finds the center of the eye.
:::
::::

::::{frame} Downloads
:class: read-only doc-links

- <a class="doc-link" href="../../grc/L09-pulse-shaping.grc" download>L09-pulse-shaping.grc</a>: 2-PAM with rectangular and RRC pulses, their spectra, and the RRC eye, with a roll-off slider. No hardware needed.
- <a class="doc-link" href="../../grc/L09-matched-filter.grc" download>L09-matched-filter.grc</a>: an RRC 2-PAM signal through noise and a clock error, then a matched filter and Symbol Sync, with eyes before and after the filter and plain decimation compared with timing recovery. No hardware needed.

Open a `.grc` file from GRC's File menu, or run `gnuradio-companion L09-pulse-shaping.grc` from the radioconda prompt.
::::

::::{frame} Summary
:class: read-only

| Idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Symbol rate | $R_s = R_b/\log_2 M$ | 4-PAM halves $R_s$ for the same $R_b$ |
| Raised cosine | zero-ISI pulse with roll-off $\alpha$ | $B = (1+\alpha)R_s$ |
| Root-raised cosine | half the raised cosine, at each end | `firdes.root_raised_cosine`, `11*sps` taps |
| Samples per symbol | `sps` = `samp_rate`/$R_s$ | an integer; L9 uses 8 |
| Eye diagram | waveform overlaid two symbols at a time | sample at the widest opening |
| Matched filter | the transmit pulse, at the receiver | about 9 dB less noise at 8 sps |
| Symbol Sync | timing error detector, loop, interpolator | Gardner, loop bandwidth 0.045 |
::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE448_L09_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE448_L09_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Looking Ahead
:::{present}
- Lesson 10 sends ASCII text over this PAM link.
- It adds bytes to bits, a frame marker, and a slicer back to bits.
- The L10 Lab runs the link over real radios.
:::

Today's receiver ends with one clean sample per symbol, and Lesson 3 already said what to do with it: decide the nearest level. Lesson 10 builds the rest of a working link around today's flowgraph. Text becomes bytes and bytes become bits before the Chunks to Symbols block; after Symbol Sync, a **Binary Slicer** turns each sample back into a bit; and because a receiver that starts listening mid-message cannot tell where one byte ends and the next begins, the transmitter adds a known marker that the receiver searches for.

The L10 Lab then moves the link from simulation to radios, where the noise and the clock error come from real hardware. Before Lesson 10, run both L9 flowgraphs, and be able to find the symbol rate that fits a given channel and the `sps` that a sample rate gives.
::::
