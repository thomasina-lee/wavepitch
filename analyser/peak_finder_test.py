
from wave_signal import Signal
from peak_finder import  PeakRangeFinder, SignalPeakFreqFinderV1
import unittest
import numpy as np

class TestNotePeakFinder(unittest.TestCase):
    
    
    def _sub_test_note_peak_finder(self, rate, duration):
        
       
        target_freqs = [246.94, 293.66, 349.23, 415.30, 493.88] # B D F G#
        target_amps = [5.0, 4.0, 4.0, 3.0, 4.0]
        
        time_x = np.linspace(0, duration, rate * duration + 1)
        signal_y = np.zeros(time_x.size)
        for freq, amp in zip(target_freqs, target_amps) :
            signal_y = signal_y + np.sin(np.pi * 2 * time_x * 1.0 * freq) * amp
        
        signal_y = signal_y + np.random.normal(0, 1, signal_y.size)
        
        
        ss =  Signal()
        ss.set_signal(signal_y, rate)
        peaks, amplitude = SignalPeakFreqFinderV1().get_peak_freq(ss)
        self.assertEqual(len(peaks), len(target_freqs))
        result = np.abs(peaks / np.array(target_freqs) -1) < 0.01
        self.assertListEqual(result.tolist(), [True]*len(target_freqs))
    
    def test_note_peak_finder(self):
        
        self._sub_test_note_peak_finder(44100.0, 0.2)
        self._sub_test_note_peak_finder(44100.0, 0.4)
        self._sub_test_note_peak_finder(88200.0, 0.2)
    
class TestPeakRangeFinder(unittest.TestCase):
    

    
    def test_get_tall_peaks(self):
        test_list = [{'y':[10,32,11,22,21,77,15,16,9,10,8], 'x': range(0, 11), 'e': [(0, 2), (2,8)]},
                     {'y':[15,10,32,11,22,21,77,15,16,9,10], 'x': range(0, 11), 'e': [(1, 3), (3,9)]},
                     ]
       
        for t in test_list:
            x = t['x']
            y = t['y']
            expected_peaks = t['e']
            
            extremas = zip(x, y)
            finder = PeakRangeFinder().set_extremas(extremas)
            
            tall_peaks = [x for x in finder.get_tall_peaks()]
            
            
            self.assertListEqual(tall_peaks, expected_peaks)
        
        
        

        
        
        
        
        