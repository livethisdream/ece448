#!/usr/bin/env python3
"""L4 figures (SDR introduction).

  L04-tuning-ranges : the tuning range of each course SDR on a log frequency
                      axis, with the signals the course receives marked. The
                      ranges are the manufacturers' published numbers (see the
                      lesson page's Sources frame).
  L04-sdr-chain     : the receive chain of a direct-conversion SDR: front end,
                      quadrature mixer and LO, low-pass filters, two ADCs, and
                      the host running GNU Radio.
  L04-mixer-shift   : a mixer moves the band around the LO frequency down to
                      0 Hz; the spectrum before and after.

The GNU Radio screenshots (L04-grc-adc.png, L04-adc-*.png) are not generated
here: they are taken from book/extras/grc/L04-adc-bits.grc running under Xvfb
(see CLAUDE.md, "Flowgraphs").

    python3 scripts/graphics/l04_figures.py
"""

from __future__ import annotations

import io
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Circle, FancyArrowPatch, FancyBboxPatch  # noqa: E402

from svg_font_stack import apply_font_stack  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUTS = (ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img")
NAVY, MID, AMBER, RED, GRAY, INK, RULE = "#004a85", "#0067b9", "#8a5a00", "#b01e24", "#5b6573", "#15202b", "#cddce9"
FILL = "#eef4fa"
plt.rcParams.update({"svg.fonttype": "none", "font.family": "sans-serif", "font.size": 11,
                     "axes.edgecolor": GRAY, "axes.labelcolor": INK, "xtick.color": GRAY, "ytick.color": GRAY,
                     "axes.spines.top": False, "axes.spines.right": False})


def write(name, fig):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    s = apply_font_stack(buf.getvalue()[buf.getvalue().index("<svg"):])
    for out in OUTS:
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {name}.svg")


def tuning_ranges():
    # Manufacturer tuning ranges in Hz. RTL-SDR Blog V4 datasheet; Great Scott
    # Gadgets (HackRF One); Analog Devices (ADALM-PLUTO, CN0566 ADALM-PHASER).
    radios = [("RTL-SDR Blog V4", 0.5e6, 1.766e9, "receive"),
              ("HackRF One", 1e6, 6e9, "half duplex"),
              ("PlutoSDR", 325e6, 3.8e9, "full duplex"),
              ("ADALM-PHASER", 10.0e9, 10.5e9, "8-element array")]
    signals = [("FM", 98e6), ("AIS", 162e6), ("433.92", 433.92e6), ("ADS-B", 1090e6),
               ("GPS L1", 1575.42e6), ("2.4 GHz ISM", 2.44e9)]
    fig, ax = plt.subplots(figsize=(8.4, 3.3))
    for i, (name, lo, hi, note) in enumerate(radios):
        y = len(radios) - 1 - i
        ax.barh(y, np.log10(hi) - np.log10(lo), left=np.log10(lo), height=0.56, color=MID if i < 3 else AMBER,
                alpha=0.9)
        ax.text(np.log10(lo) - 0.06, y, name, ha="right", va="center", color=INK, fontsize=11, fontweight="bold")
        ax.text(np.log10(hi) + 0.06, y, note, ha="left", va="center", color=GRAY, fontsize=10)
    for label, f in signals:
        ax.axvline(np.log10(f), color=RED, lw=1, ls=(0, (3, 3)), zorder=0)
        ax.text(np.log10(f) - 0.035, len(radios) - 0.35, label, rotation=90, ha="right", va="bottom", color=RED,
                fontsize=9.5)
    ticks = [1e5, 1e6, 1e7, 1e8, 1e9, 1e10]
    ax.set_xticks(np.log10(ticks), ["100 kHz", "1 MHz", "10 MHz", "100 MHz", "1 GHz", "10 GHz"])
    ax.set_xlim(5, np.log10(3e10))
    ax.set_ylim(-0.6, len(radios) + 0.75)
    ax.set_yticks([])
    ax.spines["left"].set_visible(False)
    ax.set_xlabel("tuning range (log scale)")
    write("L04-tuning-ranges", fig)


def _box(ax, x, y, w, h, text, color=NAVY, fill=FILL):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle="round,pad=0.02,rounding_size=0.08",
                                fc=fill, ec=color, lw=1.4))
    ax.text(x, y, text, ha="center", va="center", color=INK, fontsize=10.5)


def _arrow(ax, p, q, color=GRAY):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=11, color=color, lw=1.3,
                                 shrinkA=0, shrinkB=0))


