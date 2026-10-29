#!/usr/bin/env python3
"""L18 figures (ADS-B).

  L18-ppm   : the Mode S preamble and five data bits as 0.5 us chips: pulses
              at 0, 1.0, 3.5, and 4.5 us, then a 1 as pulse-quiet and a 0 as
              quiet-pulse
  L18-frame : the 112 bits of a DF17 message as its five fields (not to
              scale), with Sun's example 8D4840D6202CC371C32CE0576098 split
              under them

The GNU Radio screenshots (L18-grc-*.png, L18-adsb-*.png) are not generated
here: they are taken from the real flowgraphs running under Xvfb.

    python3 scripts/graphics/l18_figures.py
"""

from __future__ import annotations

import io
import math
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

from svg_font_stack import apply_font_stack  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUTS = (ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img")
NAVY, AMBER, RED, GREEN, GRAY, INK, RULE = "#004a85", "#8a5a00", "#b01e24", "#3f7d34", "#5b6573", "#15202b", "#cddce9"
plt.rcParams.update({"svg.fonttype": "none", "font.family": "sans-serif", "font.size": 11,
                     "axes.edgecolor": GRAY, "axes.labelcolor": INK, "xtick.color": GRAY, "ytick.color": GRAY,
                     "axes.spines.top": False, "axes.spines.right": False})

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



def ppm():
    pre = [1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0]
    bits = [1, 0, 0, 0, 1]
    chips = pre + [c for b in bits for c in ((1, 0) if b else (0, 1))]
    fig, ax = plt.subplots(figsize=(9.0, 2.6))
    t = np.arange(len(chips) + 1) * 0.5
    ax.fill_between([0, 8], -0.25, 1.35, color="#eef4fa", lw=0)
    for i, c in enumerate(chips):
        if c:
            ax.fill_between([t[i], t[i + 1]], 0, 1, color=NAVY, lw=0)
    ax.plot([0, t[-1]], [0, 0], color=GRAY, lw=1)
    for x in (0, 1.0, 3.5, 4.5):
        ax.text(x + 0.25, 1.08, f"{x:g}", ha="center", va="bottom", fontsize=9, color=GRAY)
    ax.text(4.0, 1.3, "preamble, 8 \u00b5s", ha="center", va="bottom", fontsize=11, color=INK, weight="bold")
    for k, b in enumerate(bits):
        x0 = 8 + k
        ax.plot([x0, x0], [-0.25, 1.1], color=RULE, lw=1, ls="--")
        ax.text(x0 + 0.5, -0.2, str(b), ha="center", va="top", fontsize=13, color=AMBER, weight="bold")
    ax.plot([13, 13], [-0.25, 1.1], color=RULE, lw=1, ls="--")
    ax.text(10.5, 1.3, "data: 1 \u00b5s a bit", ha="center", va="bottom", fontsize=11, color=INK, weight="bold")
    ax.text(13.2, 0.5, "1 = pulse, quiet\n0 = quiet, pulse", ha="left", va="center", fontsize=10, color=INK)
    ax.set_xlim(-0.2, 16.6); ax.set_ylim(-0.75, 1.65)
    ax.set_yticks([]); ax.spines["left"].set_visible(False)
    ax.set_xticks(range(0, 14)); ax.set_xlabel("time (\u00b5s)", fontsize=10)
    write("L18-ppm", fig)


def frame():
    # Box widths are not to scale, so the short fields have room for labels.
    fields = [("DF", 5, 12, NAVY), ("CA", 3, 10, GRAY), ("ICAO", 24, 22, AMBER), ("ME", 56, 34, GREEN), ("PI", 24, 22, RED)]
    hexes = [(0, 22, "8D", NAVY), (22, 44, "4840D6", AMBER), (44, 78, "202CC371C32CE0", GREEN), (78, 100, "576098", RED)]
    fig, ax = plt.subplots(figsize=(9.0, 1.7))
    x = 0
    for name, n, wd, col in fields:
        ax.add_patch(Rectangle((x + 0.3, 0.45), wd - 0.6, 0.5, fc=col, ec=col, alpha=0.15, lw=0))
        ax.add_patch(Rectangle((x + 0.3, 0.45), wd - 0.6, 0.5, fc="none", ec=col, lw=1.2))
        ax.text(x + wd / 2, 0.82, name, ha="center", va="center", fontsize=12, color=col, weight="bold")
        ax.text(x + wd / 2, 0.58, f"{n} bits", ha="center", va="center", fontsize=9.5, color=INK)
        x += wd
    for a0, a1, hx, col in hexes:
        ax.text((a0 + a1) / 2, 0.22, hx, ha="center", va="center", fontsize=11, color=col, family="monospace")
    ax.set_xlim(-0.5, 100.5); ax.set_ylim(0.05, 1.0); ax.axis("off")
    write("L18-frame", fig)


if __name__ == "__main__":
    ppm()
    frame()
