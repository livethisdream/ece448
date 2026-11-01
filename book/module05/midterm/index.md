---
frame_view: true
---

# Midterm — Fox Hunt and CTF

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">Midterm — Fox Hunt and CTF</h1>

<div class="title-rule"></div>

Find a hidden transmitter at 915 MHz with your own PlutoSDR, then find, demodulate, and decode eight recorded signals to their flags.

Module 5: Custom Blocks & Midterm · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '5'; counter-reset: lo 2">
  <li>I can find a hidden transmitter in a fox hunt using a PlutoSDR, an antenna, and GNU Radio.</li>
  <li>I can solve capture-the-flag challenges that require finding, capturing, demodulating, and decoding unknown signals with GNU Radio.</li>
</ol>
::::

::::{frame} Two Parts, One Submission
:::{present}
- **Fox hunt:** find a hidden transmitter with your Pluto and the receiver below.
- **CTF:** decode eight recordings of unknown signals to their flags.
- Individual and take home. Turn in one PDF.
:::

The midterm uses what you have built since Lesson 4. The fox hunt is a receive problem on the air: a hidden transmitter, a readout of its strength, and your feet. The capture-the-flag is the receive problem in a recording: eight unknown signals, each built from a modulation in this course. Both parts are **individual** and **take home**. Work alone, keep your flowgraphs, and turn in one PDF on Gradescope by the date your instructor announces, with the evidence each part asks for below.
::::

::::{frame} The Fox
:::{present}
- Hidden somewhere in the search area, sending short bursts at 915 MHz, low power.
- A PlutoSDR or a LoRa radio. Your receiver must work for either.
- You hunt with your own Pluto and antenna.
:::

The fox is a small transmitter your instructor hides inside a search area, sending short bursts at 915 MHz at low power. It might be a PlutoSDR or it might be a LoRa radio, and the receiver below finds either one, because it measures power in a channel and does not need to decode anything. You hunt with your own PlutoSDR and your own antennas, or the ones that come with the Pluto. Your instructor announces the search area and the hours the fox is on the air. Nothing you build for the hunt transmits.
::::

::::{frame} The Fox-Hunt Receiver
:::{present}
- PlutoSDR Source at 1 MS/s, 250 kHz below 915 MHz.
- Spectrum and waterfall for finding the burst.
- Channel power in dBFS, average and peak; ADC level to catch clipping.
:::

<img src="../../viz/img/MT-grc-foxhunt.png"
     alt="The MT-foxhunt flowgraph in GNU Radio Companion: a PlutoSDR Source at 1 MS/s with its LO at 914.75 MHz feeds a frequency sink, a waterfall sink, a Frequency Xlating FIR Filter centered 250 kHz up with a low-pass as wide as the Channel width slider, and a Complex To Float; the channel goes through Complex to Mag^2 into a 100 ms Moving Average and a 2 ms Moving Average with a Max over the last quarter second, each through Log10 to a Number Sink; the I and Q samples go through Abs and Max to a second Number Sink labeled ADC level"
     style="width:100%;max-width:1000px;display:block;margin:0 auto 1rem;">

`MT-foxhunt.grc` is the receiver. The Pluto's LO sits 250 kHz below 915 MHz, so its DC spike from Lesson 5 stays off the fox. A **Frequency Xlating FIR Filter** moves 915 MHz to the center and keeps a channel as wide as the **Channel width** slider. **Complex to Mag^2** turns each sample into power, and the readout shows it in dBFS two ways: the 100 ms average, and the strongest 2 ms in the last quarter second, which catches a short burst the average would smear out. The **ADC level** readout shows the largest I or Q sample; 1.0 is full scale.
::::

::::{frame} What a LoRa Burst Looks Like
:::{present}
- A chirp: a tone that sweeps from one edge of its band to the other.
- Long chirps draw diagonal stripes; short ones fill a block with sharp edges.
- A narrowband signal stays on one line.
:::

<img src="../../viz/img/MT-chirp.png"
     alt="Simulated spectrogram, time across and offset from 915 MHz up: a burst of ten chirps, each a diagonal stripe that climbs from the bottom edge of its band to the top edge and starts again, centered on 915 MHz; below it a narrowband carrier that switches on and off is a horizontal line at minus 300 kHz"
     style="width:100%;max-width:760px;display:block;margin:0 auto 1rem;">

