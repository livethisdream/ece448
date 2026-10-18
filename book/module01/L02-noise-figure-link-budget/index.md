---
frame_view: true
---

# L2 - Noise Figure and Link Budget

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">Noise Figure and Link Budget</h1>

<div class="title-rule"></div>

A link budget adds every gain and loss between two radios and compares the result to the noise floor.

Lesson 2 · Module 1: Foundations of Detection & Link Budgets · Dr. Neil Rogers
::::

::::{frame} Slides
:class: read-only

:::{admonition} Slides
:class: slides
<a href="../../slides/L02-noise-figure-link-budget.html" target="_blank" rel="noopener">html slides</a>
<a href="../../slides/L02-noise-figure-link-budget.html?print-pdf" target="_blank" rel="noopener">pdf slides</a>
<a href="../../slides/L02-noise-figure-link-budget.md" target="_blank" rel="noopener">raw markdown slides</a>
:::
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '1'">
  <li>I can define noise figure and cascade it through a receiver chain to predict system noise performance.</li>
  <li>I can compute a link budget and predict received SNR for a specified geometry, transmitter, and antenna configuration.</li>
</ol>
::::

::::{frame} Will the Link Close?
:::{present}
- A **link budget** follows the signal level from the transmitter to the receiver, in dB.
- The link **closes** when the received power clears the noise floor by the SNR the modem needs.
- The extra above that is the **margin**.
:::
:::{present}
<img src="../../viz/img/L02-link-ledger.svg"
     alt="Level diagram of a 2.45 GHz drone link: 28.0 dBm leaves the transmitter, the 3 km path removes 109.8 dB, and minus 82.8 dBm reaches the receiver, 10.2 dB above the minus 93.0 dBm sensitivity and 24.2 dB above the minus 107.0 dBm noise floor"
     style="max-width: 720px; width: 100%; display: block; margin: 0 auto;">
:::

Lesson 1 introduced the radios we will use all semester. Before we build anything with them, we need a way to answer the first question of any wireless design: will the signal arrive strong enough to decode? A **link budget** answers it. We start with the transmitter power, add every gain and subtract every loss between the two antennas, and compare what arrives with the receiver's **noise floor**. If the received power clears the floor by the signal-to-noise ratio (SNR) the demodulator needs, the link **closes**, and whatever is left over is the **margin**.

The figure is the worked example at the end of this lesson, a 2.45 GHz drone link over 3 km. The path takes almost 110 dB, far more than every other entry combined, and the signal still arrives 10.2 dB above what the receiver needs. Every number on it is something we can look up, measure, or compute, and that is the point of the method: a link budget turns "will it work?" into arithmetic we can check before we transmit.
::::

::::{frame} Part 1: The Spectrum Is Allocated
:::{present}
<img src="../../viz/img/L02-us-allocation-chart.png"
     alt="The US frequency allocation chart: every band from 3 kHz to 300 GHz drawn as a colored bar for its assigned services, such as broadcasting, mobile, fixed, aeronautical, maritime, radar, amateur, and satellite"
     style="max-width: 900px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- Every band from 3 kHz to 300 GHz has assigned services.
- Each color is one service; most bands carry several.
:::

The chart shows every allocation in the United States, from 3 kHz at the top left to 300 GHz at the bottom right, with each colored block a service such as broadcasting, mobile, aeronautical navigation, or radar. The version here is the 2003 edition; the current edition and its legend are on the <a href="https://www.ntia.gov/page/united-states-frequency-allocation-chart" target="_blank" rel="noopener">NTIA allocation chart page</a>. Two things stand out. Almost no band is empty, and most bands are shared by several services. That density is why so much of this course is about finding, identifying, and separating signals rather than generating them.
::::

