---
frame_view: true
nav: Waveform Applications & RF Reverse Engineering
---

# Module 6 — Waveform Applications & RF Reverse Engineering

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Module 06</div>

<h1 class="frame-title">Waveform Applications &amp; RF Reverse Engineering</h1>

<div class="title-rule"></div>

Real signals, real decoders: CW to AIS, and the unknown signal in between.

Lessons 12–19 · Software Defined Radios · Dr. Neil Rogers
::::

::::{frame} Where This Module Goes
CW, DTMF, HD Radio, mPSK, frequency hopping, ADS-B, and AIS, each built or decoded in GNU Radio, plus the workflow for taking an unknown signal from spectrum to bits.
::::

::::{frame} Learning Objectives (6.1-6.4)

<ol class="lo-list" style="--module: '6'">
  <li>I can transmit and receive CW (Morse) using GNU Radio and decode a received CW stream.</li>
  <li>I can decode DTMF tones from a captured audio signal.</li>
  <li>I can describe how HD Radio works and demodulate an HD Radio signal.</li>
  <li>I can implement an mPSK modulator and demodulator (BPSK, QPSK, 8PSK), recover carrier and symbol timing, and verify constellation behavior against theory.</li>
</ol>
::::

::::{frame} Learning Objectives (6.5-6.8)

<ol class="lo-list" style="--module: '6'; counter-reset: lo 4">
  <li>I can implement FHSS transmission and reception, including hop-sequence synchronization.</li>
  <li>I can perform RF reverse engineering on an unknown signal: identify its modulation, symbol rate, and payload structure.</li>
  <li>I can receive and decode ADS-B messages from aircraft transponders.</li>
  <li>I can receive and decode AIS messages from marine vessels.</li>
</ol>
::::

::::{frame} In This Module (1 of 5)

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L12-cw/index.html">
    <span class="mt-kind">Lesson · L12</span>
    <h4>CW</h4>
    <p>Send and decode Morse code in GNU Radio. Objective 6.1.</p>
  </a>
  <a class="mt-card mt-lesson" href="L12-lab-cw/index.html">
    <span class="mt-kind">L12 Lab</span>
    <h4>CW</h4>
    <p>Transmit, receive, and decode CW. Objective 6.1.</p>
  </a>
  <a class="mt-card mt-lesson" href="L13-dtmf/index.html">
    <span class="mt-kind">Lesson · L13</span>
    <h4>DTMF</h4>
    <p>Detect DTMF tones in a captured audio signal. Objective 6.2.</p>
  </a>
</div>
::::

::::{frame} In This Module (2 of 5)

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L13-lab-dtmf/index.html">
    <span class="mt-kind">L13 Lab</span>
    <h4>DTMF</h4>
    <p>Decode DTMF tones from a capture. Objective 6.2.</p>
  </a>
  <a class="mt-card mt-lesson" href="L14-hd-radio/index.html">
    <span class="mt-kind">Lesson · L14</span>
    <h4>HD Radio</h4>
    <p>How HD Radio hides OFDM sidebands beside an FM station, and how to demodulate them. Objective 6.3.</p>
  </a>
  <a class="mt-card mt-lesson" href="L14-lab-hd-radio/index.html">
    <span class="mt-kind">L14 Lab</span>
    <h4>HD Radio</h4>
    <p>Find and demodulate an HD Radio signal. Objective 6.3.</p>
  </a>
</div>
::::

::::{frame} In This Module (3 of 5)

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L15-mpsk/index.html">
    <span class="mt-kind">Lesson · L15</span>
    <h4>mPSK</h4>
    <p>BPSK, QPSK, and 8PSK in GNU Radio, with carrier and symbol-timing recovery. Objective 6.4.</p>
  </a>
  <a class="mt-card mt-lesson" href="L15-lab-mpsk/index.html">
    <span class="mt-kind">L15 Lab</span>
    <h4>mPSK</h4>
    <p>Build an mPSK modem and close the loop on carrier and timing. Objective 6.4.</p>
  </a>
  <a class="mt-card mt-lesson" href="L16-fhss/index.html">
    <span class="mt-kind">Lesson · L16</span>
    <h4>Frequency Hopping</h4>
    <p>An FHSS transmitter and receiver that stay on the same hop sequence. Objective 6.5.</p>
  </a>
</div>
::::

::::{frame} In This Module (4 of 5)

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L16-lab-fhss/index.html">
    <span class="mt-kind">L16 Lab</span>
    <h4>Frequency Hopping</h4>
    <p>Hop a transmitter and keep a receiver on it. Objective 6.5.</p>
  </a>
  <a class="mt-card mt-lesson" href="L17-rf-reverse-engineering/index.html">
    <span class="mt-kind">Lesson · L17</span>
    <h4>RF Reverse Engineering</h4>
    <p>Take an unknown signal from spectrum to bits with GQRX, URH, and GNU Radio. Objective 6.6.</p>
  </a>
  <a class="mt-card mt-lesson" href="L17-lab-rf-reverse-engineering/index.html">
    <span class="mt-kind">L17 Lab</span>
    <h4>RF Reverse Engineering</h4>
    <p>Reverse-engineer an unknown signal from capture to payload. Objective 6.6.</p>
  </a>
</div>
::::

::::{frame} In This Module (5 of 5)

<div class="module-toc">
  <a class="mt-card mt-lesson" href="L18-adsb/index.html">
    <span class="mt-kind">Lesson · L18</span>
    <h4>ADS-B</h4>
    <p>Receive and decode aircraft ADS-B messages at 1090 MHz. Objective 6.7.</p>
  </a>
  <a class="mt-card mt-lesson" href="L19-ais/index.html">
    <span class="mt-kind">Lesson · L19</span>
    <h4>AIS</h4>
    <p>Receive and decode AIS messages from ships. Objective 6.8.</p>
  </a>
  <a class="mt-card mt-lesson" href="L18-L19-lab-adsb-ais/index.html">
    <span class="mt-kind">L18–L19 Lab</span>
    <h4>ADS-B and AIS</h4>
    <p>Decode live ADS-B and AIS traffic. Objectives 6.7, 6.8.</p>
  </a>
</div>
::::
