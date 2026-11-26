#!/usr/bin/env python3
"""L6 figures (AM simulation): real GNU Radio screenshots, cropped.

Every L6 figure comes from the three flowgraphs in book/extras/grc/ running
under GNU Radio 3.10, none of which needs hardware:

  L06-am-spectrum, L06-am-envelope, L06-am-overmod   L06-dsb-am.grc at m = 0.5 and 1.4
  L06-sc-spectrum, L06-sc-mixer, L06-sc-phi0/phi90  L06-dsb-sc.grc at LO phase 0 and 90
  L06-ssb-spectra, L06-ssb-mistuned                  L06-ssb.grc, USB and LSB, and 200 Hz off
  L06-grc-dsb-am, L06-grc-ssb                        the GRC canvas (scripts/grc/grc_canvas.sh)

The running windows are captured the way scripts/grc/grc_shot.py does it, but
at 1060x900 (1060x1260 for DSB-SC's four plots), because grc_shot's 1060x560
window scrolls them. Each flowgraph ends in an Audio Sink; the capture points
ALSA at its null device so the sink opens in a container with no sound card.

Run it under Xvfb with the GNU Radio Python:

    xvfb-run -a -s "-screen 0 1400x1000x24" /usr/bin/python3.12 scripts/graphics/l06_figures.py

The GRC canvas shots need GRC's window at 1280x820 with its side panels hidden
(main_window_width/height = 1280/820, console_window_visible,
blocks_window_visible, and variable_editor_visable = False in the [main]
section of ~/.gnuradio/grc.conf), then

    xvfb-run -a -s "-screen 0 1280x820x24" scripts/grc/grc_canvas.sh book/extras/grc/L06-ssb.grc grc-ssb.png

and are cropped here with --canvas DIR, where DIR holds grc-dsb-am.png
and grc-ssb.png.

  L06-big-picture, L06-chain-* : the L6 Lab's blocks drawn as block chains
                    (GRC block names and connections, no settings), as a 2x2
                    Big Picture grid and one picture per procedure block.
                    Needs neither Xvfb nor GNU Radio:

    python3 scripts/graphics/l06_figures.py --big-picture
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUTS = (ROOT / "book/extras/viz/img", ROOT / "book/extras/slides/img/06-am-simulation")
W, H = 1060, 900
# DSB-SC has a fourth row, the receiver mixer's spectrum, so its window is taller.
HEIGHT = {"L06-dsb-sc": 1260}

# Window rows (top, bottom), measured on the captures: the control row, the
# frequency sink, and the time sinks, plus DSB-SC's mixer spectrum. Each
# control band keeps a few pixels of margin above the slider labels.
AM_CTRL, AM_SPEC, AM_TIME = (20, 62), (0, 360), (365, 870)
CTRL, SPEC, TIME = (12, 58), (0, 445), (445, 870)
SC_SPEC, SC_TIME, SC_MIX = (0, 432), (432, 862), (862, 1245)

# (flowgraph, capture name, variable settings)
RUNS = [
    ("L06-dsb-am", "am-m05", {"m": 0.5}),
    ("L06-dsb-am", "am-m14", {"m": 1.4}),
    ("L06-dsb-sc", "sc-phi0", {"phi": 0}),
    ("L06-dsb-sc", "sc-phi90", {"phi": 90}),
    ("L06-ssb", "ssb-usb", {}),
    ("L06-ssb", "ssb-lsb", {"sideband": -1}),
    ("L06-ssb", "ssb-df", {"df": 200}),
]

SHOT = """
import os, sys, importlib.util
from PyQt5 import Qt
spec = importlib.util.spec_from_file_location("fg", sys.argv[1]); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
cls = [v for v in vars(m).values() if isinstance(v, type) and issubclass(v, Qt.QWidget) and hasattr(v, 'start')][0]
app = Qt.QApplication(sys.argv[:1]); tb = cls()
for kv in sys.argv[3:]:
    k, v = kv.split('=')
    win = getattr(tb, '_' + k + '_win', None)
    boxes = win.findChildren(Qt.QDoubleSpinBox) if win is not None else []
    boxes[0].setValue(float(v)) if boxes else getattr(tb, 'set_' + k)(float(v))
tb.resize(%d, int(os.environ['SHOT_H'])); tb.start(); tb.show()
def done():
    tb.grab().save(sys.argv[2]); tb.stop(); tb.wait(); app.quit()
