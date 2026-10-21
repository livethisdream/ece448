<!-- .slide: class="title-slide" -->

<div class="title-left">

# ECE 448

Software Defined Radios

## Lesson 2 — Noise Figure and Link Budget

Spring 2027 · Dr. Neil Rogers

</div>

<div class="title-right">

![USAFA](./img/01-course-intro/USAFA-logo.png)

</div>

---

## Where We Were

- Lesson 1: the course SDRs, the RTL-SDR, the PlutoSDR, and the HackRF
- Every signal we build or decode has to arrive strong enough to use
- Before we transmit, we can predict whether it will

Today: **a link budget** adds every gain and loss between two radios and compares the result to the noise floor.

Note:
Open with the question every radio engineer asks first: will the link close? Today is the arithmetic that answers it, and we will use it in every lab this semester.

---

## Today's Plan

1. The allocated spectrum and the ISM bands
2. The Friis equation, in watts and in dB
3. Antennas: gain, beamwidth, and orientation
4. Noise: SNR, noise figure, the cascade, and the noise floor
5. SNR, sensitivity, and margin: a drone link end to end
6. Reading SNR off an SDR display

Note:
The same order as the 2025 slides. Items two through five are one calculation built in pieces, and the drone link at the end uses all of them.

---

## Will the Link Close?

<div class="fig" data-inline-svg="./fig/L02-link-ledger.svg" style="max-width:860px; margin:0 auto;"></div>

The path takes 109.8 dB, and the signal still arrives 10.2 dB above what the receiver needs.

Note:
This is the worked example from the end of the lesson. Walk left to right: 28 dBm out of the radio, cable, antenna, then the path takes almost 110 dB. Point at the two horizontal lines: the noise floor, and the sensitivity 14 dB above it. The green bracket is the margin. Everything today is how to compute each step.

---

## The Spectrum Is Allocated

<img src="./img/02-link-budget/L02-us-allocation-chart.png" alt="The US frequency allocation chart, 3 kHz to 300 GHz" style="max-height:520px; display:block; margin:0 auto;">

Every band has assigned services, and most bands are shared.

Note:
This is the 2003 edition; NTIA posts the current one. Let them look for a minute and pick out a band they use every day: broadcast FM near 100 MHz, cellular, GPS at 1575 MHz. The point is density: almost nothing is empty, which is why so much of this course is about finding and separating signals.

---

## Who May Transmit Where

<div class="fig" data-inline-svg="./fig/L02-ism-bands.svg" style="max-width:860px; margin:0 auto;"></div>

- The **ISM** bands allow low-power unlicensed use under FCC Part 15.
- Receiving is unrestricted; in class we transmit only when the lesson says to.

Note:
Pull up the NTIA allocation chart on the screen if there is time. Point out that nearly everything is licensed. The ISM bands are where Wi-Fi, Bluetooth, and drones live because nobody needs a license there. Note that the RTL-SDR stops short of 2.4 GHz and receives only. Make the transmit rule explicit: cable, shielded box, or very low power in an ISM band, and only when the lesson says so.

---

## The Friis Equation

$$P_r = \frac{P_t\ G_t\ G_r\ \lambda^2}{(4\pi R)^2}$$

- Line of sight: always check first!
- Then power, antenna gains, wavelength, and distance.

Note:
Build the equation one factor at a time, as in the 2025 slides: power transmitted, then the gains, then wavelength, then distance. The 4 pi R squared is spreading over a sphere; the lambda squared is there because a fixed-gain antenna has an effective area proportional to lambda squared.

---

## Decibels

| Parameter | Linear | dB |
| :-- | :-- | :-- |
| $P_t$ | 120 W | $50.8$ dBm |
| $G_t$ | 1201.2 | $30.8$ dB |
| $G_r$ | 281.5 | $24.5$ dB |

Products become sums in dB: $\times 2$ is $+3$ dB, 1 mW is 0 dBm, 1 W is $+30$ dBm.

Note:
Have them convert the table before revealing the dB column. dBm is relative to 1 mW and dBi is gain relative to an isotropic antenna.

---

## Friis in Decibels

$$P_r = P_t + G_t + G_r - L_p$$

$$L_p = 20\log_{10} f_\text{Hz} + 20\log_{10} R_\text{m} - 147.55$$

At 3.7 GHz over 80 km: $L_p = 141.9$ dB, so $P_r = 50.8 + 30.8 + 24.5 - 141.9 = -35.8$ dBm.

Note:
The minus 147.55 is twenty log of four pi over c, with frequency in hertz and distance in meters. The path loss is spreading, not absorption.

---

## Path Loss Rules of Thumb

| 3 km at | Path loss |
| :-- | :-- |
| 915 MHz | 101.2 dB |
| 2.45 GHz | 109.8 dB |
| 5.8 GHz | 117.3 dB |

- Doubling the distance adds 6 dB of path loss.
- Doubling the frequency adds 6 dB with fixed-gain antennas.

Note:
The 6 dB rule runs in reverse: 6 dB of margin means the link still closes at twice the distance. This is why long-range telemetry uses 915 MHz.

---

## Antennas

- **Gain** is directivity times efficiency, in dBi.
- At the half-power **beamwidth** edge the gain is 3 dB lower.
- Orientation matters: a banking drone points its beam away.
- Each cable and connector subtracts its insertion loss.

Note:
Show the antenna types and the gain pattern from the 2025 slides if there is time. A budget either assumes the worst orientation or states the one it assumes.

---

## SNR and Noise Figure

