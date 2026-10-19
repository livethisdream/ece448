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


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--canvas", type=Path, help="directory of grc_canvas.sh captures to crop")
    ap.add_argument("--keep", type=Path, help="also save the uncropped window captures here")
    a = ap.parse_args()
    if a.canvas:
        canvases(a.canvas)
    else:
        with tempfile.TemporaryDirectory() as t:
            shots = capture(Path(t))
            if a.keep:
                a.keep.mkdir(parents=True, exist_ok=True)
                for name, im in shots.items():
                    im.save(a.keep / f"{name}.png")
            figures(shots)
