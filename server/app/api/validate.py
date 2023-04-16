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


def check_suffix(file):
    suffix = file.filename.split(".")[-1]
    result = suffix == config["format"]
    info = {}
    if not result:
        info = {"suffix": {"expected": config['format'], "actual": suffix}}
    return suffix == config['format'], info


def check_audio_format(file):
    with sf.SoundFile(file) as f:
        result = True
        info = {}
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
                info[check_name] = {"expected": expected, "actual": actual}
        
        if info != {}:
            result = False

    return result, info

def check_volume_pause(file):
    result = True
    info = {}

    with contextlib.closing(wave.open(file,'rb')) as wf:
        # length check
        duration = length_check.get_audio_length(wf)
        if duration < config['shortest_length_for_sentence']:
            # failed at length check
            info = {"shortest_length_for_sentence": {"expected": config['shortest_length_for_sentence'], "actual": duration}}
            result = False
        else:
            # volume and pause check
            voiced_count, total_count, silence_ratio = silence_check.get_silence_ratio(config['vad_mode'], wf)
            volume = volume_check.get_volume(file)
            if  silence_ratio > config['silence_ratio'] and volume < config['lowest_dBFS']:
                info = {"silence_ratio": {"expected": "< " + str(config['silence_ratio']), "actual": silence_ratio},
                        "volume": {"expected": "> " + str(config['lowest_dBFS']), "actual": volume}}
                result = False
            else:
                info = {"silence_ratio": silence_ratio, "volume": volume}

    return result, info


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
        if 'audio' not in request.files:
            return jsonify(msg="Error: No audio files in request"), 400

        file = request.files['audio']

        if file.filename == '':
            return jsonify(msg="Not selected file exists"), 400
            
        result, info = check_suffix(file)
        if not result:
            response = jsonify(info=info, result=False)
            response.headers.add('Access-Control-Allow-Origin', '*')
            return response
        
        result, info = check_audio_format(file)
        response = jsonify(info=info, result=result)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
            

@blueprint.route('/volume_pause',methods=['POST'])
def validate_volume_pause():
    if request.method == 'POST' :
        # check if the post request has the file part
        if 'audio' not in request.files:
            return jsonify(msg="Error: No audio files in request"), 400

        file = request.files['audio']
        
        if file.filename == '':
            return jsonify(msg="Not selected file exists"), 400
        
        result, info = check_volume_pause(file)
        response = jsonify(info=info, result=result)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response




