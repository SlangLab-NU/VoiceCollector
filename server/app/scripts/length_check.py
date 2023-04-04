

import wave
import contextlib

def get_audio_length(f):
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)
    print("duration (s): ", round(duration, 2))
    return duration

        