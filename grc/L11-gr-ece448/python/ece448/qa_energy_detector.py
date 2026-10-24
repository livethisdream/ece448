#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2026 USAFA ECE 448.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import numpy as np
from gnuradio import gr, gr_unittest
from gnuradio import blocks

try:
    from gnuradio.ece448 import energy_detector
except ImportError:
    import os
    import sys
    dirname, filename = os.path.split(os.path.abspath(__file__))
    sys.path.append(os.path.join(dirname, "bindings"))
    from gnuradio.ece448 import energy_detector


class qa_energy_detector(gr_unittest.TestCase):

    def setUp(self):
        self.tb = gr.top_block()

    def tearDown(self):
        self.tb = None

    def run_detector(self, x, decim, threshold_db, hysteresis_db):
        src = blocks.vector_source_c(x)
        det = energy_detector(decim, threshold_db, hysteresis_db)
        power = blocks.vector_sink_f()
        key = blocks.vector_sink_f()
        self.tb.connect(src, det)
        self.tb.connect((det, 0), power)
        self.tb.connect((det, 1), key)
        self.tb.run()
        return np.array(power.data()), np.array(key.data())

    def test_instance(self):
        energy_detector(32, -20.0, 3.0)

    def test_001_power_in_db(self):
        # Amplitudes 1, 0.1, and 0.01 have powers of 0, -20, and -40 dB.
        x = np.repeat([1.0, 0.1, 0.01], 8).astype(np.complex64)
        power, key = self.run_detector(x, 8, -30.0, 3.0)
        self.assertFloatTuplesAlmostEqual(power, [0.0, -20.0, -40.0], 4)
        self.assertFloatTuplesAlmostEqual(key, [1.0, 1.0, 0.0])

    def test_002_hysteresis(self):
        # One sample per output, so each output is one input's power in dB.
        # The key turns on above -20 dB and off only below -23 dB.
        p_db = np.array([-30, -19, -21, -22, -24, -21, -19, -25])
        x = (10 ** (p_db / 20)).astype(np.complex64)
        power, key = self.run_detector(x, 1, -20.0, 3.0)
        self.assertFloatTuplesAlmostEqual(power, p_db, 4)
        self.assertFloatTuplesAlmostEqual(key, [0, 1, 1, 1, 0, 0, 1, 0])

    def test_003_keyed_tone_in_noise(self):
        # A tone of amplitude 1 keyed on for 50 ms and off for 50 ms,
        # five times, in noise 30 dB down, at 32 kHz. With 32 samples
        # averaged the key is exactly 50 outputs on, then 50 off.
        rng = np.random.default_rng(448)
        fs, decim = 32000, 32
        n = 1600
        t = np.arange(10 * n) / fs
        gate = np.tile(np.repeat([1.0, 0.0], n), 5)
        noise = 0.0316 / np.sqrt(2) * (rng.standard_normal(10 * n)
                                       + 1j * rng.standard_normal(10 * n))
        x = (gate * np.exp(2j * np.pi * 1000 * t) + noise).astype(np.complex64)
        power, key = self.run_detector(x, decim, -15.0, 3.0)
        self.assertEqual(len(key), 10 * n // decim)
        self.assertFloatTuplesAlmostEqual(key, np.tile(np.repeat([1.0, 0.0], 50), 5))


if __name__ == '__main__':
    gr_unittest.run(qa_energy_detector)
