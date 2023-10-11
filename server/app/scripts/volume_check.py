
from pydub import AudioSegment

def match_target_amplitude(file, target_dBFS):
    db_path = ""
    sound = AudioSegment.from_file(file, "wav")
    normalized_sound = match_target_amplitude(sound, -16.0)
    normalized_sound.export(db_path, format="wav")
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)


def get_volume(audio_file):
    sound = AudioSegment.from_wav(audio_file)
    volume = sound.dBFS  
    return volume

