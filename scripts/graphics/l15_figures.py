#!/usr/bin/env python3
"""L15 figures (mPSK).

  L15-8psk-map     : the L15 8PSK constellation: phase index i at 22.5 + 45i
                     degrees, and the Gray label each point carries
  L15-costas       : the Costas Loop as a block diagram: rotate, decide the
                     phase error, filter it, and update the phase estimate

The GNU Radio screenshots (L15-grc-*.png, L15-tx-*.png, L15-link-*.png,
L15-pluto-sim.png) are not generated here: they are taken from the real
flowgraphs running under Xvfb (see CLAUDE.md, "Flowgraphs").

    python3 scripts/graphics/l15_figures.py
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
from matplotlib.patches import FancyBboxPatch  # noqa: E402

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


def map_8psk():
    fig, ax = plt.subplots(figsize=(4.6, 4.6))
    ax.set_aspect("equal")
    ax.set_xlim(-1.8, 1.9)
    ax.set_ylim(-1.75, 1.75)
    for s in ("left", "bottom"):
        ax.spines[s].set_position("zero")
        ax.spines[s].set_color(RULE)
    ax.set_xticks([])
    ax.set_yticks([])
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(np.cos(th), np.sin(th), color=RULE, lw=1, ls=(0, (3, 3)), zorder=0)
    gray = [i ^ (i >> 1) for i in range(8)]
    for i in range(8):
        a = math.pi / 8 + math.pi / 4 * i
        ax.scatter([math.cos(a)], [math.sin(a)], s=60, color=NAVY, zorder=3)
        ax.text(1.36 * math.cos(a), 1.36 * math.sin(a), f"{gray[i]:03b}", ha="center", va="center",
                color=NAVY, fontsize=13, fontweight="bold", family="monospace")
        ax.text(0.74 * math.cos(a), 0.74 * math.sin(a), str(i), ha="center", va="center", color=AMBER, fontsize=11)
    ax.text(1.85, -0.12, "I", color=GRAY, ha="right", va="top")
    ax.text(0.08, 1.72, "Q", color=GRAY, ha="left", va="top")
    print("  8PSK phase index -> Gray label:", [f"{i}:{gray[i]:03b}" for i in range(8)])
    print("  8PSK Gray value -> phase index (the transmitter's Map):", [gray.index(b) for b in range(8)])
    write("L15-8psk-map", fig)


def costas():
    fig, ax = plt.subplots(figsize=(8.4, 2.7))
    ax.set_xlim(0, 10.4)
    ax.set_ylim(0, 3.0)
    ax.axis("off")

    def box(x, y, w, h, text):
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.12",
                                    fc="#eef4fa", ec=NAVY, lw=1.6))
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", color=INK, fontsize=10.5)

    def arrow(x0, y0, x1, y1):
        ax.annotate("", (x1, y1), (x0, y0), arrowprops=dict(arrowstyle="-|>", color=GRAY, lw=1.5, shrinkA=0, shrinkB=0))

    def line(xs, ys):
        ax.plot(xs, ys, color=GRAY, lw=1.5, solid_capstyle="butt")

    box(1.5, 1.9, 2.2, 0.8, "rotate back\nby the estimate")
    box(7.0, 0.25, 2.4, 0.8, "phase error\n(order M)")
    box(4.3, 0.25, 2.0, 0.8, "loop filter")
    box(1.5, 0.25, 2.2, 0.8, "phase estimate")
    ax.text(0.0, 2.3, "symbols\nin", ha="left", va="center", color=GRAY, fontsize=10)
    arrow(0.75, 2.3, 1.5, 2.3)
    arrow(3.7, 2.3, 9.2, 2.3)
    ax.text(9.3, 2.3, "symbols\nout", ha="left", va="center", color=GRAY, fontsize=10)
    line([8.2, 8.2], [2.3, 1.4])
    arrow(8.2, 1.4, 8.2, 1.05)
    arrow(7.0, 0.65, 6.3, 0.65)
    arrow(4.3, 0.65, 3.7, 0.65)
    arrow(2.6, 1.05, 2.6, 1.9)
    line([5.3, 5.3], [1.05, 1.5])
    ax.text(5.3, 1.62, "frequency estimate", ha="center", va="bottom", color=GRAY, fontsize=10)
    write("L15-costas", fig)


if __name__ == "__main__":
    map_8psk()
    costas()
