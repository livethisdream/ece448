---
frame_view: true
---

# L7 - AM and FM Receivers

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">AM and FM Receivers</h1>

<div class="title-rule"></div>

A broadcast FM receiver with RDS, an aircraft band AM receiver, and AM and FM in the same noise.

Lesson 7 · Module 3: Analog Modulation · Dr. Neil Rogers
::::

::::{frame} Slides
:class: read-only

:::{admonition} Slides
:class: slides
<a href="../../slides/L07-am-fm-receivers.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L07-am-fm-receivers.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L07-am-fm-receivers.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '3'; counter-reset: lo 2">
  <li>I can implement an FM receiver in GNU Radio, demodulate a live broadcast FM signal, and decode its RDS data.</li>
  <li>I can explain and demonstrate the trade-off between bandwidth and noise performance for AM vs. FM.</li>
</ol>
::::

::::{frame} Two Stations in a Capture
:::{present}
<img src="../../viz/img/L07-fm-band.png"
     alt="A frequency sink labeled Simulated: L7 test file, showing 2.4 MHz of the FM band centered on 100.0 MHz, with a wide station at 100.3 MHz and a weaker, flat-topped station at 99.5 MHz above a noise floor near minus 70 dB"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The capture holds two FM stations in 2.4 MHz of IQ samples.
- Today we get audio from one of them, and its station name.
:::

In the L5 Lab you recorded 2 s of the FM band to `fm_capture.cfile`. The figure is a file of the same kind: 2.4 million complex samples per second around 100.0 MHz, holding a station at 100.3 MHz and a weaker one at 99.5 MHz. It came from a GNU Radio flowgraph rather than an antenna, so the figure carries a "Simulated" label, but a receiver cannot tell the difference. The station at 100.3 MHz carries a two-tone message, the L6 message of 1 kHz and 2.5 kHz, and its name, "ECE 448", in RDS data.

By the end of the lesson we will turn that file into audio, read the station's name out of it, and then point the same flowgraph at the live band. We will also build an AM receiver for the aircraft band and compare AM and FM in the same noise.

:::{depth}
<img src="../../viz/img/L07-grc-fm-test-tx.png"
     alt="GNU Radio Companion with L07-fm-test-tx.grc open: two tones, pre-emphasis, and a level for station A's audio; an RDS Encoder, Differential Encoder, Map, Unpack K Bits, Chunks to Symbols, root raised cosine filter, resampler, and a 57 kHz Signal Source for RDS; an Add forming the multiplex, a resampler, a Frequency Mod, and a 300 kHz shift; a second station with a 600 Hz tone shifted to minus 500 kHz; a Noise Source; and an Add, Head, and File Sink"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">

The test file comes from `L07-fm-test-tx.grc`. It builds each station the way a broadcaster does, with pre-emphasis, an RDS encoder from gr-rds, and a 75 kHz peak deviation, then adds noise and writes 4 s of samples, 76.8 MB, to `L07-fm-test.cfile`. Nothing in it transmits: its last block is a File Sink. `L07-am-test-tx.grc` does the same for the AM receiver, with one station at 126.2 MHz. Run both once before class, in the folder that holds the receivers.
:::
::::

::::{frame} Wideband FM
:::{present}
- The carrier's **frequency** follows the message, up to $\Delta f$ = 75 kHz away.
- **Carson's rule** gives the bandwidth: $B \approx 2(\Delta f + W)$.
- 15 kHz audio needs 180 kHz; US stations sit 200 kHz apart.
:::

**Frequency modulation** (FM) leaves the carrier's amplitude alone and moves its frequency instead: the instantaneous frequency is $f_c + \Delta f\,x(t)$, where the message $x(t)$ stays between $-1$ and 1 and the **peak deviation** $\Delta f$ is the farthest the carrier ever moves. Broadcast FM sets $\Delta f$ = 75 kHz and carries audio up to $W$ = 15 kHz, which makes it **wideband FM** (WBFM). Two-way radios use narrowband FM, with $\Delta f$ near 2.5 or 5 kHz.