If the fox is a LoRa radio, each burst is a train of **chirps**: a tone that sweeps across the radio's band from one edge to the other, again and again. The figure is simulated and turned on its side, with time across; GNU Radio's waterfall runs time down the screen. Long chirps draw diagonal stripes. Short ones blur into a block with sharp edges at both sides of the band, which a narrowband signal never makes. If the fox is a Pluto, expect whatever burst your instructor sends. You do not need to decode either one. Set **Channel width** to cover the burst you see.
::::

::::{frame} Hunting With One Antenna
:::{present}
- Find the burst on the waterfall, then watch the Peak readout.
- Turn slowly: your body blocks the signal when the fox is behind you.
- Walk toward the strongest reading and take a new bearing.
:::

The Pluto's antennas hear all directions about equally, so your body is the direction finder. Hold the Pluto close against your chest and turn slowly through a full circle, stopping for each burst. The reading drops by several dB when your body sits between the antenna and the fox, so the fox is **behind you at the lowest reading**. That null is sharper than the peak, so use it for the bearing. Walk that way, then stop and take a new bearing. The readings jump with every step, so compare several bursts before you trust a change.
::::

::::{frame} Up Close: Lower the Gain
:::{present}
- Near the fox the ADC clips, as in Lessons 4 and 5.
- When ADC level reaches 1.0, the readout stops rising: lower RX gain.
- Compare readings only at the same gain.
:::

<img src="../../viz/img/MT-foxhunt-sim.png"
     alt="The fox-hunt receiver running on a simulated chirp burst, its plots titled SIMULATED: the RX gain slider at 40 dB and Channel width at 200000 Hz, a spectrum around 915 MHz with a small bump near 915.000 MHz, a waterfall with faint diagonal chirp marks near 915 MHz, the Channel power readout at about minus 24 dBFS average and peak, and the ADC level readout at 0.067"
     style="width:100%;max-width:820px;display:block;margin:0 auto 1rem;">

Lesson 4 showed what happens when a signal is bigger than the ADC's range: the samples clip, the spectrum grows false signals, and a stronger signal no longer reads stronger. Close to the fox that is your hunt. When the **ADC level** readout reaches 1.0, the power readout stops rising, so every step looks the same. Lower **RX gain** by 10 dB and keep going. A reading means something only together with its gain, so log both. Within a few meters, even 0 dB can clip; take the antenna off and the Pluto still hears the fox.
::::

::::{frame} Fox Hunt: Steps
:class: read-only

1. Put `MT-foxhunt.grc` in a folder, open it in GRC, plug in your Pluto with an antenna on its RX port, and run it. If GRC cannot find the Pluto, the Lesson 5 page has the install checks and the macOS URI note.
2. With the fox on the air, start at RX gain 40 dB and watch the waterfall near 915 MHz. When a burst appears, set **Channel width** to cover it, between about 125 and 250 kHz, and watch the **Peak** readout jump with each burst.
3. Screenshot the whole window the first time you see the fox, for **far**.
4. Take a bearing by body shielding: hold the Pluto against your chest, turn through a full circle in steps of about 45°, and record the Peak reading at each step over two or three bursts. The fox is opposite your lowest reading. Write down where you stood, the compass bearing to the fox, the peak reading, and the RX gain.
5. Walk along that bearing, and take a new bearing whenever the reading has climbed by about 10 dB or the path turns. Each bearing goes in your log.
6. When **ADC level** reaches 1.0, lower RX gain by 10 dB and note it in the log. Near the fox, take the antenna off if 0 dB still clips.
7. When you find the fox, do not touch or move it. Screenshot the window beside it for **near**, and photograph where it sits.
::::

::::{frame} Fox Hunt: What to Turn In
:class: read-only

