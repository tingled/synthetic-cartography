import librosa
import librosa.display
from matplotlib import pyplot as plt
from mido import Message
import numpy as np
from random import randint
from time import sleep

from .record import Recorder
from .midi_utils import open_steinberg_output, trigger_note_msgs
from .virus_utils import VirusPresetGenerator, create_virus_patch_msg


NOTE = 49


def rand_pitch():
    outport = open_steinberg_output()
    for i in range(20):
        pitch = randint(10, 60)
        outport.send(Message('note_on', note=pitch))
        sleep(0.2)
        outport.send(Message('note_off', note=pitch))


def trigger_note_msgs(note=NOTE, time=3, chan=0):
    return [Message('note_on', note=note, time=time, channel=chan),
            Message('note_off', note=note, time=time, channel=chan)]


def demo_control():
    outport = open_steinberg_output()
    msgs = []
    msgs.append(Message('note_on', note=NOTE, time=2))
    msgs.append(Message('note_off', note=NOTE, time=2))

    repeat = 10

    for i, control_val in enumerate(np.linspace(0, 127, repeat)):
        outport.send(Message('control_change', control=17, value=int(control_val)))
        for msg in msgs:
            print(msg)
            outport.send(msg)
            sleep(msg.time)


def demo_preset_gen():
    outport = open_steinberg_output()

    presets_file = 'data/virus_presets.csv'
    preset_generator = VirusPresetGenerator(presets_file)

    t = 2
    on_msg, off_msg = trigger_note_msgs(time=t)

    for i in range(5):
        data = preset_generator.generate_preset_from_seed(80)
        ctrl_msg = create_virus_preset_msg(data)
        outport.send(ctrl_msg)
        print(f"on:\t{on_msg}")
        outport.send(on_msg)
        sleep(t)
        print(f"off:\t{off_msg}")
        outport.send(off_msg)
        sleep(t)


def demo_record():
    outport = open_steinberg_output()
    r = Recorder()
    t = 2
    on_msg, off_msg = trigger_note_msgs(time=t)

    r.start_record()
    outport.send(on_msg)
    sleep(t)
    outport.send(off_msg)
    sleep(t)
    r.stop_record()
    sig = r.read_queue()
    # plt.plot(sig[:5000])
    S = librosa.feature.melspectrogram(y=sig, sr=r.sr)
    S_dB = librosa.power_to_db(S, ref=np.max)
    librosa.display.specshow(S_dB, sr=r.sr)
    plt.show()


if __name__ == '__main__':
    # demo_record()
    # demo_control()
    demo_preset_gen()