An FM signal is wider than $2\Delta f$, because the frequency swings at audio rates. **Carson's rule** gives the bandwidth that holds nearly all of the power:

$$B \approx 2(\Delta f + W)$$

For broadcast audio that is $2(75 + 15)$ = 180 kHz, which fits the 200 kHz spacing of US FM channels, 88.1 to 107.9 MHz. An AM signal carrying the same audio would be 30 kHz wide. The FM Explorer later in the lesson draws the spectrum line by line.
::::

::::{frame} The Receiver Flowgraph
:::{present}
<img src="../../viz/img/L07-grc-wbfm-rx.png"
     alt="GNU Radio Companion with L07-wbfm-rx.grc open: a File Source and a disabled Soapy RTLSDR Source feed a Frequency Xlating FIR Filter with decimation 10, then a Quadrature Demod, a Decimating FIR Filter with decimation 5, an FM Deemphasis block, a volume Multiply Const, and an Audio Sink; frequency sinks show the received band, the demodulated multiplex, and the audio"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The source is a File Source or the RTL-SDR.
- A channel filter, a demodulator, an audio filter, and de-emphasis feed the speaker.
:::

`L07-wbfm-rx.grc` is the whole receiver in six processing blocks. The File Source plays a recording, and the Soapy RTLSDR Source receives live; GRC grays it out because we disabled it. Both feed the same channel filter, so switching from a file to the air means disabling one source and enabling the other. Neither path needs a Throttle: the Audio Sink takes exactly 48,000 samples per second, as in Lesson 6, and that paces the File Source too.

The two variables at the top tie the receiver to the radio. `fc_mhz` is the frequency we tune the SDR to, or the center frequency we recorded the file at, and `station_mhz` is the station we want. The next four frames take the chain apart one block at a time.
::::

::::{frame} Channel Filter and Decimation
:::{present}
- The **Frequency Xlating FIR Filter** shifts the station to 0 Hz, filters, and decimates.
- It shifts by $f_\text{station} - f_c$ = 300 kHz and passes ±90 kHz.
- Decimating by 10 leaves 240 kS/s.
:::

The station sits 300 kHz above the center of the capture, and everything else in the 2.4 MHz is something we do not want. The **Frequency Xlating FIR Filter** does three jobs in one block. It multiplies by a complex tone at $-300$ kHz, which moves the station to 0 Hz, the same frequency shift as Lesson 6's coherent receiver. It applies a low-pass filter, here a 105 kHz cutoff with a 30 kHz transition, which passes ±90 kHz and stops everything beyond ±120 kHz, including the station at 99.5 MHz. Then it keeps every tenth sample.

Decimating by 10 leaves 240,000 samples per second. That rate holds the ±120 kHz the filter passes without aliasing, and it holds the whole demodulated signal of the next frames, which reaches 59.4 kHz. Its center frequency is the expression `(station_mhz - fc_mhz) * 1e6`, so dragging the Station slider to 99.5 tunes the other station.
::::

::::{frame} The Quadrature Demodulator
:::{present}
$$\begin{aligned}
\text{gain} &= \frac{f_s}{2\pi\,\Delta f} \\
&= \frac{240\ \text{kHz}}{2\pi \cdot 75\ \text{kHz}} = 0.509
\end{aligned}$$
:::
:::{present}
- The phase step between samples is the frequency.
- With this gain, 75 kHz of deviation gives an output of 1.
:::

After the channel filter the station is a complex signal whose phase turns faster or slower as the frequency moves. The **Quadrature Demod** block measures how far the phase turns from one sample to the next, which is the frequency at that instant: a phase step of $2\pi$ per sample would be $f_s$, so a step of $\Delta\phi$ is $f_s\,\Delta\phi / 2\pi$ hertz.

