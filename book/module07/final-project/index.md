---
frame_view: true
---

# Final Project

::::{frame}
:class: title-frame

<div class="course-mark">ECE 448 · Spring 2027</div>

<h1 class="frame-title">Final Project</h1>

<div class="title-rule"></div>

A self-defined SDR project: proposal, background research, design, prototype, then a report and live demonstration.

Module 7: Final Project · Dr. Neil Rogers
::::

::::{frame} Learning Objectives

<ol class="lo-list" style="--module: '7'; counter-reset: lo 1">
  <li>I can define the scope, objectives, and measurable success criteria for a self-directed SDR project.</li>
  <li>I can research, design, and implement a wireless communication system using an SDR and GNU Radio.</li>
  <li>I can present my project results in a professional-grade report and live demonstration and defend engineering trade-offs against my own stated success criteria.</li>
</ol>
::::

::::{frame} Your Project
:::{present}
- You choose a project that uses your PlutoSDR, built in GNU Radio.
- It is 40% of your final grade.
- Five milestones build toward a final report and a live demonstration on the last lesson day.
:::

The final project is yours to define. You pick a wireless problem, decide what success looks like, and build it with your PlutoSDR and GNU Radio. The receiver, transmitter, or decoder at the center of the project is a flowgraph you build; other software can help around it, such as a script that plots your results. The project is 40% of your final grade. It ends with a final report and a presentation with a live demonstration on the last lesson day, and each milestone before that writes one section of the report.
::::

::::{frame} Five Milestones
:::{present}
| Milestone | Objective |
| :-- | :-- |
| 1. Proposal | 7.2 |
| 2. Background Research | 7.3 |
| 3. Design Description | 7.3 |
| 4. Prototype Update | 7.3 |
| 5. Final Report and Presentation | 7.4 |
:::

The milestones come in this order, each due on the date the course schedule gives. The proposal sets your scope and success criteria (objective 7.2). The next three research, design, and build the system (7.3). The final report and presentation show what you built and defend it against the criteria you wrote in the proposal (7.4). Each milestone feeds the next, so I return feedback on one before the next is due.
::::

::::{frame} Proposal
:::{present}
- What do you want to do, and why is it interesting and reasonable?
- A short review of what others have done.
- Your end goal, and your A-, B-, and C-level outcomes.
- Your next steps.
:::

The proposal answers four questions. **What** do you want to build, and why is it interesting and reasonable to finish in one semester with one Pluto? **What has been done**: a short first look at others' work, enough to show the idea is feasible. **What is the end goal**, stated as levels of accomplishment. **What comes next**: the first things you will build or read.
::::

::::{frame} Success Levels
:::{present}
| Level | ADS-B generator, for example |
| :-- | :-- |
| C | gr-adsb decodes my frames from a SigMF recording. |
| B | It decodes them sent at 915 MHz by cable. |
| A | It decodes them over the air at low power, with positions plotted. |
:::

Your **success levels** are the criteria I grade your final report against, so write each one as something a demonstration can show is done or not done. The example is an ADS-B generator. Its C level works entirely in a recording, its B level adds the radio through a cable, and its A level adds the air. "Decodes my frames" is measurable; "works well" is not. A C level you are sure to reach and an A level that stretches you make the best proposal.
::::

::::{frame} Background Research
:::{present}
- At least four high-quality, relevant papers, blogs, or references.
- What each one did, and how it relates to your project.
- What you will use from each as a building block.
- Your next steps.
:::

Find the work your project stands on: papers, GNU Radio wiki pages and out-of-tree modules, PySDR chapters, and well-documented blog projects. For each source, summarize what its authors did, explain how it relates to your project, and name what you will use from it, such as a block, a parameter, a frame format, or a test method. Close with your next steps.
::::

::::{frame} Design Description
:::{present}
- What you will build: the subsystems and the blocks in each.
- Your unanswered questions and expected sticking points.
- How you will test and verify each level.
- Your next steps.
:::

The design description turns the proposal into a plan. Draw the system as subsystems, such as source, channel, demodulator, and decoder, and name the GNU Radio blocks, out-of-tree modules, and hardware each one uses. List the questions you cannot answer yet and the places you expect to get stuck, so we can talk about them early. Then say how you will test each success level: the recording, flowgraph display, or measurement that shows it is met.
::::

::::{frame} Prototype Update
:::{present}
- Where your design, test, and build stand.
- How you are doing against your proposal's levels.
- What changed in the design, and why.
- Your next steps.
:::

The prototype update reports what works so far. Show the flowgraphs you have built and the results they give, with screenshots or SigMF recordings, and say which success levels you have met. If the design changed, say what changed and why. Close with your plan to finish.
::::

::::{frame} Final Report and Presentation
:::{present}
- What you accomplished, and what you did not.
- Confirmation that it works: the demonstration and its evidence.
- Lessons learned and future work.
- An IEEE-quality report and a five-minute presentation with a live demonstration.
:::

The final report brings the four earlier milestones together. Say what you accomplished and what you did not, measured against your own success levels. Confirm the functionality with evidence: the live demonstration, screenshots, and the recordings and flowgraphs that produced them. Close with the lessons you learned and the work you would do next. The report is IEEE quality, typically 7 to 10 pages. The presentation is five minutes and includes the live demonstration.
::::

