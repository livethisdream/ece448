#!/usr/bin/env python3
"""Lab step pictures (L6, L7, L8, L10): GNU Radio Companion canvases, block chain only.

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
  L08-lab-tx                     the cadet's class transmitter with the packet
                                 front end and a Channel Model added
  L08-lab-link                   that transmitter with the decoder the cadet
                                 builds; the Low Pass Filter cutoff and the
                                 Quadrature Demod gain are left as
                                 cutoff_table_a and gain_table_a, Part 1 answers
  L08-fsk-link                   book/extras/grc/L08-fsk-link.grc as shipped
  L10-lab-tx                     the packet transmitter the cadet builds; the
                                 packet length is left as len_table_a, a Part 1
                                 answer
  L10-pam-link, L10-pam-pluto    book/extras/grc/ as shipped

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
    "L08-canvas-tx": LAB / "L08-lab-tx.grc",
    "L08-canvas-rx": LAB / "L08-lab-link.grc",
    "L08-canvas-link": ROOT / "book/extras/grc/L08-fsk-link.grc",
    "L10-canvas-tx": LAB / "L10-lab-tx.grc",
    "L10-canvas-link": ROOT / "book/extras/grc/L10-pam-link.grc",
    "L10-canvas-pluto": ROOT / "book/extras/grc/L10-pam-pluto.grc",
}


def offstage(src: Path, dst: Path):
    """Copy a flowgraph with its Options, variable, and import blocks moved off screen."""
    d = yaml.safe_load(src.read_text())
    for b in d["blocks"]:
        if b["id"].startswith("variable") or b["id"] in ("import",):
            b["states"]["coordinate"] = [W + 400, H + 400]
    d["options"]["states"]["coordinate"] = [W + 600, H + 600]
    dst.write_text(yaml.safe_dump(d, sort_keys=False))


def shoot(name: str, grc: Path, tmp: Path):
    g = tmp / grc.name
    offstage(grc, g)
    raw = tmp / f"{name}-raw.png"
    for _ in range(4):                  # GRC under Xvfb now and then dies at start-up; try again
        raw.unlink(missing_ok=True)
        subprocess.run(["xvfb-run", "-a", "-s", f"-screen 0 {W}x{H}x24",
                        str(ROOT / "scripts/grc/grc_canvas.sh"), str(g), str(raw), f"{W}x{H}"])
        if raw.exists() and raw.stat().st_size > 20000:
            break
    else:
        raise SystemExit(f"GRC did not render {grc.name}")
    im = Image.open(raw).convert("RGB").crop((0, 70, W, H))      # drop the menu and toolbar
    bb = ImageOps.invert(im.convert("L")).point(lambda v: 255 if v > 12 else 0).getbbox()
    im = im.crop((max(0, bb[0] - 10), max(0, bb[1] - 10), min(im.width, bb[2] + 50), min(im.height, bb[3] + 10)))
    im.save(IMG / f"{name}.png")
    print(f"wrote {name}.png {im.size}")


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as t:
        import sys
        for name, grc in SHOTS.items():
            if len(sys.argv) == 1 or name in sys.argv[1:]:
                shoot(name, grc, Path(t))
