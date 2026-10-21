---
frame_view: true
---

# L16 - Frequency Hopping

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">Frequency Hopping</h1>

<div class="title-rule"></div>

An FHSS transmitter and receiver that stay on the same hop sequence.

Lesson 16 · Module 6: Waveform Applications & RF Reverse Engineering · Dr. Neil Rogers
::::

::::{frame} Slides
:class: read-only

:::{admonition} Slides
:class: slides
<a href="../../slides/L16-fhss.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L16-fhss.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L16-fhss.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '6'; counter-reset: lo 4">
  <li>I can implement FHSS transmission and reception, including hop-sequence synchronization.</li>
</ol>
::::

::::{frame} A Link That Hops
:::{present}
<img src="../../viz/img/L16-link-jam.png"
     alt="The L16 link flowgraph running at noise amplitude 1 with a jammer of amplitude 3 on channel 4: the received-band waterfall shows short dashes stepping among eight channels from minus 35 to plus 35 kHz and a solid vertical jammer line at plus 5 kHz; the After Hop Sync waterfall shows the signal held still at 0 Hz and the jammer as short dashes at other frequencies; the labels read Receiver locked, Packets 86 correct of 98 sent in 24 s (88%), and Received USAFA ECE 448"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The transmitter changes channel every 240 ms, in an order only the receiver knows.
- A jammer parked on one channel stops only one hop in eight.
:::

The figure is today's flowgraph, `L16-fhss-link.grc`, running. The transmitter is Lesson 8's FSK modem sending Lesson 10's packets, one packet per **hop**, and it moves to a new channel for every hop. The left waterfall is the band the receiver sees: the signal appears as short dashes that step around eight channels, and a **jammer**, a strong tone parked on one channel, is the solid vertical line at +5 kHz.

The receiver follows the same sequence of channels. The right waterfall is its output after the **Hop Sync** block: the signal stands still at 0 Hz, and now the jammer appears to hop. The receiver loses only the hops that land on the jammed channel, 1 in 8, and the Packets label shows 88% of the packets arriving intact. This is **frequency-hopping spread spectrum** (FHSS).
::::

::::{frame} Where Frequency Hopping Is Used
:::{present}
- **Bluetooth Classic**: 79 channels at 2.4 GHz, up to 1600 hops a second.
- **SINCGARS**: the Army's VHF radio, 2320 channels, about 100 hops a second.
- **ISM-band hoppers** at 915 MHz: at least 50 channels.
:::

Hopping solves two problems at once. Interference on one channel, from a microwave oven, a Wi-Fi network, or a jammer, costs a hopping link only the hops that land there. And a listener who does not know the sequence hears only short bursts scattered across the band.

Bluetooth Classic hops among 79 channels 1 MHz apart, from 2402 MHz up, in slots of 625 µs, up to 1600 hops a second, and its **adaptive frequency hopping** (AFH) drops channels that stay busy. SINCGARS, the Army's VHF-FM combat net radio, hops about 100 times a second among up to 2320 channels 25 kHz apart; its sequence comes from a transmission security key and the time of day, so a radio without the key cannot follow it. Unlicensed hoppers at 915 MHz fall under FCC Part 15.247, which requires a pseudo-random sequence that uses every channel equally, at least 50 channels for a narrowband signal, and no more than 0.4 s on any one channel in 20 s.
::::

::::{frame} Part 1: The Hopping Transmitter
:::{present}
<img src="../../viz/img/L16-grc-tx.png"
     alt="The L16 transmitter flowgraph in GNU Radio Companion: two Vector Sources with Stream to Tagged Stream, a Protocol Formatter, and a four-input Tagged Stream Mux build each hop's packet; Unpack K Bits, Chunks to Symbols, Repeat, and Frequency Mod make Lesson 8's FSK; a Vector Source of hop frequencies, a Repeat of 30,720 samples, and a VCO make the hopping tone; a Multiply combines them, followed by a Throttle, a waterfall, and a time sink of the hop frequency"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The top row is Lesson 8's FSK transmitter with Lesson 10's packets.
- A **VCO** driven by the hop sequence is the hop synthesizer.
- **Multiply** moves the FSK signal to each hop's channel.
:::

