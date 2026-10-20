#!/usr/bin/env python3
"""L11 figures (out-of-tree modules and custom blocks), and the module zip.

  L11-oot-tree     : the gr-ece448 tree that gr_modtool makes, with the three
                     files a Python block lives in picked out, and the command
                     that writes each one.
  L11-block-types  : sync, decimator, interpolator, and general blocks as
                     input and output samples: 1:1, N:1, 1:N, and any ratio.
  L11-energy-steps : what the Energy Detector does to each run of N samples:
                     average |x|^2, convert to dB, then key on above the
                     threshold and off below the threshold minus the
                     hysteresis.

It also writes book/extras/grc/L11-gr-ece448.zip from the module tree beside
it, so the download and the tree on GitHub are the same files.

The GNU Radio screenshots (L11-grc-*.png, L11-keyed-*.png) are not generated
here: they are taken from the real flowgraphs in book/extras/grc/ running under
Xvfb (see CLAUDE.md, "Flowgraphs").

    python3 scripts/graphics/l11_figures.py
"""

from __future__ import annotations

import io
import re
import zipfile
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle  # noqa: E402

from svg_font_stack import apply_font_stack  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
OUTS = (ROOT / "book/extras/slides/fig", ROOT / "book/extras/viz/img")
TREE = ROOT / "book/extras/grc/L11-gr-ece448"
ZIP = ROOT / "book/extras/grc/L11-gr-ece448.zip"
NAVY, AMBER, RED, GREEN, GRAY, INK, RULE = "#004a85", "#8a5a00", "#b01e24", "#3f7d34", "#5b6573", "#15202b", "#cddce9"
MONO = "DejaVu Sans Mono"
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


def oot_tree():
    # (indent, name, color, note); the three files of the block are navy.
    rows = [
        (0, "gr-ece448/", INK, "gr_modtool newmod ece448"),
        (1, "CMakeLists.txt", GRAY, "finds GNU Radio, sets the install paths"),
        (1, "grc/", INK, ""),
        (2, "ece448_energy_detector.block.yml", NAVY, "how GRC shows the block"),
        (1, "python/ece448/", INK, ""),
        (2, "__init__.py", GRAY, "imports the block into gnuradio.ece448"),
        (2, "energy_detector.py", NAVY, "the block: __init__ and work()"),
        (2, "qa_energy_detector.py", NAVY, "the unit test ctest runs"),
        (2, "CMakeLists.txt", GRAY, "lists the files to install and test"),
        (1, "include/, lib/, python/ece448/bindings/", GRAY, "C++ only; unused here"),
        (1, "apps/, docs/, examples/, cmake/", GRAY, ""),
    ]
    fig, ax = plt.subplots(figsize=(8.4, 3.9))
    n = len(rows)
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.9, n)
    ax.axis("off")
    for k, (ind, name, col, note) in enumerate(rows):
        y = n - 1 - k
        x = 0.15 + 0.42 * ind
        if ind:
            ax.plot([x - 0.3, x - 0.3, x - 0.08], [y + 0.5, y, y], color=RULE, lw=1.2)
        ax.text(x, y, name, ha="left", va="center", family=MONO, fontsize=10.5, color=col,
                fontweight="bold" if col == NAVY else "normal")
        if note:
            ax.text(5.75, y, note, ha="left", va="center", fontsize=10, color=AMBER if k == 0 else GRAY)
    ax.text(5.75, -0.75, "gr_modtool add writes the three navy files", ha="left", va="center",
            fontsize=10, color=NAVY, fontweight="bold")
    write("L11-oot-tree", fig)


def block_types():
    fig, axes = plt.subplots(1, 4, figsize=(8.6, 2.5))
    specs = [("sync", "1 in : 1 out", 6, 6), ("decimator", "N in : 1 out", 8, 2),
             ("interpolator", "1 in : N out", 2, 8), ("general", "any ratio", 6, 3)]
    for ax, (name, ratio, nin, nout) in zip(axes, specs):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.axis("off")
        ax.add_patch(FancyBboxPatch((2.3, 3.4), 5.4, 3.2, boxstyle="round,pad=0.1", fc="#eef4fa", ec=NAVY, lw=1.2))
        ax.text(5, 5, name, ha="center", va="center", color=NAVY, fontsize=9.5, fontweight="bold")
        for i in range(nin):
            ax.plot(0.5, 1 + 8 * (i + 0.5) / nin, "o", ms=4.5, color=GRAY)
        for i in range(nout):
            ax.plot(9.5, 1 + 8 * (i + 0.5) / nout, "o", ms=4.5, color=AMBER)
        ax.add_patch(FancyArrowPatch((0.9, 5), (2.2, 5), arrowstyle="-|>", mutation_scale=10, color=GRAY))
        ax.add_patch(FancyArrowPatch((7.8, 5), (9.1, 5), arrowstyle="-|>", mutation_scale=10, color=GRAY))
        ax.text(5, -0.4, ratio, ha="center", va="center", fontsize=10, color=INK)
    write("L11-block-types", fig)


def energy_steps():
    fig, ax = plt.subplots(figsize=(8.6, 2.2))
    ax.set_xlim(0, 21)
    ax.set_ylim(0, 4)
    ax.axis("off")
    steps = [("N complex\nsamples", GRAY), ("average\n|x|²", NAVY), ("10 log₁₀", NAVY),
             ("compare with\nthe levels", NAVY), ("key\n0 or 1", AMBER)]
    w, gap = 3.3, 1.0
    for k, (s, col) in enumerate(steps):
        x = 0.2 + k * (w + gap)
        ax.add_patch(FancyBboxPatch((x, 1.2), w, 1.9, boxstyle="round,pad=0.08",
                                    fc="#eef4fa" if col == NAVY else "#ffffff", ec=col, lw=1.2))
        ax.text(x + w / 2, 2.15, s, ha="center", va="center", fontsize=9.5, color=col, fontweight="bold")
        if k < len(steps) - 1:
            ax.add_patch(FancyArrowPatch((x + w + 0.1, 2.15), (x + w + gap - 0.1, 2.15), arrowstyle="-|>",
                                         mutation_scale=10, color=GRAY))
    ax.text(0.2 + 2 * (w + gap) + w / 2, 0.55, "power output (dB)", ha="center", va="center", fontsize=10, color=NAVY)
    ax.text(0.2 + 4 * (w + gap) + w / 2, 0.55, "key output", ha="center", va="center", fontsize=10, color=AMBER)
    ax.add_patch(Rectangle((0.2 + w + gap - 0.15, 0.95), 2 * w + gap + 0.3, 2.4, fc="none", ec=RULE, lw=1, ls=(0, (3, 3))))
    ax.text(0.2 + w + gap + w + gap / 2, 3.65, "one output per N inputs", ha="center", va="center", fontsize=10, color=GRAY)
    write("L11-energy-steps", fig)


def module_zip():
    """Zip the tree with fixed timestamps, so an unchanged tree gives an unchanged zip."""
    files = sorted(p for p in TREE.rglob("*") if p.is_file() and "__pycache__" not in p.parts
                   and not p.relative_to(TREE).parts[0].startswith("build"))
    with zipfile.ZipFile(ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for p in files:
            info = zipfile.ZipInfo("gr-ece448/" + p.relative_to(TREE).as_posix(), date_time=(2026, 10, 20, 0, 0, 0))
            info.external_attr = 0o644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, p.read_bytes())
    print(f"wrote {ZIP.name}: {len(files)} files")


if __name__ == "__main__":
    oot_tree()
    block_types()
    energy_steps()
    module_zip()
