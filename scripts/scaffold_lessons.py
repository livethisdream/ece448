#!/usr/bin/env python3
"""Scaffold the ECE 448 lesson pages, module pages, and TOC from one manifest.

For each lesson in LESSONS, lab in LABS, and page in EXTRA_PAGES that does not
already exist, this writes
  book/moduleNN/<slug>/index.md     a frame page: title, objectives, the
                                    legacy slides, and what comes next

It also rewrites every module landing page (book/moduleNN/index.md) and
book/_toc.yml. Existing lesson pages are left UNTOUCHED unless --force is
passed, so a lesson that has since been converted to the ECE 444 format is
safe to re-run over. Module pages are regenerated every run until one is hand
written; set generate_index=False on it in MODULES when that happens.

Lessons are topics, not class periods (the ECE 444 rule). A lab is a child
page of its lesson, `LNN-lab-<slug>`, titled "LNN Lab — <Topic>", and takes no
lesson number of its own. The midterm and the final project are pages too,
but calendar events rather than lessons.

No new reveal.js decks are generated. Until a lesson is converted, its page
links the legacy Beamer PDF under book/extras/legacy/ where one exists.

The manifest is the single source of truth for lesson numbers, titles,
objectives, labs, and which legacy deck a lesson uses. Edit it and re-run.

Usage:
    python scripts/scaffold_lessons.py            # create missing pages + modules + toc
    python scripts/scaffold_lessons.py --force    # also overwrite existing lesson pages (careful!)
    python scripts/scaffold_lessons.py --dry-run  # print what would happen, write nothing
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BOOK = REPO / "book"
LEGACY = BOOK / "extras" / "legacy"

COURSE = "ECE 448"
COURSE_TITLE = "Software Defined Radios"
TERM = "Spring 2027"
INSTRUCTORS = "Dr. Neil Rogers"

# ---- Learning objectives (Neil, 2026-10-17) --------------------------------
# The seven-module list from the 2026 site syllabus. Edited: 3.3 (adds RDS),
# 5.3-5.4 (the midterm is a fox hunt and a CTF), 6.4 (adds carrier and timing
# recovery). Change one here, in book/syllabus.md, and in every lesson that
# quotes it, together.
LO_TEXT = {
    "1.1": "I can define noise figure and cascade it through a receiver chain to predict system noise performance.",
    "1.2": "I can compute a link budget and predict received SNR for a specified geometry, transmitter, and antenna configuration.",
    "1.3": "I can describe signal-space concepts (basis functions, constellations, decision regions) and apply them to a digital modulation scheme.",
    "2.1": "I can describe what a Software Defined Radio is, contrast it with a traditional hardware radio, and identify the SDR platforms used in this course (RTL-SDR, HackRF, PlutoSDR, ADALM-PHASER).",
    "2.2": "I can identify the roles of the RF frontend, ADC/DAC, and host in an SDR signal chain and describe sample-rate, bandwidth, and dynamic-range trade-offs.",
    "2.3": "I can install GNU Radio and use GNU Radio Companion (GRC) to build, inspect, and run a basic flowgraph.",
    "2.4": "I can capture a real RF signal using an SDR and interpret its time- and frequency-domain representations.",
    "3.1": "I can describe DSB-AM, DSB-SC, and SSB and identify each on a spectrum.",
    "3.2": "I can implement an AM modulator and demodulator in GNU Radio and verify demodulated audio against the source.",
    "3.3": "I can implement an FM receiver in GNU Radio, demodulate a live broadcast FM signal, and decode its RDS data.",
    "3.4": "I can explain and demonstrate the trade-off between bandwidth and noise performance for AM vs. FM.",
    "4.1": "I can describe FSK modulation and implement an FSK transmitter and receiver in GNU Radio.",
    "4.2": "I can describe PAM theory and identify the pulse-shaping, symbol-rate, and bandwidth trade-offs.",
    "4.3": "I can apply matched filtering and symbol-timing recovery to a received PAM signal.",
    "4.4": "I can implement a PAM link that transmits and receives ASCII text end-to-end.",
    "5.1": "I can create a GNU Radio out-of-tree (OOT) module and add a custom Python block to it.",
    "5.2": "I can implement a custom signal-processing block from scratch and integrate it into a GNU Radio flowgraph.",
    "5.3": "I can find a hidden transmitter in a direction-finding fox hunt using an SDR and a directional antenna.",
    "5.4": "I can solve capture-the-flag challenges that require finding, capturing, demodulating, and decoding unknown signals with GNU Radio.",
    "6.1": "I can transmit and receive CW (Morse) using GNU Radio and decode a received CW stream.",
    "6.2": "I can decode DTMF tones from a captured audio signal.",
    "6.3": "I can describe how HD Radio works and demodulate an HD Radio signal.",
    "6.4": "I can implement an mPSK modulator and demodulator (BPSK, QPSK, 8PSK), recover carrier and symbol timing, and verify constellation behavior against theory.",
    "6.5": "I can implement FHSS transmission and reception, including hop-sequence synchronization.",
    "6.6": "I can perform RF reverse engineering on an unknown signal: identify its modulation, symbol rate, and payload structure.",
    "6.7": "I can receive and decode ADS-B messages from aircraft transponders.",
    "6.8": "I can receive and decode AIS messages from marine vessels.",
    "7.1": "I can describe QAM and OFDM and identify use cases for each.",
    "7.2": "I can define the scope, objectives, and measurable success criteria for a self-directed SDR project.",
    "7.3": "I can research, design, and implement a wireless communication system using an SDR and GNU Radio.",
    "7.4": "I can present my project results in a professional-grade report and live demonstration and defend engineering trade-offs against my own stated success criteria.",
}

# ---- Module metadata (Neil, 2026-10-17: the seven modules of the old site) --
MODULES = {
    1: dict(
        name="Foundations of Detection & Link Budgets",
        tagline="Will the link close? The few numbers you need before hardware touches a signal.",
        synopsis="Noise figure, cascade analysis, the link budget, and signal space: just enough to predict whether a link will work and to read a constellation.",
        generate_index=True,
    ),
    2: dict(
        name="SDR & GNU Radio Foundations",
        tagline="The radio is software now. Meet the hardware, then build your first flowgraph.",
        synopsis="What is inside an SDR, how sample rate and bandwidth trade, and your first GNU Radio flowgraphs against real captured signals.",
        generate_index=True,
    ),
    3: dict(
        name="Analog Modulation",
        tagline="AM and FM: build them, receive them, and hear the difference.",
        synopsis="Simulate AM, then build AM and FM receivers in GNU Radio and pull a live broadcast station, RDS data included, off the air.",
        generate_index=True,
    ),
    4: dict(
        name="Digital Modulation",
        tagline="From bits to waveforms and back: FSK and PAM, end to end.",
        synopsis="FSK and PAM from the flowgraph up: pulse shaping, matched filtering, and timing recovery, finishing with a link that carries ASCII text.",
        generate_index=True,
    ),
    5: dict(
        name="Custom Blocks & Midterm",
        tagline="When GNU Radio does not have the block, write it.",
        synopsis="Out-of-tree modules and custom Python blocks, then the midterm: a fox hunt for a hidden transmitter and a capture-the-flag.",
        generate_index=True,
    ),
    6: dict(
        name="Waveform Applications & RF Reverse Engineering",
        tagline="Real signals, real decoders: CW to AIS, and the unknown signal in between.",
        synopsis="CW, DTMF, HD Radio, mPSK, frequency hopping, ADS-B, and AIS, each built or decoded in GNU Radio, plus the workflow for taking an unknown signal from spectrum to bits.",
        generate_index=True,
    ),
    7: dict(
        name="Final Project",
        tagline="Your project, your success criteria, your defense.",
        synopsis="QAM and OFDM, then the self-defined final project: proposal, research, prototype, and a report and live demonstration against the success criteria you wrote.",
        generate_index=True,
    ),
}

# ---- Legacy decks: Beamer PDFs under book/extras/legacy/ ---------------------
# key -> (label, file). Supplemental references live under legacy/refs/.
DECKS = {
    "noise": ("Noise Figure and Link Budget, slides", "L02-noise-figure-link-budget.pdf"),
    "space": ("Signal Space, slides", "L03-signal-space.pdf"),
    "sdr": ("SDR Introduction, slides", "L04-sdr-introduction.pdf"),
    "am": ("AM Simulation, slides", "L07-am-simulation.pdf"),
    "amfm": ("AM and FM Receivers, slides", "L08-am-fm-receivers.pdf"),
    "pam": ("PAM Theory, slides", "L13-pam-theory.pdf"),
    "ascii": ("ASCII over PAM, slides", "L14-ascii-pam.pdf"),
    "fp": ("Final Project Introduction, slides", "L16-final-project-intro.pdf"),
    "dtmf": ("DTMF, slides", "L22-dtmf.pdf"),
    "hd": ("HD Radio, slides", "L24-hd-radio.pdf"),
    "rfre": ("RF Reverse Engineering, slides", "L31-rf-reverse-engineering.pdf"),
    "adsb": ("ADS-B, slides", "L35-adsb.pdf"),
    "ais": ("AIS, slides", "L36-ais.pdf"),
    "ref-nrsc": ("NRSC-1011s HD Radio specification", "refs/nrsc-1011s_hd-radio.pdf"),
    "ref-diff": ("Differential encoding tutorial", "refs/differential-encoding-tutorial.pdf"),
    "ref-adsb": ("ADS-B decoding guide", "refs/adsb-decode-guide.pdf"),
    "ref-1090": ("The 1090 MHz Riddle", "refs/1090_Riddle.pdf"),
    "ref-magazu": ("ADS-B (Magazu, USAF)", "refs/adsb_magazu_usaf.pdf"),
}

# ---- Lesson manifest (Neil, 2026-10-17) ------------------------------------
# (module, num, slug, title, [lo_ids], [deck keys], synopsis)
LESSONS = [
    (1, 1, "L01-course-intro", "Course Introduction", [], [], "What an SDR is, the signals around you, and how the course is run."),
    (1, 2, "L02-noise-figure-link-budget", "Noise Figure and Link Budget", ["1.1", "1.2"], ["noise"], "Cascade noise figure through a receiver and predict the SNR a link delivers."),
    (1, 3, "L03-signal-space", "Signal Space", ["1.3"], ["space"], "Basis functions, constellations, and decision regions: the picture every digital receiver works from."),

    (2, 4, "L04-sdr-introduction", "SDR Introduction", ["2.1", "2.2"], ["sdr"], "The SDR platforms in this course, what is inside them, and the sample-rate, bandwidth, and dynamic-range trade-offs."),
    (2, 5, "L05-gnu-radio-intro", "GNU Radio Introduction", ["2.3", "2.4"], [], "GNU Radio Companion from install to a running flowgraph, then a real capture in time and frequency."),

    (3, 6, "L06-am-simulation", "AM Simulation", ["3.1", "3.2"], ["am"], "DSB-AM, DSB-SC, and SSB built and demodulated in GNU Radio."),
    (3, 7, "L07-am-fm-receivers", "AM and FM Receivers", ["3.3", "3.4"], ["amfm"], "AM and FM receivers, a live broadcast FM station, and its RDS data."),

    (4, 8, "L08-fsk", "FSK", ["4.1"], [], "An FSK transmitter and receiver in GNU Radio."),
    (4, 9, "L09-pam-theory", "PAM Theory", ["4.2", "4.3"], ["pam"], "Pulse shaping, symbol rate, bandwidth, matched filtering, and timing recovery."),
    (4, 10, "L10-ascii-pam", "ASCII over PAM", ["4.4"], ["ascii"], "A PAM link that carries ASCII text end to end."),

    (5, 11, "L11-custom-blocks", "Out-of-Tree Modules and Custom Blocks", ["5.1", "5.2"], [], "Package a GNU Radio out-of-tree module and write your own Python block."),

    (6, 12, "L12-cw", "CW", ["6.1"], [], "Send and decode Morse code in GNU Radio."),
    (6, 13, "L13-dtmf", "DTMF", ["6.2"], ["dtmf"], "Detect DTMF tones in a captured audio signal."),
    (6, 14, "L14-hd-radio", "HD Radio", ["6.3"], ["hd", "ref-nrsc"], "How HD Radio hides OFDM sidebands beside an FM station, and how to demodulate them."),
    (6, 15, "L15-mpsk", "mPSK", ["6.4"], ["ref-diff"], "BPSK, QPSK, and 8PSK in GNU Radio, with carrier and symbol-timing recovery."),
    (6, 16, "L16-fhss", "Frequency Hopping", ["6.5"], [], "An FHSS transmitter and receiver that stay on the same hop sequence."),
    (6, 17, "L17-rf-reverse-engineering", "RF Reverse Engineering", ["6.6"], ["rfre"], "Take an unknown signal from spectrum to bits with GQRX, URH, and GNU Radio."),
    (6, 18, "L18-adsb", "ADS-B", ["6.7"], ["adsb", "ref-adsb", "ref-1090", "ref-magazu"], "Receive and decode aircraft ADS-B messages at 1090 MHz."),
    (6, 19, "L19-ais", "AIS", ["6.8"], ["ais"], "Receive and decode AIS messages from ships."),

    (7, 20, "L20-qam-ofdm", "QAM and OFDM", ["7.1"], [], "QAM and OFDM, and where each one is used."),
]

# ---- Labs: child pages of a lesson, no lesson number of their own ----------
# (module, anchor lesson slug, lab slug, toc title, synopsis[, lo_ids])
# lo_ids defaults to the anchor lesson's objectives.
LABS = [
    (2, "L05-gnu-radio-intro", "L05-lab-first-flowgraphs", "L5 Lab — First Flowgraphs", "Build, run, and inspect your first flowgraphs against a real capture."),
    (3, "L06-am-simulation", "L06-lab-am-simulation", "L6 Lab — AM Simulation", "Build an AM modulator and demodulator and check the audio against the source."),
    (3, "L07-am-fm-receivers", "L07-lab-am-fm-receivers", "L7 Lab — AM and FM Receivers", "Receive a live FM broadcast and decode its RDS data."),
    (4, "L08-fsk", "L08-lab-fsk", "L8 Lab — FSK", "Send and receive data over an FSK link."),
    (4, "L10-ascii-pam", "L10-lab-pam-link", "L10 Lab — PAM Link", "Send ASCII text over a PAM link, end to end."),
    (5, "L11-custom-blocks", "L11-lab-custom-block", "L11 Lab — Custom Block", "Write a custom block and use it in a working flowgraph."),
    (6, "L12-cw", "L12-lab-cw", "L12 Lab — CW", "Transmit, receive, and decode CW."),
    (6, "L13-dtmf", "L13-lab-dtmf", "L13 Lab — DTMF", "Decode DTMF tones from a capture."),
    (6, "L14-hd-radio", "L14-lab-hd-radio", "L14 Lab — HD Radio", "Find and demodulate an HD Radio signal."),
    (6, "L15-mpsk", "L15-lab-mpsk", "L15 Lab — mPSK", "Build an mPSK modem and close the loop on carrier and timing."),
    (6, "L16-fhss", "L16-lab-fhss", "L16 Lab — Frequency Hopping", "Hop a transmitter and keep a receiver on it."),
    (6, "L17-rf-reverse-engineering", "L17-lab-rf-reverse-engineering", "L17 Lab — RF Reverse Engineering", "Reverse-engineer an unknown signal from capture to payload."),
    (6, "L19-ais", "L18-L19-lab-adsb-ais", "L18–L19 Lab — ADS-B and AIS", "Decode live ADS-B and AIS traffic.", ["6.7", "6.8"]),
]

# ---- Calendar events with pages of their own --------------------------------
# (module, after lesson slug, slug, toc title, [lo_ids], [deck keys], synopsis)
EXTRA_PAGES = [
    (5, "L11-lab-custom-block", "midterm", "Midterm — Fox Hunt and CTF", ["5.3", "5.4"], [], "A direction-finding fox hunt for a hidden transmitter, and a capture-the-flag."),
    (7, "L20-qam-ofdm", "final-project", "Final Project", ["7.2", "7.3", "7.4"], ["fp"], "A self-defined SDR project: proposal, background research, design, prototype, then a report and live demonstration."),
]


def lo_list_html(lo_ids, indent="  "):
    """Group the objectives by module; each <ol> numbers itself as M.k."""
    out, run = [], []
    for i in lo_ids + [None]:
        if run and (i is None or i.split(".")[0] != run[0].split(".")[0]):
            mod, first = run[0].split(".")
            reset = f"; counter-reset: lo {int(first) - 1}" if int(first) > 1 else ""
            items = "\n".join(f"{indent}<li>{LO_TEXT[x]}</li>" for x in run)
            out.append(f'<ol class="lo-list" style="--module: \'{mod}\'{reset}">\n{items}\n</ol>')
            run = []
        if i is not None:
            run.append(i)
    return "\n\n".join(out)


def obj_label(lo_ids):
    if not lo_ids:
        return ""
    return ("Objective " if len(lo_ids) == 1 else "Objectives ") + ", ".join(lo_ids)


def legacy_frame(decks):
    if not decks:
        return ""
    lines = [
        f'- <a class="doc-link" href="../../legacy/{DECKS[k][1]}" target="_blank" rel="noopener">{DECKS[k][0]} (PDF)</a>'
        for k in decks
    ]
    return f"""::::{{frame}} Legacy Slides and References
