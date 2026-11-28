#!/usr/bin/env python3
"""Lab step pictures (L6, L7, L8, L10, L11): GNU Radio Companion canvases, block chain only.

Neil, 2026-11-26: each lab step picture shows how the blocks connect, from
GRC itself. The flowgraphs pictured are the lab's own builds, in
scripts/graphics/lab_grc/ (not published to the site):

  L06-lab-dsb-am, -dsb-sc, -ssb  the L6 flowgraphs with the lab's message
                                 (1.5 and 2.25 kHz, 0.5 each)
  L07-lab-wbfm, -capture         the receiver the cadet builds (decimate by 5,
                                 then 10); the Quadrature Demod gain is left as
                                 qd_gain, a Part 1 answer, so GRC marks it red
  L07-lab-rds-air, -am-air       L07-rds-rx.grc and L07-am-rx.grc switched to
                                 the PlutoSDR Source, as the cadet runs them
  L07-am-vs-fm                   book/extras/grc/L07-am-vs-fm.grc as shipped
  L08-lab-view                   the flowgraph that reads the tones and the
                                 symbol rate off the L8 Lab recording
  L08-lab-decoder                the decoder the cadet builds for that recording,
                                 with f_center, dev, and baud left undefined:
                                 the cadet sets them from the recording
  L11-lab-rx, L11-lab-link       book/extras/grc/ as shipped, with the Key
                                 Decoder's work() (and the Key Encoder's
                                 make_key()) still empty; the sliders, msg,
                                 and the Received label and its probe stay
                                 in view (KEEP)
  L08-lab-offset                 that decoder with the offset the cadet adds (a
                                 Signal Source at a random, unshown frequency and
                                 a Multiply) and the RX tuning slider that moves
                                 the Frequency Xlating FIR Filter's center
  L10-pam-pluto                  book/extras/grc/ as shipped, as three
                                 crops (CLUSTERS) for the L10 Lab's polarity,
                                 oscillator, and level blocks

For each, a copy moves the Options, variable, and import blocks off the
visible canvas, GRC is screenshot with scripts/grc/grc_canvas.sh, and the
image is cropped to the blocks that remain. Run under the GNU Radio Python:

    /usr/bin/python3.12 scripts/graphics/lab_canvas.py
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

import yaml
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[2]
LAB = ROOT / "scripts/graphics/lab_grc"
IMG = ROOT / "book/extras/viz/img"
W, H = 2400, 1500
SHOTS = {
    "L06-canvas-dsb-am": LAB / "L06-lab-dsb-am.grc",
    "L06-canvas-dsb-sc": LAB / "L06-lab-dsb-sc.grc",
    "L06-canvas-ssb": LAB / "L06-lab-ssb.grc",
    "L07-canvas-wbfm": LAB / "L07-lab-wbfm.grc",
    "L07-canvas-capture": LAB / "L07-lab-capture.grc",
    "L07-canvas-rds-air": LAB / "L07-lab-rds-air.grc",
    "L07-canvas-am-air": LAB / "L07-lab-am-air.grc",
    "L07-canvas-am-vs-fm": ROOT / "book/extras/grc/L07-am-vs-fm.grc",
    "L08-canvas-view": LAB / "L08-lab-view.grc",
    "L08-canvas-decoder": LAB / "L08-lab-decoder.grc",
    "L11-canvas-rx": ROOT / "book/extras/grc/L11-lab-rx.grc",
    "L11-canvas-link": ROOT / "book/extras/grc/L11-lab-link.grc",
    "L11-chain-rx": ROOT / "book/extras/grc/L11-lab-rx.grc",       # signal blocks only, for
    "L11-chain-link": ROOT / "book/extras/grc/L11-lab-link.grc",   # the lab's Big Picture
    "L08-canvas-offset": LAB / "L08-lab-offset.grc",
}


# Crops of L10-pam-pluto.grc for the L10 Lab's procedure blocks: the named blocks
# are laid out near the origin, sliders and switches included, and every other
# block drops far below the canvas, so its wires leave the picture downward and
# no port is left unconnected (which GRC would draw red). {name: (ymax, {block: (x, y)})}
L10 = ROOT / "book/extras/grc/L10-pam-pluto.grc"
CLUSTERS = {
    "L10-canvas-polarity": (540, {
        "polarity": (770, 8), "digital_symbol_sync_xx_0": (8, 200), "digital_costas_loop_cc_0": (330, 220),
        "blocks_complex_to_real_0": (575, 240), "blocks_multiply_const_vxx_1": (770, 240),
        "digital_binary_slicer_fb_0": (970, 245), "qtgui_const_sink_x_1": (8, 420),
        "qtgui_const_sink_x_0": (575, 400)}),
    # tx_err stays off the picture: GRC would print the random draw it made.
    "L10-canvas-oscillator": (580, {
        "tx_error": (8, 8), "rx_tune": (560, 8),
        "rational_resampler_xxx_0": (8, 210), "iio_pluto_sink_0": (250, 190),
        "iio_pluto_source_0": (560, 180), "rational_resampler_xxx_1": (820, 220),
        "qtgui_freq_sink_x_0": (820, 400)}),
    "L10-canvas-level": (560, {
        "tx_atten": (8, 8), "rx_gain": (330, 8),
        "rational_resampler_xxx_0": (8, 170), "iio_pluto_sink_0": (250, 150),
        "iio_pluto_source_0": (560, 150), "rational_resampler_xxx_1": (820, 190),
        "analog_agc2_xx_0": (1060, 190), "qtgui_time_sink_x_0": (820, 380)}),
}


def cluster(src: Path, dst: Path, place: dict):
    """Copy a flowgraph with the named blocks placed as given and every other block,
    the Options block included, dropped below the visible canvas."""
    d = yaml.safe_load(src.read_text())
    for b in d["blocks"]:
        if b["name"] in place:
            b["states"]["coordinate"] = list(place[b["name"]])
        else:
            x, y = b["states"]["coordinate"]
            b["states"]["coordinate"] = [x, y + H + 600]
    d["options"]["states"]["coordinate"] = [W + 600, H + 600]
    dst.write_text(yaml.safe_dump(d, sort_keys=False))


# Variable blocks a lab step names, kept on the canvas for that picture.
KEEP = {
    "L11-canvas-rx": {"threshold", "hyst", "rx_text", "rx_label"},
    "L11-canvas-link": {"threshold", "hyst", "noise", "msg", "rx_text", "rx_label"},
}


def offstage(src: Path, dst: Path, keep=frozenset()):
    """Copy a flowgraph with its Options, variable, and import blocks moved off screen."""
    d = yaml.safe_load(src.read_text())
    for b in d["blocks"]:
        if b["name"] in keep:
            continue
        if b["id"].startswith("variable") or b["id"] in ("import",):
            b["states"]["coordinate"] = [W + 400, H + 400]
    d["options"]["states"]["coordinate"] = [W + 600, H + 600]
    dst.write_text(yaml.safe_dump(d, sort_keys=False))


def shoot(name: str, grc: Path, tmp: Path, ymax: int | None = None, place: dict | None = None):
    g = tmp / grc.name
    if place:
        cluster(grc, g, place)
    else:
        offstage(grc, g, KEEP.get(name, frozenset()))
    raw = tmp / f"{name}-raw.png"
    for _ in range(4):                  # GRC under Xvfb now and then dies at start-up; try again
        raw.unlink(missing_ok=True)
        subprocess.run(["xvfb-run", "-a", "-s", f"-screen 0 {W}x{H}x24",
                        str(ROOT / "scripts/grc/grc_canvas.sh"), str(g), str(raw), f"{W}x{H}"])
        if raw.exists() and raw.stat().st_size > 20000:
            break
    else:
        raise SystemExit(f"GRC did not render {grc.name}")
    im = Image.open(raw).convert("RGB").crop((0, 70, W, H if ymax is None else 70 + ymax))  # drop the menu and toolbar
    bb = ImageOps.invert(im.convert("L")).point(lambda v: 255 if v > 12 else 0).getbbox()
    im = im.crop((max(0, bb[0] - 10), max(0, bb[1] - 10), min(im.width, bb[2] + 50), min(im.height, bb[3] + 10)))
    im.save(IMG / f"{name}.png")
    print(f"wrote {name}.png {im.size}")


def decoder_props(tmp: Path):
    """L11-decoder-props: the Key Decoder's properties dialog once boundary and gap
    are arguments, with placeholder zeros (no lab values), from GRC itself."""
    d = yaml.safe_load((ROOT / "book/extras/grc/L11-lab-rx.grc").read_text())
    for b in d["blocks"]:
        if b["name"] == "decoder":
            b["parameters"]["_source_code"] = b["parameters"]["_source_code"].replace(
                "def __init__(self):", "def __init__(self, boundary=0, gap=0):")
            b["parameters"].update(boundary="0", gap="0")
            b["states"]["_io_cache"] = ("('Key Decoder', 'blk', [('boundary', '0'), ('gap', '0')], "
                                        "[('0', 'float', 1)], [], '', [])")
            b["states"]["coordinate"] = [100, 100]
        else:
            b["states"]["coordinate"] = [3000, 3000]
    d["options"]["states"]["coordinate"] = [3200, 3200]
    d["connections"] = []
    g = tmp / "props.grc"
    g.write_text(yaml.safe_dump(d, sort_keys=False))
    raw = tmp / "props.png"
    sh = tmp / "props.sh"
    sh.write_text(f"""#!/bin/bash