Qt.QTimer.singleShot(3000, done); app.exec_()
""" % W


def capture(tmp: Path) -> dict:
    """Compile each flowgraph, run it headless, and return the captures by name."""
    (tmp / "shot.py").write_text(SHOT)
    (tmp / "asound.conf").write_text("pcm.!default { type null }\nctl.!default { type hw card 0 }\n")
    env = {**os.environ, "ALSA_CONFIG_PATH": str(tmp / "asound.conf")}
    for fg in sorted({r[0] for r in RUNS}):
        subprocess.run([sys.executable, "/usr/bin/grcc", "-o", str(tmp), str(ROOT / f"book/extras/grc/{fg}.grc")],
                       check=True, capture_output=True)
    from PIL import Image
    shots = {}
    for fg, name, sets in RUNS:
        out = tmp / f"{name}.png"
        py = tmp / (fg.replace("-", "_") + ".py")
        subprocess.run([sys.executable, str(tmp / "shot.py"), str(py), str(out)] + [f"{k}={v}" for k, v in sets.items()],
                       check=True, capture_output=True, env={**env, "SHOT_H": str(HEIGHT.get(fg, H))})
        shots[name] = Image.open(out).convert("RGB")
        print("captured", name)
    return shots


def stack(parts):
    from PIL import Image
    o = Image.new("RGB", (max(p.size[0] for p in parts), sum(p.size[1] for p in parts)), (239, 239, 239))
    y = 0
    for p in parts:
        o.paste(p, (0, y))
        y += p.size[1]
    return o


def save(name, im):
    for out in OUTS:
        out.mkdir(parents=True, exist_ok=True)
        im.save(out / f"{name}.png")
    print(f"wrote {name}.png")


def figures(s):
    band = lambda im, r: im.crop((0, r[0], W, r[1]))
    save("L06-am-spectrum", band(s["am-m05"], AM_SPEC))
    save("L06-am-envelope", stack([band(s["am-m05"], AM_CTRL), band(s["am-m05"], AM_TIME)]))
    save("L06-am-overmod", stack([band(s["am-m14"], AM_CTRL), band(s["am-m14"], AM_TIME)]))
    save("L06-sc-spectrum", band(s["sc-phi0"], SC_SPEC))
    save("L06-sc-mixer", stack([band(s["sc-phi0"], CTRL), band(s["sc-phi0"], SC_MIX)]))
    for k in ("sc-phi0", "sc-phi90"):
        save(f"L06-{k}", stack([band(s[k], CTRL), band(s[k], SC_TIME)]))
    save("L06-ssb-spectra", stack([band(s["ssb-usb"], SPEC), band(s["ssb-lsb"], SPEC)]))
    save("L06-ssb-mistuned", stack([band(s["ssb-df"], CTRL), band(s["ssb-df"], TIME)]))


def canvases(src: Path):
    """Crop GRC canvas captures: drop the menu and toolbar, then trim the blank canvas."""
    from PIL import Image, ImageOps
    for n in ("dsb-am", "ssb"):
        g = Image.open(src / f"grc-{n}.png").convert("RGB").crop((0, 66, 1280, 816))
        bb = ImageOps.invert(g.convert("L")).point(lambda v: 255 if v > 8 else 0).getbbox()
        save(f"L06-grc-{n}", g.crop((0, 0, min(1280, bb[2] + 8), min(750, bb[3] + 8))))


# ---- block chains: how the blocks connect, with no settings shown -----------
# Each lab block's picture is its flowgraph drawn as named GRC blocks and the
# connections between them (Neil, 2026-11-26: "crop each step picture to the
# block chain only", so no lesson setting shows and no result is previewed).
BW, BH, DX = 1.75, 0.62, 2.15          # box width and height, column spacing


def _clip(c, toward):
    """Where the segment from box center c toward a point leaves the box."""
    import math
    (x0, y0), (x1, y1) = c, toward
    dx, dy = x1 - x0, y1 - y0
    if dx == 0 and dy == 0:
        return c
    t = min((BW / 2) / abs(dx) if dx else math.inf, (BH / 2) / abs(dy) if dy else math.inf)
    return (x0 + t * dx, y0 + t * dy)


def draw_chain(ax, blocks, edges, title=None, accent=()):
    """blocks: {key: (col, row, label)}; edges: (a, b) or (a, b, [(col,row) bends])."""
    from matplotlib.patches import FancyBboxPatch
    pos = {k: (c * DX, -r) for k, (c, r, _) in blocks.items()}
    for e in edges:
        a, b = e[0], e[1]
        pts = [pos[a]] + [(c * DX, -r) for c, r in (e[2] if len(e) > 2 else [])] + [pos[b]]
        pts[0] = _clip(pos[a], pts[1])
        pts[-1] = _clip(pos[b], pts[-2])
        xs, ys = zip(*pts)
        ax.plot(xs[:-1] + (xs[-1],), ys, color="#5b6573", lw=1.1, solid_capstyle="butt")
        ax.annotate("", xy=pts[-1], xytext=pts[-2],
                    arrowprops=dict(arrowstyle="-|>", color="#5b6573", lw=1.1, mutation_scale=9))
    xs = [v[0] for v in pos.values()]; ys = [v[1] for v in pos.values()]
    ax.set_xlim(min(xs) - BW / 2 - 0.15, max(xs) + BW / 2 + 0.15)
    ax.set_ylim(min(ys) - BH / 2 - 0.15, max(ys) + BH / 2 + 0.15)
    ax.set_aspect("equal"); ax.axis("off")
    # Size the labels to the boxes as drawn, so every panel reads alike.
    ax.apply_aspect()
    bb = ax.get_window_extent()
    ppu = min(bb.width / (ax.get_xlim()[1] - ax.get_xlim()[0]), bb.height / (ax.get_ylim()[1] - ax.get_ylim()[0]))
    fs = min(10.5, BW * ppu * 0.92 / (15 * 0.47) * 72 / ax.figure.dpi)
    for k, (c, r, label) in blocks.items():
        x, y = pos[k]
        hot = k in accent
        ax.add_patch(FancyBboxPatch((x - BW / 2, y - BH / 2), BW, BH, boxstyle="round,pad=0.02,rounding_size=0.08",
                                    fc="#fde9c8" if hot else "#e8f0f8", ec="#b06b00" if hot else "#004a85", lw=1.1))
        ax.text(x, y, label, ha="center", va="center", fontsize=fs, color="#15202b", linespacing=1.0)
    if title:
        ax.set_title(title, color="#15202b", fontsize=12, fontweight="bold", loc="left")


SS, MC, FIR = "Signal Source", "Multiply Const", "Decimating\nFIR Filter"

DSB_AM = ({"s1": (0, 0, SS), "s2": (0, 1, SS), "add": (1, 0.5, "Add"), "mc": (2, 0.5, MC),
           "ac": (3, 0.5, "Add Const"), "mul": (4, 0.5, "Multiply"), "car": (4, -0.7, SS),
           "fsk": (5, 0.5, "QT GUI\nFrequency Sink"), "dly": (3, 1.7, "Delay"), "tsk": (5, 1.7, "QT GUI\nTime Sink"),
           "abs": (0, 2.9, "Abs"), "fir": (1, 2.9, FIR), "pi": (2, 2.9, MC), "dcb": (3, 2.9, "DC Blocker"),
           "vol": (4, 2.9, MC), "aud": (5, 2.9, "Audio Sink")},
          [("s1", "add"), ("s2", "add"), ("add", "mc"), ("mc", "ac"), ("ac", "mul"), ("car", "mul"), ("mul", "fsk"),
           ("ac", "dly"), ("dly", "tsk"), ("mul", "abs", [(4.5, 0.5), (4.5, 2.25), (0, 2.25)]), ("abs", "fir"), ("fir", "pi"),
           ("pi", "dcb"), ("dcb", "vol"), ("vol", "aud"), ("pi", "tsk", [(2, 2.42), (5.45, 2.42), (5.45, 1.7)])])

DSB_SC = ({"s1": (0, 0, SS), "s2": (0, 1, SS), "add": (1, 0.5, "Add"), "mul": (2, 0.5, "Multiply"),
           "car": (2, -0.7, SS), "fsk": (3, -0.7, "QT GUI\nFrequency Sink"),
           "prod": (3, 0.5, "Multiply"), "lo": (3, 1.7, SS), "cl": (4, 0.5, FIR), "x2": (5, 0.5, MC),
           "rect": (3, 2.9, "Abs"), "el": (4, 2.9, FIR), "pi": (5, 2.9, MC),
           "sel": (6, 1.7, "Selector"), "tsk": (6, 0.5, "QT GUI\nTime Sink"), "aud": (6, 2.9, "DC Blocker,\nvolume, Audio Sink")},
          [("s1", "add"), ("s2", "add"), ("add", "mul"), ("car", "mul"), ("mul", "fsk"), ("mul", "prod"), ("lo", "prod"),
           ("prod", "cl"), ("cl", "x2"), ("mul", "rect", [(2, 2.9)]), ("rect", "el"), ("el", "pi"),
           ("x2", "sel"), ("pi", "sel"), ("x2", "tsk"), ("sel", "aud")])

SSB = ({"s1": (0, 0, SS), "s2": (0, 1, SS), "add": (1, 0.5, "Add"), "hil": (2, 0.5, "Hilbert"),
        "mul": (3, 0.5, "Multiply"), "car": (3, -0.7, SS), "re": (4, 0.5, "Complex\nTo Real"),
        "fsk": (5, -0.7, "QT GUI\nFrequency Sink"), "prod": (5, 0.5, "Multiply"), "lo": (5, 1.7, SS),
        "lpf": (6, 0.5, FIR), "x2": (7, 0.5, MC), "tsk": (7, 1.7, "QT GUI\nTime Sink"), "aud": (7, -0.7, "volume,\nAudio Sink")},
       [("s1", "add"), ("s2", "add"), ("add", "hil"), ("hil", "mul"), ("car", "mul"), ("mul", "re"), ("re", "fsk"),
        ("re", "prod"), ("lo", "prod"), ("prod", "lpf"), ("lpf", "x2"), ("x2", "tsk"), ("x2", "aud")])


def chain_fig(name, spec, width):
    import io
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    blocks, edges = spec
    rows = max(r for _, r, _ in blocks.values()) - min(r for _, r, _ in blocks.values()) + 1
    fig, ax = plt.subplots(figsize=(width, 0.62 * rows + 0.4))
    draw_chain(ax, blocks, edges)
    img = ROOT / "book/extras/viz/img"
    fig.savefig(img / f"{name}.png", dpi=130, bbox_inches="tight", pad_inches=0.05, facecolor="white")
    plt.close(fig)
    print(f"wrote {name}.png")


def big_picture():
    """The lab's three blocks as a 2x2 grid of block chains, plus the lab's own legend panel."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, axs = plt.subplots(2, 2, figsize=(13, 6.6))
    draw_chain(axs[0, 0], *DSB_AM, title="Steps 1-10: build DSB-AM")
    draw_chain(axs[0, 1], *DSB_SC, title="Steps 11-14: receive DSB-SC")
    draw_chain(axs[1, 0], *SSB, title="Steps 15-17: receive SSB")
    ax = axs[1, 1]; ax.axis("off")
    ax.set_title("What you record", color="#15202b", fontsize=12, fontweight="bold", loc="left")
    for i, t in enumerate(["Figure 1: your DSB-AM flowgraph and its window",
                           "Figure 2: the DSB-AM, DSB-SC, and LSB spectra",
                           "Figure 3: the DSB-SC time sink at an LO phase error",
                           "Table B: the coherent output's peak",
                           "Table B: the largest tuning error you cannot hear"]):
        ax.text(0.02, 0.85 - 0.15 * i, t, fontsize=11.5, color="#15202b", transform=ax.transAxes, va="center")
    fig.tight_layout(h_pad=2.0, w_pad=2.5)
    fig.savefig(ROOT / "book/extras/viz/img/L06-big-picture.png", dpi=110, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote L06-big-picture.png")
    chain_fig("L06-chain-dsb-am", DSB_AM, 8)
    chain_fig("L06-chain-dsb-sc", DSB_SC, 9)
    chain_fig("L06-chain-ssb", SSB, 10)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--big-picture", action="store_true", help="only draw the L6 Lab's Big Picture grid and block chains")
    ap.add_argument("--canvas", type=Path, help="directory of grc_canvas.sh captures to crop")
    ap.add_argument("--keep", type=Path, help="also save the uncropped window captures here")
    a = ap.parse_args()
    if a.big_picture:
        big_picture()
    elif a.canvas:
        canvases(a.canvas)
    else:
        with tempfile.TemporaryDirectory() as t:
            shots = capture(Path(t))
            if a.keep:
                a.keep.mkdir(parents=True, exist_ok=True)
                for name, im in shots.items():
                    im.save(a.keep / f"{name}.png")
            figures(shots)