:class: read-only doc-links

{chr(10).join(lines)}

:::{{depth}}
These are the slides this topic was last taught from, posted as they were
while the lesson is converted to the new format.
:::
::::
"""


def title_frame(title, synopsis, footer):
    return f"""::::{{frame}}
:class: title-frame

<div class="course-mark">{COURSE} · {TERM}</div>

<h1 class="frame-title">{title}</h1>

<div class="title-rule"></div>

{synopsis}

{footer}
::::
"""


def lo_frame(lo_ids):
    if not lo_ids:
        return ""
    return f"""::::{{frame}} Learning Objectives

{lo_list_html(lo_ids)}
::::
"""


UNDER_CONSTRUCTION = """::::{frame} Under Construction
:class: read-only

This page is being converted to the new course format. The objectives above
are current; the notes, slides, and practice problems will follow before the
lesson is taught.
::::
"""


def lesson_index_md(mnum, num, title, lo_ids, decks, synopsis):
    m = MODULES[mnum]
    return f"""---
frame_view: true
---

# L{num} - {title}

{title_frame(title, synopsis, f"Lesson {num} · Module {mnum}: {m['name']} · {INSTRUCTORS}")}
{lo_frame(lo_ids)}
{legacy_frame(decks)}
{UNDER_CONSTRUCTION}"""


def lab_los(lab):
    return lab[5] if len(lab) > 5 else next(x[4] for x in LESSONS if x[2] == lab[1])


def lab_index_md(lab):
    mnum, _anchor, _slug, title, synopsis = lab[:5]
    lo_ids = lab_los(lab)
    m = MODULES[mnum]
    topic = title.split(" — ", 1)[1]
    return f"""---