export NO_AT_BRIDGE=1
/usr/bin/python3.12 /usr/bin/gnuradio-companion {g} >/dev/null 2>&1 &
for i in $(seq 1 40); do sleep 0.5; W=$(xdotool search --name "GNU Radio Companion" 2>/dev/null | head -1); [ -n "$W" ] && break; done
sleep 4
xdotool mousemove 140 198 click --repeat 2 --delay 80 1; sleep 3
xwd -root -silent | convert xwd:- {raw}
""")
    sh.chmod(0o755)
    for _ in range(4):                  # GRC under Xvfb now and then dies at start-up; try again
        raw.unlink(missing_ok=True)
        subprocess.run(["xvfb-run", "-a", "-s", "-screen 0 1280x820x24", str(sh)])
        if raw.exists() and raw.stat().st_size > 20000:
            break
    else:
        raise SystemExit("GRC did not open the properties dialog")
    Image.open(raw).convert("RGB").crop((682, 320, 1280, 470)).save(IMG / "L11-decoder-props.png")
    print("wrote L11-decoder-props.png")


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as t:
        import sys
        for name, grc in SHOTS.items():
            if len(sys.argv) == 1 or name in sys.argv[1:]:
                shoot(name, grc, Path(t))
        if len(sys.argv) == 1 or "L11-decoder-props" in sys.argv[1:]:
            decoder_props(Path(t))
        for name, (ymax, place) in CLUSTERS.items():
            if len(sys.argv) == 1 or name in sys.argv[1:]:
                shoot(name, L10, Path(t), ymax, place)
