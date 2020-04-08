import mido


def open_output():
    return open_steinberg_output()


def get_steinberg_device_name():
    output_names = [n for n in mido.get_output_names() if 'steinberg' in n.lower()]
    if len(output_names) != 1:
        raise Exception(f"Found the following steinberg MIDI devices: {output_names}. Expected only one")
    return output_names[0]


def open_steinberg_output():
    return mido.open_output(get_steinberg_device_name(), autoreset=True)


def open_steinberg_input():
    return mido.open_input(get_steinberg_device_name())
