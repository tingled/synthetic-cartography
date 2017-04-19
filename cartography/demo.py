import numpy as np

from mido import open_output, Message
from random import randint
from time import sleep


def rand_pitch():
    outport = open_output()
    for i in range(20):
        pitch = randint(10, 60)
        outport.send(Message('note_on', note=pitch))
        sleep(0.2)
        outport.send(Message('note_off', note=pitch))


def demo_control():
    outport = open_output()
    msgs = []
    msgs.append(Message('note_on', note=50, time=1))
    msgs.append(Message('note_off', note=50, time=0.5))

    repeat = 10

    for i, control_val in enumerate(np.linspace(0, 127, repeat)):
        outport.send(Message('control_change', control=17, value=int(control_val)))
        for msg in msgs:
            outport.send(msg)
            sleep(msg.time)


if __name__ == '__main__':
    demo_control()
