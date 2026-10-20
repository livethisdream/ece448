#!/usr/bin/env python3
"""L12 figures (CW).

  L12-paris-timing   : the word PARIS keyed on a grid of Morse units, with a
                       dit, a dah, and the 1-, 3-, and 7-unit gaps labeled;
                       50 units in all, the PARIS standard behind WPM.
  L12-decoder-windows: how the L12 decoder sorts what it measures: a mark
                       under 2 units is a dit and a longer one a dah; a space
                       under 2 units stays inside the character, 2 to 5 ends
                       the character, and 5 or more ends the word.

The GNU Radio screenshots (L12-grc-*.png, L12-tx-clicks.png, L12-link-*.png)
are not generated here: they are taken from the real flowgraphs in
book/extras/grc/ running under Xvfb (see CLAUDE.md, "Flowgraphs").

    python3 scripts/graphics/l12_figures.py
"""

from __future__ import annotations

import io
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Rectangle  # noqa: E402

from svg_font_stack import apply_font_stack  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUTS = (ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img")
NAVY, AMBER, RED, GREEN, GRAY, INK, RULE = "#004a85", "#8a5a00", "#b01e24", "#3f7d34", "#5b6573", "#15202b", "#cddce9"
plt.rcParams.update({"svg.fonttype": "none", "font.family": "sans-serif", "font.size": 11,
                     "axes.edgecolor": GRAY, "axes.labelcolor": INK, "xtick.color": GRAY, "ytick.color": GRAY,
                     "axes.spines.top": False, "axes.spines.right": False})

MORSE = {"P": ".--.", "A": ".-", "R": ".-.", "I": "..", "S": "..."}


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


def paris_timing():
    # (start, length, kind, letter) for every mark and gap of "PARIS "
    marks, gaps, letters = [], [], []
    t = 0
    for c in "PARIS":
        c0 = t
        for k, s in enumerate(MORSE[c]):
            n = 1 if s == "." else 3
            marks.append((t, n))
            t += n
            if k < len(MORSE[c]) - 1:
                gaps.append((t, 1))
                t += 1
        letters.append((c, c0, t))
        gaps.append((t, 3 if c != "S" else 7))
        t += 3 if c != "S" else 7
    total = t
    fig, ax = plt.subplots(figsize=(9.0, 2.9))
    ax.set_xlim(-0.6, total + 0.6)
    ax.set_ylim(-2.15, 2.25)
    ax.axis("off")
    for u in range(total + 1):
        ax.plot([u, u], [-0.05, 1.05], color=RULE, lw=0.6, zorder=0)
    for x0, n in marks:
        ax.add_patch(Rectangle((x0, 0), n, 1, fc=NAVY, ec="white", lw=0.8))
    ax.plot([0, total], [0, 0], color=GRAY, lw=1)
    for c, a, b in letters:
        ax.text((a + b) / 2, 1.45, c, ha="center", va="center", color=NAVY, fontsize=14, fontweight="bold")
    # labels below: one example of each element, taken from P and the end
    def brace(a, b, y, text, col):
        ax.annotate("", xy=(a, y), xytext=(b, y), arrowprops=dict(arrowstyle="<->", color=col, lw=1.1,
                                                                  shrinkA=0, shrinkB=0))
        ax.text((a + b) / 2, y - 0.42, text, ha="center", va="center", color=col, fontsize=10)
    brace(0, 1, -0.45, "dit\n1", NAVY)
    brace(2, 5, -0.45, "dah\n3", NAVY)
    brace(1, 2, -1.55, "gap in a\nletter: 1", AMBER)
    p_end = letters[0][2]
    brace(p_end, p_end + 3, -0.45, "gap between\nletters: 3", AMBER)
    s_end = letters[-1][2]
    brace(s_end, s_end + 7, -0.45, "gap between\nwords: 7", AMBER)
    ax.text(0, 2.05, f"PARIS = {total} units: one word at any speed", ha="left", va="center", color=INK,
            fontsize=11)
    write("L12-paris-timing", fig)


def decoder_windows():
    fig, axs = plt.subplots(2, 1, figsize=(8.4, 2.9), gridspec_kw=dict(hspace=0.9))
    rows = [
        ("mark", [(0, 0.3, "ignored", GRAY), (0.3, 2, "dit", NAVY), (2, 8, "dah", NAVY)], [1, 3]),
        ("space", [(0, 0.3, "ignored", GRAY), (0.3, 2, "inside a letter", AMBER), (2, 5, "end of letter", AMBER),
                   (5, 8, "end of word", AMBER)], [1, 3, 7]),
    ]
    for ax, (name, spans, ideal) in zip(axs, rows):
        ax.set_xlim(0, 8)
        ax.set_ylim(0, 1)
        ax.set_yticks([])
        ax.spines["left"].set_visible(False)
        ax.set_xticks(range(9))
        ax.set_xlabel(f"{name} length (units at the decoder's WPM)", fontsize=10, color=GRAY, labelpad=2)
        for k, (a, b, lab, col) in enumerate(spans):
            alpha = 0.12 if col == GRAY else (0.16 if k % 2 else 0.30)
            ax.add_patch(Rectangle((a, 0), b - a, 1, fc=col, ec="white", lw=1.5, alpha=alpha))
            if b - a > 0.5:
                ax.text((a + b) / 2, 0.62, lab, ha="center", va="center", color=col if col != GRAY else INK,
                        fontsize=10.5, fontweight="bold")
        for x in ideal:
            ax.plot([x, x], [0.05, 0.38], color=INK, lw=2)
            ax.text(x + 0.09, 0.22, str(x), ha="left", va="center", color=INK, fontsize=9.5)
        for x in sorted({b for _, b, _, _ in spans[:-1]}):
            ax.plot([x, x], [0, 1], color=RED, lw=1.2, ls=(0, (3, 2)))
    axs[0].text(0, 1.18, "black ticks: what a perfect sender sends; gray: under 0.3 unit, ignored as noise",
                transform=axs[0].transAxes, ha="left", va="bottom", fontsize=10, color=GRAY)
    write("L12-decoder-windows", fig)


if __name__ == "__main__":
    paris_timing()
    decoder_windows()
