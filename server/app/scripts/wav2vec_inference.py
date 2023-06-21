from huggingsound import SpeechRecognitionModel
from server.app.log import logger as logger

logger = logger.load_log()

model = SpeechRecognitionModel("jonatasgrosman/wav2vec2-large-xlsr-53-english")
# audio_paths = ["/path/to/file.mp3", "/path/to/another_file.wav"]
audio_paths = [
    "D:/capstone/VoiceCollector/server/F/F01/Session1/wav_headMic/0132.wav",
    "D:/capstone/VoiceCollector/server/F/F01/Session1/wav_headMic/0130.wav",
    "D:/capstone/VoiceCollector/server/F/F03/Session3/wav_headMic/0162.wav",
    "D:/capstone/VoiceCollector/server/F/F03/Session3/wav_headMic/0199.wav",
    "D:/capstone/VoiceCollector/server/F/F03/Session3/wav_headMic/0182.wav",
]
# prompt_ids = ["0132", "0130"]
prompts = [
    "When he speaks, his voice is just a bit cracked and quivers a trifle.",
    "Grandfather likes to be modern in his language.",
    "Night after night, they received annoying phone calls.",
    "Help Greg to pick a peck of potatoes.",
    "He played basketball there while working toward a law degree."
]
transcriptions = model.transcribe(audio_paths)
logger.info(f'{[x["transcription"] for x in transcriptions]}')

# references = [{"path": audio_paths[i], "transcription": prompts[i]} for i in range(len(audio_paths))]
# evaluation = model.evaluate(references)
# print(evaluation)
