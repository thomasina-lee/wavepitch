import unittest

from wave_reader import PartialWaveReader, SimpleWebStreamer
import scipy.io.wavfile as spwavfile
import numpy as np

class TestPartialWaveReader(unittest.TestCase):



    def sub_test_wave_reader(self):
        
        
        
        pass
        


    def test_wave_reader(self):
        """
        plan, read file locally using scipy.wave
        then read file using streamer
        check if sample rate the same
        find 5 random points to check if data are equal
        """
        
        file_name = '../../../../../Music/rise like a phoenix beginning.wav'
        url = 'https://s3-eu-west-1.amazonaws.com/music-analysis/rise like a phoenix beginning.wav'
        max_bytes_allowed = 200001
        target_sample_size = 200001 / 4  ### this is hand calculated, 
                                         ### allowing for 1 mb data, the test file should be stereo 
        
        
        file_sample_rate, file_data_whole = spwavfile.read(file_name)
        
        
        wreader = PartialWaveReader(SimpleWebStreamer(url))
        wreader.set_max_byte_allowed(max_bytes_allowed)
        web_sample_rate, web_data = wreader.numpy_read_wav()
        
        
        file_data = file_data_whole[0:target_sample_size, 0]

        self.assertEqual(file_sample_rate, web_sample_rate)
        
        
        self.assertTrue(np.all(np.equal(file_data, web_data)))
        pass
        
        
        
    