`L16-fhss-tx.grc` builds the transmitter. The top row is the FSK transmitter of Lesson 8 at 1000 baud with a 1 kHz deviation, running at 128 kHz so the hops have room. A **Tagged Stream Mux** with four inputs assembles each packet: 2 guard bytes, the 12-byte access code and header from the **Protocol Formatter**, the 14-byte line `USAFA ECE 448` with its newline, and 2 more guard bytes.

The bottom row is the **hop synthesizer**. A **Vector Source** repeats the list of hop frequencies, a **Repeat** block holds each one for 30,720 samples, one hop, and a **VCO** turns each value into a tone at that many hertz. Multiplying the FSK signal by that tone moves it to the hop's channel, the way a radio's synthesizer and mixer move a signal to its carrier.
::::

::::{frame} One Packet per Hop
:::{present}
<img src="../../viz/img/L16-hop-frame.svg"
     alt="One hop of the L16 link to scale: 16 guard bits, a 64-bit access code, a 32-bit header, a 112-bit payload of USAFA ECE 448 and a newline, and 16 more guard bits, 240 bits or 240 ms at 1000 baud"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Each hop carries exactly one packet: 240 bits, 240 ms.
- Guard bits at each end let the receiver's timing be off a little.
:::

The packet and the hop have the same length, so every hop boundary falls between two packets and no packet is ever split across two channels. Bluetooth works the same way: each packet fits in one 625 µs slot or in several slots on one frequency.

The **guard bits** at each end are the alternating pattern 01010101. They carry no data. If the receiver changes channel a few milliseconds late, it misses part of the leading guard, and if it changes early, part of the trailing guard; in both cases the access code, header, and payload still arrive on the right channel. The Timing Error frame below measures how much error the 16 guard bits at each end absorb.
::::

::::{frame} The Hop Sequence
:::{present}
<img src="../../viz/img/L16-tx-hops.png"
     alt="The L16 transmitter running: the Hop key slider reads 448 and the label reads Hop sequence 7 2 0 6 4 1 3 5; the waterfall shows dashes stepping among eight channels from minus 35 to plus 35 kHz; the time sink shows the hop frequency as a staircase over 4 s, holding each of minus 15, minus 35, plus 25, plus 5, minus 25, minus 5, plus 15, and plus 35 kHz for 240 ms, then repeating"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Eight channels, 10 kHz apart, from −35 to +35 kHz.
- A **key** seeds a pseudo-random order that visits each channel once per cycle.
:::

Channel $k$, for $k = 0$ to 7, sits at

$$f_k = 10\text{ kHz} \times (k - 3.5),$$

so channel 0 is at −35 kHz and channel 7 at +35 kHz. The FSK signal is about 4 kHz wide, so neighboring channels do not overlap. The variable `seq` holds the **hop sequence**, `np.random.default_rng(key).permutation(8)`: a shuffled list of the 8 channels, set by the **key**. Key 448 gives 7, 2, 0, 6, 4, 1, 3, 5, and the time sink on the right shows the same order as frequencies. Moving the Hop key slider gives a different order.

A permutation uses each channel exactly once per **cycle** of 8 hops, which meets Part 15's equal-use rule and, as Part 3 shows, makes acquiring sync simple. Real systems use much longer sequences: Bluetooth computes each hop from the master's 28-bit clock and its address, and its sequence takes about 23 hours to repeat.
::::

::::{frame} Hop Timing
:class: read-only

At $R_s = 1000$ baud, a hop of $n$ bits lasts

$$\begin{aligned}
T_\text{hop} &= \frac{n}{R_s} \\
&= \frac{240}{1000\text{ baud}} = 240 \text{ ms},
\end{aligned}$$

and the 128 kHz flowgraph holds each hop frequency for $128{,}000 \times 0.240 = 30{,}720$ samples. The hop rate and the time for one cycle of $N$ channels are

$$\begin{aligned}
\text{hop rate} &= \frac{1}{T_\text{hop}} \\
&= 4.17 \text{ hops/s}, \\
T_\text{cycle} &= N\,T_\text{hop} \\
&= 8 \times 240 \text{ ms} = 1.92 \text{ s}.
\end{aligned}$$

| | L16 link | Bluetooth Classic | SINCGARS |
| :-- | :-: | :-: | :-: |
| Channels | 8 | 79 | up to 2320 |
| Spacing | 10 kHz | 1 MHz | 25 kHz |
| Hop rate | 4.17 hops/s | up to 1600 hops/s | about 100 hops/s |
| Time on one hop | 240 ms | 625 µs | about 10 ms |