::::{frame} Defending Your Trade-Offs
:::{present}
- Grade yourself against your own A, B, and C levels.
- For each design choice, say what you gave up and why.
- A level you missed, explained with evidence, still shows engineering.
:::

Objective 7.4 asks you to **defend your trade-offs**. Every design gives something up: a lower sample rate lets the Pluto stream without dropping samples but narrows the band you see, and a cable makes a link reliable but leaves out the air. For each choice, state what you chose, what you gave up, and how the result compares with the level you set. A missed A level, with a clear account of what limited it, still meets the objective.
::::

::::{frame} Transmitting Safely
:::{present}
- Receive anything in the Pluto's range: 70 MHz to 6 GHz.
- Transmit only at 915 MHz, by cable through a 30 dB attenuator or over the air at low power.
- Never transmit on a real service's frequency.
:::

Your Pluto can receive any real signal in its range, on its own frequency. A signal your project generates is a different matter: whatever it imitates, you send it at 915 MHz, either into a cable through the 30 dB attenuator, as in the L16 Lab, or over the air at low power where I approve it for your project. Never transmit on the frequency of a real service such as aircraft, ships, satellites, or a commercial radio's own band.
::::

::::{frame} Project Ideas
:::{present}
- FPV drone video detector
- Reverse engineering a radio device you own
- ADS-B generator at 915 MHz
- Frequency-hopping link
- Doppler radar at 915 MHz
- Weather satellite images from Meteor-M
:::

These ideas come from past projects and from what the course has built. Each one is a starting point; your proposal sets its scope. Ideas of your own are welcome. The next frame says a little about each one.
::::

::::{frame} About the Ideas
:class: read-only

- **FPV drone video detector.** Find and identify the analog video a hobby drone sends near 5.8 GHz, receive only. I have a starting point for this one; ask me.
- **Reverse engineering a radio device.** Capture a remote, sensor, or other device you own, receive only, and decode its protocol as in Lesson 17. A message you regenerate goes out at 915 MHz.
- **ADS-B generator.** Build ADS-B frames in GNU Radio, send them at 915 MHz, and decode them with gr-adsb, as in the success levels above. Never at 1090 MHz.
- **Frequency-hopping link.** Extend the Lesson 16 link at 915 MHz: more channels, faster hops, or a receiver that finds the hop pattern.
- **Doppler radar.** Send a steady tone at 915 MHz at low power and measure the Doppler shift of a person walking or a fan turning.
- **Weather satellite images.** Receive the Meteor-M LRPT signal near 137.9 MHz, demodulate its QPSK as in Lesson 15, and build an antenna for it. The NOAA APT satellites that older guides use stopped transmitting in August 2025, so check recent Meteor-M passes before you commit.
- **More ideas.** The RTL-SDR Blog (rtl-sdr.com) posts SDR projects every week. Many use an RTL-SDR, so check that the frequency and bandwidth fit your Pluto.
::::

::::{frame} Grading
:class: read-only

Each milestone is a checkpoint, assessed on the course's binary scale (syllabus, Grading): **1** when it meets the objective it serves, and **0** when it does not yet. You may revise a checkpoint after feedback under course policy, unless no effort is evident.

| Milestone | Objective | Meets the objective when |
| :-- | :-- | :-- |
| Proposal | 7.2 | the scope is reasonable and every success level can be shown done or not done |
| Background Research | 7.3 | you summarize at least four relevant sources and tie each to a building block |
| Design Description | 7.3 | the subsystems, blocks, open questions, and test plan are all stated |
| Prototype Update | 7.3 | working flowgraphs and results are shown against the levels |
| Final Report and Presentation | 7.4 | the demonstration works, and the report defends the result against your own levels |

You may collaborate, and you must document it (syllabus, Collaboration and Documentation).
::::

::::{frame} What to Turn In
:class: read-only

- **Milestones 1 to 4:** each one as a section of your report, by the date on the course schedule.
- **Final report:** the full report, IEEE quality, typically 7 to 10 pages, with a documentation statement.
- **Code:** your flowgraphs and scripts in a GitHub repository, linked from the report.
- **Evidence:** screenshots and, where the project records or receives signals, the SigMF recordings (`.sigmf-data` and `.sigmf-meta`) the results come from.
- **Presentation:** five minutes on the last lesson day, with a live demonstration on your Pluto.
::::

::::{frame} Legacy Slides and References
:class: read-only doc-links

- <a class="doc-link" href="../../legacy/L16-final-project-intro.pdf" target="_blank" rel="noopener">Final Project Introduction, slides (PDF)</a>

:::{depth}
These are the slides this topic was last taught from, posted as they were.
This page now covers the same ground.
:::
::::

::::{frame} Getting Started
:::{present}
- Pick two or three ideas and check each against your Pluto's range and bandwidth.
- Bring them to EI before the proposal is due.
- Keep every flowgraph from the course; most projects start from one.
:::

Start by picking two or three ideas and checking each one against what your Pluto can do: its frequency range, the bandwidth it streams, and the 915 MHz rule for anything you send. Bring the ones you like to EI, and we will settle on a scope that fits one semester before the proposal is due. Most projects start from a lesson's flowgraph, so keep every one you have built.
::::
