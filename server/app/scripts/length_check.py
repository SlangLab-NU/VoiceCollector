

import wave
import contextlib

def get_audio_length(f):
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)
    print("duration: %f",duration)
    return duration

        