::::{frame} Who May Transmit Where
:::{present}
- The FCC allocates every band; most require a license.
- The **ISM** bands (915 MHz, 2.4 GHz, 5.8 GHz) allow low-power unlicensed use, which is why Wi-Fi, Bluetooth, and most drones live there.
- Receiving is unrestricted; transmitting is not.
:::
:::{present}
<img src="../../viz/img/L02-ism-bands.svg"
     alt="The US ISM bands at 6.78, 13.56, 27.12, and 40.68 MHz and at 915, 2450, and 5800 MHz on a log frequency axis, with the tuning ranges of the RTL-SDR, 24 MHz to 1.766 GHz, the PlutoSDR, 325 MHz to 3.8 GHz, and the HackRF One, 1 MHz to 6 GHz"
     style="max-width: 720px; width: 100%; display: block; margin: 0 auto;">
:::

In the United States the FCC (and the NTIA, for federal users) allocates the radio spectrum, and the allocation chart shows who holds each band. Almost all of it requires a license to transmit. The exceptions that matter most in this course are the **industrial, scientific, and medical (ISM)** bands. Part 15 of the FCC rules lets anyone transmit there at low power without a license, provided they accept interference from everyone else, and that is why Wi-Fi, Bluetooth, garage-door openers, and most hobby drones share 915 MHz, 2.4 GHz, and 5.8 GHz.

Two rules govern what we do with the SDRs. Receiving is unrestricted: we can tune anywhere the hardware reaches and look at whatever is there, which is most of this course. Transmitting is not: in class we transmit only into a cable, into a shielded enclosure, or at very low power in an ISM band, and only when the lesson says to. The figure shows where the ISM bands fall against the tuning range of each course SDR. The RTL-SDR receives only, and it reaches 915 MHz but not 2.4 GHz; the PlutoSDR and the HackRF cover all three of the common ISM bands.
::::

::::{frame} Decibels
:::{present}
| Change | In dB |
| :-- | :-- |
| ×2 power | $+3$ dB |
| ×10 power | $+10$ dB |
| 1 mW | $0$ dBm |
| 1 W | $+30$ dBm |
:::
:::{present}
- Gains and losses add in dB.
- dBm is power relative to 1 mW; dBi is gain relative to an isotropic antenna.
:::

A link budget multiplies a long chain of gains and losses, and the numbers span many orders of magnitude: a transmitter puts out a watt, and the receiver collects a few picowatts. Decibels turn those products into sums and keep the numbers readable. A power ratio $P_2/P_1$ in decibels is

$$\text{dB} = 10\log_{10}\frac{P_2}{P_1}$$

An absolute power takes a reference: **dBm** is power relative to 1 mW, so 630 mW is $10\log_{10}(630) = 28.0$ dBm and 1 pW is $-90$ dBm. **dBi** is antenna gain relative to an isotropic antenna. With every quantity in dB, a received power is the transmitter power plus the gains minus the losses, and we can do most link budgets in our heads. The four rows of the table are worth memorizing: a factor of two is 3 dB, a factor of ten is 10 dB, and 0 dBm and $+30$ dBm are 1 mW and 1 W.
::::

::::{frame} Part 2: Friis in Decibels
:::{present}
$$P_r = P_t + G_t + G_r - L_p$$

$$\begin{aligned}
L_p &= 20\log_{10}\frac{4\pi d}{\lambda} \\
&= 20\log_{10} d_{\text{km}} + 20\log_{10} f_{\text{MHz}} + 32.45
\end{aligned}$$

- $L_p$ is the **free-space path loss** in dB.
:::

The Friis transmission equation gives the power one antenna collects from another in free space:

$$P_r = P_t\ G_t\ G_r \left(\frac{\lambda}{4\pi d}\right)^2$$

with $P_t$ the transmitted power, $G_t$ and $G_r$ the antenna gains, $d$ the distance, and $\lambda$ the wavelength. Taking $10\log_{10}$ of both sides turns the product into the sum on the slide, with the last factor collected into the **free-space path loss** $L_p$. Writing $\lambda = c/f$ and putting the distance in kilometers and the frequency in megahertz collects every constant into the 32.45 dB term, which is the form to use with a calculator.

