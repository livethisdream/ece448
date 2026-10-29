---
frame_view: true
---

# L18 - ADS-B

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">ADS-B</h1>

<div class="title-rule"></div>

We generate ADS-B messages as pulses, receive them at 1090 MHz, and decode each aircraft's identity, altitude, and position.

Lesson 18 · Module 6: Waveform Applications & RF Reverse Engineering · Dr. Neil Rogers
::::

::::{frame} Slides
:class: read-only

:::{admonition} Slides
:class: slides
<a href="../../slides/L18-adsb.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L18-adsb.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L18-adsb.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '6'; counter-reset: lo 6">
  <li>I can receive and decode ADS-B messages from aircraft transponders.</li>
</ol>
::::

::::{frame} Aircraft Overhead
:::{present}
<img src="../../viz/img/L18-adsb-rx.png"
     alt="L18-adsb-rx.grc running on the simulated recording, labeled SIMULATED: the Messages label reads 561 passed parity, 7 failed; a 20 ms time plot shows three short spikes of different heights above the noise; a triggered plot shows one message's preamble and first bits as narrow pulses; the Aircraft label lists four aircraft, ECE448, SKW3301, N731RG, and FALCON21, each with altitude, speed, track, and latitude and longitude near Colorado Springs"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Run `L18-adsb-tx.grc`, then `L18-adsb-rx.grc`.
- Each spike is one message; the table fills with aircraft.
:::

Every airliner over Colorado Springs announces its identity, altitude, position, and velocity several times a second on 1090 MHz, and an RTL-SDR on a windowsill can hear them. The figure is today's receiver, `L18-adsb-rx.grc`, playing a simulated recording of four aircraft near USAFA. Each spike in the left plot is one message, 120 µs long; the right plot zooms in on one of them; and the table at the bottom fills in as the decoder reads each message.

The topics and their order follow the 2025 slides: what ADS-B is, its pulses, a generator that builds them, the message, and the tools that decode it. We build the generator and the receiver in GNU Radio, then point the receiver at the sky.
::::

::::{frame} ADS-B and Mode S
:::{present}
- **Mode S** transponders reply to radar on 1090 MHz.
- **ADS-B** has them broadcast on their own, about twice a second.
- The common form is the **extended squitter**, Downlink Format 17.
:::

**Automatic Dependent Surveillance–Broadcast** (ADS-B) lets an aircraft tell everyone around it where it is. "Automatic" means no one has to ask, "dependent" means the position comes from the aircraft's own GPS, and "broadcast" means anyone can listen: air traffic control, other aircraft, and us.

It grew out of **Mode S** (Mode Select), the transponder system that answers a secondary radar's interrogation on 1030 MHz with a reply on 1090 MHz. Mode S defines many message formats, and ADS-B adds one more: an **extended squitter**, a 112-bit message the transponder sends without being asked. Its Downlink Format (DF) number is 17; DF 18 is the same message from a device that is not a transponder, such as a ground vehicle. In the US, small aircraft below 18,000 ft may instead use **UAT** on 978 MHz, a different waveform that this lesson does not cover. The 1090 MHz Riddle, by Junzi Sun, is the reference the slides use for every detail of the message.
::::

::::{frame} Find It on the Air
:::{present}
- Tune SDR Flex, or GQRX, to 1090 MHz at 2.4 MS/s.
- Look for short dots scattered across the waterfall, then attach dump1090.
:::

We start on the air with **SDR Flex**, the course's explore tool, or **GQRX** if SDR Flex is not set up. The live radio and the dump1090 decoder need SDR Flex's full version, run from its Docker image or as a server against your own GNU Radio; its browser version has neither. SDR Flex's README says its radio drivers have not yet been tried with a real radio, and we have not tested it live in this course, so GQRX is the tested path for the first look.

1. Set the input to the RTL-SDR, the sample rate to 2.4 MS/s, and the gain high, near 40 dB.
2. Tune to 1090 MHz.
3. Watch the waterfall. ADS-B is not a steady carrier: it is short dots of energy scattered in time across about 2 MHz around 1090 MHz, more of them when aircraft are close.
4. In SDR Flex, attach the **dump1090** decoder; its README lists dump1090 among the decoders that take IQ straight from the spectrum, with no demodulator in front. GQRX has no ADS-B decoder, so in GQRX the dots are as far as we go.