Our link hops slowly so that the waterfall can show each hop. A real hopper sends the same kind of packet in a much shorter hop; the blocks and the synchronization problem are the same. The guard bits take 32 of the 240 bits, 13% of each hop.
::::

::::{frame} FHSS Explorer
:class: viz-frame

:::{depth}
Each column is one hop. The filled cell is the transmitter's channel and the amber box the receiver's; a navy cell is a delivered hop and a gray one is lost. The red band is the jammer. Start with 8 channels and 1 jammed channel: 1 hop in 8 is lost, and the long-run delivery matches $1 - 1/8$. Widen the jammer or reduce the channels and watch the delivered fraction follow $1 -$ jammed/channels. Set the receiver offset to +1: the box is always one step ahead, and nothing arrives. Then press the acquire button: the receiver waits on the sync channel, in amber on the axis, and locks when the transmitter arrives there. Move the jammer onto the sync channel, and the receiver never locks.
:::

:::{present}
<iframe src="../../viz/fhss-explorer.html"
        width="100%" height="485"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="FHSS explorer: a hop sequence on a grid of channel against hop, the receiver's channel on each hop, and a jammer, with the delivered fraction as the channels, the jammer, the receiver's offset, and the key change">
</iframe>
:::
::::

::::{frame} Part 2: The Receiver
:::{present}
<img src="../../viz/img/L16-grc-link.png"
     alt="The L16 link flowgraph in GNU Radio Companion: the hopping transmitter of L16-fhss-tx.grc, a Throttle, a Delay for the path delay, and an Add with a Noise Source and a Signal Source jammer; a Virtual Sink and Virtual Source carry the channel to the receiver row: Hop Sync, a decimating Low Pass Filter, Quadrature Demod, Moving Average, Symbol Sync, Binary Slicer, Correlate Access Code - Tag Stream, Repack Bits, and the Text Sink, whose pkt message port connects back to Hop Sync; two waterfall sinks show the band before and after Hop Sync"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- **Hop Sync** undoes each hop: the signal comes out at 0 Hz.
- Everything after it is Lesson 8's FSK receiver.
- The Text Sink tells Hop Sync each time a packet arrives.
:::

`L16-fhss-link.grc` adds a channel and a receiver to the transmitter. The channel delays the signal by a path delay the receiver does not know, adds noise, and adds the jammer, a tone of adjustable amplitude at the center of one channel.

The receiver starts with **Hop Sync**, an Embedded Python Block. It multiplies the received band by a tone at minus the current hop frequency, which **de-hops** the signal: every hop comes out at 0 Hz. A **Low Pass Filter** then keeps ±2 kHz and decimates by 4 to 32 kHz, which removes the other seven channels, and from the **Quadrature Demod** on, the receiver is Lesson 8's, with the same Symbol Sync, access-code search, and Text Sink. The Text Sink sends a message to Hop Sync each time a packet arrives, which tells Hop Sync it is still on the right hops.
::::

::::{frame} De-Hopping
:::{present}
<img src="../../viz/img/L16-link-clean.png"
     alt="The L16 link at noise amplitude 1 with no jammer: the received-band waterfall shows the hopping dashes; the After Hop Sync waterfall shows one steady vertical trace at 0 Hz; the labels read Receiver locked, Packets 82 correct of 82 sent in 20 s (100%), and Received USAFA ECE 448"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Multiplying by the conjugate of the hop tone moves every hop to 0 Hz.
- With no jammer, every packet arrives.
:::

The transmitter multiplied by $e^{j2\pi f_k t}$ on hop $k$; Hop Sync multiplies by $e^{-j2\pi f_k t}$ on the same hop, and the two cancel. The right waterfall shows the result: one steady trace at 0 Hz, the FSK signal of Lesson 8, while the noise stays spread across the band. The Low Pass Filter keeps only the 4 kHz around 0 Hz, so the receiver sees the same signal-to-noise ratio as a fixed-channel link with the same noise density. At noise amplitude 1, every packet arrives; at 2, 97% did, and at 2.5, 70%.

