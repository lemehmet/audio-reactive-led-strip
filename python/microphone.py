import time
import numpy as np
import pyaudio
import config


def start_stream(callback, running_config):
    p = pyaudio.PyAudio()
    frames_per_buffer = int(running_config['MIC_RATE'] / running_config['FPS'])
    stream = p.open(input_device_index = running_config['INPUT_DEVICE_INDEX'],
    format=pyaudio.paInt16,
                    channels=1,
                    rate=running_config['MIC_RATE'],
                    input=True,
                    frames_per_buffer=frames_per_buffer)
    overflows = 0
    prev_ovf_time = time.time()
    while True:
        try:
            y = np.fromstring(stream.read(frames_per_buffer, exception_on_overflow=False), dtype=np.int16)
            y = y.astype(np.float32)
            stream.read(stream.get_read_available(), exception_on_overflow=False)
            callback(y)
        except IOError:
            overflows += 1
            if time.time() > prev_ovf_time + 1:
                prev_ovf_time = time.time()
                print('Audio buffer has overflowed {} times'.format(overflows))
    stream.stop_stream()
    stream.close()
    p.terminate()
