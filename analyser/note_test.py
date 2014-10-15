import note
import unittest

class TestNote(unittest.TestCase):
    
    def test_name(self):
        
        n, o = note.MusicNote().create_note_from_freq(262).get_name()
        self.assertEqual(n, 'C')
        self.assertEqual(o, 4)
        
        freqs = [440, 349, 359]
        expected_list = [('A', 4),  ('F', 4), None ]
        
        for freq, expected in zip(freqs, expected_list):
            
            nt = note.MusicNote.create_note_from_freq(freq)
            
            if nt is None:
                self.assertEqual(expected, None)
            else:
                r = nt.get_name()
                self.assertEqual(expected, r)
        
        
    
        
        
    def test_get_freq(self):
        
        self.assertAlmostEqual(note.MusicNote.create_note_from_freq(440).get_freq(), 440, delta= 0.01)
        
        self.assertAlmostEqual(note.MusicNote().get_freq(), 261.63, delta= 0.01)