The gain scales that frequency into a convenient number. With the gain above, a carrier 75 kHz above center produces an output of exactly 1, so the output is the transmitted message at its original scale. The block ignores amplitude entirely, which is why an FM receiver needs no AGC, and why a weakening FM station sounds normal until it nears the threshold that ends this lesson.
::::

::::{frame} The Multiplex
:::{present}
<img src="../../viz/img/L07-fm-multiplex.svg"
     alt="The FM broadcast baseband from 0 to 60 kHz: L plus R mono audio from 0 to 15 kHz, a pilot line at 19 kHz, the L minus R stereo signal as two sidebands from 23 to 53 kHz around a missing carrier at 38 kHz, and RDS at 57 kHz"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The demodulator's output is the **multiplex**: more than audio.
- The pilot is at 19 kHz, stereo is DSB-SC at 38 kHz, and RDS is at 57 kHz.
:::

The demodulator does not output audio; it outputs whatever the station put on its carrier, which is several signals side by side. The mono audio, the sum of the left and right channels, fills 0 to 15 kHz, so a mono receiver works by keeping only that band. A stereo station adds the difference of the two channels as DSB-SC on 38 kHz, the signal of Lesson 6 that needs carrier recovery, and sends a 19 kHz **pilot** so receivers can rebuild the 38 kHz carrier by doubling it. Above that, at 57 kHz, three times the pilot, sits **RDS**.

:::{depth}
<img src="../../viz/img/L07-mpx.png"
     alt="A frequency sink labeled Simulated: L7 test file, showing the demodulated multiplex from 0 to 120 kHz: lines at 1 and 2.5 kHz, a noise floor that rises from minus 100 dB at 5 kHz to minus 80 dB at 60 kHz, and the RDS signal as two humps at 56 and 58 kHz"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">

The frequency sink above is the multiplex of the test station. It has the two message tones and RDS, and no pilot or stereo, because the test station is mono. Notice that the noise floor rises with frequency: FM noise at the demodulator's output grows with distance from the carrier, so the top of the audio band, the stereo signal, and RDS all receive more noise than the bottom of the audio. A live stereo station shows the pilot line and the stereo band on the same display.
:::
::::

::::{frame} Audio and De-emphasis
:::{present}
- A 15 kHz low-pass filter decimates by 5, from 240 to 48 kS/s.
- **De-emphasis** (75 μs) cuts the treble the transmitter boosted.
- It removes the high-frequency noise along with the boost.
:::

A **Decimating FIR Filter** keeps the mono band, 0 to 15 kHz with a 3 kHz transition, and decimates by 5 to the sound card's 48 kHz. Every other part of the multiplex is above 15 kHz, so this one filter removes the pilot, the stereo signal, and RDS.

The transmitter boosts the treble of its audio before modulating, a step called **pre-emphasis**, by up to 17 dB at 15 kHz in the US. The **FM Deemphasis** block applies the opposite filter, set by a 75 μs time constant with its corner at 2.1 kHz, which restores the original audio balance. Because the noise rises with frequency, cutting the treble at the receiver removes the most noise exactly where there is the most of it. Europe uses 50 μs, so a European station sounds slightly bright on a US setting, but it plays.
::::

::::{frame} Running the Receiver
:::{present}
<img src="../../viz/img/L07-wbfm-rx.png"
     alt="The L7 WBFM receiver window labeled Simulated: L7 test file. Controls for SDR center 100.0, Station 100.300, and Volume 0.3; the received band with stations at 99.5 and 100.3 MHz; the demodulated multiplex from 0 to 120 kHz with two tones near 0 and RDS near 57 kHz; and the audio spectrum after de-emphasis with lines at 1 and 2.5 kHz"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The audio shows the two tones at 1 and 2.5 kHz.
- Dragging Station to 99.5 plays a 600 Hz tone.
:::

The figure is the receiver running on the test file. The bottom right sink is the audio after de-emphasis, with the 1 kHz and 2.5 kHz tones of the message and nothing else above the floor, which is the check that the receiver works: the demodulated audio matches what the test transmitter sent. Drag the Station slider to 99.5 and the audio changes to the second station's single 600 Hz tone.

