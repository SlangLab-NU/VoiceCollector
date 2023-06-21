

import wave
import contextlib
from server.app.log import logger as logger

logger = logger.load_log()

def get_audio_length(f):
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)
    logger.info(f"duration (s): {round(duration, 2)}")
    return duration

        