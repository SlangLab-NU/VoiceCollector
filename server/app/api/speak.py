"""
Speak API route handlers. They handle requests related to reference text, recording, receiving audio file and so on.

"""
from flask import Blueprint, jsonify

blueprint = Blueprint('speak', __name__, url_prefix="/speak")

@blueprint.route('/')
def speak():
    """Get all reference texts

    Args:

    Returns:
        _type_: _description_
    """
    return jsonify(dict())


@blueprint.route('/get_reference')
def get_reference():
    """Get all reference texts

    Args:

    Returns:
        _type_: _description_
    """
    return jsonify(dict(texts=["The cat sat on the mat.", ]))