To use your own L5 capture, set the File Source's file to `fm_capture.cfile`, type the center frequency you recorded at into SDR center, and set Station to the station you centered. To receive live, disable the File Source, enable the RTL-SDR Source, and run it again. A real station's audio sink will show music or speech rather than two lines.
::::

::::{frame} RDS
:::{present}
- The **Radio Data System** sends 1187.5 bits per second on 57 kHz.
- It is BPSK with differential coding and biphase symbols.
- Groups of 104 bits carry the station name, program type, and text.
:::

The **Radio Data System** (RDS, called RBDS in North America) adds a slow digital channel to an FM station. It runs at 1187.5 bits per second, which is 57 kHz divided by 48, on a 57 kHz subcarrier. The station sends each bit as two half-bit symbols of opposite sign, a **biphase** code, and the result is BPSK on the subcarrier: a DSB-SC signal like Lesson 6's, which needs its carrier recovered. The bits are also differentially coded, so the receiver needs only the changes between bits, and a 180° error in the recovered carrier does no harm.

The data arrives in **groups** of 104 bits, four 26-bit blocks that each carry 16 data bits and a 10-bit check word, so one group takes 87.6 ms. The **PI** code is the station's 16-bit identifier, the **PS** name is the eight characters a car radio displays, sent two per group, and the **radiotext** is up to 64 characters of free text.
::::

::::{frame} Decoding RDS
:::{present}
<img src="../../viz/img/L07-rds-decoded.png"
     alt="The RDS part of the L7 receiver labeled Simulated: L7 test file: a constellation sink with two tight clusters at minus 1 and plus 1, and the gr-rds panel showing Frequency 100.3, Station Name ECE 448, Program Type 1093, PI Information, the clock time, and Radiotext USAFA ECE 448 test signal, simulated"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Two clusters show BPSK with its carrier recovered.
- The panel shows the station name, "ECE 448", and the radiotext.
:::

:::{depth}
<img src="../../viz/img/L07-grc-rds.png"
     alt="The RDS branch of L07-rds-rx.grc: a Frequency Xlating FIR Filter at 57 kHz with decimation 10, a Rational Resampler 19 over 24, a Decimating FIR Filter with the biphase taps, an AGC, a Symbol Sync, a Constellation Receiver, a Differential Decoder, and the gr-rds RDS Decoder, RDS Parser, and RDS Panel"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::

`L07-rds-rx.grc` is the WBFM receiver with an RDS branch added to the demodulator's output, following the receiver that ships with gr-rds. A second Frequency Xlating FIR Filter moves 57 kHz to 0 Hz and decimates to 24 kHz, and a Rational Resampler converts to 19 kHz, which is exactly 16 samples per bit. A matched filter for the biphase symbols, an AGC, and a **Symbol Sync** find the bit timing, and the **Constellation Receiver** recovers the subcarrier's phase, which is the carrier recovery Lesson 6 said DSB-SC needs. The two tight clusters on the constellation show it working. A Differential Decoder undoes the differential coding, and the three gr-rds blocks find the 104-bit groups, check them, and display what they carry.

The panel shows "ECE 448" and the test transmitter's radiotext. It also shows the station's PI code, 1093 in hexadecimal, under "Program Type" and the program type under "PI": the panel swaps those two labels, so read them the other way around on a live station too. The RDS blocks come from **gr-rds**, which radioconda installs as `gnuradio-rds`.
::::

::::{frame} An AM Receiver
:::{present}
<img src="../../viz/img/L07-am-rx.png"
     alt="The L7 AM receiver window labeled Simulated: L7 test file: the received band around 126.0 MHz with one narrow station at 126.2 MHz; the channel after the filter with a carrier at 0 and sideband lines at plus and minus 1 and 2.5 kHz; and the audio after the AGC, the two-tone message repeating every 2 ms"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Aircraft voice and ATIS use AM from 118 to 137 MHz.
