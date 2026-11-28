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

  L11-key-timing   : what the Key Timer counts on the Morse "ECE" key at 1000
                     samples per second: each mark's length in key samples,
                     the 120-sample boundary between a dit and a dah, and a
                     call of work() that ends inside a dah.
  L11-lab-tree     : the gr-l11lab files the L11 Lab edits (Steps 9-12), with
                     a PNG copy for the lab's Big Picture.
  L11-big-picture  : the L11 Lab's blocks: the receiver canvas, the module
                     steps, and the link canvas (from scripts/graphics/lab_canvas.py),
                     with what the cadet records. Run with --big-picture.

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
import numpy as np

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


def key_timing():
    pat = [1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0, 0]
    key = np.repeat(pat, 60)
    n = np.arange(key.size)
    fig, ax = plt.subplots(figsize=(8.6, 2.9))
    ax.step(n, key, where="post", color=NAVY, lw=1.8)
    ax.set_ylim(-0.95, 1.85)
    ax.set_xlim(-10, key.size + 10)
    ax.set_yticks([0, 1])
    ax.set_xlabel("key sample (1000 per second)")
    ax.set_ylabel("key")
    edges = np.flatnonzero(np.diff(np.r_[0, key, 0]))
    for a, b in zip(edges[::2], edges[1::2]):
        w = b - a
        col = AMBER if w > 120 else GRAY
        ax.annotate("", (a, 1.18), (b, 1.18), arrowprops=dict(arrowstyle="<->", color=col, lw=1))
        ax.text((a + b) / 2, 1.34, f"{w}", ha="center", va="bottom", fontsize=10, color=col, fontweight="bold")
    ax.text(key.size + 5, 1.62, "samples in each mark", ha="right", va="bottom", fontsize=9.5, color=GRAY)
    ax.annotate("", (480, -0.45), (600, -0.45), arrowprops=dict(arrowstyle="|-|", color=RED, lw=1.2))
    ax.text(615, -0.45, "boundary: 120 samples; shorter is a dit, longer a dah", ha="left", va="center",
            fontsize=9.5, color=RED)
    ax.axvline(330, color=GREEN, lw=1.2, ls=(0, (4, 3)))
    ax.text(340, -0.78, "a call of work() ends here; self.run = 90 carries to the next call", ha="left",
            va="center", fontsize=9.5, color=GREEN)
    write("L11-key-timing", fig)


def lab_tree():
    rows = [
        (0, "gr-l11lab/", INK, "gr_modtool newmod l11lab"),
        (1, "grc/", INK, ""),
        (2, "l11lab_key_decoder.block.yml", NAVY, "Step 11: label, make, parameters, input"),
        (1, "python/l11lab/", INK, ""),
        (2, "key_decoder.py", NAVY, "Step 10: your class, renamed key_decoder"),
        (2, "qa_key_decoder.py", NAVY, "Step 12: your unit test"),
        (2, "CMakeLists.txt", AMBER, "Step 10: gr_python_install lists key_decoder.py"),
        (1, "build/", GRAY, "Step 13: cmake, ctest, install"),
    ]
    fig, ax = plt.subplots(figsize=(8.4, 2.9))
    n = len(rows)
    ax.set_xlim(0, 10)
    ax.set_ylim(-0.4, n)
    ax.axis("off")
    for k, (ind, name, col, note) in enumerate(rows):
        y = n - 1 - k
        x = 0.15 + 0.42 * ind
        if ind:
            ax.plot([x - 0.3, x - 0.3, x - 0.08], [y + 0.5, y, y], color=RULE, lw=1.2)
        ax.text(x, y, name, ha="left", va="center", family=MONO, fontsize=10.5, color=col,
                fontweight="bold" if col in (NAVY, AMBER) else "normal")
        if note:
            ax.text(5.0, y, note, ha="left", va="center", fontsize=10, color=AMBER if col == AMBER else GRAY)
    fig.savefig(ROOT / "book/extras/viz/img/L11-lab-tree.png", dpi=110, bbox_inches="tight", facecolor="white")
    write("L11-lab-tree", fig)


def big_picture():
    """The lab's three blocks in a row: receiver canvas, module files, link canvas."""
    img = ROOT / "book/extras/viz/img"
    fig, axs = plt.subplots(3, 1, figsize=(11, 10), gridspec_kw={"height_ratios": [1.0, 0.75, 1.0]})
    for ax, (name, title) in zip(axs, [
            ("L11-chain-rx", "Steps 1-8: run the broken chain, write the Key Decoder"),
            ("L11-lab-tree", "Steps 9-14: put it in a module, gr-l11lab"),
            ("L11-chain-link", "Steps 15-18: write the Key Encoder, send your own line")]):
        ax.imshow(plt.imread(img / f"{name}.png")); ax.axis("off")
        ax.set_title(title, color=INK, fontsize=15, fontweight="bold", loc="left")
    fig.tight_layout(h_pad=1.5)
    fig.savefig(img / "L11-big-picture.png", dpi=100, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote L11-big-picture.png")


if __name__ == "__main__":
    import sys
    if "--lab" in sys.argv:
        key_timing()
        lab_tree()
        raise SystemExit
    if "--big-picture" in sys.argv:
        big_picture()
        raise SystemExit
    oot_tree()
    block_types()
    energy_steps()
    module_zip()
