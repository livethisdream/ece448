<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 448

Software Defined Radios

## Lesson 18 — ADS-B

Spring 2027 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where We Were

- Lesson 12: on-off keying, the simplest pulse signal
- Lesson 11: Embedded Python Blocks
- Lesson 17: finding the bits in an unknown signal

Today we generate, receive, and decode aircraft ADS-B messages.

Note:
Open L18-adsb-tx.grc and L18-adsb-rx.grc in GRC before class, and run the generator once so the recording exists. If the room has a window, an RTL-SDR on the sill hears real aircraft for the On the SDR slide.

---

## Today's Plan

1. ADS-B and Mode S
2. The physical layer: pulse-position modulation
3. The ADS-B Out generator, and our PPM block
4. The message: DF, ICAO, ME, parity
5. The receiver and the Mode S Decoder
6. Noise, tools, and live aircraft

Note:
These follow the 2025 slides in order. The reference for every message detail is Sun's The 1090 Megahertz Riddle, in the slides' references.

---

## Aircraft Overhead

<img src="./img/18-adsb/L18-adsb-rx.png" alt="L18-adsb-rx.grc on the simulated recording: pulses, one triggered message, and a table of four aircraft near USAFA" style="max-height:440px; display:block; margin:0 auto;">

Each spike is one 120 µs message; the table fills with aircraft.

Note:
Run the receiver live. Point at the left plot: each spike is a message. The right plot freezes one on its first pulse. The table at the bottom is what the decoder has read so far. The recording is simulated, and the figure says so.

---

## ADS-B and Mode S

- **Mode S** transponders reply to radar on 1090 MHz.
- **ADS-B** has them broadcast on their own, about twice a second.
- The common form is the **extended squitter**, DF 17.

Note:
Automatic: no one asks. Dependent: the position comes from the aircraft's GPS. Broadcast: anyone may listen. Secondary radar interrogates on 1030 MHz and the transponder answers on 1090. DF 18 is the same message from a device that is not a transponder. In the US, small aircraft below 18,000 ft may use UAT on 978 MHz instead, a different waveform we do not cover.

---

## Find It on the Air

1. RTL-SDR at 2.4 MS/s, gain near 40 dB
2. Tune to 1090 MHz
3. Look for short dots scattered in time
4. In SDR Flex, attach dump1090

Note:
SDR Flex's full version (Docker or server) has the live radio and the dump1090 decoder; the browser version has neither. Its README says the radio drivers have not been tried with a real radio yet, so GQRX is the tested path for the first look. GQRX has no ADS-B decoder: the dots are as far as GQRX goes.

---

## The Physical Layer

<div class="fig" data-inline-svg="./fig/L18-ppm.svg" style="max-width:820px; margin:0 auto;"></div>

A 1 is pulse then quiet; a 0 is quiet then pulse: **pulse-position modulation**.

Note:
Each pulse is 0.5 us and each bit 1 us, so 1 Mb/s. Every bit holds exactly one pulse, so the receiver compares halves and never needs the signal's strength. The preamble's four pulses, at 0, 1.0, 3.5, and 4.5 us, cannot be imitated by data. At 2 MS/s each half bit is one sample, a chip: 16 chips of preamble, 224 of data, 120 us in all.

---

## Message Explorer

<iframe src="../viz/adsb-ppm.html" width="100%" height="473" style="border:1px solid #cddce9; border-radius:6px;" title="ADS-B message explorer"></iframe>

Note:
Start with the first 16 bits: each bit's pulse sits in one half. Raise the noise until a bit turns red and the parity fails. Switch messages: identification, position, velocity.

---

## The ADS-B Out Generator

<img src="./img/18-adsb/L18-grc-tx.png" alt="L18-adsb-tx.grc in GRC: ADS-B Out block, Head, Float To Complex, a carrier, noise, Throttle, and a SigMF Sink" style="max-height:330px; display:block; margin:0 auto;">

PPM chips, then a carrier, then noise, as on the 2025 slides.

Note:
The ADS-B Out block is an Embedded Python Block like Lesson 11's. It writes 0.5 s to L18-adsb-sim.sigmf-data and .sigmf-meta, labeled Simulated. The aircraft send several times more often than real ones, so the half second holds about 60 messages. Nothing transmits: the last block is a file sink.

---

## Inside the PPM Block

```python
out = [1,0,1,0,0,0,0,1,0,1,0,0,0,0,0,0]   # preamble
for x in bits:                             # 112 bits
    out += [1, 0] if x else [0, 1]         # PPM
```

