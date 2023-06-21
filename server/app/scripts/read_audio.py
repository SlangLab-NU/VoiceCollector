from pydub import AudioSegment
from pathlib import Path
from server.app.log import logger as logger

logger = logger.load_log()

folder = Path(__file__).absolute().parent.parent.parent / "tests" / "samples"

def read_audio(file):
    path = folder / "normal.weba"
    # path = folder / "normal.wav"
    # sound = AudioSegment.from_file(path, format="webm")
    # sound = AudioSegment.from_wav(path)
    sound = AudioSegment.from_file(path)

    logger.info(f"Channels: {sound.channels}")
    logger.info(f"Frame Rate: {sound.frame_rate}")
    logger.info(f"Sample width: {sound.sample_width}")
    
    sound = sound.set_sample_width(2)
    logger.info(f"Sample width: {sound.sample_width}")
    
    
    # sound.export(folder / "normal.wav", format="wav")
    logger.info(f"{sound}")
    return sound

read_audio("")