Free-space path loss is not absorption. The energy spreads over a sphere that grows as $d^2$, and the receiving antenna captures a fixed area of it. The $\lambda^2$ appears because a fixed-gain antenna has an effective area proportional to $\lambda^2$, so the same 1 dBi antenna collects less power at a higher frequency.
::::

::::{frame} Path Loss Rules of Thumb
:::{present}
- Doubling the distance adds 6 dB of path loss.
- Doubling the frequency adds 6 dB with fixed-gain antennas.

| 3 km at | Path loss |
| :-- | :-- |
| 915 MHz | 101.2 dB |
| 2.45 GHz | 109.8 dB |
| 5.8 GHz | 117.3 dB |
:::

Path loss grows as $20\log_{10} d$, so every doubling of distance adds $20\log_{10}2 = 6.0$ dB, and every factor of ten adds 20 dB. The frequency term behaves the same way. That is why a 915 MHz telemetry radio outranges a 2.4 GHz radio at the same power and antenna gain: at 3 km the 915 MHz link loses 8.6 dB less, which is a factor of 2.7 in distance for the same received power.

The 6 dB rule also runs in reverse. If a link has 6 dB of margin, it will still close at twice the distance, with nothing left over. If it has 12 dB, it reaches four times as far. We will use that to read the range of a link straight off its margin.
::::

::::{frame} Antennas, Pointing, and Other Losses
:::{present}
- Antenna gain applies only along the main beam; at the half-power edge it is 3 dB lower.
- Each cable and connector subtracts its insertion loss.
- Below about 10 GHz the clear atmosphere adds little; rain and foliage add more.
:::

The gain on a datasheet is the peak gain, along the antenna's main beam. A directional antenna pointed away from the other end of the link delivers less: at the edge of the half-power beamwidth it delivers 3 dB less by definition, and in a null it delivers almost nothing. A drone that banks, a handheld radio held sideways, or two linear antennas at right angles to each other can each lose several dB. A budget either assumes worst-case pointing or states the pointing it assumes.

Every cable, connector, filter, and switch between the radio and its antenna subtracts its **insertion loss**. A few meters of thin coax at 2.4 GHz loses a dB or more, which is why cable length belongs in the budget.

The atmosphere is nearly transparent below about 10 GHz. Above that, water vapor and rain add loss, and near 60 GHz oxygen absorbs about 15 dB/km at sea level (ITU-R P.676). Foliage, walls, and people in the path add loss at any frequency, and an indoor Wi-Fi budget can lose 10 dB or more through a couple of walls. These losses are hard to predict exactly, which is one reason a link budget carries margin.
::::

::::{frame} Part 3: The Noise Floor
:::{present}
$$N = kTB \quad\Rightarrow\quad -174\ \text{dBm/Hz at 290 K}$$

$$N_\text{floor} = -174 + 10\log_{10}B + \text{NF} \quad \text{(dBm)}$$

- 1 MHz with NF 7 dB gives $-107.0$ dBm.
:::

Every resistor at temperature $T$ produces thermal noise power $kTB$ in a bandwidth $B$, where $k = 1.38\times10^{-23}$ J/K is Boltzmann's constant. At the standard reference temperature of 290 K that is $4.0\times10^{-21}$ W in each hertz, or $-174$ dBm/Hz, and it is the number to remember. The noise a receiver sees grows with the bandwidth it lets through, so a receiver that uses 1 MHz starts from $-174 + 60 = -114$ dBm.

A real receiver adds noise of its own on top of that, and its **noise figure** NF measures how much, in dB. The receiver's noise floor is the sum of the three terms on the slide. For the drone link, 1 MHz of bandwidth and a 7 dB noise figure put the floor at $-107.0$ dBm. Two consequences follow. Narrowing the bandwidth lowers the floor, 3 dB for every halving, and that is one reason narrowband signals such as CW and FSK reach so far. And a lower noise figure lowers the floor dB for dB, which is the job of a low-noise amplifier.
::::