$$\text{SNR} = \frac{P_\text{sig}}{P_\text{noise}} \qquad \text{NF} = 10\log_{10}\frac{\text{SNR}\_\text{in}}{\text{SNR}\_\text{out}}$$

- Every stage lowers the SNR; NF says by how many dB.
- Typical receivers: 2 to 8 dB. A good LNA is about 1 dB.

Note:
SNR is the one noise number this course uses. A passive loss at room temperature has a noise figure equal to its loss: three dB of coax lowers the SNR by three dB.

---

## Cascaded Noise Figure

$$F = F_1 + \frac{F_2 - 1}{G_1} + \frac{F_3 - 1}{G_1 G_2} + \cdots$$

<div class="callout">The first stage sets the floor. It should have a low noise figure and enough gain to make the rest unimportant.</div>

Note:
Use linear ratios. All of the gain ahead of a stage divides down its extra noise. Any loss in front of the first amplifier adds to the noise figure dB for dB.

---

## Where the LNA Goes

<div class="fig" data-inline-svg="./fig/L02-noise-cascade.svg" style="max-width:860px; margin:0 auto;"></div>

The same three parts give 1.4, 4.2, or 11.0 dB; mount the LNA at the antenna.

Note:
Read the three rows off the figure; no need to work the arithmetic on the board. Ten dB of noise figure is a factor of 3.2 in range.

---

## Noise Sources and the Noise Floor

$$N_\text{floor} = -174 + 10\log_{10}B + \text{NF} \quad \text{(dBm)}$$

- Thermal and shot noise give $kTB$: $-174$ dBm/Hz at 290 K.
- 1 MHz with NF 7 dB gives $-107.0$ dBm.
- Halving the bandwidth lowers the floor 3 dB.

Note:
Minus 174 dBm per hertz is the number to remember. Sixty dB for one megahertz takes it to minus 114, and the noise figure adds the rest. Other sources, generation-recombination, temperature fluctuation, and quantum noise, add smaller amounts.

---

## The Atmosphere

- Below about 10 GHz the clear atmosphere adds little.
- Water vapor and rain add loss above that; oxygen absorbs strongly near 60 GHz.
- Foliage and walls add loss at any frequency.

Note:
Show the atmospheric attenuation chart from the 2025 slides. Every band our SDRs reach is below 10 GHz. Near 60 GHz oxygen absorbs about 15 dB per kilometer.

---

## SNR, Sensitivity, and Margin

$$\text{SNR} = P_r - N_\text{floor}$$

$$P_\text{sens} = N_\text{floor} + \text{SNR}\_\text{req}$$

$$\text{margin} = P_r - P_\text{sens}$$

Design for about 10 dB of margin.

Note:
The required SNR comes from the radio's datasheet, which usually quotes the sensitivity directly. Ten dB of margin covers fading, pointing, weather, and a warm receiver, and it means the link would still close at about three times the distance.

---

## Worked Example: A Drone Link

| Quantity | Work | Result |
| :-- | :-- | :-- |
| EIRP | $28.0 - 1.5 + 4.0$ | $30.5$ dBm |
| Path loss | 3 km at 2.45 GHz | $109.8$ dB |
| Received | $30.5 - 109.8 - 3.5$ | $-82.8$ dBm |
| Floor | $-174 + 60 + 7$ | $-107.0$ dBm |
| Margin | $24.2 - 14$ | $10.2$ dB |

Note:
630 mW into a 4 dBi antenna, a 1 dBi ground antenna, 1.5 dB of cable on each side, and 3 dB of pointing loss when the drone banks. 1 MHz, NF 7 dB, and the modem needs 14 dB. The 3.5 in the received line is pointing, receive antenna, and receive cable together. With 10.2 dB of margin the link would reach about 9.7 km.

---

<!-- .slide: class="viz-cue-slide" -->

## Link Budget Explorer

- Drag the distance from 3 km to 6 km: the margin drops 6.0 dB.
- Raise the bandwidth to 20 MHz: the floor rises 13 dB.
- The GPS preset arrives about 18 dB below the floor.

<p class="viz-cue">↗ Interactive on the lesson page</p>

Note:
Demo live from the lesson page. Start on the drone preset, double the distance, then widen the bandwidth. Then load GPS: the signal is below the noise floor, and the receiver still works because correlating against the known code recovers about 30 dB. That is spread spectrum, and we will see its cousin, frequency hopping, in Lesson 16.

---

## Reading SNR on an SDR

- The spectrum display reads in dBFS, relative to full scale, not dBm.
- SNR is a difference, so read the peak and the floor.
- Each FFT bin holds $f_s/N$ Hz of noise; doubling $N$ lowers the displayed floor 3 dB.

Note:
Converting dBFS to dBm takes a calibrated source, but an SNR does not need one. The display shows the SNR in one bin. To get the SNR the demodulator sees, scale the floor up to the signal's bandwidth. We will do this on real captures from Lesson 5 on.

---

## Key Point

<div class="callout">A link closes when the received power clears the noise floor by the SNR the receiver needs. Path loss sets the size of the problem, and the first stage of the receiver sets the floor.</div>

Note:
If they remember one formula, it is minus 174 plus ten log B plus NF.

---

## Looking Ahead

- Lesson 3: what a digital signal looks like as the SNR falls
- Lesson 4: inside the SDR, where the noise figure and bandwidth are set
- Practice set: path loss, noise floor, cascade, and a GPS link budget

Note:
Before next time they should be able to compute a path loss and a noise floor in their heads to within a dB. The GPS question on the practice set is the 2025 homework, and it deserves the most time.
