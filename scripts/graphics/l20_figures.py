#!/usr/bin/env python3
"""L20 figures (QAM and OFDM).

  L20-guard   : two OFDM symbols, each with its guard (a copy of the symbol's
                end), the same two symbols arriving again as a later echo, and
                the receiver's FFT window over symbol 2. An echo that ends
                inside the guard leaves the window holding symbol 2 alone.

The GNU Radio screenshots (L20-grc-*.png, L20-qam-*.png, L20-ofdm-*.png) are not
generated here: they are taken from the real flowgraphs running under Xvfb (see
CLAUDE.md, "Flowgraphs").

    python3 scripts/graphics/l20_figures.py
"""

from __future__ import annotations

import io
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, Rectangle  # noqa: E402

from svg_font_stack import apply_font_stack  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUTS = (ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img")
NAVY, AMBER, GRAY, INK, RULE = "#004a85", "#8a5a00", "#5b6573", "#15202b", "#cddce9"
plt.rcParams.update({"svg.fonttype": "none", "font.family": "sans-serif", "font.size": 11})


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


def guard():
    # L20-ofdm-link.grc's numbers: a 64-sample symbol and a 16-sample guard.
    N, CP, ECHO = 64, 16, 8
    fig, ax = plt.subplots(figsize=(8.6, 2.9))
    ax.set_xlim(-6, 2 * (N + CP) + 22)
    ax.set_ylim(-0.85, 2.95)
    ax.axis("off")

    def row(y, x0, alpha, label):
        for k in range(2):
            s = x0 + k * (N + CP)
            ax.add_patch(Rectangle((s, y), CP, 0.62, fc=AMBER, ec="white", lw=1.5, alpha=alpha))
            ax.add_patch(Rectangle((s + CP, y), N, 0.62, fc=NAVY, ec="white", lw=1.5, alpha=alpha))
            ax.text(s + CP / 2, y + 0.31, "guard", color="white", ha="center", va="center", fontsize=9)
            ax.text(s + CP + N / 2, y + 0.31, f"symbol {k + 1}", color="white", ha="center", va="center",
                    fontsize=11, fontweight="bold")
        ax.text(x0 + 2 * (N + CP) + 3, y + 0.31, label, color=INK, ha="left", va="center")

    row(1.35, 0, 1.0, "direct")
    row(0.35, ECHO, 0.55, "echo")
    # the guard is a copy of the end of its symbol
    ax.plot([N, N, N + CP, N + CP], [2.0, 2.1, 2.1, 2.0], color=AMBER, lw=1.4)
    ax.add_patch(FancyArrowPatch((N + CP / 2, 2.12), (CP / 2, 2.02), connectionstyle="arc3,rad=0.25",
                                 arrowstyle="-|>", mutation_scale=12, color=AMBER, lw=1.4))
    ax.text((N + CP) / 2 + 4, 2.78, "copy", color=AMBER, ha="center", va="center", fontsize=10)
    # FFT window over symbol 2 of the direct path
    w0 = N + 2 * CP
    ax.plot([w0, w0, w0 + N, w0 + N], [-0.05, -0.25, -0.25, -0.05], color=INK, lw=1.4)
    ax.text(w0 + N / 2, -0.55, "FFT window", color=INK, ha="center", va="center")
    for x in (w0, w0 + N):
        ax.plot([x, x], [-0.05, 2.05], color=GRAY, lw=0.8, ls=(0, (3, 3)))
    write("L20-guard", fig)


if __name__ == "__main__":
    guard()