::::{frame} Noise Figure
:::{present}
$$F = \frac{\text{SNR}_\text{in}}{\text{SNR}_\text{out}} \qquad \text{NF} = 10\log_{10}F$$

- Every stage lowers the SNR; NF says by how much.
- A passive loss of $L$ dB at room temperature has $\text{NF} = L$.
- A good LNA is about 1 dB; an SDR front end is several dB.
:::

The **noise factor** $F$ is the ratio of the SNR at a stage's input to the SNR at its output, and the **noise figure** is the same ratio in dB. A perfect, noiseless stage has $F = 1$ and NF $= 0$ dB. Every real stage adds some noise, so the SNR always gets worse through it, and NF states by how many dB.

Two cases are worth knowing by heart. A passive loss at room temperature, a cable or a filter, has a noise figure equal to its loss: 3 dB of coax lowers the SNR by 3 dB. A **low-noise amplifier (LNA)** is built to add as little noise as possible while it raises the signal, and a good one has a noise figure near 1 dB. The front end of a general-purpose SDR trades noise performance for frequency coverage and usually lands at several dB, which is why an external LNA often improves a weak-signal receiver.
::::

::::{frame} Cascaded Noise Figure
:::{present}
$$F = F_1 + \frac{F_2 - 1}{G_1} + \frac{F_3 - 1}{G_1 G_2} + \cdots$$

- The gain ahead of each stage divides down its noise.
- The first stage sets the floor, so it should have low NF and high gain.
:::

A receiver is a chain of stages, and the Friis formula for noise combines their noise factors $F_n$ and linear gains $G_n$ into the noise factor of the whole chain. The terms must be linear ratios, not dB, so convert before adding. Each stage after the first contributes its excess noise $F_n - 1$ divided by all of the gain ahead of it. Behind a 20 dB LNA, a stage's excess noise counts one hundred times less than it would at the antenna.

The design rule follows directly. The first stage dominates the noise figure of the whole receiver, so it should be a low-noise stage with enough gain to make everything after it unimportant. Any loss in front of that stage adds to the system noise figure dB for dB, because nothing ahead of it divides it down.
::::

::::{frame} Where the LNA Goes
:::{present}
<img src="../../viz/img/L02-noise-cascade.svg"
     alt="The same LNA, 3 dB cable, and SDR in three arrangements. With the LNA at the antenna the system noise figure is 1.4 dB; with the cable ahead of the LNA it is 4.2 dB; with no LNA it is 11.0 dB"
     style="max-width: 720px; width: 100%; display: block; margin: 0 auto;">
:::
:::{present}
- The same three parts give 1.4, 4.2, or 11.0 dB.
- Mount the LNA at the antenna, ahead of the cable.
:::

:::{admonition} Worked example — the LNA at the antenna
:class: tip
An LNA with NF 1 dB and 20 dB of gain, a coax run with 3 dB of loss, and an SDR with NF 8 dB. In linear terms the LNA is $F_1 = 1.26$, $G_1 = 100$; the cable is $F_2 = 2.00$, $G_2 = 0.50$; the SDR is $F_3 = 6.31$.

$$\begin{aligned}
F &= 1.26 + \frac{2.00 - 1}{100} + \frac{6.31 - 1}{100 \times 0.50} \\
&= 1.26 + 0.01 + 0.11 = 1.38
\end{aligned}$$

which is NF $= 1.4$ dB. With the cable first, the cable's 3 dB sits in front of everything and the LNA's gain cannot divide it down:

$$\begin{aligned}
F &= 2.00 + \frac{1.26 - 1}{0.50} + \frac{6.31 - 1}{0.50 \times 100} \\
&= 2.00 + 0.52 + 0.11 = 2.62
\end{aligned}$$

which is NF $= 4.2$ dB. Without the LNA the cable and the SDR alone give 11.0 dB. The same three parts span almost 10 dB of noise figure, and 10 dB of noise floor is a factor of $\sqrt{10} = 3.2$ in range.
:::
::::

