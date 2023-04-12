"""
Validate API route handlers

This handler handles the validation pipeline, which consists of the following steps,

Correct format? -> Appropriate volume and pauses?

Each step is performed by a module/function which takes an audio file and returns a boolean.


"""
from flask import Blueprint, jsonify, request, flash
from ..scripts import silence_check, volume_check, length_check
import wave
import contextlib
import json
import pathlib
import soundfile as sf

blueprint = Blueprint('validate', __name__, url_prefix="/validate")

current_dir = pathlib.Path(__file__).parent.resolve()
config_path = current_dir / ".." / "config.json"
with open(config_path, "r") as f:
    config = json.load(f)

@blueprint.route('/',methods=["GET"])
def validate():
    """Validate the audio with data format, volume and pause check

    Args:
        

    Returns:
        _type_: _description_
    """
    return jsonify(dict(msg="/validate"))


@blueprint.route('/format',methods=['POST'])
def validate_format():
    if request.method == 'POST' :
        if 'file' not in request.files:
            return jsonify(dict(msg="Error: No audio files in request"))
    
        else:
            file = request.files['file']
            expected_format = config['format']
            postfix = file.filename.split(".")[-1]
            postfix_check = (postfix == expected_format)
            if not postfix_check:
                response = jsonify(postfix={"expected": expected_format, "actual": postfix}, result=False)
                response.headers.add('Access-Control-Allow-Origin', '*')
                return response
            
            with sf.SoundFile(file) as f:
                result = True
                response = {}
                for SoundFile_attr, check_name  in zip(
                    [
                        "format",
                        "samplerate",
                        "channels",
                        "subtype",
                    ],
                    [
                        "major_format",
                        "sample_rate",
                        "channels",
                        "subtype",
                    ],
                    
                ):
                    actual = getattr(f, SoundFile_attr)
                    expected = config[check_name]
                    if actual != expected:
                        if result:
                            result = False
                        response[check_name] = {"expected": expected, "actual": actual}

                return jsonify(**response, result=result)
    
    return jsonify(dict(msg="/validate/format"))


@blueprint.route('/volume_pause',methods=['POST'])
def validate_volume_pause():
    global vad, target_dbfs
    if request.method == 'POST' :
            # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify(dict(msg="Error: No audio files in request"))
        else: 
            file = request.files['file']
            with contextlib.closing(wave.open(file,'rb')) as wf:
                # length check
                duration = length_check.get_audio_length(wf)
                if duration < config['shortest_length_for_sentence']:
                    # failed at length check
                    return jsonify(shortest_length_for_sentence={"expected": config['shortest_length_for_sentence'], "actual": duration}, result=False)

                # volume and pause check
                voiced_count, total_count, silence_ratio = silence_check.get_silence_ratio(config['vad_mode'], wf)
                volume = volume_check.get_volume(file)
                if  silence_ratio > config['silence_ratio'] and volume < config['lowest_dBFS']:
                    return jsonify(silence_ratio={"expected": "< " + str(config['silence_ratio']), "actual": silence_ratio}, 
                                    volume={"expected": "> " + str(config['lowest_dBFS']), "actual": volume},  
                                    result=False)
                else:
                    return jsonify(silence_ratio=silence_ratio, volume=volume ,result=True)




