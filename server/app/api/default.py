"""
A default handler for debug purpose.

"""

from flask import Blueprint, jsonify

blueprint = Blueprint('default', __name__, url_prefix="/")

@blueprint.route('/')
def get_scores():
    return jsonify(dict(msg="Welcome to VoiceCollector backend API."))

@blueprint.route('/get-csv', methods=['GET'])
def generate_csv():
    return jsonify({'message': 'Hello, World!'})