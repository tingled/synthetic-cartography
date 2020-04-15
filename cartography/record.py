import numpy as np
import pyaudio
from pyaudio import PyAudio
from queue import Queue
import struct

from time import sleep


def get_steinberg_device_idx(pa: PyAudio) -> int:
    """
    looks up the steinberg device index
    """
    for i in range(pa.get_device_count()):
        name = pa.get_device_info_by_index(i)['name']
        if 'steinberg' in name.lower():
            return i
    raise Exception("Couldn't find steinberg audio device")


class Recorder:
    def __init__(self, chunk_size=512, channels=1):
        # for some reason, when chunk size is 1024 we observe some
        # non-random discontonuities in the signal every 1024*3 samples,
        # which leads to very noticeable transients in the spectrogram
        self.format = pyaudio.paFloat32
        self.chunk_size = chunk_size
        self.channels = channels
        self.pa = PyAudio()
        self.frame_queue = Queue()
        self.device_idx = get_steinberg_device_idx(self.pa)
        self.sr = int(self.pa.get_device_info_by_index(self.device_idx)['defaultSampleRate'])

    def _get_callback(self):
        def cb(input_data, frame_cnt, time_info, status_flags):
            self.frame_queue.put(input_data)
            return (None, pyaudio.paContinue)
        return cb

    def start_record(self):
        self.stream = self.pa.open(
                input_device_index=self.device_idx,
                rate=self.sr,
                format=self.format,
                channels=self.channels,
                input=True,
                stream_callback=self._get_callback(),
                frames_per_buffer=self.chunk_size)

    def stop_record(self):
        self.stream.stop_stream()
        # unpacker = struct.Struct('f' * self.chunk_size)
        # input_data = None  # TODO
        # output = []
        # output += unpacker.unpack(input_data)

    def read_queue(self):
        s = struct.Struct('f'*self.chunk_size)
        y = []
        while not self.frame_queue.empty():
            y += s.unpack(self.frame_queue.get())
        return np.array(y)


if __name__ == '__main__':
    r = Recorder()
    r.start_record()
    sleep(2)
    r.stop_record()
    print(r.read_queue())
