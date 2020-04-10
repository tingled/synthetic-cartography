"""
the purpose of this script is to download the factory presets from the access
virus via a midi sysex dump
"""
import pandas as pd

from midi_utils import open_steinberg_input
from virus_utils import parse_virus_preset_dump


input_port = open_steinberg_input()

print('start dumping now')
input('press any key when finished')

data = []

for msg in input_port.iter_pending():
    data.append(parse_virus_preset_dump(msg))

print(f"found {len(data)} presets")

df = pd.DataFrame(data)
df.to_csv('data/virus_presets.csv', index=False)
