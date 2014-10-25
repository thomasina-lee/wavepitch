
import numpy as np
import scipy.signal as spsignal

class PeakRangeFinder:
    
    
    def __init__(self):
        self._unset()

        
    def _unset(self):
        self._extremas = []
        self._valid_start = 0
        self._valid_end = 0
        self._valid_extremas = []
        self._tall_peak_threshold = 1.5
        self._peak_base_threshold = 1.0
        self._min_peak_value = 0
     
    def set_min_peak_value(self, min_peak_value):    
        self._min_peak_value = min_peak_value
        return self
        
    def set_extremas(self, extremas):
        if len(extremas) < 3 : 
            self._unset()
            return self
        

        self._extremas = extremas
        self._valid_start = 0
        self._valid_end = len(extremas)
        if self._extremas[0][1] > self._extremas[1][1]:
            self._valid_start = 1
            
        if self._extremas[self._valid_end-1][1] > self._extremas[self._valid_end-2][1]:
            self._valid_end = self._valid_end - 1
            
        if self._valid_start >= self._valid_end: 
            self._unset()
            return self
        
        self._valid_extremas = self._extremas[self._valid_start: self._valid_end]
        return self
        
    def set_tall_threshold(self, threshold):
        self._tall_peak_threshold = threshold
        return self
            
    def get_peaks(self):
        
        for ii in range(0, self.get_peak_count()):
            
            yield (ii, self.get_peak(ii))
    
    
    def get_peak_count(self):
        return len(self._valid_extremas) / 2
       
    def get_peak(self, pos):
        if pos >= (self._valid_end - self._valid_start) / 2: return None
        return self._valid_extremas[pos * 2 : (pos * 2) + 3]
        
    

    
    def _is_tall_peak(self, vv):
        
        
        return vv[1][1] * 2.0 / (vv[0][1] + vv[2][1]) > self._tall_peak_threshold  \
            and vv[1][1] > self._min_peak_value
    
   
    def _peak_base_direction(self, vv):
        
        slope = ( vv[2][1] - vv[0][1] ) *1.0/( vv[2][0] - vv[0][0] )
        if abs(slope) <  self._peak_base_threshold:
            return 0
        
        return -1 if slope < 0 else 1
            
            
    
    def _merge_peak(self, p1, p2):
        max_value = p1[1] if p1[1][1] >  p2[1][1] else p2[1]
        return [p1[0], max_value, p2[2]]
        
    
    def get_tall_peaks(self):
        tall_peaks = []
        pending_peak = None
        ii = 0
        last_appended = False
        while ii < self.get_peak_count():
            appended = False
            peak = self.get_peak(ii)
            base_direction = self._peak_base_direction(peak)
            if pending_peak is not None:
                peak = self._merge_peak(pending_peak, peak)
                pending_peak = None
                
            base_direction = self._peak_base_direction(peak)
            if self._is_tall_peak(peak):
                tall_peaks.append (peak)
                appended = True
                
             
            elif base_direction < 0 and last_appended == True:
                prev_peak = tall_peaks.pop()
                peak = self._merge_peak(prev_peak, peak)
                tall_peaks.append(peak)
                appended = True
            
            elif base_direction > 0:
                pending_peak = peak
                
                
            last_appended = appended
            ii = ii + 1
    
        return [(peak[0][0], peak[2][0])  for peak in tall_peaks]
    
    
    
    
    
    

class FreqPeakFinderV1:

    def __init__(self, freq, spectrum):
        
        self._freq = np.array(freq)
        self._spectrum = np.array(spectrum)
        self._conv_window = spsignal.general_gaussian(10, 1, 3)
        
    def set_conv_window(self, conv_window):
        self._conv_window = conv_window
        
        
    def _smooth(self):
        self._smoothed_spectrum = spsignal.convolve(self._spectrum, 
                                           self._conv_window, 
                                           'same')
        
    
    def _get_smoothed_extremas(self):
        min_x = spsignal.argrelmin(self._smoothed_spectrum)[0]
        max_x = spsignal.argrelmax(self._smoothed_spectrum)[0]
        min_y = self._smoothed_spectrum[min_x]
        max_y = self._smoothed_spectrum[max_x]
        merged = zip(min_x, min_y) + zip(max_x, max_y)
        merged.sort(lambda x, y: cmp(x[0], y[0]))

        merged.insert(0, (0, self._smoothed_spectrum[0]))
        last = len(self._smoothed_spectrum) -1
        merged.append((last, self._smoothed_spectrum[last]))
        return merged
    
    def _find_min_peak_value(self):
        
        pc = np.percentile(self._smoothed_spectrum, 99.5)
        lmean = np.mean(self._smoothed_spectrum[self._smoothed_spectrum < pc])
        lstd = np.std(self._smoothed_spectrum[self._smoothed_spectrum < pc])
        min_peak_value = lmean + 2.0 * lstd
        
        #min_peak_value = (np.mean(self._smoothed_spectrum[self._smoothed_spectrum < pc]) + 
        #                  np.mean(self._smoothed_spectrum[self._smoothed_spectrum >= pc]))/2
        
        #rev = np.sort(self._smoothed_spectrum)[::-1]
        #csum = np.cumsum(rev) 
        #total = np.sum(rev)
        #min_peak_value = np.min(sorted[csum < total * 0.95])
        
        print 'min peak value = ' + str(min_peak_value)
        return min_peak_value
    
    def _find_tall_smooth_peak(self, extremas):
        extremas = self._get_smoothed_extremas()
        min_peak_value = self._find_min_peak_value()
        finder = PeakRangeFinder().set_extremas(extremas).set_min_peak_value(min_peak_value)
        
        return finder.get_tall_peaks()
    
    def _find_tall_peak_max(self, tall_peak_range):
        max_idxs = []
        for rng in tall_peak_range:
            
            argmax = np.argmax(self._spectrum[rng[0]:rng[1]])
            
            max_idxs.append(argmax + rng[0])
        return max_idxs
        
    
    def get_peak(self):
        self._smooth()
        extremas = self._get_smoothed_extremas()
        tall_peak_range = self._find_tall_smooth_peak(extremas)
        
        max_idxs = self._find_tall_peak_max(tall_peak_range)
        
        peak_freqs = self._freq[max_idxs]
        peak_amplitude = self._spectrum[max_idxs]
        return peak_freqs, peak_amplitude
    



class SignalPeakFreqFinderV1:
    
    def _conv_window_fn(self, sig):
        
        duration = 1.0 /  sig.get_rate() *  sig.get_signal_length()
        base_duration =  0.2
        window_width = 15.0 *  duration / base_duration
        #sigma = 3.0  *  duration / base_duration
        #conv_window = spsignal.general_gaussian(window_width, 1, sigma)
        conv_window = spsignal.hamming(window_width, False)
        return conv_window
    
    
    
    def __init__(self, formula_name='amplitute'):
        self._formula_name = formula_name
        pass
        
    def _formula(self, freq, amplitute):
        if self._formula_name == 'power':
            print 'power!'
            return amplitute * amplitute
        else :
            return amplitute 
    
        
    def call(self, sig):
        
        freq, amplitute = sig.get_freq_amplitute()
        
        val = self._formula(freq, amplitute)
        note_peak_finder = FreqPeakFinderV1(freq, val)
        

        conv_window = self._conv_window_fn(sig)
        note_peak_finder.set_conv_window(conv_window)
        peak_freqs, peak_amplitude = note_peak_finder.get_peak()
        
        
        return peak_freqs, peak_amplitude


    
   
    
    
        

    


    


        

