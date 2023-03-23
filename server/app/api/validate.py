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

blueprint = Blueprint('validate', __name__, url_prefix="/validate")

vad = 3

@blueprint.route('/',methods=["GET"])
def validate():
    """Validate the audio with data format, volume and pause check

    Args:
        

    Returns:
        _type_: _description_
    """
    return jsonify(dict(msg="/validate"))


@blueprint.route('/format',methods=['GET', 'POST'])
def validate_format():
    return jsonify(dict(msg="/validate/format"))


@blueprint.route('/volume_pause',methods=['GET', 'POST'])
def validate_volume_pause():
    global vad, target_dbfs
    if request.method == 'POST' :
            # check if the post request has the file part
        if 'file' not in request.files:
            return jsonify(dict(msg="Error: No audio files in request"))
        else: 
            file = request.files['file']
            with contextlib.closing(wave.open(file,'rb')) as wf:
                duration = length_check.get_audio_length(wf)
                if duration < 0.15:
                    # failed at length check
                    return jsonify(result=False)
                silence_ratio = silence_check.is_valid_speech(vad,wf)
                volume = volume_check.get_volume(file)
                print("volume: %f", volume)
                # print("silence_ratio: %f", silence_ratio)
                if  silence_ratio > 0.9 and volume < -18:
                    return jsonify(result=False)
                else:
                    return jsonify(result=True)
    if request.method == 'GET':
            return jsonify(dict(msg="/validate/volume_pause/GET"))





