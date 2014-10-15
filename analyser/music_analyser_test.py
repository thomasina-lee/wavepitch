

import unittest
import numpy as np

from mock import MagicMock

from music_analyser import MusicAnalyser
from wave_signal import Signal, SignalSliceGenerator

class TestMusicAnalyser(unittest.TestCase):


    def test_music_analyser(self):
        
        
        sub_signal = Signal()
        sub_signal.get_peak_freq = MagicMock()
        sub_signal.get_peak_freq.return_value = [392.00, 493.88, 587.33, 600.00]
        sub_signal.get_length = MagicMock()
        sub_signal.get_length.return_value = 44100 * 0.2
        
        the_signal = Signal()
        the_signal.get_sub_signal = MagicMock()
        the_signal.get_sub_signal.return_value = sub_signal
        
        ma = MusicAnalyser(the_signal, SignalSliceGenerator(44100*5, 44100))
        xt, x_name, t = ma.generate_matrix()
        expected_slice = np.zeros([97])
        expected_slice[[55, 59, 62]] = 1
       
        self.assertListEqual(xt[:,5].tolist(), expected_slice.tolist())
        
        
        
    