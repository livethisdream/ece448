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

1. Who may transmit where: the ISM bands
2. Decibels and the Friis equation in dB
3. The noise floor and the noise figure
4. Cascaded noise figure, and where the LNA goes
5. SNR, sensitivity, and margin: a drone link end to end
6. Reading SNR off an SDR display

Note:
Six items, and items two through five are one calculation built in pieces. The drone link at the end uses all of them.

---

## Will the Link Close?

<div class="fig" data-inline-svg="./fig/L02-link-ledger.svg" style="max-width:860px; margin:0 auto;"></div>

The path takes 109.8 dB, and the signal still arrives 10.2 dB above what the receiver needs.

Note:
This is the worked example from the end of the lesson. Walk left to right: 28 dBm out of the radio, cable, antenna, then the path takes almost 110 dB. Point at the two horizontal lines: the noise floor, and the sensitivity 14 dB above it. The green bracket is the margin. Everything today is how to compute each step.

---

## Who May Transmit Where

<div class="fig" data-inline-svg="./fig/L02-ism-bands.svg" style="max-width:860px; margin:0 auto;"></div>

- The **ISM** bands allow low-power unlicensed use under FCC Part 15.
- Receiving is unrestricted; in class we transmit only when the lesson says to.

Note:
Pull up the NTIA allocation chart on the screen if there is time. Point out that nearly everything is licensed. The ISM bands are where Wi-Fi, Bluetooth, and drones live because nobody needs a license there. Note that the RTL-SDR stops short of 2.4 GHz and receives only. Make the transmit rule explicit: cable, shielded box, or very low power in an ISM band, and only when the lesson says so.

---

## Decibels

| Change | In dB |
| :-- | :-- |
| ×2 power | $+3$ dB |
| ×10 power | $+10$ dB |
| 1 mW | $0$ dBm |
| 1 W | $+30$ dBm |

Gains and losses add in dB; dBm is power relative to 1 mW, and dBi is gain relative to an isotropic antenna.

Note:
Quick drill: 630 milliwatts is about 28 dBm; 1 picowatt is minus 90 dBm. Have them do two or three in their heads.

---

## Friis in Decibels

$$P_r = P_t + G_t + G_r - L_p$$

$$L_p = 20\log_{10} d_{\text{km}} + 20\log_{10} f_{\text{MHz}} + 32.45$$

<div class="callout">The free-space path loss \(L_p\) is spreading, not absorption.</div>

Note:
Start from the linear Friis equation they saw in ECE 444 or 447, P r equals P t G t G r times lambda over four pi d squared, and take ten log of both sides. The 32.45 collects four pi over c with kilometers and megahertz. The lambda squared is there because a fixed-gain antenna has an effective area proportional to lambda squared.

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

## Antennas, Pointing, and Other Losses

- Gain applies along the main beam; at the half-power edge it is 3 dB lower.
- Each cable and connector subtracts its insertion loss.
- Below about 10 GHz the clear atmosphere adds little; rain, foliage, and walls add more.

Note:
A drone that banks puts the ground station off its antenna's beam. A budget either assumes the worst pointing or states the pointing it assumes. Near 60 GHz oxygen absorbs about 15 dB per kilometer, which is why short links use that band.

---

## The Noise Floor

$$N_\text{floor} = -174 + 10\log_{10}B + \text{NF} \quad \text{(dBm)}$$

- $kT$ at 290 K is $-174$ dBm/Hz.
- 1 MHz with NF 7 dB gives $-107.0$ dBm.
- Halving the bandwidth lowers the floor 3 dB.

Note:
Minus 174 dBm per hertz is the number to remember. Sixty dB for one megahertz takes it to minus 114, and the receiver's noise figure adds the rest. Narrowband signals such as CW reach far because their floor is low.

---

## Noise Figure

$$F = \frac{\text{SNR}\_\text{in}}{\text{SNR}\_\text{out}} \qquad \text{NF} = 10\log_{10}F$$

- Every stage lowers the SNR; NF says by how much.
- A passive loss of $L$ dB at room temperature has NF $= L$.
- A good LNA is about 1 dB; an SDR front end is several dB.

Note:
Three dB of coax lowers the SNR by three dB. A general-purpose SDR covers gigahertz of spectrum and does not have the best noise figure anywhere in it, which is why an external LNA helps a weak-signal receiver.

---

## Cascaded Noise Figure

$$F = F_1 + \frac{F_2 - 1}{G_1} + \frac{F_3 - 1}{G_1 G_2} + \cdots$$

<div class="callout">The first stage sets the floor. It should have a low noise figure and enough gain to make the rest unimportant.</div>

Note:
Use linear ratios only. All of the gain ahead of a stage divides down its excess noise. Any loss in front of the first amplifier adds to the noise figure dB for dB.

---

## Where the LNA Goes

<div class="fig" data-inline-svg="./fig/L02-noise-cascade.svg" style="max-width:860px; margin:0 auto;"></div>

The same three parts give 1.4, 4.2, or 11.0 dB; mount the LNA at the antenna.

Note:
Work the top row on the board: 1.26 plus 1 over 100 plus 5.31 over 50 is 1.38, or 1.4 dB. Then swap the cable to the front and it is 4.2 dB. Ten dB of noise figure is a factor of 3.2 in range.

---

## SNR, Sensitivity, and Margin

$$\text{SNR} = P_r - N_\text{floor}$$

$$P_\text{sens} = N_\text{floor} + \text{SNR}\_\text{req}$$

$$\text{margin} = P_r - P_\text{sens}$$

Design for about 10 dB of margin.

Note:
The required SNR comes from the modulation, which is Lesson 3. Datasheets usually quote the sensitivity directly. Ten dB of margin covers fading, pointing, weather, and a warm receiver, and it means the link would still close at about three times the distance.

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

- Lesson 3: where the required SNR comes from, the modulation's signal space
- Lesson 4: inside the SDR, where the noise figure and bandwidth are set
- Practice set: path loss, noise floor, cascade, and a GPS link budget

Note:
Before next time they should be able to compute a path loss and a noise floor in their heads to within a dB. The GPS question on the practice set deserves the most time.