frame_view: true
---

# {title}

{title_frame(topic, synopsis, f"{title.split(' — ')[0]} · Module {mnum}: {m['name']} · {INSTRUCTORS}")}
{lo_frame(lo_ids)}
::::{{frame}} Lab Packet
:class: read-only

One packet, one submission: Part 1 Pre-Lab before the period, Part 2 on the
bench in class, Part 3 Writeup after. The {TERM} packet will be posted here
before the lab.
::::
"""


def extra_index_md(mnum, title, lo_ids, decks, synopsis):
    m = MODULES[mnum]
    return f"""---
frame_view: true
---

# {title}

{title_frame(title, synopsis, f"Module {mnum}: {m['name']} · {INSTRUCTORS}")}
{lo_frame(lo_ids)}
{legacy_frame(decks)}
{UNDER_CONSTRUCTION}"""


def module_pages(mnum):
    """Every page in a module, in TOC order: (slug, toc title, kind, los, synopsis)."""
    pages = []
    for (mm, num, slug, title, lo_ids, _d, synopsis) in LESSONS:
        if mm != mnum:
            continue
        pages.append((slug, f"L{num} — {title}", f"Lesson · L{num}", lo_ids, synopsis))
        for lab in LABS:
            if lab[1] == slug:
                pages.append((lab[2], lab[3], "Lab", lab_los(lab), lab[4]))
        for (em, after, eslug, etitle, elos, _ed, esyn) in EXTRA_PAGES:
            if after == slug:
                pages.append((eslug, etitle, "Event", elos, esyn))
    # an extra page may follow a lab rather than a lesson
    for (em, after, eslug, etitle, elos, _ed, esyn) in EXTRA_PAGES:
        if em == mnum and eslug not in [p[0] for p in pages]:
            idx = [p[0] for p in pages].index(after) + 1
            pages.insert(idx, (eslug, etitle, "Event", elos, esyn))
    return pages


def module_index_md(mnum):
    m = MODULES[mnum]
    nums = [x[1] for x in LESSONS if x[0] == mnum]
    rng = f"Lesson {nums[0]}" if len(nums) == 1 else f"Lessons {nums[0]}–{nums[-1]}"
    los = [lo for lo in LO_TEXT if lo.startswith(f"{mnum}.")]
    lo_frames = []
    # Four objectives a frame at most, or a present-mode frame overflows.
    for k in range(0, len(los), 4):
        part = los[k:k + 4]
        sub = "" if len(los) <= 4 else f" ({part[0]}-{part[-1]})"
        lo_frames.append(f"""::::{{frame}} Learning Objectives{sub}

