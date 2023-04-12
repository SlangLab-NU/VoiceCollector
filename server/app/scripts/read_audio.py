from pydub import AudioSegment
from pathlib import Path

folder = Path(__file__).absolute().parent.parent.parent / "tests" / "samples"

def read_audio(file):
    path = folder / "normal.weba"
    # path = folder / "normal.wav"
    # sound = AudioSegment.from_file(path, format="webm")
    # sound = AudioSegment.from_wav(path)
    sound = AudioSegment.from_file(path)

    print("Channels: ", sound.channels)
    print("Frame Rate: ", sound.frame_rate)
    print("Sample width: ", sound.sample_width)
    
    sound = sound.set_sample_width(2)
    print("Sample width: ", sound.sample_width)
    
    
    # sound.export(folder / "normal.wav", format="wav")
    print(sound)
    return sound

read_audio("")