def sdr_chain():
    fig, ax = plt.subplots(figsize=(9.4, 3.5))
    ax.set_xlim(0, 11.6)
    ax.set_ylim(0, 4.2)
    ax.axis("off")
    yI, yQ, yM = 3.2, 1.0, 2.1
    # antenna
    ax.plot([0.35, 0.35], [yM, yM + 1.0], color=INK, lw=1.4)
    ax.plot([0.12, 0.35, 0.58], [yM + 1.25, yM + 1.0, yM + 1.25], color=INK, lw=1.4)
    _arrow(ax, (0.35, yM), (0.75, yM))
    _box(ax, 1.2, yM, 0.9, 0.62, "filter")
    _arrow(ax, (1.65, yM), (1.95, yM))
    _box(ax, 2.35, yM, 0.8, 0.62, "LNA")
    ax.plot([2.75, 3.05, 3.05], [yM, yM, yM], color=GRAY, lw=1.3)
    ax.plot([3.05, 3.05], [yQ, yI], color=GRAY, lw=1.3)
    _arrow(ax, (3.05, yI), (3.75, yI))
    _arrow(ax, (3.05, yQ), (3.75, yQ))
    for y in (yI, yQ):
        ax.add_patch(Circle((4.0, y), 0.25, fc="white", ec=NAVY, lw=1.4))
        ax.text(4.0, y, "×", ha="center", va="center", fontsize=14, color=NAVY)
    # LO and 90 degree shift
    _box(ax, 5.2, yM + 0.35, 0.8, 0.5, "LO", color=AMBER, fill="#fbf3e4")
    _box(ax, 5.2, yM - 0.45, 0.8, 0.5, "90°", color=AMBER, fill="#fbf3e4")
    ax.plot([4.8, 4.0], [yM + 0.35, yM + 0.35], color=AMBER, lw=1.3)
    _arrow(ax, (4.0, yM + 0.35), (4.0, yI - 0.25), color=AMBER)
    _arrow(ax, (5.2, yM + 0.1), (5.2, yM - 0.2), color=AMBER)
    ax.plot([4.8, 4.0], [yM - 0.45, yM - 0.45], color=AMBER, lw=1.3)
    _arrow(ax, (4.0, yM - 0.45), (4.0, yQ + 0.25), color=AMBER)
    for y, lab in ((yI, "I"), (yQ, "Q")):
        _arrow(ax, (4.25, y), (6.05, y))
        _box(ax, 6.55, y, 1.0, 0.62, "LPF")
        _arrow(ax, (7.05, y), (7.3, y))
        _box(ax, 7.75, y, 0.9, 0.62, "ADC")
        _arrow(ax, (8.2, y), (8.85, y))
        ax.text(8.5, y + 0.22, lab, ha="center", va="bottom", color=NAVY, fontsize=11, fontweight="bold")
    _box(ax, 9.75, yM, 1.6, 2.9, "USB\n\nhost:\nGNU Radio", color=NAVY, fill="#e3edf6")
    # section labels
    for x0, x1, lab in ((0.7, 2.8, "RF front end"), (3.6, 5.65, "mixer and LO"), (6.0, 8.25, "digitize"),
                        (8.9, 10.6, "host")):
        ax.plot([x0, x1], [0.25, 0.25], color=RULE, lw=3)
        ax.text((x0 + x1) / 2, 0.02, lab, ha="center", va="bottom", color=GRAY, fontsize=10)
    write("L04-sdr-chain", fig)


def mixer_shift():
    f = np.linspace(-3.2, 3.2, 1200)

    def band(c, w=0.42, h=1.0):
        return h * np.exp(-0.5 * ((f - c) / w) ** 8)

    fig, (a1, a2) = plt.subplots(1, 2, figsize=(8.6, 2.6), sharey=True)
    # Before: three stations around the LO; frequencies relative to 100.0 MHz.
    rf = band(-1.6, 0.18, 0.55) + band(0.3, 0.18, 1.0) + band(1.4, 0.18, 0.75)
    a1.fill_between(f, rf, color=MID, alpha=0.85, lw=0)
    a1.axvline(0, color=AMBER, lw=1.8)
    a1.text(0.08, 1.12, "$f_{LO}$ = 100.0 MHz", color=AMBER, fontsize=10.5, ha="left")
    a1.set_xticks([-3, -2, -1, 0, 1, 2, 3], ["97", "98", "99", "100", "101", "102", "103"])
    a1.set_xlabel("frequency at the antenna (MHz)")
    a1.set_title("before the mixer", color=GRAY, fontsize=11, loc="left")
    a2.fill_between(f, rf, color=MID, alpha=0.85, lw=0)
    a2.axvline(0, color=AMBER, lw=1.8, ls=(0, (3, 3)))
    a2.set_xticks([-3, -2, -1, 0, 1, 2, 3], ["−3", "−2", "−1", "0", "+1", "+2", "+3"])
    a2.set_xlabel("frequency after the mixer (MHz)")
    a2.set_title("after the mixer", color=GRAY, fontsize=11, loc="left")
    for a in (a1, a2):
        a.set_yticks([])
        a.spines["left"].set_visible(False)
        a.set_ylim(0, 1.35)
    write("L04-mixer-shift", fig)


if __name__ == "__main__":
    tuning_ranges()
    sdr_chain()
    mixer_shift()
