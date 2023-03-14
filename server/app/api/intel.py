"""
Intel API route handlers. It handles requests to calculate the intelligibility score.

"""
from flask import Blueprint, jsonify

blueprint = Blueprint('intel', __name__, url_prefix="/intel")

class Model:
    def __init__(self) -> None:
        print("MODEL created")
    
    def __del__(self):
        print("Model destroyed")
    
    def inference(self):
        print("Model infer")

model = Model()

@blueprint.route('/')
def get_scores():
    model.inference()
    return jsonify(dict(msg="/get_scores"))


@blueprint.route('/sequence_matcher')
def get_sequence_matcher_score():
    model.inference()

    return jsonify(dict(msg="/sequence_matcher"))


@blueprint.route('/levenshtein_distance')
def get_levenshtein_distance_score():
    model.inference()
    return jsonify(dict(msg="/levenshtein_distance"))