The SDR Flex steps follow its README and its server README, which lists the dump1090 decoder; the GQRX steps follow GQRX's own documentation at gqrx.dk.
::::

::::{frame} The Physical Layer
:::{present}
<img src="../../viz/img/L18-ppm.svg"
     alt="The Mode S preamble and five data bits as 0.5 microsecond chips: preamble pulses start at 0, 1.0, 3.5, and 4.5 microseconds within 8 microseconds; then the bits 1, 0, 0, 0, 1, each 1 microsecond long, where a 1 is a pulse then quiet and a 0 is quiet then a pulse"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Each bit is 1 µs: a 1 is pulse then quiet, a 0 is quiet then pulse.
- That is **pulse-position modulation** (PPM).
:::

ADS-B turns the carrier on and off, which is amplitude modulation, and the bit lives in *where* the 0.5 µs pulse sits within its 1 µs: a 1 puts the pulse in the first half and a 0 in the second. That is **pulse-position modulation** (PPM), and it sends 1 million bits a second. Every bit holds exactly one pulse, so a receiver decides each bit by comparing the two halves, and it never needs to know how strong the aircraft is.

Each message starts with an 8 µs **preamble** of four pulses, at 0, 1.0, 3.5, and 4.5 µs, which no run of data bits can imitate. The 112 bits follow, so a whole message lasts 120 µs. At 2 MS/s every half bit is one sample, which we call a **chip**: the preamble is 16 chips and the message 224.
::::

::::{frame} Message Explorer
:class: viz-frame

:::{depth}
The explorer draws three real messages as the chips a receiver sees at 2 MS/s: the identification message from Sun's book, and a position and a velocity message from today's generator. The receiver compares the two chips of each bit, and the parity check decides whether to keep the message. Start with the first 16 bits and watch each bit's pulse sit in one half of its microsecond. Then raise the noise until a pulse in the wrong half wins, a bit turns red, and the parity fails.
:::

:::{present}
<iframe src="../../viz/adsb-ppm.html"
        width="100%" height="480"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="ADS-B message explorer: the preamble and pulse-position chips of a Mode S message, its five fields, and whether its parity passes as noise rises">
</iframe>
:::
::::

::::{frame} The ADS-B Out Generator
:::{present}
<img src="../../viz/img/L18-grc-tx.png"
     alt="GNU Radio Companion with L18-adsb-tx.grc open: the ADS-B Out embedded block, a Head of 1 million samples, Float To Complex, a Multiply by a 75 kHz Signal Source, an Add with a Noise Source, a Throttle, and a SigMF Sink writing L18-adsb-sim.sigmf-data, with a Complex to Mag feeding a triggered QT GUI Time Sink"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The **ADS-B Out** block writes PPM chips for four aircraft.
- The carrier, noise, and a SigMF Sink follow, as on the 2025 slides.
:::

The slides build their test signal in steps: PPM, then AM on a carrier, then noise. `L18-adsb-tx.grc` does the same in GNU Radio. The **ADS-B Out** block is an Embedded Python Block, the kind the L11 lesson built, and it writes the chips of every message for four simulated aircraft near USAFA. Float To Complex and a Multiply put those chips on a carrier 75 kHz from the center, the Noise Source adds noise, and a **SigMF Sink** writes 0.5 s to `L18-adsb-sim.sigmf-data` with its sample rate and the 1090 MHz center frequency in `L18-adsb-sim.sigmf-meta`, whose description says Simulated.

The aircraft send several times as often as real ones do, so the half second holds about 60 messages. Nothing transmits: the last block is a file sink.
::::

::::{frame} Inside the PPM Block
:::{present}
```python
out = [1,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0]   # preamble
for x in bits:                             # 112 bits
    out += [1, 0] if x else [0, 1]         # PPM
```
:::
:::{present}
- The block builds 88 bits of message, appends 24 parity bits, and makes chips.
- Double-click it in GRC to read or edit the code.
:::

