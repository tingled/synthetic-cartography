import numpy as np

from mido import open_output, Message
from random import randint
from time import sleep


def rand_pitch():
    outport = open_output()
    for i in range(20):
        pitch = randint(10, 60)
        outport.send(Message('note_on', note=pitch, channel=1))
        sleep(0.2)
        outport.send(Message('note_off', note=pitch, channel=1))


def demo_control():
    outport = open_output()

    chans = 16

    for chan in range(chans):
        print(f'onset on channel {chan}')
        outport.send(Message('note_on', note=50, time=1, channel=chan))
        sleep(1)
        outport.send(Message('note_off', note=50, time=0.5, channel=chan))
        sleep(0.5)


if __name__ == '__main__':
    demo_control()
