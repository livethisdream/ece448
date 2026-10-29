#!/usr/bin/env python3
"""L17 figures (RF reverse engineering).

  L17-process   : the five steps of the 2025 lesson: find the carrier, identify
                  the modulation, identify the encoding, build an encoder, and
                  transmit, into a cable only.
  L17-frame     : one frame of the Simulated fan remote's Light button: the
                  on/off chips, the 3-chip PWM bits, and the three fields.
  L17-encodings : the same four bits keyed three common ways: pulse width,
                  pulse distance, and Manchester.

The recording L17-fan-remote.sigmf-data comes from book/extras/grc/
L17-fan-remote-gen.grc. The GNU Radio and URH screenshots (L17-view-*.png,
L17-tx-sim.png, L17-grc-*.png, L17-urh-*.png) are not generated here: they
are taken from the real flowgraphs and from URH 2.10 running under Xvfb on that
recording (see CLAUDE.md, "Flowgraphs").

    python3 scripts/graphics/l17_figures.py
"""

from __future__ import annotations

import io
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

from svg_font_stack import apply_font_stack  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUTS = (ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img")
NAVY, AMBER, RED, GREEN, GRAY, INK, RULE = "#004a85", "#8a5a00", "#b01e24", "#3f7d34", "#5b6573", "#15202b", "#cddce9"
plt.rcParams.update({"svg.fonttype": "none", "font.family": "sans-serif", "font.size": 11,
                     "axes.edgecolor": GRAY, "axes.labelcolor": INK, "xtick.color": GRAY, "ytick.color": GRAY,
                     "axes.spines.top": False, "axes.spines.right": False})

# The Simulated fan remote, as L17-fan-remote-gen.grc makes it
ADDR, LIGHT = 0xA6, 0x1
PWM = {0: [1, 0, 0], 1: [1, 1, 0]}


def write(name, fig):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    s = apply_font_stack(buf.getvalue()[buf.getvalue().index("<svg"):])
    s = re.sub(r' d="([^"]*)"', lambda m: ' d="' + re.sub(r"(\d+\.\d)\d+", r"\1", m.group(1)) + '"', s)
    for out in OUTS:
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {name}.svg")


def process():
    steps = [("1", "Find the\ncarrier", "spectrum and\nwaterfall"),
             ("2", "Identify the\nmodulation", "OOK, FSK,\nPSK, ..."),
             ("3", "Identify the\nencoding", "bits, fields,\nrates"),
             ("4", "Build an\nencoder", "GNU Radio\nflowgraph"),
             ("5", "Transmit", "into a cable\nonly")]
    fig, ax = plt.subplots(figsize=(9.6, 1.9))
    ax.set_xlim(0, 10); ax.set_ylim(0, 2.15); ax.axis("off")
    for i, (n, title, sub) in enumerate(steps):
        x = 0.1 + i * 2.0
        color = RED if i == 4 else NAVY
        ax.add_patch(FancyBboxPatch((x, 0.55), 1.6, 1.25, boxstyle="round,pad=0.02,rounding_size=0.12",
                                    fc="none", ec=color, lw=1.6))
        ax.text(x + 0.8, 1.42, title, ha="center", va="center", color=INK, fontsize=11.5, fontweight="bold")
        ax.text(x + 0.8, 0.86, sub, ha="center", va="center", color=GRAY, fontsize=9.5)
        ax.text(x + 0.8, 1.98, f"Step {n}", ha="center", va="center", color=color, fontsize=10, fontweight="bold")
        if i < 4:
            ax.annotate("", xy=(x + 1.98, 1.17), xytext=(x + 1.62, 1.17),
                        arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.3))
    ax.text(5.0, 0.18, "Steps 1 to 3 work from a recording; steps 4 and 5 build it back.",
            ha="center", va="center", color=GRAY, fontsize=9.5)
    write("L17-process", fig)


