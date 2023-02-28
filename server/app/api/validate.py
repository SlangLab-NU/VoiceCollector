"""
Validate API route handlers

This handler handles the validation pipeline, which consists of the following steps,

Correct format? -> Appropriate volume and pauses?

Each step is performed by a module/function which takes an audio file and returns a boolean.


"""
from flask import Blueprint, jsonify

blueprint = Blueprint('validate', __name__, url_prefix="/validate")

@blueprint.route('/')
def validate():
    """Validate the audio with the pipeline

    Args:
        

    Returns:
        _type_: _description_
    """
    return jsonify(dict(msg="/validate"))


@blueprint.route('/format')
def validate_format():
    return jsonify(dict(msg="/validate/format"))


@blueprint.route('/volume_pause')
def validate_volume_pause():
    return jsonify(dict(msg="/validate/volume_pause"))


