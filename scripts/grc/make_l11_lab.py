#!/usr/bin/env python3
"""The L11 Lab's recording and flowgraphs.

  book/extras/grc/L11-lab-remote.sigmf-data/.sigmf-meta
      A Simulated on-off keyed transmitter at 915 MHz sending one line of
      text four times in a code the cadet works out from the key. 24 kS/s.
  book/extras/grc/L11-lab-rx.grc
      The receiver with its decoder missing: File Source on the recording,
      Throttle, the Energy Detector (as an Embedded Python Block, so the
      flowgraph runs on any laptop), the power and key plots, and a Key
      Decoder whose work() is empty, read by a Function Probe into the
      Received label.
  book/extras/grc/L11-lab-link.grc
      The cadet's own line, from a Key Encoder whose make_key() the cadet
      writes, in noise, into the same receiver. The Noise amplitude slider
      opens where the levels need setting.

The code itself (which part carries a bit, how long each part lasts) is the
lab's puzzle. Its constants and the line are not in this public file: the
recording is made from a private code file in ECE448-faculty, passed as the
one argument. Without it, only the two flowgraphs are written.
Normalize and check the flowgraphs after running this:

    /usr/bin/python3.12 scripts/grc/make_l11_lab.py [L11-lab-code.json]
    /usr/bin/python3.12 scripts/grc/grc_normalize.py book/extras/grc/L11-lab-*.grc
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

import numpy as np
import yaml

ROOT = Path(__file__).resolve().parents[2]
GRC = ROOT / "book/extras/grc"
TEMPLATE = GRC / "L11-keyed-carrier-epy.grc"

FS = 24000              # recording and link sample rate (S/s)
DECIM = 12              # Energy Detector: key at 2 kHz
TONE = 2000.0           # carrier offset in the recording (Hz)
AMP = 0.5
NOISE_DB = -30.0        # recording noise power (dB, relative to 1)
REPEATS = 4

SKELETON = '''"""Key Decoder: reads the Energy Detector's key and shows the line of text
it carries. The Received label reads last_line() through a Function Probe.

work() is yours to write (L11 Lab, Steps 5 to 8). Add any parameters you
need to __init__(); GRC shows each one in the block's properties."""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):
    def __init__(self):
        gr.sync_block.__init__(self, name='Key Decoder', in_sig=[np.float32], out_sig=None)
        self.line = '(nothing decoded)'

    def work(self, input_items, output_items):
        key = input_items[0]
        # Turn the key into text here, and set self.line when a line ends.
        return len(key)

    def last_line(self):
        return self.line
'''


ENCODER = '''"""Key Encoder: sends the line msg in the lab's code as a key, over and
over: 1 while the carrier is on, 0 while it is off.

make_key() is yours to write (L11 Lab, Step 16). Set Samples per unit to the
number of 24 kHz samples in one unit of the code you worked out."""

import numpy as np
from gnuradio import gr


class blk(gr.sync_block):
    def __init__(self, msg='Your line here', samples_per_unit=1):
        gr.sync_block.__init__(self, name='Key Encoder', in_sig=None, out_sig=[np.float32])
        units = self.make_key(msg) or [0]
        self.key = np.repeat(np.array(units, dtype=np.float32), max(1, int(samples_per_unit)))
        self.i = 0

    def make_key(self, msg):
        # Return the key for msg plus its newline, one entry per unit, ending
        # with the silence that separates two sendings.
        return []

    def work(self, input_items, output_items):
        out = output_items[0]
        idx = (self.i + np.arange(len(out))) % len(self.key)
        out[:] = self.key[idx]
        self.i = (self.i + len(out)) % len(self.key)
        return len(out)
