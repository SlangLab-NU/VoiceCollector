from http import server
from pathlib import Path
from re import A
import intel_score
from huggingsound import SpeechRecognitionModel
from pydub import AudioSegment


model = SpeechRecognitionModel("jonatasgrosman/wav2vec2-large-xlsr-53-english")

current_dir = Path(__file__).parent.resolve()
server_dir = current_dir.parent.parent

# F1_session1 = server_dir /  "F" / "F01" / "Session1"
# F3_session1 = server_dir /  "F" / "F03" / "Session1"
# F3_session2 = server_dir /  "F" / "F03" / "Session2"
# F3_session3 = server_dir /  "F" / "F03" / "Session3"
# F4_session1 = server_dir /  "F" / "F04" / "Session1"
# F4_session2 = server_dir /  "F" / "F04" / "Session2"

# FC1_session1 = server_dir /  "FC" / "FC01" / "Session1"
# FC2_session2 = server_dir /  "FC" / "FC02" / "Session2"
# FC2_session3 = server_dir /  "FC" / "FC02" / "Session3"
# FC3_session1 = server_dir /  "FC" / "FC03" / "Session1"
# FC3_session1 = server_dir /  "FC" / "FC03" / "Session1"
# FC3_session2 = server_dir /  "FC" / "FC03" / "Session2"

for voice_dir in server_dir.iterdir():
    if voice_dir.name not in ["F", "FC"]:
        continue
    for speaker_dir in voice_dir.iterdir():
        # if speaker_dir.name not in ["FC02"]:
        #     continue
        for session_path in speaker_dir.glob("Session*"):
            # if session_path.name not in ["Session3"]:
            #     continue
            record_path = session_path / "wav_arrayMic"

            prompt_path = session_path / "prompts"

            record_files = list(record_path.glob("*.*"))
            # prompt_files = list(prompt_path.glob("*.*"))

            broken_count = 0
            batch_size = 24
            i = 0
            total_batches = len(record_files) // batch_size

            total_scores = {"sequence_matcher": [], "cer": [], "metaphone_match": []}

            for i in range(total_batches):
                batch_record_files = record_files[i * batch_size : (i + 1) * batch_size]
                # batch_prompt_files = prompt_files[i * batch_size : (i + 1) * batch_size]

                batch_prompt_files = [prompt_path / (rf.stem + ".txt") for rf in batch_record_files]

                # Only evaluate files that have both record and prompt, since TORGO has some missing prompts
                batch_files = list(filter(lambda x: x[1].exists(), zip(batch_record_files, batch_prompt_files)))

                if len(batch_files) == 0:
                    continue

                valid_rf = []
                valid_pf = []
                for rf, pf in batch_files:
                    try:
                        AudioSegment.from_wav(rf)
                        valid_rf.append(rf)
                        valid_pf.append(pf)
                    except:
                        broken_count += 1

                # No valid files in batch
                if len(valid_rf) == 0:
                    continue

                # batch_files = zip(valid_rf, valid_pf)

                transcriptions = [x["transcription"] for x in model.transcribe(valid_rf)]
                prompts = [x.read_text() for x in valid_pf]

                a = zip(transcriptions, prompts)
                a = filter(lambda x: not "[" in x[1], a)    # Remove prompt with instructions
                a = filter(lambda x: not x[1].endswith(".jpg"), a)  # Remove prompt with picture
                a = filter(lambda x: not "xxx" in x[1], a)  # Remove prompt with unusable content
                a = filter(lambda x: len(x[0]) > 0, a)  # Remove empty transcription
                a = list(a)

                transcriptions, prompts = zip(*a)

                scores = intel_score.evaluate(transcriptions, prompts)
                for key in scores:
                    total_scores[key].extend(scores[key])

            print(session_path) 
            print("Number of broken files:", broken_count)
            for key, value in total_scores.items():
                print(f"{key}: {sum(value) / len(value)}")
            print()


