#!/usr/bin/env python3
"""L7 figures (AM and FM receivers).

  L07-fm-multiplex : the baseband a broadcast FM station puts on its carrier,
                     0 to 60 kHz: mono audio (L+R), the 19 kHz stereo pilot,
                     the stereo difference (L-R) as DSB-SC on 38 kHz, and RDS
                     on 57 kHz. A layout of the standard, not a measurement,
                     so the levels are schematic and the axis carries none.

The GNU Radio screenshots (L07-grc-*.png, L07-wbfm-rx.png, L07-rds-decoded.png,
and the rest) are not generated here: they are taken from the real flowgraphs
in book/extras/grc/ running under Xvfb on the test files that L07-fm-test-tx.grc
and L07-am-test-tx.grc write (see CLAUDE.md, "Flowgraphs"). The ones that stand
in for a live capture carry a "Simulated" label on the image.

  L07-big-picture, L07-chain-* : the L7 Lab's blocks drawn as block chains
                     (GRC block names and connections, no settings), as a 2x2
                     Big Picture grid and one picture per procedure block; PNG.

    python3 scripts/graphics/l07_figures.py
"""

from __future__ import annotations

import io
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import Polygon  # noqa: E402

from svg_font_stack import apply_font_stack  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUTS = (ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img")
NAVY, BLUE, AMBER, RED, GREEN = "#004a85", "#0067b9", "#8a5a00", "#b01e24", "#3f7d34"
GRAY, INK, RULE, PALE = "#5b6573", "#15202b", "#cddce9", "#eef4fa"
plt.rcParams.update({"svg.fonttype": "none", "font.family": "sans-serif", "font.size": 11,
                     "axes.edgecolor": GRAY, "axes.labelcolor": INK, "xtick.color": GRAY, "ytick.color": GRAY,
                     "axes.spines.top": False, "axes.spines.right": False, "axes.spines.left": False})


def write(name, fig):
    buf = io.StringIO()
    fig.savefig(buf, format="svg", transparent=True, bbox_inches="tight", pad_inches=0.06)
    plt.close(fig)
    s = apply_font_stack(buf.getvalue()[buf.getvalue().index("<svg"):])
    for out in OUTS:
        out.mkdir(parents=True, exist_ok=True)
        (out / f"{name}.svg").write_text(s, encoding="utf-8")
    print(f"wrote {name}.svg")


def fm_multiplex():
    fig, ax = plt.subplots(figsize=(8, 3.0))
    # Mono audio, 30 Hz to 15 kHz, sloping down as program audio does
    ax.add_patch(Polygon([(0.03, 0), (0.03, 0.9), (15, 0.55), (15, 0)], color=NAVY, alpha=0.85, lw=0))
    ax.text(7.5, 0.32, "L+R\n(mono audio)", ha="center", va="center", color="white", fontsize=10.5, fontweight="bold")
    # Stereo pilot
    ax.plot([19, 19], [0, 0.42], color=RED, lw=2.4)
    ax.text(19, 0.47, "pilot\n19", ha="center", va="bottom", color=RED, fontsize=10)
    # L-R as DSB-SC on 38 kHz: two mirror-image sidebands, no carrier
    ax.add_patch(Polygon([(23, 0), (23, 0.55), (37.97, 0.9), (37.97, 0)], color=BLUE, alpha=0.55, lw=0))
    ax.add_patch(Polygon([(38.03, 0), (38.03, 0.9), (53, 0.55), (53, 0)], color=BLUE, alpha=0.55, lw=0))
    ax.plot([38, 38], [0, 1.0], color=GRAY, lw=1, ls=(0, (3, 3)))
    ax.text(38, 1.04, "38 (no carrier)", ha="center", va="bottom", color=GRAY, fontsize=9.5)
    ax.text(30.5, 0.25, "L−R", ha="center", va="center", color=NAVY, fontsize=10.5, fontweight="bold")
    ax.text(45.5, 0.25, "L−R", ha="center", va="center", color=NAVY, fontsize=10.5, fontweight="bold")
    # RDS, about 2.4 kHz either side of 57 kHz
    ax.add_patch(Polygon([(54.6, 0), (55.8, 0.2), (58.2, 0.2), (59.4, 0)], color=GREEN, alpha=0.9, lw=0))
    ax.text(57, 0.25, "RDS\n57", ha="center", va="bottom", color=GREEN, fontsize=10, fontweight="bold")
    ax.set_xlim(0, 62)
    ax.set_ylim(0, 1.25)
    ax.set_yticks([])
    ax.set_xticks([0, 15, 19, 23, 38, 53, 57])
    ax.set_xlabel("frequency after the FM demodulator (kHz)")
    write("L07-fm-multiplex", fig)


# ---- block chains: how the blocks connect, with no settings shown -----------
# Drawn with l06_figures.draw_chain (Neil, 2026-11-26: each step picture shows
# the block chain only, so no lesson setting shows and no result is previewed).
FIR, XL = "Decimating\nFIR Filter", "Frequency\nXlating FIR"
WBFM = ({"src": (0, 0, "File Source"), "xl": (1, 0, XL), "qd": (2, 0, "Quadrature\nDemod"), "af": (3, 0, FIR),
         "de": (4, 0, "FM\nDeemphasis"), "vol": (5, 0, "Multiply Const"), "aud": (6, 0, "Audio Sink"),
         "mpx": (2, 1.2, "QT GUI\nFrequency Sink"), "afs": (5, 1.2, "QT GUI\nFrequency Sink")},
        [("src", "xl"), ("xl", "qd"), ("qd", "af"), ("af", "de"), ("de", "vol"), ("vol", "aud"), ("qd", "mpx"),
         ("de", "afs", [(4, 1.2)])])
CAPTURE = (dict(WBFM[0], src=(0, 0, "File Source:\nfm_capture")), WBFM[1])
AIR = ({"plu": (0, 0, "PlutoSDR\nSource"), "xl": (1, 0, XL), "qd": (2, 0, "Quadrature\nDemod"),
        "aud": (3, 0, "audio chain,\nAudio Sink"), "rs": (2, 1.2, XL), "rr": (3, 1.2, "Rational\nResampler"),
        "sy": (4, 1.2, "AGC,\nSymbol Sync"), "cr": (5, 1.2, "Constellation\nReceiver"),
        "rds": (6, 1.2, "RDS\nDecoder"),
        "plu2": (0, 2.6, "PlutoSDR\nSource"), "xl2": (1, 2.6, XL), "mag": (2, 2.6, "Complex\nto Mag"),
        "lp": (3, 2.6, FIR), "dc": (4, 2.6, "DC Blocker"), "agc": (5, 2.6, "AGC"), "aud2": (6, 2.6, "volume,\nAudio Sink")},
       [("plu", "xl"), ("xl", "qd"), ("qd", "aud"), ("qd", "rs"), ("rs", "rr"), ("rr", "sy"), ("sy", "cr"), ("cr", "rds"),
        ("plu2", "xl2"), ("xl2", "mag"), ("mag", "lp"), ("lp", "dc"), ("dc", "agc"), ("agc", "aud2")])
NOISE = ({"tone": (0, 0.75, "Signal Source"), "ac": (1, 0, "Add Const,\nscale"), "fc": (2, 0, "Float To\nComplex"),
          "amadd": (3, 0, "Add"), "amf": (4, 0, FIR), "mag": (5, 0, "Complex\nto Mag"),
          "fmm": (1, 1.5, "Frequency\nMod"), "fmadd": (3, 1.5, "Add"), "fmf": (4, 1.5, "FIR Filter"),
          "qd": (5, 1.5, "Quadrature\nDemod"), "noise": (2, 0.75, "Noise Source"),
          "sel": (6, 0.75, "audio filters,\nSelector"), "aud": (7, 0.75, "Audio Sink"), "met": (7, 1.5, "SNR meters")},
         [("tone", "ac"), ("tone", "fmm"), ("ac", "fc"), ("fc", "amadd"), ("amadd", "amf"), ("amf", "mag"),
          ("fmm", "fmadd"), ("fmadd", "fmf"), ("fmf", "qd"), ("noise", "amadd"), ("noise", "fmadd"),
          ("mag", "sel"), ("qd", "sel"), ("sel", "aud"), ("sel", "met")])


def chain_png(name, spec, width):
    from l06_figures import draw_chain
    blocks, edges = spec
    rows = max(r for _, r, _ in blocks.values()) - min(r for _, r, _ in blocks.values()) + 1
    fig, ax = plt.subplots(figsize=(width, 0.62 * rows + 0.4))
    draw_chain(ax, blocks, edges)
    fig.savefig(ROOT / "book/extras/viz/img" / f"{name}.png", dpi=130, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    print(f"wrote {name}.png")


def big_picture():
    """The lab's four blocks as a 2x2 grid of block chains."""
    from l06_figures import draw_chain
    fig, axs = plt.subplots(2, 2, figsize=(13, 6.2))
    draw_chain(axs[0, 0], *WBFM, title="Steps 1-8: build the receiver", accent=("qd",))
    draw_chain(axs[0, 1], *CAPTURE, title="Steps 9-11: your capture", accent=("src", "mpx"))
    draw_chain(axs[1, 0], *AIR, title="Steps 12-19: on the air (RDS, then ATIS)")
    draw_chain(axs[1, 1], *NOISE, title="Steps 20-23: AM and FM in noise", accent=("noise",))
    fig.tight_layout(h_pad=2.0, w_pad=2.5)
    fig.savefig(ROOT / "book/extras/viz/img/L07-big-picture.png", dpi=110, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote L07-big-picture.png")
    chain_png("L07-chain-wbfm", WBFM, 9)
    chain_png("L07-chain-capture", CAPTURE, 9)
    chain_png("L07-chain-air", AIR, 9)
    chain_png("L07-chain-noise", NOISE, 9)


if __name__ == "__main__":
    import sys
    if "--big-picture" not in sys.argv:
        fm_multiplex()
    big_picture()