The slides' objective: develop a PPM modulation block.

Note:
Double-click the block and choose Open in Editor. Around these lines it builds 88 bits of message from the AIRCRAFT list, appends 24 parity bits, and places each message at a random time, so messages sometimes overlap as in the sky. Add a fifth aircraft to the list and the receiver shows it.

---

## Message Structure

<div class="fig" data-inline-svg="./fig/L18-frame.svg" style="max-width:820px; margin:0 auto;"></div>

| DF | CA | ICAO | ME | PI |
| :-: | :-: | :-: | :-: | :-: |
| format | capability | address | message | parity |

Note:
The slides' example 8D4840D6202CC371C32CE0576098 is from Sun's book: 8D is DF 17 and CA 5, the address is 4840D6, and the ME field is the callsign KLM1023. The parity bits come from the first 88 bits with a fixed 25-bit generator; the decoder repeats the calculation and drops any message that disagrees.

---

## What the ME Field Carries

| Type code | Message |
| :-: | :-- |
| 1–4 | identification: callsign |
| 9–18 | airborne position, altitude |
| 19 | velocity |

Note:
The callsign is eight 6-bit characters; the altitude is in 25 ft steps. Position uses Compact Position Reporting: even and odd messages with two zone sizes. A receiver pairs them or uses a reference position within 180 nautical miles. Our decoder uses USAFA as its reference.

---

## The Receiver

<img src="./img/18-adsb/L18-grc-rx.png" alt="L18-adsb-rx.grc in GRC: SigMF Source, Throttle, a disabled RTL-SDR Source, noise, Complex to Mag, two time sinks, and the Mode S Decoder" style="max-height:330px; display:block; margin:0 auto;">

**Complex to Mag** gives the pulse train; a triggered **Time Sink** freezes one message.

Note:
PPM needs only the magnitude, not the phase. The left time sink runs freely over 20 ms. The right one triggers at 0.3 and shows 60 us from just before the first pulse. For live signals, the RTL-SDR Source replaces the SigMF Source and Throttle.

---

## Decoding Step by Step

1. Find four preamble pulses with quiet between them.
2. Compare each pair of chips: the larger half is the pulse.
3. Check the parity, then print and tabulate.

Note:
The Mode S Decoder is an Embedded Python Block. It prints each message to the GRC console in hex with what it says, and the Messages label counts passes and failures; both start over when a slider moves.

---

## What Noise Does

<img src="./img/18-adsb/L18-adsb-noise.png" alt="The receiver with added noise 0.15: the floor rises, only the strongest aircraft remain in the table" style="max-height:420px; display:block; margin:0 auto;">

Raise **Added noise**: the weak aircraft drop out first.

Note:
At 0.15 the floor rises until only the two strongest aircraft stand clear. The others still send, but noise beats a pulse in some chip pair of almost every message, so the parity fails. Distance does the same thing to real aircraft. The trigger starts firing on noise.

---

## Ready-Made Decoders

- **dump1090**: RTL-SDR at 2.4 MS/s, live table and maps
- **SDRangel**: ADS-B demodulator with a map
- **gr-adsb**: GNU Radio blocks; a 3.10 branch, not built here

Note:
dump1090 --interactive prints a table like ours; it is packaged as dump1090-mutability or dump1090-fa. We ran dump1090-mutability on our recording, resampled to 2.4 MS/s, and it listed the same four aircraft with the same callsigns, altitudes, and positions.

---

## Key Point

<div class="callout">ADS-B sends 112-bit messages on 1090 MHz as pulses: each bit is one 0.5 µs pulse in the first or second half of its microsecond. The receiver finds the preamble, compares chip pairs, and keeps messages whose parity checks.</div>

Note:
The decoder needs only the magnitude of the signal.

---

## On the SDR

- Disable the SigMF Source and Throttle; enable the RTL-SDR Source.
- Antenna at a window, gain near 40 dB.
- Receive only: never transmit on 1090 MHz.

Note:
A quarter wave at 1090 MHz is about 6.9 cm, so the RTL-SDR's antenna works. Live pulses are weaker; lower the trigger level if the right plot never fires. 1090 MHz carries replies that air traffic control and collision avoidance depend on, and nothing in a message proves who sent it; the slides' Magazu thesis studies false targets. Our generator only writes a file.

---

## Looking Ahead

- Lesson 19: AIS, the ships' version, on VHF with GMSK
- L18–L19 Lab: live aircraft and a recording of ships

Note:
In the lab, cadets build the ADS-B front end themselves and compare the aircraft they decode with a public flight tracker.
