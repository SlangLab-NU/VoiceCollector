"""
Intel API route handlers. It handles requests to calculate the intelligibility score.

"""
from flask import Blueprint, jsonify, request
from ..scripts import intel_score

blueprint = Blueprint('intel', __name__, url_prefix="/intel")

@blueprint.route('/', methods=["GET"])
def get_scores():
    # After db is setup, `data` should look like `{"audio_id", "..." "ref_id": "..."}` and the audio file is uploaded
    data = request.json
    y_pred, y_true = data["y_pred"], data["y_true"]
    return intel_score.evaluate(y_pred, y_true)
    

@blueprint.route('/sequence_matcher')
def get_sequence_matcher_score():
    return jsonify(dict(msg="/sequence_matcher"))


# @blueprint.route('/levenshtein_distance')
# def get_levenshtein_distance_score():
#     return jsonify(dict(msg="/levenshtein_distance"))