FSK suits a hopper because the receiver does not need the carrier's phase. The transmitter's and receiver's synthesizers do not start each hop at the same phase on a real radio, and the Quadrature Demod measures only the change of phase from sample to sample, so a phase jump at a hop boundary costs at most one bit, inside the guard. Bluetooth uses GFSK for the same reason.
::::

::::{frame} Part 3: Finding the Hops
:::{present}
<img src="../../viz/img/L16-acquire.svg"
     alt="Fourteen hops on a grid of channel against time: the transmitter's channels step through the sequence; the receiver, drawn as a dashed box, stays on the sync channel, channel 7, for five hops, and when the transmitter arrives on channel 7 for hop 0, the receiver's box follows the transmitter on every hop after that"
     style="max-width: 760px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The receiver parks on the **sync channel**, the channel of hop 0.
- When the power there jumps, hop 0 has started: it locks and hops from then on.
:::

A receiver that knows the key still does not know two things when it starts: which hop the transmitter is on, and when that hop began. The path delay alone is unknown, and on a real radio so are the latency of USB buffers and the instant the transmitter started. We use **sync on a known hop**. Hop Sync parks on the **sync channel**, `seq[0]`, channel 7 for key 448, and measures the power in it every 0.5 ms. Because the sequence visits each channel once per cycle, the transmitter can appear on channel 7 only on hop 0. When the power in the last 2 ms rises 6 dB above its average over the 18 ms before, hop 0 has just begun, and Hop Sync takes that instant as its hop boundary and starts hopping. It waits at most one cycle, 1.92 s.

Other designs were possible. A **start-of-hop marker**, such as the access code alone, gives timing within a hop but not which hop it is. **Time of day**, which SINCGARS uses, needs a clock shared to within the guard time. Sync on a known hop needs neither, only the key; its weakness is the one channel it listens on, which the Jammer frames below measure.
::::

::::{frame} Losing and Regaining Sync
:::{present}
<img src="../../viz/img/L16-link-resync.png"
     alt="The L16 link 9 s after the path delay slider moved from 100 to 400 ms: the After Hop Sync waterfall shows the steady trace at 0 Hz, then a stretch about 2.4 s long where the signal appears at scattered frequencies, then the steady trace again; the labels read Receiver locked, Packets 26 correct of 36 sent in 9 s (72%), and Received USAFA ECE 448"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- After about 10 hops with no packet, Hop Sync parks again.
- It locks on the next hop 0: here 10 packets were lost.
:::

The figure moves the path delay from 100 to 400 ms while the link runs, as if the transmitter had moved. The receiver's hop boundaries now fall 300 ms, more than a whole hop, away from the transmitter's, so it lands on the wrong channels and the scattered stretch on the right waterfall appears. Hop Sync counts the hops since the last packet, and when more than 9 pass, a cycle and a hop, with none, it parks on the sync channel again. It locks when hop 0 next arrives, and the steady trace returns.

The receiver loses about 10 hops, 2.4 s, plus up to one more cycle, 1.92 s, depending on where in the cycle the transmitter is when Hop Sync parks. Here the Packets label shows 26 of 36 packets since the slider moved: the receiver lost 10 hops, 2.4 s.
::::

::::{frame} Off by One Hop
:::{present}
<img src="../../viz/img/L16-link-offset.png"
     alt="The L16 link with the Receiver hop offset at plus 1: the received-band waterfall shows the normal hopping dashes; the After Hop Sync waterfall shows dashes scattered at offsets such as minus 60, minus 20, plus 20, and plus 60 kHz instead of a steady trace at 0 Hz; the labels read Packets 0 correct of 99 sent in 24 s (0%) and Received waiting for a packet"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- One hop ahead, the receiver is never on the transmitter's channel.
- Not one packet in 99 arrives.
:::

The Receiver hop offset slider moves the receiver's sequence ahead of the transmitter's by whole hops. At +1, Hop Sync locks at the right moment but tunes to `seq[k+1]` while the transmitter is on `seq[k]`. Consecutive entries of a permutation are always different channels, so the receiver is never on the right one: the right waterfall shows the signal scattered at the differences between channels, as far as 70 kHz from 0 Hz, and nothing passes the Low Pass Filter. Offsets of −1, +2, and −2 gave the same result, no packets at all.

The watchdog does not rescue it, because Hop Sync applies the offset after every lock. A sync error of a whole hop is the worst error a hopper can make: a receiver with the right timing on the wrong hop receives less than one with no hopping at all.
::::

