


from wave_signal import  SignalSliceGenerator
import unittest
import numpy as np


        
    
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
        