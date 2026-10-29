#!/usr/bin/env python3
"""L19 figures (AIS).

  L19-burst : one AIS position report in its 26.67 ms slot of 256 bits
              (not to scale): ramp, training, start flag, 168-bit message,
              CRC, end flag, and the buffer left for stuffed bits and distance

The GNU Radio screenshots (L19-grc-*.png, L19-ais-*.png) are not generated
here: they are taken from the real flowgraphs running under Xvfb.

    python3 scripts/graphics/l19_figures.py
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



def burst():
    # Box widths are not to scale, so the short parts have room for labels.
    parts = [("ramp", 8, 9, GRAY), ("training", 24, 14, NAVY), ("flag", 8, 9, AMBER), ("message", 168, 30, GREEN),
             ("CRC", 16, 10, RED), ("flag", 8, 9, AMBER), ("buffer", 24, 12, GRAY)]
    fig, ax = plt.subplots(figsize=(9.0, 1.7))
    x = 0
    for name, n, wd, col in parts:
        ax.add_patch(Rectangle((x + 0.2, 0.35), wd - 0.4, 0.55, fc=col, ec=col, alpha=0.15, lw=0))
        ax.add_patch(Rectangle((x + 0.2, 0.35), wd - 0.4, 0.55, fc="none", ec=col, lw=1.2))
        ax.text(x + wd / 2, 0.72, name, ha="center", va="center", fontsize=11, color=col, weight="bold")
        ax.text(x + wd / 2, 0.5, f"{n} bits", ha="center", va="center", fontsize=9.5, color=INK)
        x += wd
    ax.text(9 + 7, 0.2, "0101\u2026", ha="center", va="center", fontsize=10, color=NAVY, family="monospace")
    for x0 in (23 + 4.5, 72 + 4.5):
        ax.text(x0, 0.2, "0x7E", ha="center", va="center", fontsize=10, color=AMBER, family="monospace")
    ax.text(x / 2 + 6, 0.02, "one slot: 256 bits at 9600 b/s = 26.67 ms", ha="center", va="center", fontsize=10.5, color=INK)
    ax.set_xlim(-0.5, x + 0.5); ax.set_ylim(-0.1, 0.95); ax.axis("off")
    write("L19-burst", fig)


if __name__ == "__main__":
    burst()