The slides' fourth objective is to develop a PPM modulation block, and the code above is the heart of ours: the preamble's 16 chips, then two chips for each of the 112 bits. Around it, the block builds each message from the aircraft list at the top of its code, using the encodings the next frames describe, and computes the 24 parity bits from the first 88. It then places each message at a random time, so messages from different aircraft sometimes overlap, as they do in the sky.

Double-click the block in GRC and choose Open in Editor to see all of it. The list `AIRCRAFT` holds each aircraft's address, callsign, position, altitude, speed, and heading; add a fifth aircraft there, run the generator, and the receiver shows it.
::::

::::{frame} Message Structure
:::{present}
<img src="../../viz/img/L18-frame.svg"
     alt="The 112 bits of a DF17 message as five fields, not to scale: DF 5 bits, CA 3 bits, ICAO 24 bits, ME 56 bits, and PI 24 bits, with the example 8D4840D6202CC371C32CE0576098 split under them as 8D, 4840D6, 202CC371C32CE0, and 576098"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- **ICAO**: the aircraft's 24-bit address. **ME**: the 56-bit message.
- **PI**: 24 parity bits; a message that fails them is dropped.
:::

| Bits | Field | What it holds |
| :-- | :-- | :-- |
| 1–5 | DF | Downlink Format: 17 for ADS-B |
| 6–8 | CA | transponder capability |
| 9–32 | ICAO | the aircraft's address, unique worldwide |
| 33–88 | ME | the message: identity, position, or velocity |
| 89–112 | PI | parity |

The slides' example, `8D4840D6202CC371C32CE0576098`, comes from Sun's book. Its first byte, 8D, is DF 17 and CA 5; the aircraft's address is 4840D6; and its ME field decodes to the callsign KLM1023. The parity bits are computed from the first 88 with a fixed 25-bit generator, and the receiver repeats that calculation: if a single bit arrived wrong, the result disagrees and the message is dropped. The decoder does this for us.
::::

::::{frame} What the ME Field Carries
:::{present}
| Type code | Message |
| :-: | :-- |
| 1–4 | identification: callsign |
| 9–18 | airborne position, barometric altitude |
| 19 | velocity: speed, track, climb rate |
:::

The first 5 bits of the ME field are its **type code**, which says how to read the other 51. An **identification** message carries the callsign as eight 6-bit characters. An **airborne position** message carries the altitude in 25 ft steps and a compressed latitude and longitude. A **velocity** message carries the east and north speeds, from which the decoder finds ground speed and track, and the climb rate. Sun's book lists every type code; these three are the ones our decoder reads.

Position takes a little care. To fit in 34 bits, it is sent in **Compact Position Reporting** (CPR), which gives the position within one of many zones but not which zone. Aircraft alternate two zone sizes, called even and odd, and a receiver either pairs an even and an odd message or uses a reference position it already knows within 180 nautical miles. Our decoder uses USAFA as its reference, so its positions are right anywhere in Colorado.
::::

::::{frame} The Receiver
:::{present}
<img src="../../viz/img/L18-grc-rx.png"
     alt="GNU Radio Companion with L18-adsb-rx.grc open: a SigMF Source and a Throttle, a disabled Soapy RTLSDR Source at 1090 MHz, and a Noise Source with its Added noise slider, into an Add, then Complex to Mag feeding two QT GUI Time Sinks and the Mode S Decoder embedded block, with Function Probes and QT GUI Labels for the message count and the aircraft table"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- **Complex to Mag** turns the samples into pulse heights.
- The triggered **Time Sink** freezes one message on its first pulse.
:::

The receiver is short, because PPM needs only the size of each sample, not its phase. The SigMF Source plays the recording and the Throttle paces it at 2 MS/s; for live signals, a Soapy RTLSDR Source replaces both. An Add mixes in noise from the **Added noise** slider. **Complex to Mag** gives each sample's magnitude, which is the pulse train.

Two QT GUI Time Sinks show it. The left one runs freely over 20 ms, so each message is a spike. The right one is **triggered**: it waits until the magnitude crosses 0.3, then freezes 60 µs starting just before that point, so we see the preamble's four pulses and the first bits of one message.
::::

::::{frame} Decoding Step by Step
:::{present}
1. Find four preamble pulses with quiet between them.
2. Compare each pair of chips: the larger half is the pulse.
3. Check the parity, then print and tabulate.
:::