'''


def units(code: dict) -> list[int]:
    """One line of text as the code's key, one entry per unit (the private code file)."""
    seq: list[int] = []
    for c in (code["text"] + "\n").encode():
        for b in format(c, "08b"):
            seq += code["bit"][b]
    return seq + code["end"]


def recording(code: dict):
    seq = [0] * code["lead"] + units(code) * REPEATS
    key = np.repeat(np.array(seq, dtype=np.float32), code["unit_samples"])
    n = np.arange(key.size)
    rng = np.random.default_rng(448)
    s = AMP * key * np.exp(2j * np.pi * TONE / FS * n)
    sigma = np.sqrt(10 ** (NOISE_DB / 10) / 2)
    s = s + sigma * (rng.standard_normal(key.size) + 1j * rng.standard_normal(key.size))
    s.astype(np.complex64).tofile(GRC / "L11-lab-remote.sigmf-data")
    meta = {
        "global": {
            "core:datatype": "cf32_le",
            "core:sample_rate": float(FS),
            "core:version": "1.0.0",
            "core:hw": "Simulated in Python; no radio",
            "core:author": "ECE 448",
            "core:description": "L11 Lab: a Simulated on-off keyed transmitter sending one line "
                                "of text four times, recorded at 915 MHz with the carrier 2 kHz "
                                "above center.",
        },
        "captures": [{"core:sample_start": 0, "core:frequency": 915e6}],
        "annotations": [],
    }
    (GRC / "L11-lab-remote.sigmf-meta").write_text(json.dumps(meta, indent=2) + "\n")
    return key.size / FS


def block(d, name):
    return next(b for b in d["blocks"] if b["name"] == name)


def base():
    """The template, cut down to the Energy Detector, its sliders, and its two plots."""
    d = yaml.safe_load(TEMPLATE.read_text())
    keep = {"samp_rate", "decim", "threshold", "hyst", "analog_const_source_x_0",
            "analog_const_source_x_1", "blocks_throttle2_0", "epy_block_0",
            "qtgui_time_sink_x_0", "qtgui_time_sink_x_1"}
    d["blocks"] = [b for b in d["blocks"] if b["name"] in keep]
    d["connections"] = [c for c in d["connections"] if c[0] in keep and c[2] in keep]
    block(d, "samp_rate")["parameters"]["value"] = str(FS)
    block(d, "decim")["parameters"]["value"] = str(DECIM)
    block(d, "threshold")["parameters"]["value"] = "-20"
    block(d, "threshold")["parameters"]["label"] = "Threshold (dB)"
    block(d, "hyst")["parameters"]["label"] = "Hysteresis (dB)"
    block(d, "threshold")["parameters"]["gui_hint"] = "0,0,1,1"
    block(d, "hyst")["parameters"]["gui_hint"] = "0,1,1,1"
    ed = block(d, "epy_block_0")
    ed["name"] = "energy"
    d["connections"] = [[("energy" if x == "epy_block_0" else x) for x in c] for c in d["connections"]]
    for ts, n in (("qtgui_time_sink_x_0", 1), ("qtgui_time_sink_x_1", 2)):
        p = block(d, ts)["parameters"]
        p.update(size="1000", tr_mode="qtgui.TRIG_MODE_FREE", tr_tag='""', srate="samp_rate / decim",
                 gui_hint=f"{n},0,1,3", update_time="0.10")
    p = block(d, "qtgui_time_sink_x_0")["parameters"]
    p.update(ymin="-40", ymax="5")
    p = block(d, "qtgui_time_sink_x_1")["parameters"]
    p.update(nconnections="1", ymin="-0.25", ymax="1.25", label1="Key")
    d["connections"] = [c for c in d["connections"] if not (c[2] == "qtgui_time_sink_x_1" and c[3] == "1")]
    dec = {
        "name": "decoder", "id": "epy_block",
        "parameters": {"_source_code": SKELETON, "affinity": "", "alias": "", "comment": "",
                       "maxoutbuf": "0", "minoutbuf": "0"},
        "states": {"_io_cache": "('Key Decoder', 'blk', [], [('0', 'float', 1)], [], '', [])",
                   "bus_sink": False, "bus_source": False, "bus_structure": None,
                   "coordinate": [1320, 560], "rotation": 0, "state": "enabled"},
    }
    probe = {
        "name": "rx_text", "id": "variable_function_probe",
        "parameters": {"block_id": "decoder", "comment": "", "function_args": "",
                       "function_name": "last_line", "poll_rate": "4", "value": "'(nothing decoded)'"},
        "states": {"bus_sink": False, "bus_source": False, "bus_structure": None,
                   "coordinate": [1320, 680], "rotation": 0, "state": "enabled"},
    }
    label = {
        "name": "rx_label", "id": "variable_qtgui_label",
        "parameters": {"comment": "", "formatter": "lambda x: ':  ' + x", "gui_hint": "3,0,1,3",
                       "label": "Received", "type": "string", "value": "rx_text"},
        "states": {"bus_sink": False, "bus_source": False, "bus_structure": None,
                   "coordinate": [1500, 680], "rotation": 0, "state": "enabled"},
    }
    d["blocks"] += [dec, probe, label]
    d["connections"].append(["energy", "1", "decoder", "0"])
    return d


def rx():
    d = base()
    o = d["options"]["parameters"]
    o.update(id="L11_lab_rx", title="L11 Lab - Receiver",
             description="L11 Lab: the recording through the Energy Detector into a Key Decoder "
                         "whose work() you write. No hardware; transmits nothing.",
             window_size="(1060,800)")
    src = {
        "name": "src", "id": "blocks_file_source",
        "parameters": {"affinity": "", "alias": "", "begin_tag": "pmt.PMT_NIL", "comment": "",
                       "file": "'L11-lab-remote.sigmf-data'", "length": "0", "maxoutbuf": "0",
                       "minoutbuf": "0", "offset": "0", "repeat": "True", "type": "complex", "vlen": "1"},
        "states": {"bus_sink": False, "bus_source": False, "bus_structure": None,
                   "coordinate": [560, 300], "rotation": 0, "state": "enabled"},
    }
    d["blocks"].append(src)
    d["connections"].append(["src", "0", "blocks_throttle2_0", "0"])
    (GRC / "L11-lab-rx.grc").write_text(yaml.safe_dump(d, sort_keys=False))


def link():
    d = base()
    t = yaml.safe_load(TEMPLATE.read_text())
    o = d["options"]["parameters"]
    o.update(id="L11_lab_link", title="L11 Lab - Link",
             description="L11 Lab: your own line in the lab's code, in noise, into the Energy "
                         "Detector and a Key Decoder. No hardware; transmits nothing.",
             window_size="(1060,800)")
    names = {b["name"]: b for b in t["blocks"]}
    add = []
    for n in ("noise", "analog_noise_source_x_0", "analog_sig_source_x_0", "blocks_add_xx_0",
              "blocks_float_to_complex_0", "blocks_multiply_xx_0"):
        add.append(copy.deepcopy(names[n]))
    d["blocks"] += add
    block(d, "noise")["parameters"].update(value="0.12", stop="0.5", step="0.01",
                                           label="Noise amplitude", gui_hint="0,2,1,1")
    block(d, "analog_sig_source_x_0")["parameters"].update(freq=str(int(TONE)), amp=str(AMP))
    d["blocks"].append({"name": "msg", "id": "variable", "parameters": {"comment": "", "value": "'Your line here'"},
                        "states": {"bus_sink": False, "bus_source": False, "bus_structure": None,
                                   "coordinate": [176, 76], "rotation": 0, "state": "enabled"}})
    d["blocks"].append({
        "name": "encoder", "id": "epy_block",
        "parameters": {"_source_code": ENCODER, "affinity": "", "alias": "", "comment": "",
                       "maxoutbuf": "0", "minoutbuf": "0", "msg": "msg", "samples_per_unit": "1"},
        "states": {"_io_cache": "('Key Encoder', 'blk', [('msg', \"'Your line here'\"), ('samples_per_unit', '1')], [], [('0', 'float', 1)], '', ['msg', 'samples_per_unit'])",
                   "bus_sink": False, "bus_source": False, "bus_structure": None,
                   "coordinate": [8, 220], "rotation": 0, "state": "enabled"}})
    for c in t["connections"]:
        if (c[0], c[2]) in (("blocks_float_to_complex_0", "blocks_multiply_xx_0"),
                            ("analog_sig_source_x_0", "blocks_multiply_xx_0"),
                            ("blocks_multiply_xx_0", "blocks_add_xx_0"),
                            ("analog_noise_source_x_0", "blocks_add_xx_0")):
            d["connections"].append(c)
    d["connections"].append(["encoder", "0", "blocks_float_to_complex_0", "0"])
    d["connections"].append(["blocks_add_xx_0", "0", "blocks_throttle2_0", "0"])
    (GRC / "L11-lab-link.grc").write_text(yaml.safe_dump(d, sort_keys=False))


if __name__ == "__main__":
    import sys
    # The recording needs the private code file (ECE448-faculty/lab-keys/src/
    # L11-lab-code.json): its text, units per bit, end, lead, and samples per unit.
    if len(sys.argv) > 1:
        code = json.loads(Path(sys.argv[1]).read_text())
        print(f"recording: {recording(code):.2f} s")
    rx()
    link()
    print("wrote L11-lab-rx.grc and L11-lab-link.grc")