- The filter cuts off at 5 kHz and decimates 2.4 MS/s by 50 to 48 kS/s.
- **Complex to Mag** is the envelope detector.
:::

Aircraft and control towers talk in AM between 118 and 137 MHz, and most airports with a control tower broadcast an **ATIS**, a recorded loop of the current weather and runway in use, continuously on one of those frequencies. That makes ATIS a steady signal to receive, as Lesson 6 suggested. `L07-am-rx.grc` has the same front end as the FM receiver: a File Source or the RTL-SDR, and a Frequency Xlating FIR Filter. This one has a 5 kHz cutoff, which keeps the voice band with room for a small tuning error, and it decimates by 50, from 2.4 MS/s straight to the sound card's 48 kS/s.

:::{depth}
<img src="../../viz/img/L07-grc-am-rx.png"
     alt="GNU Radio Companion with L07-am-rx.grc open: a File Source and a disabled Soapy RTLSDR Source feed a Frequency Xlating FIR Filter with decimation 50, then Complex to Mag, a Decimating FIR Filter with the 3 kHz low-pass taps, a DC Blocker, an AGC, a volume Multiply Const, and an Audio Sink"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::

After the filter, the AM station is a complex signal with its carrier at 0 Hz, and its envelope is the magnitude of each sample. **Complex to Mag** replaces the Abs block of Lesson 6, and the rest is the L6 receiver: the same 3 kHz low-pass taps and a DC Blocker that removes the carrier's constant. An **AGC** block then holds the audio level steady, because a station's strength depends on the aircraft's distance and an AM receiver's output depends on it directly. The figure shows the receiver on `L07-am-test.cfile`, which carries the L6 two-tone message at $m$ = 0.5; the audio repeats every 2 ms, as it did in Lesson 6.
::::

::::{frame} AM and FM in the Same Noise
:::{present}
<img src="../../viz/img/L07-amfm-30.png"
     alt="L07-am-vs-fm.grc at C/N 30 dB and 25 kHz deviation: output SNR meters read 29.5 dB for AM and 48.7 dB for FM; the outputs' spectrum shows the 1 kHz tone with the AM noise floor near minus 64 dB and the FM floor near minus 85 dB rising toward 5 kHz; the time sink shows both outputs as clean 1 kHz sine waves"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Both carry the same tone at the same power in the same noise.
- AM in 10 kHz reaches 29.5 dB, and FM in 60 kHz reaches 48.7 dB.
:::

`L07-am-vs-fm.grc` sends one 1 kHz tone two ways with the same carrier power: as AM at $m$ = 1, the best case from Lesson 6, and as FM with 25 kHz deviation. Both go through the same noise, and each receiver filters to its own channel, 10 kHz for AM and $2(25 + 5)$ = 60 kHz for FM by Carson's rule with a 5 kHz audio band. Each output then passes the same 5 kHz audio filter, and a meter built from blocks measures the tone's power against everything else in the audio band: the **output SNR**. The C/N slider sets the carrier-to-noise ratio in 10 kHz, the AM channel.

:::{depth}
<img src="../../viz/img/L07-grc-am-vs-fm.png"
     alt="GNU Radio Companion with L07-am-vs-fm.grc open: a 1 kHz Signal Source feeds an AM branch (Add Const 1, a power scale, Float To Complex) and a Frequency Mod; one Noise Source adds to both; the AM receiver is a Decimating FIR Filter, Complex to Mag, DC Blocker, scale, and audio filter; the FM receiver is a channel filter, Quadrature Demod, and audio filter; below, band-pass and band-reject filters, RMS, Log10, and Subtract blocks form the two SNR meters feeding a Number Sink"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::