def frame():
    word = ADDR << 8 | LIGHT << 4 | (LIGHT ^ 0xF)
    bits = [(word >> (15 - i)) & 1 for i in range(16)]
    chips = sum((PWM[b] for b in bits), [])
    fig, ax = plt.subplots(figsize=(9.6, 2.6))
    t = [0]; y = [0]
    for k, c in enumerate(chips):
        t += [k, k + 1]; y += [c, c]
    ax.plot([v * 0.4 for v in t], y, color=NAVY, lw=1.6, drawstyle="default")
    for i, b in enumerate(bits):
        x0 = i * 1.2
        ax.axvline(x0, color=RULE, lw=0.8, zorder=0)
        ax.text(x0 + 0.6, 1.25, str(b), ha="center", va="center", color=INK, fontsize=12, fontweight="bold")
    ax.axvline(16 * 1.2, color=RULE, lw=0.8, zorder=0)
    fields = [(0, 8, "address  0xA6", NAVY), (8, 12, "command  0x1", AMBER), (12, 16, "check  0xE", GREEN)]
    for a, b, label, color in fields:
        ax.annotate("", xy=(a * 1.2 + 0.05, 1.62), xytext=(b * 1.2 - 0.05, 1.62),
                    arrowprops=dict(arrowstyle="<->", color=color, lw=1.3))
        ax.text((a + b) * 0.6, 1.82, label, ha="center", va="bottom", color=color, fontsize=11, fontweight="bold")
    ax.set_xlim(-0.2, 21.6); ax.set_ylim(-0.25, 2.4)
    ax.set_yticks([0, 1]); ax.set_yticklabels(["off", "on"])
    ax.set_xticks([0, 4.8, 9.6, 14.4, 19.2])
    ax.set_xlabel("time (ms): 400 µs chips, 3 chips per bit, 1.2 ms per bit")
    ax.spines["left"].set_visible(False)
    ax.text(19.5, 0.5, "Simulated", ha="left", va="center", color=RED, fontsize=10, fontweight="bold")
    write("L17-frame", fig)


def encodings():
    bits = [1, 0, 1, 1]
    rows = [("Pulse width", {0: [1, 0, 0], 1: [1, 1, 0]}, "every bit starts on;\nthe pulse length is the bit"),
            ("Pulse distance", {0: [1, 0], 1: [1, 0, 0, 0]}, "pulses are all short;\nthe gap length is the bit"),
            ("Manchester", {0: [0, 1], 1: [1, 0]}, "every bit has a\ntransition in its middle")]
    fig, axes = plt.subplots(3, 1, figsize=(9.0, 3.9), sharex=True)
    for ax, (name, pat, note) in zip(axes, rows):
        chips = sum((pat[b] for b in bits), [])
        edges, t = [0], 0
        for b in bits:
            t += len(pat[b]); edges.append(t)
        tt = [0]; yy = [0]
        for k, c in enumerate(chips):
            tt += [k, k + 1]; yy += [c, c]
        ax.plot(tt, yy, color=NAVY, lw=1.6)
        for e in edges:
            ax.axvline(e, color=RULE, lw=0.8, zorder=0)
        for b, a, z in zip(bits, edges, edges[1:]):
            ax.text((a + z) / 2, 1.32, str(b), ha="center", color=INK, fontsize=11, fontweight="bold")
        ax.set_ylim(-0.2, 1.65); ax.set_yticks([]); ax.spines["left"].set_visible(False)
        ax.text(-0.5, 0.55, name, ha="right", va="center", color=INK, fontsize=11, fontweight="bold")
        ax.text(16.6, 0.55, note, ha="left", va="center", color=GRAY, fontsize=9.5)
        ax.set_xlim(0, 16.4)
    axes[-1].set_xticks([]); axes[-1].set_xlabel("the bits 1 0 1 1, one chip per grid step")
    fig.subplots_adjust(hspace=0.25)
    write("L17-encodings", fig)


if __name__ == "__main__":
    process()
    frame()
    encodings()
