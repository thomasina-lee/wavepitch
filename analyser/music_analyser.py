
import wave_signal
from numpy import rate
from note import MusicNote
import numpy as np
import json
from wave_reader import PartialWaveReader, SimpleWebStreamer

class MusicAnalyser:
    
    def __init__(self, wave_signal, slice_generator):
        
        self._wave_signal = wave_signal
        self._signal_slice_generator = slice_generator
        
    
    def _get_note_numbers(self, sub_signal):
        peak_freq, peak_amplitude = sub_signal.get_peak_freq()
        paired = [{'freq': x[0], 'amp': x[1]} for x in zip(peak_freq, peak_amplitude)]
        valid_music_note_pair = filter(lambda m: m['note'].is_note(),  
                                  [{'note': MusicNote().set_from_freq(f['freq'], 0.3),
                                    'amp': f['amp']} for f in paired])
        return [ mn['note'].get_note_number() for mn in  valid_music_note_pair ], \
                  [ mn['amp'] for mn in valid_music_note_pair ]
            
    

    
    def generate_matrix(self):
        duration = self._signal_slice_generator.get_window_width()
        t = []
        x_name = [MusicNote(ii).get_name() for ii in range(0, 97)]
        x = range(0, 97)
        xt = np.zeros([97, self._signal_slice_generator.get_nmr_slice()])
        for ii, (window_start, window_value) in enumerate(self._signal_slice_generator.generate_slices()):

            t.append(window_value *1.0 / self._wave_signal.get_rate())
            sub_signal = self._wave_signal.get_sub_signal(window_start, duration, False)
            note_number, note_amplitute = self._get_note_numbers(sub_signal)
            xt[note_number, ii] = note_amplitute
            
            
        return xt, x, x_name, t
            
            
def analyse_wav_signal(sig):  
    
    slice_generator =  wave_signal.SignalSliceGenerator(sig.get_signal_length(),sig.get_rate())
    
    mana = MusicAnalyser(sig, slice_generator)
    active_notes_0, note_numbers, note_name_0, time_values = mana.generate_matrix()
    
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

def analyse_wav_file(file_name):
    sig = wave_signal.Signal()
    sig.load_file(file_name)
    
    return analyse_wav_signal(sig)


def analyse_wav_url(url, max_byte_allowed = 1024*100, timeout = 10):
    wreader = PartialWaveReader(SimpleWebStreamer(url).set_timeout(timeout))
    wreader.set_max_byte_allowed(max_byte_allowed)

    sample_rate, wave_data = wreader.numpy_read_wav()
    
    
    sig = wave_signal.Signal()
    
    sig.set_signal(wave_data, sample_rate)
    
    return analyse_wav_signal(sig)
        