- **Where the fox was**: the building and room or spot, a photo of where it sits, and the time you found it.
- **Two screenshots** of the receiver window: **far**, when you first saw the fox, and **near**, beside it. Each shows the waterfall, the readouts, and the RX gain.
- **A bearing log** of at least four bearings: the time, where you stood, the compass bearing to the fox, the Peak reading in dBFS, and the RX gain.
- **Two or three sentences** on what worked: where the body null helped, and where the gain or reflections fooled you.
::::

::::{frame} Capture the Flag
:::{present}
- Eight SigMF recordings of unknown signals.
- Each decodes to a flag of the form ECE448{...}.
- Some carry only the text inside the braces; you add the braces.
:::

The second part is eight recordings, each a SigMF pair like the L7 Lab's test files: the samples in `.sigmf-data`, and the datatype, sample rate, and center frequency in `.sigmf-meta`. Each recording holds one signal at a sample rate, offset, and noise level of its own. Some are modulations you have built (AM, FM, FSK, PAM). Others are signals Module 6 covers in depth, such as Morse, keypad tones, remotes, PSK, and hopping, and for those the lesson pages on this site are yours to read ahead. Decode it to its **flag**, a line of text of the form `ECE448{...}`. Morse, speech, and keypad tones cannot send a brace, so a signal like that carries only the text inside them; turn it in as `ECE448{TEXT}`.
::::

::::{frame} Find, Demodulate, Decode
:::{present}
- Read the meta file, then look: spectrum, waterfall, time.
- Name the modulation, then move it to the center at a rate you know.
- Build or reuse the receiver that fits, and read the flag.
:::

Work each recording from the outside in. Read the `.sigmf-meta` first: the datatype tells you how to open it, and the sample rate sets every display. Play it through a **SigMF Source (Minimal)** and **Throttle** into a frequency sink, a waterfall, and a time sink, and find the signal. Ask what changes: the amplitude, the frequency, or the phase, and how fast. Then move the signal to 0 Hz with a **Frequency Xlating FIR Filter**, decimate to a rate the receiver you need expects, and build or reuse that receiver from the lesson that fits.
::::

::::{frame} The Challenges
:class: read-only

All eight are simulated in software, not captured from an antenna; each meta file says so. The center frequency is part of the story, not a place to transmit.

| # | Recording | Datatype | Sample rate | Center | Points | Hint |
| :-: | :-- | :-- | --: | --: | --: | :-- |
| 1 | `MT-ctf-1` | cf32_le | 32 kS/s | 144.05 MHz | 100 | Listen to the rhythm. |
| 2 | `MT-ctf-2` | ci16_le | 50 kS/s | 146.52 MHz | 100 | Read the datatype before you open it. |
| 3 | `MT-ctf-3` | cf32_le | 48 kS/s | 915 MHz | 150 | Twelve keys, two tones each. |
| 4 | `MT-ctf-4` | cf32_le | 250 kS/s | 433.92 MHz | 200 | A long pulse and a short pulse. A character is eight bits, most significant first. |
| 5 | `MT-ctf-5` | cf32_le | 96 kS/s | 915 MHz | 200 | The packets are framed the way the L8 and L10 links frame them. |
| 6 | `MT-ctf-6` | cf32_le | 64 kS/s | 915 MHz | 200 | Find the symbol rate first. |
| 7 | `MT-ctf-7` | cf32_le | 200 kS/s | 915 MHz | 300 | Four points, and every symbol is sent as a change. |
| 8 | `MT-ctf-8` | cf32_le | 160 kS/s | 915 MHz | 300 | You do not need the whole pattern; each piece knows its place. |

The CTF is worth 1550 points in all. `ci16_le` is interleaved 16-bit I and Q: in the SigMF Source choose complex short, and follow it with **IShort To Complex**, scaled by 1/32768.
::::

::::{frame} CTF: What to Turn In
:class: read-only

For each challenge you solve:

- **The flag**, exactly as `ECE448{...}`.
- **A screenshot of your flowgraph** in GRC, with the display or text output that shows the flag.
- **How you identified the signal**, in a few sentences: what the waterfall, spectrum, or time sink showed, which modulation that pointed to, and the settings you chose (offset, decimation, symbol rate, and the like).

A flag without its writeup does not count. Partial work on an unsolved challenge, such as a correct identification and a demodulated signal that you could not decode, is worth reporting; it can earn partial credit.
::::