::::{frame} Timing Error
:class: read-only

The Receiver timing error slider shifts every hop boundary of the receiver by a fixed time after it locks; a positive error means the receiver changes channel late. We measured the link headless, without the Throttle, at noise amplitude 1: three runs of 120 hops at each setting.

| Timing error | Delivered | What the receiver misses |
| :-: | :-: | :-- |
| −24 ms | 0% | the trailing guard and the whole newline |
| −20 ms | 5% | the trailing guard and 4 bits of the newline |
| −17 ms | 45% | the trailing guard and the first bit of the newline |
| −16 to +18 ms | 100% | only guard bits |
| +20 ms | 68% | the leading guard and 4 bits of the access code |
| +24 ms | 16% | the leading guard and 8 bits of the access code |

The window runs from −16 to +18 ms, about the 16 ms of guard at each end. It reaches a little further on the late side because the access-code search accepts a packet with up to 2 wrong bits of its 64, and a missed bit is wrong only half the time. More guard bits widen the window and lower the share of each hop that carries data: the guard costs 13% here, and a one-slot Bluetooth packet lasts at most 366 µs, which leaves about 40% of the 625 µs slot for the synthesizer to settle.
::::

::::{frame} Part 4: A Narrowband Jammer
:::{present}
<img src="../../viz/img/L16-link-jam.png"
     alt="The L16 link with a jammer of amplitude 3 on channel 4: the received band shows the jammer as a solid line at plus 5 kHz among the hopping dashes; after Hop Sync the signal is steady at 0 Hz and the jammer appears as short dashes at other frequencies; the Packets label reads 86 correct of 98 sent in 24 s (88%)"
     style="max-width: 820px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- After de-hopping, the jammer is the signal that hops.
- It reaches the receiver on 1 hop in 8: 88% of packets arrive.
:::

The jammer is a tone of amplitude 3 at the center of channel 4, 9.5 dB stronger than our signal. The receiver multiplies the whole band by the hop tone, so the jammer moves to a new frequency every hop; on most hops it lands outside the Low Pass Filter. Only on the hop where the receiver tunes to channel 4 does the jammer land at 0 Hz, between the FSK tones at ±1 kHz, and capture the Quadrature Demod.

With one of $N$ channels jammed, the fraction of packets delivered is about

$$P = 1 - \frac{1}{N},$$

which is 7/8, or 88%, for our 8 channels. We measured 280 of 319 packets, 87.8%, at jammer amplitudes of 1, 3, and 10: once the jammer is strong enough to take a hop, more power does not take more hops.
::::

::::{frame} Jammer Sweep
:class: read-only

We measured the link headless at noise amplitude 1, with two noise seeds at each setting: 320 hops when hopping over 8 channels, and 160 when the transmitter and receiver stay on one channel with the jammer on it.

| Jammer amplitude | Jammer vs. signal | One fixed channel | Hopping, 8 channels |
| :-: | :-: | :-: | :-: |
| 0.5 | −6 dB | 100% | 100% |
| 1 | 0 dB | 0% | 88% |
| 3 | +9.5 dB | 0% | 88% |
| 10 | +20 dB | 0% | 88% |

A jammer equal in power to the signal stops a fixed-channel link completely, and the hopping link still delivers 7 packets in 8. To take every hop, the jammer has to cover all 8 channels. The same transmitter power spread over 8 channels puts $10 \log_{10} 8 = 9$ dB less on each: eight tones of amplitude 0.354, together equal in power to one tone of amplitude 1, blocked no packets at all. Eight tones of amplitude 1, 8 times the power, let only 10% through once the receiver had locked.

The receiver has one weak point, the sync channel. With the tone of amplitude 3 on the sync channel, channel 7, from the start, Hop Sync never saw the power jump and never locked: 0 packets. Turned on after the receiver had locked, the same jammer took only its 1 hop in 8, and 89% arrived. A real system protects acquisition by using several sync channels, as Bluetooth's inquiry procedure does with 32, or by sending the hop number in every packet so that any hop can serve.
::::

::::{frame} Frequency Hopping on a Real Radio
:::{present}
- The L16 Lab sends this link through one PlutoSDR, TX port to RX port, through a 30 dB attenuator.
- All 8 channels fit in the Pluto's sample rate, so it never retunes.
- Nothing in L16 transmits over the air.
:::