At 30 dB, AM delivers 29.5 dB, close to its C/N, and FM delivers 48.7 dB, about 19 dB better. The FM receiver lets in six times as much noise, yet its output is cleaner. The demodulator's output follows how far the frequency swings, and a 25 kHz swing is large next to the small frequency jitter that the noise adds to a strong carrier. The spectrum shows the result: FM's noise floor sits about 20 dB under AM's. Each doubling of the deviation improves FM's output by another 5 to 6 dB, as long as the signal stays above threshold.
::::

::::{frame} The FM Threshold
:::{present}
<img src="../../viz/img/L07-amfm-15.png"
     alt="L07-am-vs-fm.grc at C/N 15 dB: output SNR meters read 14.4 dB for AM and 25.3 dB for FM; FM's noise floor is now flat near minus 63 dB and only about 12 dB under AM's"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
| C/N in 10 kHz | 30 | 20 | 15 | 10 |
| :-- | :-: | :-: | :-: | :-: |
| AM | 29.5 | 19.4 | 14.4 | 9.2 |
| FM, 5 kHz | 35.5 | 25.5 | 20.5 | 14.2 |
| FM, 25 kHz | 48.5 | 39.2 | 26.1 | 9.3 |
| FM, 50 kHz | 53.2 | 39.5 | 17.3 | 6.4 |
:::

FM's advantage holds only while the carrier stays well above the noise in the FM receiver's own bandwidth. Below about 10 dB there, noise occasionally swings the phase through a full turn, and the demodulator turns each slip into a click. That is the **FM threshold**: below it, FM's output falls quickly. The table is the output SNR in dB, measured with the flowgraph at three deviations, each the average of about 12 s of meter readings, because near threshold the meters wander by about 1 dB as clicks come and go. At 15 dB, the 25 kHz signal is 7 dB above the noise in its 60 kHz band and has lost about 7 dB of its advantage. At 10 dB it is no better than AM.

Wider deviation raises the output SNR above threshold, 53.2 dB against 48.5 at 30 dB C/N, but it also widens the receiver's filter, which lets in more noise and raises the threshold. At 10 dB, the 50 kHz signal is worse than AM, and the 5 kHz signal, which gains only 6 dB at 30 dB C/N, is the best of the four. That is the relationship the objective asks about: FM uses bandwidth to get a cleaner output, and the improvement lasts only while the signal is strong. Broadcast FM uses it because a broadcast station is strong and has a 200 kHz channel to fill. Aircraft use AM because a weak AM signal stays intelligible, and because two aircraft transmitting at once are both heard, where an FM receiver would lock onto the stronger one.
::::

::::{frame} FM Explorer
:class: viz-frame

:::{depth}
The left panel shows the spectral lines of a carrier frequency modulated by one tone, with Carson's band shaded; the right panel shows how much of the power falls inside a band of each width. Start with the L7 flowgraph preset and notice that the lines stop just outside Carson's band. Set the deviation to 2.4 kHz with a 1 kHz tone and watch the carrier line vanish, which is how technicians calibrate a transmitter's deviation. Whatever the settings, Carson's band holds at least 96% of the power.
:::

:::{present}
<iframe src="../../viz/fm-explorer.html"
        width="100%" height="407"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="FM explorer: the line spectrum of a tone-modulated FM signal against deviation and tone frequency, with Carson's bandwidth and the share of power inside it">
</iframe>
:::
::::

::::{frame} Key Point
:::{present}
:class: callout
FM spreads the message over a wider channel, and above threshold its receiver returns a cleaner output than AM. Below threshold the improvement disappears, and a wider channel reaches threshold sooner.
:::
::::

::::{frame} On the SDR
:::{present}
- Tune the SDR a few hundred kHz off the station, away from the DC spike.
- Set RF gain from your L5 gain table.
- Receiving is unrestricted, and the RTL-SDR receives only.
:::

