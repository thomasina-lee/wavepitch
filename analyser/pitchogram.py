
import numpy as np

import scipy.stats as spstats
from note import MusicNote
from wave_reader import PartialWaveReader, SimpleWebStreamer
from wave_signal import Signal, SignalSliceGenerator
import json
# such neat method, need some credits :)
# http://stackoverflow.com/questions/4373631/sum-array-by-number-in-numpy

def _sum_by_group(values, groups):
    """
    :param frequency
    :return the corresponding note number 
        (1 increment represent a semitone, A(octative 4) = 44 )
    """
    order = np.argsort(groups)
    groups = groups[order]
    values = values[order]
    values.cumsum(out=values)
    index = np.ones(len(groups), 'bool')
    index[:-1] = groups[1:] != groups[:-1]
    values = values[index]
    groups = groups[index]
    values[1:] = values[1:] - values[:-1]
    return values, groups


def _get_note_number(freq):
    """
    :param freq:  frequency from which we extract the note number  
    :return the corresponding music note number 
        (1 increment represent a semitone, A(octative 4) = 57 )
    """
    mn = MusicNote.create_note_from_freq(freq, 0.5)
    note_nmr = -1
    if mn is not None:
        note_nmr = MusicNote.create_note_from_freq(freq, 0.5).get_note_number()
    return note_nmr



class NoiseCutoff:
    
    def __init__(self, q=95, percent=0.99):
        """
        :param q:    q-percentile for noise cutoff calculation
        :param percent: percentage of what we accept as 'noise'
        """
        self._noise_cutoff_q = q
        self._noise_cutoff_perc = percent

    def call(self, arr):
        
        
        
        percentile = np.percentile(arr, self._noise_cutoff_q)
        arr_lower = arr[arr <= percentile]
        avg = np.mean(arr_lower)
        std = np.std(arr_lower)
        cutoff = avg + spstats.norm.ppf(self._noise_cutoff_perc) * std
        return cutoff

# this is essentially a function, but 
# python does not really have closure
class PitchosliceGenerator:
    """
    this, given a function, returns an array
    of how strong each note is
    
       
    """
    def __init__(self, noise_cutoff = None):
        
        self._noise_cutoff = noise_cutoff          
    
    
    def call(self, sig):
        freqs, ampls = sig.get_freq_amplitute()
        powers  = ampls **2 / ampls.size **2
        fn = np.vectorize(_get_note_number)
        freq_note_numbers = fn(freqs)
        idx_valid = freq_note_numbers >=0
        powers, freq_note_numbers = _sum_by_group(powers[idx_valid], freq_note_numbers[idx_valid])
        
        strengths = np.zeros(MusicNote.max_note_number + 1)
        strengths[freq_note_numbers] = powers
        note_number = np.arange(0, MusicNote.max_note_number + 1)
        if self._noise_cutoff is not None:
            
            note_number, strengths  = self._filter(strengths, note_number)
            
        return note_number, strengths
        
    
    def _filter(self, strengths, note_number):
        cutoff = self._noise_cutoff.call(strengths)
        idx = strengths > cutoff
        
        return note_number[idx], strengths[idx]
    
    
    

        
        
class PitchogramGenerator:
    
    def __init__(self, wave_signal, slice_generator, 
                 pitchoslice_generator = PitchosliceGenerator(NoiseCutoff())):
        
        self._wave_signal = wave_signal
        self._signal_slice_generator = slice_generator
        self._pitchoslice_generator = pitchoslice_generator
        self._note_acceptance_threshold = 0.5
    
    

            
    
    
    def generate_matrix(self):
        """
        :returns strengths(of note, n x t matrix), note_numbers(n), note_name, time(t)
        """
        
        duration = self._signal_slice_generator.get_window_width()
        t = []
        x_name = [MusicNote(ii).get_name() for ii in range(0, 97)]
        x = range(0, 97)
        xt = np.zeros([97, self._signal_slice_generator.get_nmr_slice()])
        
        for ii, (window_start, window_value) in enumerate(self._signal_slice_generator.generate_slices()):
            
            t.append(window_value *1.0 / self._wave_signal.get_rate())
            
            sub_signal = self._wave_signal.get_sub_signal(window_start, duration, False)
            
            note_number, strengths = self._pitchoslice_generator.call(sub_signal)
           
            xt[note_number, ii] = strengths
            
        
        return xt, x, x_name, t
    
    

def pitchogram_from_signal(sig, filtered = True):  
    
    slice_generator =  SignalSliceGenerator(sig.get_signal_length(),sig.get_rate())
    slice_generator.set_interval(0.1, True)
    
    noise_cutoff = NoiseCutoff() if filtered else None
    
    pitchogram_generator = PitchogramGenerator(sig, slice_generator,
                                               PitchosliceGenerator(noise_cutoff))
    
    active_notes_0, note_numbers, note_name_0, time_values = pitchogram_generator.generate_matrix()
    
    note_names = ['%s(%s)' % x for x in note_name_0]
    
    active_notes = [{'n': x, 't': y, 'v': active_notes_0[x, y]} 
                    for x in range(0, active_notes_0.shape[0])
                    for y in range(0, active_notes_0.shape[1])
                    if active_notes_0[x, y] > 0]
    
    payload = json.dumps({"active_notes":active_notes, 
                          "note_names": note_names, 
                          "note_numbers": note_numbers, 
                          "time_values": time_values})
    
    return payload

def pitchogram_from_url(url, max_byte_allowed = 1024*100, timeout = 10, filtered = True):
    wreader = PartialWaveReader(SimpleWebStreamer(url).set_timeout(timeout))
    wreader.set_max_byte_allowed(max_byte_allowed)
    
    sample_rate, wave_data = wreader.numpy_read_wav()
    
    sig = Signal()
    
    sig.set_signal(wave_data, sample_rate)
    
    return pitchogram_from_signal(sig, filtered)
        