The **Mode S Decoder** is an Embedded Python Block, and its steps are the ones above. It slides along the magnitude looking for the preamble: chips 0, 2, 7, and 9 well above the noise and the chips between them quiet. At each match it reads the next 224 chips in pairs and calls a bit a 1 when the first chip of its pair is larger. Then it checks the parity, drops the message if it fails, and otherwise prints it in hex with what it says and updates the aircraft table.

The GRC console shows each message as the decoder prints it, for example `8D4840D6202CC371C32CE0576098  ICAO 4840D6  callsign KLM1023`. The Messages label counts the messages that passed parity and those that failed, and both start over when a slider moves.
::::

::::{frame} What Noise Does
:::{present}
<img src="../../viz/img/L18-adsb-noise.png"
     alt="L18-adsb-rx.grc labeled SIMULATED with the added noise at 0.15: the noise floor in the 20 ms plot has risen to about 0.4, with two clear spikes and a third barely above it; the triggered plot shows noise instead of a message; the table lists only ECE448 and FALCON21, the two strongest aircraft"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Raise **Added noise** and watch the weak aircraft disappear first.
- The trigger starts firing on noise instead of messages.
:::

The figure raises the added noise to 0.15. The floor of the 20 ms plot climbs until only the two strongest aircraft stand clearly above it. The weaker two still send, but a noise peak now beats a pulse in some chip pair of almost every message, the parity fails, and they drop out of the table. The triggered plot starts firing on noise peaks, because they now cross 0.3 on their own.

A real receiver sees the same thing with distance. A nearby aircraft decodes cleanly, a distant one decodes only now and then, and one past the horizon not at all. Move the slider a step at a time and watch which aircraft go first.
::::

::::{frame} Ready-Made Decoders
:::{present}
- **dump1090** decodes from an RTL-SDR and shows a live table and map.
- **SDRangel** has an ADS-B demodulator with a map.
- **gr-adsb** is a set of GNU Radio blocks for the same job.
:::

The slides list three tools. **dump1090** is the standard command-line decoder; it reads the RTL-SDR at 2.4 MS/s, and `dump1090 --interactive` prints a table much like ours; its network options feed the aircraft to other programs, including web maps. It is packaged on Linux as dump1090-mutability or dump1090-fa, and SDR Flex's full version runs it as a decoder. **SDRangel** is a graphical SDR program with an ADS-B demodulator. **gr-adsb**, by Matt Hostetter, is an out-of-tree GNU Radio module with a demodulator and decoder block; it has a branch for GNU Radio 3.10, but we have not built it in this course, so our flowgraphs use the Mode S Decoder above, which needs only radioconda.

We ran dump1090-mutability on our simulated recording, resampled to its 2.4 MS/s, and it listed the same four aircraft with the same callsigns, altitudes, and positions as our decoder.
::::

::::{frame} Key Point
:::{present}
:class: callout
ADS-B sends 112-bit messages on 1090 MHz as pulses: each bit is one 0.5 µs pulse in the first or second half of its microsecond. The receiver finds the preamble, compares chip pairs, and keeps messages whose parity checks.
:::
::::

::::{frame} On the SDR
:::{present}
- Disable the SigMF Source and the Throttle, enable the RTL-SDR Source.
- Put the antenna at a window, gain near 40 dB, and run it.
- Receive only: nothing in this course transmits on 1090 MHz.
:::

To go live, select the SigMF Source and the Throttle in `L18-adsb-rx.grc`, press D to disable both, enable the Soapy RTLSDR Source, and run it; it is already at 1090 MHz and 2 MS/s. A quarter wavelength at 1090 MHz is about 6.9 cm, so the RTL-SDR's small antenna works, and a window facing the approach to Colorado Springs or Denver works best. Live pulses arrive weaker than the simulated ones, so if the triggered plot never fires, lower its trigger level in the time sink's settings.

