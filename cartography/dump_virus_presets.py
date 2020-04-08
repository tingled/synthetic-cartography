"""
the purpose of this script is to download the factory presets from the access
virus via a midi sysex dump
"""
import pandas as pd
from time import sleep
from queue import Queue

from midi_utils import open_steinberg_input


input_port = open_steinberg_input()

print('start dumping now')
input('press any key when finished')

data = []

for msg in input_port.iter_pending():
    data.append(msg.data)

print(f"found {len(data)} presets")

df = pd.DataFrame(data)
df.to_csv('virus_presets.csv')
