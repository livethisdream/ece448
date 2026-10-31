#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2026 USAFA ECE 448.
#
# SPDX-License-Identifier: GPL-3.0-or-later
#


import numpy as np
from gnuradio import gr


class energy_detector(gr.decim_block):
    """
    Energy Detector: averages |x|^2 over each run of `decim` input samples
    and makes one output sample per run on each of two outputs.

    Output 0 is that average power in dB. Output 1 is a key: 1.0 while a
    signal is present and 0.0 while it is not. The key turns on when the
    power rises above threshold_db and turns off only when the power falls
    below threshold_db - hysteresis_db, so noise near the threshold does
    not make the key chatter.
    """
    def __init__(self, decim=32, threshold_db=-20.0, hysteresis_db=3.0):
        gr.decim_block.__init__(self,
            name="Energy Detector",
            in_sig=[np.complex64],
            out_sig=[np.float32, np.float32],
            decim=decim)
        self.decim = decim
        self.threshold_db = threshold_db
        self.hysteresis_db = hysteresis_db
        self.key = 0.0          # the key state carries over between calls

    def set_threshold_db(self, threshold_db):
        self.threshold_db = threshold_db

    def set_hysteresis_db(self, hysteresis_db):
        self.hysteresis_db = hysteresis_db

    def work(self, input_items, output_items):
        n = len(output_items[0])
        x = input_items[0][:n * self.decim].reshape(n, self.decim)
        power_db = 10 * np.log10(np.mean(x.real**2 + x.imag**2, axis=1) + 1e-12)
        for i, p in enumerate(power_db):
            if self.key == 0.0 and p > self.threshold_db:
                self.key = 1.0
            elif self.key == 1.0 and p < self.threshold_db - self.hysteresis_db:
                self.key = 0.0
            output_items[1][i] = self.key
        output_items[0][:] = power_db
        return n