::::{frame} Part 4: SNR and Margin
:::{present}
$$\begin{aligned}
\text{SNR} &= P_r - N_\text{floor} \\
P_\text{sens} &= N_\text{floor} + \text{SNR}_\text{req} \\
\text{margin} &= P_r - P_\text{sens}
\end{aligned}$$

- Design for about 10 dB of margin.
:::

The received SNR is the received power minus the noise floor, both in dBm. The demodulator needs some minimum SNR to deliver an acceptable error rate, and Lesson 3 shows how that requirement follows from the modulation. Adding it to the floor gives the receiver's **sensitivity**, the weakest signal it can use, which radio datasheets usually quote directly. The **margin** is how far the received power sits above the sensitivity.

A link with 0 dB of margin works only on a good day. Fading, a bad antenna angle, a wet radome, or a warmer receiver all take a few dB at unpredictable times, so a typical design goal is about 10 dB of margin. Because path loss grows 6 dB per doubling of distance, 10 dB of margin also says the link would close, with nothing to spare, at about three times the distance.
::::

::::{frame} Worked Example: A Drone Link
:::{present}
| Step | Result |
| :-- | :-- |
| EIRP | $30.5$ dBm |
| Path loss, 3 km | $109.8$ dB |
| Received | $-82.8$ dBm |
| Floor, 1 MHz | $-107.0$ dBm |
| Margin | $10.2$ dB |
:::
:::{present}
- The radio needs 14 dB of SNR, so its sensitivity is $-93.0$ dBm.
:::

:::{admonition} Worked example — a 2.45 GHz drone link
:class: tip
A drone's 2.45 GHz telemetry radio transmits 630 mW into a 4 dBi antenna, and the ground station uses a 1 dBi antenna at up to 3 km. Each side has 1.5 dB of cable and connector loss, and the drone may bank until the ground station sits at the edge of its antenna's half-power beamwidth, a 3 dB pointing loss. The radio uses 1 MHz of bandwidth, has a 7 dB noise figure, and needs 14 dB of SNR.

| Quantity | Work | Result |
| :-- | :-- | :-- |
| Transmit power | $10\log_{10}(630)$ | $28.0$ dBm |
| EIRP | $28.0 - 1.5 + 4.0$ | $30.5$ dBm |
| Path loss | $20\log_{10}3 + 20\log_{10}2450 + 32.45$ | $109.8$ dB |
| Received | $30.5 - 109.8 - 3.0 + 1.0 - 1.5$ | $-82.8$ dBm |
| Noise floor | $-174 + 10\log_{10}(10^6) + 7$ | $-107.0$ dBm |
| SNR | $-82.8 - (-107.0)$ | $24.2$ dB |
| Sensitivity | $-107.0 + 14$ | $-93.0$ dBm |
| Margin | $-82.8 - (-93.0)$ | $10.2$ dB |

The link meets the 10 dB goal. The effective isotropic radiated power, **EIRP**, is the transmit power plus the antenna gain minus the transmit-side losses, the power an isotropic antenna would need to produce the same signal along the beam; regulators limit it in the ISM bands. With all 10.2 dB used, the range could stretch by $10^{10.2/20} = 3.2$ times, to about 9.7 km, before the link fails.
:::
::::

::::{frame} Link Budget Explorer
:class: viz-frame

:::{depth}
The widget starts on the drone link above. The four steps are the transmitter, the EIRP after the transmit antenna, the level after the path, and the receiver input after the remaining losses; the dashed red line is the noise floor and the dotted line is the sensitivity. Drag the distance to 6 km and watch the margin drop by 6.0 dB. Raise the bandwidth to 20 MHz and watch the floor rise by 13 dB, so a wideband link loses range for the same power. Then try the two other presets. The Wi-Fi link loses 10 dB to walls and needs 25 dB of SNR for a fast modulation, so it has little margin even at 50 m. The GPS link arrives about 18 dB *below* the noise floor; a GPS receiver still works because it correlates the signal against a known 1023-chip code, which recovers about 30 dB.
:::

