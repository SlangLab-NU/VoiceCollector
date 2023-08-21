"""
A default handler for debug purpose.

"""

from flask import Blueprint, jsonify

blueprint = Blueprint('default', __name__, url_prefix="/")

@blueprint.route('/')
def get_scores():
    return jsonify(dict(msg="Welcome to VoiceCollector backend API."))