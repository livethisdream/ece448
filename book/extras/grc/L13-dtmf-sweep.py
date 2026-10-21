#!/usr/bin/env python3
"""L13: measure where the DTMF decoder fails.

Runs the DTMF Dialer and DTMF Decoder blocks from L13-dtmf-link.grc headless,
with no Throttle and no noise except in the snr table, and counts how many
dialings of a number the decoder gets exactly right as one setting at a time
moves away from a clean signal. Each setting is the same as the slider of that
name in L13-dtmf-link.grc.

    python L13-dtmf-sweep.py            # the noise and frequency-error sweeps behind the lesson page
    python L13-dtmf-sweep.py snr        # one table: snr or offset

Put it in the same folder as L13-dtmf-link.grc. Run it from the radioconda
prompt, where GNU Radio's Python is the first python on the path.
"""
import pathlib
import sys
import types

import numpy as np
import yaml
from gnuradio import analog, blocks, gr

HERE = pathlib.Path(__file__).resolve().parent
TRIALS = 40          # dialings per setting
PHONE = '7195550148'
ALL16 = '123A456B789C*0#D'


def load_blocks():
    """Take the Embedded Python Blocks' code out of the link flowgraph."""
    grc = yaml.safe_load((HERE / 'L13-dtmf-link.grc').read_text())
    mods = {}
    for b in grc['blocks']:
        if b['id'] == 'epy_block':
            m = types.ModuleType(b['name'])
            exec(b['parameters']['_source_code'], m.__dict__)
            mods[b['name']] = m
    return mods['dialer'], mods['dtmf_decoder']


DIALER, DECODER = load_blocks()


def run(number, snr_db=None, twist_db=0.0, tone_ms=50, gap_ms=50, offset_pct=0.0,
        round_k=False, trials=TRIALS, seed=1):
    """Dial `number` `trials` times; return how many dialings decode exactly."""
    level = 0.3
    dial = DIALER.blk(digits=number, tone_ms=tone_ms, gap_ms=gap_ms, pause_ms=500,
                      level=level, twist_db=twist_db, offset_pct=offset_pct)
    period = int(round(8000 * (len(number) * (tone_ms + gap_ms) + 500) / 1000))
    dec = DECODER.blk(expected=number, round_k=round_k)
    tb = gr.top_block()
    head = blocks.head(gr.sizeof_float, period * trials)
    if snr_db is None:
        tb.connect(dial, head)
    else:
        # SNR during a tone over the whole 0-4 kHz band, as in L13-dtmf-link.grc
        sigma = level * ((1 + 10 ** (twist_db / 10)) / 2 / 10 ** (snr_db / 10)) ** 0.5
        add = blocks.add_ff()
        tb.connect(dial, (add, 0))
        tb.connect(analog.noise_source_f(analog.GR_GAUSSIAN, sigma, seed), (add, 1))
        tb.connect(add, head)
    tb.connect(head, dec)
    tb.run()
    if dec.number:          # the last dialing ends with the stream, not a pause
        dec.finish()
    return dec.good


def table(name, values, **fixed):
    print(f'{name:>12}:  ' + '  '.join(f'{v:>6}' for v in values))
    counts = [run(**fixed, **{name: v}) for v in values]
    print(f'{"correct":>12}:  ' + '  '.join(f'{c:>3}/{TRIALS}' for c in counts), flush=True)


TABLES = {
    'snr': lambda: table('snr_db', [6, 4, 3, 2, 1, 0, -1], number=PHONE),
    'offset': lambda: table('offset_pct', [-3.5, -2.5, -2.0, -1.5, -1.0, 1.0, 1.5, 2.0, 2.5, 3.5], number=ALL16),
}

if __name__ == '__main__':
    for key in sys.argv[1:] or TABLES:
        print(f'== {key}')
        TABLES[key]()