:::{present}
<iframe src="../../viz/link-budget.html"
        width="100%" height="484"
        style="border: 1px solid #cddce9; border-radius: 6px;"
        loading="lazy"
        title="Link budget explorer: transmitter power, frequency, distance, antenna gains, losses, bandwidth, noise figure, and required SNR, with the level diagram, the noise floor, and the margin">
</iframe>
:::
::::

::::{frame} Reading SNR on an SDR
:::{present}
- An SDR spectrum display reads in dBFS, relative to full scale, not dBm.
- SNR is a difference, so read the peak and the floor.
- Each FFT bin holds $f_s/N$ Hz of noise; doubling $N$ lowers the floor 3 dB.
:::

From Lesson 5 on we will read signals off the GNU Radio frequency sink. Its vertical axis is in **dBFS**, decibels relative to the full scale of the analog-to-digital converter, not in dBm. Turning dBFS into dBm takes a calibration against a known source, but an SNR does not need one: it is the difference between two levels on the same axis, so the peak minus the floor gives it directly.

The bandwidth needs one more step. A spectrum display with an $N$-point FFT at sample rate $f_s$ splits the band into bins $f_s/N$ wide, and each bin holds only that much of the noise. A narrow tone puts all of its power in one bin, so doubling the FFT size lowers the displayed noise floor by 3 dB and leaves the tone where it was. The SNR read off the display is the SNR in one bin, not in the signal's full bandwidth. To find the SNR the demodulator sees, scale the floor to the signal bandwidth $B$ by adding $10\log_{10}(B N/f_s)$ dB to it.
::::

::::{frame} Key Point
:::{present}
:class: callout
A link closes when the received power clears the noise floor by the SNR the receiver needs. Path loss sets the size of the problem, and the first stage of the receiver sets the floor.
:::
::::

::::{frame} Summary
:class: read-only

| Idea | What it is | Number to remember |
| :-- | :-- | :-- |
| Path loss | $20\log_{10}(4\pi d/\lambda)$ | $+6$ dB per doubling of $d$ or $f$ |
| Thermal noise | $kTB$ at 290 K | $-174$ dBm/Hz |
| Noise floor | $-174 + 10\log_{10}B + \text{NF}$ | $-114$ dBm in 1 MHz before NF |
| Noise figure | $\text{SNR}_\text{in}/\text{SNR}_\text{out}$ in dB | LNA about 1 dB; passive loss NF $=$ loss |
| Cascade | $F_1 + (F_2 - 1)/G_1 + \cdots$ | the first stage dominates |
| Sensitivity | floor $+$ required SNR | from the datasheet or the modulation |
| Margin | received $-$ sensitivity | design for about 10 dB |
::::

::::{frame} Practice
:class: read-only doc-links

- <a class="doc-link" href="../../practice/ECE448_L02_Practice_blank.pdf" target="_blank" rel="noopener">Problem set (PDF)</a>
- <a class="doc-link doc-key" href="../../practice/ECE448_L02_Practice_SOLUTIONS.pdf" target="_blank" rel="noopener">Solutions (PDF)</a>
::::

::::{frame} Looking Ahead
:::{present}
- Lesson 3 shows where the required SNR comes from: the modulation's signal space.
- Lesson 4 opens the SDR and its front end, where the noise figure is set.
:::

Today we took the receiver's required SNR as a given, the 14 dB in the drone example. Lesson 3 explains where it comes from. A modulation places its symbols at points in a signal space, and the noise floor we computed today spreads each received symbol into a cloud around its point; the SNR a modem needs is whatever keeps those clouds from overlapping too often.

Lesson 4 then opens the SDRs themselves: the RF front end, the mixer and filters, and the analog-to-digital converter, which together set the noise figure, the bandwidth, and the dynamic range we used in today's budget. Before the next lesson, be able to compute a free-space path loss and a noise floor in your head to within a dB, because every lab in this course starts by checking that the signal will be there to receive.
::::