On the air, the receivers need three settings from Lesson 5. Tune the SDR a few hundred kilohertz away from the station, so the RTL-SDR's DC spike at the center stays out of the channel filter, and give the Station slider the station's real frequency. Set the RF gain slider to the highest gain in your L5 Lab gain table at which no new signals appeared between stations. For ATIS, look up the airport's frequency in the FAA Chart Supplement or on a sectional chart, and expect a weaker signal than broadcast FM, because aircraft band stations are lower in power and need line of sight.

RDS needs a stronger signal than the audio does, because its 57 kHz subcarrier sits where the multiplex noise is highest. If the station name never appears, raise the gain or choose a stronger station before changing the flowgraph. As Lesson 2 said, receiving is unrestricted and transmitting is not; the RTL-SDR receives only, and nothing in this lesson transmits.
::::

::::{frame} Downloads
:class: read-only doc-links

- <a class="doc-link" href="../../grc/L07-fm-test-tx.grc" download>L07-fm-test-tx.grc</a>: writes `L07-fm-test.cfile`, 4 s (76.8 MB) of a simulated FM band around 100.0 MHz with two stations, one carrying RDS. Needs gr-rds. Run it once; it stops on its own.
- <a class="doc-link" href="../../grc/L07-am-test-tx.grc" download>L07-am-test-tx.grc</a>: writes `L07-am-test.cfile`, 4 s (76.8 MB) of a simulated AM station at 126.2 MHz carrying the L6 two-tone message.
- <a class="doc-link" href="../../grc/L07-wbfm-rx.grc" download>L07-wbfm-rx.grc</a>: the broadcast FM receiver, playing the test file, your L5 capture, or the RTL-SDR.
- <a class="doc-link" href="../../grc/L07-rds-rx.grc" download>L07-rds-rx.grc</a>: the same receiver with the RDS decoder. Needs gr-rds.
- <a class="doc-link" href="../../grc/L07-am-rx.grc" download>L07-am-rx.grc</a>: the AM receiver for the aircraft band.
- <a class="doc-link" href="../../grc/L07-am-vs-fm.grc" download>L07-am-vs-fm.grc</a>: one tone as AM and as FM in the same noise, with output SNR meters. No hardware needed.

Put every file in one folder; GRC runs a flowgraph from its own folder, so the receivers find the test files there. Each receiver plays through your laptop's speakers; start with the volume low. If GRC reports the RDS blocks as missing, install gr-rds from the radioconda prompt with `conda install gnuradio-rds`.
::::

::::{frame} Summary
:class: read-only

| Receiver | Front end | Demodulator | After it | Number to remember |
| :-- | :-- | :-- | :-- | :-- |
| WBFM | Xlating FIR, ±90 kHz, ÷10 | Quadrature Demod, gain $f_s/2\pi\Delta f$ | 15 kHz low-pass ÷5, de-emphasis 75 μs | $B \approx 2(\Delta f + W)$ = 180 kHz |
| RDS | Xlating FIR at 57 kHz, resample to 19 kHz | Symbol Sync, Constellation Receiver | Differential Decoder, gr-rds | 1187.5 bit/s, 104-bit groups |
| AM | Xlating FIR, ±5 kHz, ÷50 | Complex to Mag | 3 kHz low-pass, DC Blocker, AGC | 118 to 137 MHz |
| AM vs. FM | same power, same noise | | output SNR meters | FM +19 dB at 25 kHz, until threshold |
::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE448_L07_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE448_L07_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Looking Ahead
:::{present}
- The L7 Lab plays your L5 capture, then receives live FM, RDS, and ATIS.
- Lesson 8 sends bits by switching frequency: FSK.
:::

Today we built a broadcast FM receiver, added an RDS decoder to it, built an AM receiver for the aircraft band, and measured what FM's extra bandwidth does in noise. The L7 Lab is the bench version: play your own L5 capture through the receiver, receive a live station and its RDS name, receive an ATIS broadcast, and fill in the AM and FM output SNR table yourself.

Lesson 8 moves from analog to digital modulation. Its first signal, frequency-shift keying, is FM with a message that takes only two values, so its receiver uses the same quadrature demodulator as today's.
::::