{lo_list_html(part)}
::::
""")
    pages = module_pages(mnum)
    cards = []
    for (slug, ttl, kind, lo_ids, synopsis) in pages:
        name = ttl.split(" — ", 1)[-1]
        label = obj_label(lo_ids)
        tail = f" {label}." if label else ""
        cards.append(
            f"""  <a class="mt-card mt-lesson" href="{slug}/index.html">
    <span class="mt-kind">{kind if kind.startswith('Lesson') else ttl.split(' — ')[0]}</span>
    <h4>{name}</h4>
    <p>{synopsis}{tail}</p>
  </a>"""
        )
    card_frames = []
    for k in range(0, len(cards), 3):
        body = "\n".join(cards[k:k + 3])
        part = "" if len(cards) <= 3 else f" ({k // 3 + 1} of {(len(cards) + 2) // 3})"
        card_frames.append(f"""::::{{frame}} In This Module{part}

<div class="module-toc">
{body}
</div>
::::
""")
    return f"""---
frame_view: true
nav: {m['name']}
---

# Module {mnum} — {m['name']}

::::{{frame}}
:class: title-frame

<div class="course-mark">{COURSE} · Module {mnum:02d}</div>

<h1 class="frame-title">{m['name'].replace('&', '&amp;')}</h1>

