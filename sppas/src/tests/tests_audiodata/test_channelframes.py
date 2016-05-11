#!/usr/bin/env python2
# -*- coding: utf8 -*-

import sys
from os.path import abspath, dirname
SPPAS = dirname(dirname(dirname(abspath(__file__))))
sys.path.append( SPPAS )

import unittest
import os

import audiodata.io
from audiodata.channel import Channel
from audiodata.channelframes import ChannelFrames

from tests.paths import SPPASSAMPLES, TEMP
sample_1 = os.path.join(SPPASSAMPLES, "samples-eng", "oriana1.wav")  # mono; 16000Hz; 16bits
sample_2 = os.path.join(SPPASSAMPLES, "samples-fra", "F_F_B003-P9.wav")  # mono; 44100Hz; 32bits


class TestChannelFrames(unittest.TestCase):

    def setUp(self):
        self._sample_1 = audiodata.io.open(sample_1)
        self._sample_2 = audiodata.io.open(sample_2)

    def tearDown(self):
        self._sample_1.close()
        self._sample_2.close()

    def test_CreateSilence(self):
        self._sample_1.extract_channel(0)
        self._sample_2.extract_channel(0)

        channel = self._sample_1.get_channel(0)
        monofrag = ChannelFrames(channel.frames)
        monofrag.append_silence(1000)
        self.assertEqual(channel.get_nframes()+1000, len(monofrag.get_frames())/channel.get_sampwidth())
