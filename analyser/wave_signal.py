

import numpy as np
import scipy.io.wavfile as spwavfile
import scipy.signal as spsignal

import peak_finder
    
    
class Signal:
    def __init__(self):
        
        self._rate = 0
        self._signal_values = None
        
        
    def load_file(self, file_name, track=0):
        
        self._rate,  data = spwavfile.read(file_name)
        self._signal_values = data[:, track]
        
        return self
    
    def set_signal(self, signal, rate):
        self._rate = rate
        self._signal_values = np.array(signal, copy = False)
        return self
        
    def get_sub_signal(self, start_time, duration, is_time = True):
        if is_time:
            start = int(self._rate * start_time)
            end = int(self._rate * (start_time + duration))
        else:
            start = start_time
            end = (start_time + duration)
            
        sub_signal = self._signal_values[start:end]
        return Signal().set_signal(sub_signal, self._rate)
    
    
    def get_signal_length(self):
        return self._signal_values.size
    
    def get_rate(self):
        return self._rate
    
    def get_freq_amplitute(self):
        
        
        full_amplitute = np.fft.fft(self._signal_values)
        full_freq = np.fft.fftfreq(self._signal_values.size, 1.0/self._rate)
        
        n = self._signal_values.size /2

        amplitute = np.abs(full_amplitute[0:n]) 
        freq = full_freq[0:n]
        
        return freq, amplitute
        
    
#    def _get_conv_window_param(self):   
#        duration = 1.0 /  self._rate * len(self._signal_values)
#        base_duration =  0.2
#        window_width = 10.0 *  duration / base_duration
#        sigma = 3.0  *  duration / base_duration
#        return window_width , sigma
#    
#    def get_peak_freq(self):
#        freq, amplitute = self.get_freq_amplitute()
#        note_peak_finder = peak_finder.NotePeakFinder(freq, amplitute)
#        
#       window_width , sigma = self._get_conv_window_param()
#        #print window_width, sigma
#        conv_window = spsignal.general_gaussian(window_width, 1, sigma)
#        
#        note_peak_finder.set_conv_window(conv_window)
#        peak_freqs, peak_amplitude = note_peak_finder.get_peak_freq()
#        
#        print peak_amplitude
#        return peak_freqs, peak_amplitude
    


class SignalSliceGenerator:
    """
        we have N windows of equal width:
         (a[i], b[i])  0 <= i < N
        used to extract frequency at time t[i]
        
        interval = a[i+1] - a[i]
        windiw_width = b[i] - a[i]  (for all i, it should all be the same)
        offset = t[i] - a[i]
        initial = a[0]
        
        rate is number of samples per seconds
        N is total number of samples
        
    """
    
    def __init__(self, N, rate):

        
        self._N = N
        self._rate = rate
        self._interval = int(rate * 0.2)
        self._windiw_width =  int(rate * 0.2)
        self._offset = int(rate * 0.1)
        self._initial = 0

       
    def _convert_set_value(self, value, is_time):
        if is_time:
            return int(value * self._rate)
        else:
            return int(value)
    
    def set_interval(self, interval, is_time = True):
        """ 
        if is_time == True 
        then interval is given as seconds, and the number of sample is given as interval * rate
        else interval is given as number of samples 
        """
        self._interval = self._convert_set_value(interval, is_time)
        return self
        
    def set_window_width(self, window_width, is_time = True):
        """
        similar to set_interval
        """
        self._windiw_width = self._convert_set_value(window_width, is_time)
        return self
        
    def set_offset(self, offset, is_time = True):
        """
        similar to set_interval
        """
        self._offset = self._convert_set_value(offset, is_time)
        return self
    
    def set_initial(self, initial, is_time = True):
        """
        similar to set_interval
        """
        self._initial = self._convert_set_value(initial, is_time)
        return self    
    
    def get_window_width(self):
        return self._windiw_width

    def get_nmr_slice(self):
        return int((self._N - self._initial - self._windiw_width) * 1.0 / self._interval) + 1
        
    
    def generate_slices(self):
        
        nmr_slice = self.get_nmr_slice()
        for ii in range(0, nmr_slice):
            window_start = self._initial + ii * self._interval
            window_value = window_start + self._offset
            yield window_start, window_value
            