Anyone may receive ADS-B. Transmitting it is another matter: 1090 MHz carries the replies that air traffic control and collision-avoidance systems depend on, and nothing in a message proves who sent it, which is why false targets are a research topic (the slides' Magazu thesis). Our generator writes a file and never connects to a transmitter, and no flowgraph in this course transmits on 1090 MHz.
::::

::::{frame} Downloads
:class: read-only doc-links

- <a class="doc-link" href="../../grc/L18-adsb-tx.grc" download>L18-adsb-tx.grc</a>: the ADS-B Out generator. Writes `L18-adsb-sim.sigmf-data` and `.sigmf-meta`, 0.5 s (8 MB) of four simulated aircraft at 2 MS/s, then stops. Run it once. No hardware needed.
- <a class="doc-link" href="../../grc/L18-adsb-rx.grc" download>L18-adsb-rx.grc</a>: the receiver, with the pulse plots, the Mode S Decoder, the Added noise slider, and a disabled RTL-SDR Source for live signals.

Put both flowgraphs in one folder and run the generator first; GRC runs a flowgraph from its own folder, so the receiver finds the recording there. The two decoders are Embedded Python Blocks saved inside the `.grc` files.

**What this lesson follows.** The topics and their order come from the slides. The hands-on steps follow the references the slides list and the documentation of the tools:

- <a class="doc-link" href="../../legacy/L35-adsb.pdf" target="_blank" rel="noopener">ADS-B slides (PDF)</a>
- <a class="doc-link" href="../../legacy/refs/1090_Riddle.pdf" target="_blank" rel="noopener">The 1090 Megahertz Riddle, Junzi Sun (PDF)</a>: the message, the type codes, the parity, and CPR. Its earlier version is the <a class="doc-link" href="../../legacy/refs/adsb-decode-guide.pdf" target="_blank" rel="noopener">ADS-B Decoding Guide (PDF)</a>.
- <a class="doc-link" href="../../legacy/refs/adsb_magazu_usaf.pdf" target="_blank" rel="noopener">Magazu, AFIT thesis on ADS-B false targets (PDF)</a>: why ADS-B is open to spoofing.
- <a href="https://wiki.gnuradio.org/index.php/Embedded_Python_Block" target="_blank" rel="noopener">GNU Radio wiki, Embedded Python Block</a>, for the ADS-B Out and Mode S Decoder blocks, and the wiki pages of the other blocks, which have the same names as the blocks.
- <a href="https://github.com/livethisdream/sdr-flex" target="_blank" rel="noopener">SDR Flex and its README</a>, the course's explore tool, and GQRX, which radioconda installs, as the fallback.
- <a href="https://github.com/flightaware/dump1090" target="_blank" rel="noopener">dump1090</a>, <a href="https://github.com/f4exb/sdrangel" target="_blank" rel="noopener">SDRangel</a>, and <a href="https://github.com/mhostetter/gr-adsb" target="_blank" rel="noopener">gr-adsb</a>, the slides' tools.
::::

::::{frame} Summary
:class: read-only

| Idea | What to know | In GNU Radio |
| :-- | :-- | :-- |
| ADS-B | Mode S extended squitter, DF 17, 1090 MHz | the Soapy RTLSDR Source at 1090 MHz |
| PPM | 1 µs a bit; a 1 is pulse then quiet | 2 MS/s: two chips a bit |
| Preamble | pulses at 0, 1.0, 3.5, 4.5 µs | the trigger on the Time Sink |
| Message | DF, CA, ICAO, ME, PI: 112 bits | the Mode S Decoder |
| Type code | 1–4 callsign, 9–18 position, 19 velocity | the decoder's table |
| Parity | 24 bits; a failed message is dropped | the Messages label |
| Noise | weak aircraft drop out first | the Added noise slider |
| Tools | dump1090, SDRangel, gr-adsb | dump1090 at 2.4 MS/s |
::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE448_L18_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE448_L18_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Looking Ahead
:::{present}
- Lesson 19 decodes AIS, the ships' version of ADS-B.
- The L18–L19 Lab decodes live aircraft and a recording of ships.
:::

Today we built ADS-B messages as pulses, received them with a magnitude and a triggered plot, and decoded them with a block that finds the preamble, compares chip pairs, and checks the parity. Lesson 19 turns to **AIS**, which does the same job for ships on VHF, with FM in place of pulses and a CRC in place of Mode S parity.

The L18–L19 Lab follows Lesson 19. You build an ADS-B front end yourself, decode the aircraft overhead and compare them with a public flight tracker, then build an AIS receiver and decode a recording of ships.
::::