<div class="title-rule"></div>

{m['tagline']}

{rng} · {COURSE_TITLE} · {INSTRUCTORS}
::::

::::{{frame}} Where This Module Goes
{m['synopsis']}
::::

{chr(10).join(lo_frames)}
{chr(10).join(card_frames)}"""


def toc_yaml():
    lines = [
        "# Table of contents for ECE 448.",
        "# Generated by scripts/scaffold_lessons.py from the LESSONS manifest.",
        "# Re-run that script after editing the manifest; hand edits here will be overwritten.",
        "",
        "format: jb-book",
        "root: intro",
        "",
        "parts:",
        "  - caption: Course Information",
        "    chapters:",
        "      - file: syllabus",
        "      - file: materials",
    ]
    for mnum, m in MODULES.items():
        lines += ["", f"  - caption: Module {mnum} — {m['name']}", "    chapters:",
                  f"      - file: module{mnum:02d}/index", f"        title: Module {mnum} overview"]
        for (slug, ttl, *_rest) in module_pages(mnum):
            lines.append(f"      - file: module{mnum:02d}/{slug}/index")
            lines.append(f'        title: "{ttl}"')
    return "\n".join(lines) + "\n"


def write(path: Path, content: str, force: bool, dry: bool, kind: str):
    exists = path.exists()
    if exists and not force:
        print(f"  skip (exists): {path.relative_to(REPO)}")
        return False
    print(f"  {'overwrite' if exists else 'write'} {kind}: {path.relative_to(REPO)}")
    if not dry:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return True


def check_manifest():
    nums = [x[1] for x in LESSONS]
    assert nums == list(range(1, len(LESSONS) + 1)), "lesson numbers must run 1..N with no gaps"
    slugs = {x[2] for x in LESSONS}
    for x in LESSONS + [(e[0], 0, e[2], e[3], e[4], e[5], e[6]) for e in EXTRA_PAGES]:
        for lo in x[4]:
            assert lo in LO_TEXT, f"{x[2]}: unknown objective {lo}"
        for d in x[5]:
            assert d in DECKS, f"{x[2]}: unknown deck {d}"
    for lab in LABS:
        assert lab[1] in slugs, f"{lab[2]}: unknown anchor lesson {lab[1]}"
    for _key, (_label, f) in DECKS.items():
        assert (LEGACY / f).exists(), f"missing legacy/{f}"
    taught = {lo for x in LESSONS for lo in x[4]} | {lo for e in EXTRA_PAGES for lo in e[4]}
    missing = sorted(set(LO_TEXT) - taught)
    assert not missing, f"objectives no page serves: {missing}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="overwrite existing lesson pages")
    ap.add_argument("--dry-run", action="store_true", help="print actions, write nothing")
    args = ap.parse_args()
    check_manifest()

    print("== Lesson pages ==")
    for (mnum, num, slug, title, lo_ids, decks, synopsis) in LESSONS:
        idx = BOOK / f"module{mnum:02d}" / slug / "index.md"
        write(idx, lesson_index_md(mnum, num, title, lo_ids, decks, synopsis), args.force, args.dry_run, "lesson")
    for lab in LABS:
        idx = BOOK / f"module{lab[0]:02d}" / lab[2] / "index.md"
        write(idx, lab_index_md(lab), args.force, args.dry_run, "lab")
    for (mnum, _after, slug, title, lo_ids, decks, synopsis) in EXTRA_PAGES:
        idx = BOOK / f"module{mnum:02d}" / slug / "index.md"
        write(idx, extra_index_md(mnum, title, lo_ids, decks, synopsis), args.force, args.dry_run, "page")

    print("== Module landing pages ==")
    for mnum, m in MODULES.items():
        if not m.get("generate_index"):
            print(f"  skip module {mnum} index (hand-written)")
            continue
        write(BOOK / f"module{mnum:02d}" / "index.md", module_index_md(mnum), True, args.dry_run, "module")

    print("== _toc.yml ==")
    write(BOOK / "_toc.yml", toc_yaml(), True, args.dry_run, "toc")
    print("done.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