::::{frame} Rules and Grading
:class: read-only

**Rules.** Work alone. You may use this course site, your own flowgraphs and notes, the GNU Radio wiki, and PySDR. You may not discuss the fox's location or any challenge with anyone but your instructor until the midterm closes. Generative AI is not allowed (syllabus, Authorized resources). The hunt is receive only: never transmit at any time during the midterm.

| Part | What earns credit | Weight |
| :-- | :-- | --: |
| Fox hunt | Found the fox: its location, with a photo | 20% |
| | Evidence: the far and near screenshots and the bearing log | 20% |
| CTF | Points for each flag, out of 1550, counted only with its writeup | 50% |
| | Quality of the writeups: identification and flowgraph | 10% |
::::

::::{frame} Downloads
:class: read-only doc-links

- <a class="doc-link" href="../../grc/MT-foxhunt.grc" download>MT-foxhunt.grc</a>: the fox-hunt receiver. It needs a PlutoSDR in extended-frequency mode, so it was compiled under GNU Radio 3.10 but not run here on a radio.
- The eight CTF recordings, each a `.sigmf-data` and `.sigmf-meta` pair, about 15 MB in all. GRC 3.10 marks the SigMF Source (Minimal) block as deprecated and warns when the flowgraph loads; the warning is harmless.
  - <a class="doc-link" href="../../grc/MT-ctf-1.sigmf-data" download>MT-ctf-1.sigmf-data</a> and <a class="doc-link" href="../../grc/MT-ctf-1.sigmf-meta" download>.sigmf-meta</a>, 3.1 MB
  - <a class="doc-link" href="../../grc/MT-ctf-2.sigmf-data" download>MT-ctf-2.sigmf-data</a> and <a class="doc-link" href="../../grc/MT-ctf-2.sigmf-meta" download>.sigmf-meta</a>, 3.7 MB
  - <a class="doc-link" href="../../grc/MT-ctf-3.sigmf-data" download>MT-ctf-3.sigmf-data</a> and <a class="doc-link" href="../../grc/MT-ctf-3.sigmf-meta" download>.sigmf-meta</a>, 2.5 MB
  - <a class="doc-link" href="../../grc/MT-ctf-4.sigmf-data" download>MT-ctf-4.sigmf-data</a> and <a class="doc-link" href="../../grc/MT-ctf-4.sigmf-meta" download>.sigmf-meta</a>, 1.6 MB
  - <a class="doc-link" href="../../grc/MT-ctf-5.sigmf-data" download>MT-ctf-5.sigmf-data</a> and <a class="doc-link" href="../../grc/MT-ctf-5.sigmf-meta" download>.sigmf-meta</a>, 1.1 MB
  - <a class="doc-link" href="../../grc/MT-ctf-6.sigmf-data" download>MT-ctf-6.sigmf-data</a> and <a class="doc-link" href="../../grc/MT-ctf-6.sigmf-meta" download>.sigmf-meta</a>, 0.5 MB
  - <a class="doc-link" href="../../grc/MT-ctf-7.sigmf-data" download>MT-ctf-7.sigmf-data</a> and <a class="doc-link" href="../../grc/MT-ctf-7.sigmf-meta" download>.sigmf-meta</a>, 0.4 MB
  - <a class="doc-link" href="../../grc/MT-ctf-8.sigmf-data" download>MT-ctf-8.sigmf-data</a> and <a class="doc-link" href="../../grc/MT-ctf-8.sigmf-meta" download>.sigmf-meta</a>, 2.6 MB
- The L7 Lab page shows how to play a `.sigmf-data` file through a File Source; the SigMF Source (Minimal) does the same and reads the sample rate for you.
::::

::::{frame} Looking Ahead
:::{present}
- Module 6 builds the receivers for real signals: CW, DTMF, HD Radio, PSK, hopping, and more.
- Keep your midterm flowgraphs; they are a start on Module 6.
:::

Module 6 starts with Lesson 12, CW, and works through the signals you meet on the air, from keypad tones to aircraft. Several of them are CTF signals taken further, so keep every flowgraph you build for the midterm.
::::
