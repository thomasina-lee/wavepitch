



import math

class MusicNote:
    
    names_sharp = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    names_flat = ['C','Db','D','Eb','E','F','Gb','G','Ab','A','Bb','B']
    names = ['C','C#/Db','D','D#/Eb','E','F','F#/Gb','G','G#/Ab','A','A#/Bb','B']
    inv_name_lookup = dict([ (x, i) for i, x in set(enumerate(names_sharp)).union(set(enumerate(names_flat)))])
    _freq_A4 = 440.0
    _note_nmr_A4 = 57
    max_note_number= 12 * 8 - 1
    
    @staticmethod
    def _note_nmr_from_freq(freq, threshold = 0.1):
        if freq <= 0: return
        est_nmr = math.log(freq / MusicNote._freq_A4, 2) * 12
        
        round_nmr = int(round(est_nmr))
        note_nmr = round_nmr + MusicNote._note_nmr_A4 
        
        diff = est_nmr - round_nmr
        if diff >= -threshold and diff < threshold and note_nmr >= 0 and note_nmr < MusicNote.max_note_number + 1:
            return round_nmr + MusicNote._note_nmr_A4 
    
    @staticmethod
    def create_note_from_freq(freq, threshold = 0.1):
        note_nmr  = MusicNote._note_nmr_from_freq(freq, threshold)
        if note_nmr is not None:
            return MusicNote(note_nmr)
    
    def set_from_freq(self, freq, threshold=0.1):
        note_nmr  = MusicNote._note_nmr_from_freq(freq, threshold)
        if note_nmr is not None:
            self._note_nmr = note_nmr
        else:
            self._note_nmr = -1
        return self
    
    def __init__(self, note_nmr = 48):

        self._note_nmr =  note_nmr
    
    def is_note(self):
        return self._note_nmr != -1
    
    def get_freq(self):
        if self._note_nmr == -1: return -1
        return math.pow(2, (self._note_nmr - MusicNote._note_nmr_A4)/12.0) * MusicNote._freq_A4 
        
    def get_name(self, mode = 0):
        if self._note_nmr == -1: return '-', -1
        if mode == 0:
            lookup = MusicNote.names
        elif mode < 0:
            lookup = MusicNote.names_flat
        else:
            lookup = MusicNote.names_sharp
        
        
        q = self._note_nmr / 12
        r = self._note_nmr % 12
        
        
        return lookup[r], q
    
    def get_note_number(self):
        return self._note_nmr
        