The L16 Lab moves this link onto a PlutoSDR at 915 MHz. The transmit half ends at a PlutoSDR Sink instead of the channel, with a jammer tone added in software before it, and the receive half starts at a PlutoSDR Source, with the same Hop Sync and FSK receiver. As in L10 and L12, a Rational Resampler raises the 128 kHz stream by 8, to 1.024 MS/s, on the way out and lowers it on the way in, and an **AGC** holds the received level steady. The radio adds a delay of its own between the TX and RX ports, which Hop Sync finds the same way it finds the simulated path delay.

All eight channels lie within ±40 kHz, inside the 1.024 MS/s the Pluto samples, so the hopping happens in software and the Pluto's own synthesizer never changes frequency. A hopper whose channels span more than its sample rate, such as SINCGARS over 58 MHz, retunes its synthesizer at every hop, and the time the synthesizer takes to settle limits its hop rate.

In class we transmit only into a cable, into a shielded enclosure, or at very low power in an ISM band, and only when the lesson says to. Nothing in this lesson transmits; the L16 Lab transmits from the Pluto's TX port through an inline 30 dB attenuator into its own RX port. We have run the PlutoSDR flowgraph only in simulation, with a model of the cable in place of the radio, so the lab is its first run on hardware.
::::

::::{frame} Key Point
:::{present}
:class: callout
A hopper sends each packet on a new channel in a keyed order. A receiver with the same key and hop timing de-hops it, and a narrowband jammer takes only its own channel's hops. Off by one hop, nothing arrives.
:::
::::

::::{frame} Downloads
:class: read-only doc-links

- <a class="doc-link" href="../../grc/L16-fhss-tx.grc" download>L16-fhss-tx.grc</a>: the hopping FSK transmitter, with a slider for the hop key, a waterfall, and the hop frequency over time. No hardware needed.
- <a class="doc-link" href="../../grc/L16-fhss-link.grc" download>L16-fhss-link.grc</a>: the whole link, with sliders for the noise, the jammer, the path delay, and the receiver's hop offset and timing error, waterfalls before and after Hop Sync, and the received text. No hardware needed.

Open a `.grc` file from GRC's File menu, or run `gnuradio-companion L16-fhss-link.grc` from the radioconda prompt. Hop Sync and the Text Sink are Embedded Python Blocks, saved inside the `.grc` file; double-click one and choose Open in Editor to read its code. The number of channels, `nch`, the guard bytes, `guard`, and the receiver's key, `rx_key`, are variables you can edit on the canvas. The L16 Lab page has the PlutoSDR version of the link.
::::

::::{frame} Summary
:class: read-only

| Idea | What it is | Number to remember |
| :-- | :-- | :-- |
| FHSS | each packet on a new channel, in a keyed order | 8 channels, 10 kHz apart |
| Hop | one packet: guard, access code, header, payload, guard | 240 bits, 240 ms |
| Hop synthesizer | Vector Source, Repeat, VCO, Multiply | 30,720 samples a hop |
| Hop sequence | a permutation of the channels, set by the key | 7 2 0 6 4 1 3 5 for key 448 |
| De-hopping | multiply by the conjugate hop tone | signal back at 0 Hz |
| Sync on a known hop | park on `seq[0]`, lock when the power jumps | at most one cycle, 1.92 s |
| Sync error | off by one hop | 0 packets |
| Timing error | absorbed by the guard bits | −16 to +18 ms |
| Narrowband jammer | takes the hops on its channel | $1 - 1/N$ delivered |
::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE448_L16_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE448_L16_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Looking Ahead
:::{present}
- The L16 Lab builds a hopper and a de-hopper, measures jamming and sync, and runs the link on a PlutoSDR.
- Lesson 17 takes an unknown signal from spectrum to bits.
:::

The L16 Lab is the hands-on version of this lesson. You build a hop synthesizer and a de-hopper from standard blocks on an empty canvas, measure how many packets get through as the jammer, the number of channels, and the receiver's timing change, and then send the hopping link through a PlutoSDR and a cable.

Lesson 17 turns to RF reverse engineering: capturing an unknown signal and working out its modulation, its symbol rate, and its bits. A hopper is one of the harder signals to reverse engineer, because a receiver parked on one channel sees only one hop in $N$.
::::
