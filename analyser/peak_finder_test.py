

from peak_finder import  PeakRangeFinder
import unittest
import numpy as np


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
        
        
        

        
        
        
        
        