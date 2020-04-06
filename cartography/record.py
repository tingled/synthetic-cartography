import numpy as np
import pyaudio
import struct

from time import sleep

class Recorder:
    def __init__(chunk_size=1024, sr=22050, channels=1):
        self.format = pyaudio.paFloat32
        self.chunk_size = chunk_size
        self.sr = sr
        self.channels = channels
        self.pa = pyaudio.PyAudio()
        self.frames = None

    def _get_callback(self):
        def cb(input_data, frame_cnt, time_info, status_flags):
            self.frame_queue.push(input_data)
            return (None, pyaudio.paContinue)
        return cb

    def start_record(self):
        self.stream = self.pa.open(
                format=self.format,
                channels=self.channels,
                input=True,
                frames_per_buffer=chunk_size)

    def stop_record(self):
        unpacker = struct.Struct('f' * self.chunk_size)

        output += unpacker.unpack(input_data)

p = pyaudio.PyAudio()
stop_time = 0

def callback(input_data, frame_cnt, time_info, status_flags):
    print('.')
    global stop_time
    print(stop_time)
    if time_info['input_buffer_adc_time'] > stop_time:
        return (None, pyaudio.paComplete)
    else:
        return (None, pyaudio.paContinue)

stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=22050,
                input=True,
                frames_per_buffer=1024,
                stream_callback=callback)

stop_time = stream.get_time() + 2

print("* recording")
sleep(1)

frames = []

"""
#for i in range(0, int(np.ceil(RATE / CHUNK * RECORD_SECONDS))):
#data = stream.read(CHUNK)
#frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

#s = struct.Struct('f'*CHUNK)
y = []
for frame in frames:
    y += s.unpack(frame)
"""
#for i in range(0, int(np.ceil(RATE / CHUNK * RECORD_SECONDS))):
#data = stream.read(CHUNK)
#frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

#s = struct.Struct('f'*CHUNK)
y = []
for frame in frames:
    y += s.unpack(frame)
