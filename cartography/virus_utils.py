"""
we can inspect the factory installed presets for the access virus
by reading its MIDI sysex dumps.

these messages are formatted: (0, 32, 51, 1, dd, 16, bb, ss, [256 ints], cs)
where dd is the device id, bb is bank, ss is program number, and cs is checksum

we can also use this same fromat to write parameters to the working preset

for more info see page 255 of the virus B manual: https://www.virus.info/downloads
"""

from mido import Message
import numpy as np
from numpy import ndarray
from pandas import DataFrame
from typing import Callable, List

VIRUS_SYSEX_HEADER = [0, 32, 51, 1, 0, 16, 0, 127]
VIRUS_SYSEX_CHECKSUM = [0]  # this value seems to be ignored on write


def parse_virus_preset_dump(msg: Message) -> List[int]:
    """
    strips sysex header and checksum bits to return list of presets
    """
    data = list(msg.data[len(VIRUS_SYSEX_HEADER): -len(VIRUS_SYSEX_CHECKSUM)])
    assert len(data) == 256
    return data


def create_virus_preset_msg(params: list) -> Message:
    """
    takes a list of 256 parameter values and creates a Mido sysex message
    to update the virus
    """
    assert len(params) == 256, params
    data = VIRUS_SYSEX_HEADER + params + VIRUS_SYSEX_CHECKSUM
    return Message('sysex', data=data)
