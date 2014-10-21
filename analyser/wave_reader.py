
import requests
import numpy as np
import struct




class Closer(object):
    """
    This object should be created with a with statement,
    and it assumes there is a .close() method within 
    the object.  Upon exit it will call close method to close it
    """
    
    def __init__(self, obj):
        """
        :param obj: an object with a close method which closes upon exit
        """
        
        self.obj = obj
    def __enter__(self):
        return self.obj
    
    def __exit__(self, *exc_info):
        try:
            close_it = self.obj.close
        except AttributeError:
            pass
        else:
            close_it()
    

class SimpleWebStreamer:
    
    def __init__(self, url):
        """
        this is a stream reader
        :param url: url to be opened

        e.g.
        SampleWebStreamer('https:/some.host/some.file.name')
        """
        
        self._url = url
        self._timeout = 10
        

    def set_timeout(self, value):
        self._timeout = value
        return self

    def open(self):
        self._response = requests.get(self._url, stream = True, timeout = self._timeout)
        return self
        
    def file_size(self):
        """
        this obtains the file size of the ulr
        
        :returns: file size, or None if not exist
         
        """
        
        #response = requests.head(self._url)
        
        file_size = None
        if self._response.headers is not None and 'content-length' in self._response.headers:
            
            file_size_str=self._response.headers['content-length']
    
            if file_size_str.isdigit():
                file_size = int(file_size_str)
            else:
                file_size = None
            
        return file_size
        


        
    def read(self, chunk_size):
        """
        this reads the chunk.
        :param chunk_size: size of chunk in byte to read
        
        :returns: a byte string
         
        """
        data = self._response.raw.read(chunk_size)
        return data
        
    def close(self):
        self._response.close()
        


def step_range(start, end, step=1):
    """
    this function is like range in python, except that 
    it will also give the step size 
    """
    ii = start
    
    while ii < end - step:
        
        yield ii, step
        ii += step
        
    
    yield ii, end - ii    
         
        
class PartialWaveReader():
    "This is a class which allows partial reads from a web site"
    
    def __init__(self, stream_reader):
        """
        this takes a stream, check if it is a WAVE file
        and return the first channel of the wave file as numpy
        and get a maximum of bytes
        
        It is currently using channel 0 for extraction
        """
        self._stream_reader = stream_reader
        

        
        self._max_bytes_allowed = 1024 * 1024
        self._max_block_size_per_read = 1024  #byte
        self._channel_to_extract = 0  # for stereo, there are 2 channels, we will use channel 0

    def _populate_file_size(self, reader):
        file_size = reader.file_size()
        if file_size == None:
            raise Exception('Unknown File Size')
        if file_size < 44:
            raise Exception('File Too Small')
            
        self._file_size = file_size
    
    def set_max_byte_allowed(self, max_byte_allowed):
        self._max_bytes_allowed = max_byte_allowed
        return self
    
    def _extract_file_header_data(self, reader):
        
        
        header_data = reader.read(44)
       
        self._chunk_id, self._chunk_size, self._format_, \
        self._sub_chunk_1_id, self._sub_chunk_1_size, \
        self._audio_format, self._num_channels, \
        self._sample_rate, self._byte_rate, \
        self._block_align, self._bits_per_sample, \
        self._sub_chunk_2_id, self._sub_chunk_2_size \
        = struct.unpack("4si4s4sihhiihh4si", header_data)
        
        
        
    def _preload_calculation(self):
        self._samples_per_read = self._max_block_size_per_read / self._block_align
        self._samples_to_read = self._max_bytes_allowed / self._block_align
        
        self._file_samples = self._file_size /  self._block_align
        self._start_sample = 0
        self._end_sample = self._file_samples if self._samples_to_read > self._file_samples else self._samples_to_read
            
        
        self._npdtype = np.int16
                   
    
    def _check_is_supported(self):
        check_list = [ 
             self._chunk_id == 'RIFF',
             self._format_ == 'WAVE',
             self._sub_chunk_1_id == 'fmt ',
             self._sub_chunk_2_id == 'data',
             
             self._chunk_size + 8 == self._file_size,
             self._sub_chunk_1_size + self._sub_chunk_2_size + 20 == self._chunk_size,
            
             self._byte_rate == self._sample_rate * self._num_channels * self._bits_per_sample / 8,
             self._block_align == self._bits_per_sample / 8 * self._num_channels,
             self._bits_per_sample in [16],
             self._audio_format == 1
         ]
        
        is_ok = reduce(lambda x, y: x and y, check_list, True)
        
        return is_ok
    
    
    def _create_numpy_array(self, reader):
        
        self._np_wav_data = np.zeros(self._samples_to_read, self._npdtype)
        for pos, sample_step in step_range(self._start_sample, self._end_sample, self._samples_per_read):
            
            bytes_to_read = sample_step * self._block_align
            data = reader.read(bytes_to_read)
            if len(data) != bytes_to_read:
                raise Exception('data read is less then expected')
            
            tmp_array = np.frombuffer(data, self._npdtype).reshape((sample_step, 
                                                                    self._num_channels))
            
            
            self._np_wav_data[pos: pos + sample_step ]
            self._np_wav_data[pos: pos + sample_step ] = tmp_array[:, 0]
        
    
    def numpy_read_wav(self):
        """
        this reads the WAVE data as numpy
        
        :returns: sample_rate, numpy array of wave data
         
        """
        with Closer(self._stream_reader.open()) as reader:
            self._populate_file_size(reader)
        
            self._extract_file_header_data(reader)
            if not self._check_is_supported():
                raise Exception('Unknow file format or file not supported')
            self._preload_calculation()
            
            self._create_numpy_array(reader)
            
            
        
        return self._sample_rate, self._np_wav_data 
        
    