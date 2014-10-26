

from wave_signal import Signal, SignalSliceGenerator
import pitchogram
import unittest
import numpy as np
from mock import MagicMock


class TestPitchoSliceGeneratorSimple(unittest.TestCase):
    
    
    def test_noise_cutoff(self):
        arr = np.array([1,1,1,1,2,2,2,2])
        cutoff = pitchogram.NoiseCutoff(70, 0.975).call(arr)
        self.assertAlmostEqual(cutoff, 2.479981992)
        
        
        arr = np.array([1,1,1,1,1,1,1,1])
        cutoff = pitchogram.NoiseCutoff(70, 0.975).call(arr)
        self.assertAlmostEqual(cutoff, 1)
        
        
    def _generate_sample_signal(self, rate, duration, target_freqs, target_amps, noise_std):
        time_x = np.linspace(0, duration, rate * duration + 1)
        signal_y = np.zeros(time_x.size)
        for freq, amp in zip(target_freqs, target_amps) :
            signal_y = signal_y + np.sin(np.pi * 2 * time_x * 1.0 * freq) * amp
        
        signal_y = signal_y + np.random.normal(0, noise_std, signal_y.size)
        
        ss =  Signal()
        ss.set_signal(signal_y, rate)
        return ss
        
    
    def _sub_test_pitchoslice_simple(self, rate, duration):
        
        target_note_numbers = [47, 50, 53, 56, 59]
        target_freqs = [246.94, 293.66, 349.23, 415.30, 493.88] # B D F B
        target_amps = [5.0, 4.0, 4.0, 3.0, 4.0]
        
        ss = self._generate_sample_signal(rate, duration, target_freqs, target_amps, 1.0)

        
        note_numbers, power_vals = pitchogram.PitchosliceGenerator(pitchogram.NoiseCutoff(95, 0.99)).call(ss)
        idx = np.array([x in target_note_numbers for x in note_numbers])

        self.assertEqual(len(note_numbers[idx]), len(target_note_numbers))
        
        self.assertTrue(note_numbers.size < 20)
        result = np.abs(power_vals[idx] / (np.array(target_amps) **2) -1) < 0.20

        self.assertListEqual(result.tolist(), [True]*len(target_freqs))
        
        
    
    def test_pitchoslice_simple(self):
        
        self._sub_test_pitchoslice_simple(44100.0, 0.2)
        self._sub_test_pitchoslice_simple(44100.0, 0.4)
        self._sub_test_pitchoslice_simple(88200.0, 0.2)
        
        
        
class TestPitchogramGenerator(unittest.TestCase):


    def test_music_analyser(self):

        amp=[5.00, 3.88, 4.33]       
        pslice_generator = pitchogram.PitchosliceGenerator()
        pslice_generator.call = MagicMock()
        pslice_generator.call.return_value = ([55, 59, 62], amp )
        sub_signal = Signal()
       
       
        sub_signal.get_length = MagicMock()
        sub_signal.get_length.return_value = 44100 * 0.2
    
        
        the_signal = Signal()
        the_signal.get_sub_signal = MagicMock()
        the_signal.get_sub_signal.return_value = sub_signal
        the_signal.get_rate = MagicMock()
        the_signal.get_rate.return_value = 44100
        pg = pitchogram.PitchogramGenerator(the_signal, SignalSliceGenerator(44100*5, 44100), pslice_generator)
        xt, x, x_name, t = pg.generate_matrix()
        expected_slice = np.zeros([97])
        expected_slice[[55, 59, 62]] =  amp
       
        self.assertListEqual(xt[:,5].tolist(), expected_slice.tolist())
        
        
        
    def test_analyse_url(self):
        """ this is currently not really a test 
        """ 
        url = 'https://s3-eu-west-1.amazonaws.com/music-analysis/rise like a phoenix beginning.wav'
        #print analyse_wav_url(url)