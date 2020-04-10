import numpy as np

from mido import Message
from random import randint
from time import sleep

from midi_utils import open_steinberg_output


def rand_pitch():
    outport = open_steinberg_output()
    for i in range(20):
        pitch = randint(10, 60)
        outport.send(Message('note_on', note=pitch))
        sleep(0.2)
        outport.send(Message('note_off', note=pitch))


def trigger_note_msgs(note=50, time=1, chan=0):
    return [Message('note_on', note=note, time=time, channel=chan),
            Message('note_off', note=note, time=time, channel=chan)]


def demo_control():
    outport = open_steinberg_output()
    msgs = []
    msgs.append(Message('note_on', note=50, time=1))
    msgs.append(Message('note_off', note=50, time=0.5))

    repeat = 10

    for i, control_val in enumerate(np.linspace(0, 127, repeat)):
        outport.send(Message('control_change', control=17, value=int(control_val)))
        for msg in msgs:
            print(msg)
            outport.send(msg)
            sleep(msg.time)


if __name__ == '__main__':
    outport = open_steinberg_output()
    for i in range(3):
        t = 1
        on_msg, off_msg = trigger_note_msgs(time=t)
        outport.send(on_msg)
        print(on_msg)
        sleep(t)
        outport.send(off_msg)
        sleep(t)
