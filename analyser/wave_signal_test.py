


from wave_signal import Signal, SignalSliceGenerator
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
        peaks, amplitude = ss.get_peak_freq()
        self.assertEqual(len(peaks), len(target_freqs))
        result = np.abs(peaks / np.array(target_freqs) -1) < 0.01
        self.assertListEqual(result.tolist(), [True]*len(target_freqs))
    
    def test_note_peak_finder(self):
        
        self._sub_test_note_peak_finder(44100.0, 0.2)
        self._sub_test_note_peak_finder(44100.0, 0.4)
        self._sub_test_note_peak_finder(88200.0, 0.2)
        
        
        
    
class TestSignalSlicer(unittest.TestCase):
    
   
    
    def test_slice_generator(self):
        slice_iterator = SignalSliceGenerator(441000, 44100)
        
        self.assertEqual(slice_iterator.get_nmr_slice(), 50)
        result = list(slice_iterator.generate_slices())
          
        self.assertListEqual([x[0] for x in result], [x* 8820 for x in range(0, 50)])
        self.assertListEqual([x[1] for x in result], [x* 8820 + 4410 for x in range(0, 50)])
        
        slice_iterator = SignalSliceGenerator(441000, 44100)
        slice_iterator.set_initial(0.1, True)
        slice_iterator.set_window_width(0.4*44100, False)
        slice_iterator.set_interval(0.3)
        slice_iterator.set_offset(0.15)
        
        self.assertEqual(slice_iterator.get_nmr_slice(), 32)
        result = list(slice_iterator.generate_slices())
          
        self.assertListEqual([x[0] for x in result], [4410 + x* 13230 for x in range(0, 32)])
        self.assertListEqual([x[1] for x in result], [x* 13230 + 6615 + 4410 for x in range(0, 32)])
        