"""
Hello API route handlers

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
    return jsonify(dict(texts=["I am happy to meet you.", "The cat sat on the mat."]))