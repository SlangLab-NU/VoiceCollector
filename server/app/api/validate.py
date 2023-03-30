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
            filename_format_check = (file.filename.split(".")[-1] == config['major_format'].lower())
            with sf.SoundFile(file) as f:
                major_format_check = (f.format == config['major_format'])
                sample_rate_check = (f.samplerate == config['sample_rate'])
                channel_check = (f.channels == config['channels'])
                subtype_check = (f.subtype == config['subtype'])
                if filename_format_check and major_format_check and sample_rate_check and channel_check and subtype_check:
                    return jsonify(result=True)
                else:
                    return jsonify(result=False)
    
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
                    return jsonify(result=False)

                # volume and pause check
                silence_ratio = silence_check.is_valid_speech(config['vad_mode'],wf)
                volume = volume_check.get_volume(file)
                # print("silence_ratio: %f", silence_ratio)
                if  silence_ratio > config['silence_ratio'] and volume < config['lowest_dBFS']:
                    return jsonify(result=False)
                else:
                    return jsonify(result=True)




