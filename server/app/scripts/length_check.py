import wave
import contextlib
from ..log import logger

logger = logger.load_log()

def get_audio_length(f):
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)
    logger.info(f"duration (s): {round(duration, 2)}")
    return duration

        