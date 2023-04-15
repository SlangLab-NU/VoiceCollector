"""
Intel API route handlers. It handles requests to calculate the intelligibility score.

"""
from flask import Blueprint, jsonify, request, abort, redirect, url_for
import os
from huggingsound import SpeechRecognitionModel
from werkzeug.utils import secure_filename
from pathlib import Path
from ..scripts import intel_score

UPLOAD_FOLDER = Path(__file__).parent.parent / "uploads"
ALLOWED_EXTENSIONS = {'wav'}

blueprint = Blueprint('intel', __name__, url_prefix="/intel")

model = SpeechRecognitionModel("jonatasgrosman/wav2vec2-large-xlsr-53-english")


def transcribe(model, audio_files):
    transcriptions = model.transcribe(audio_files)
    return {'transcriptions': [x["transcription"] for x in transcriptions]}


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@blueprint.route('/transcribe', methods=["POST"])
def get_transcripts():
    # check if the post request has the file part
    if 'audio' not in request.files:
        return jsonify(msg="No file part"), 400
    files = request.files.getlist("audio")
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    for f in files:
        if f.filename == '':
            return jsonify(msg="Not selected file exists"), 400
        if not allowed_file(f.filename):
            return jsonify(msg="Not allowed extension exists"), 400
    
    # filename = secure_filename(file.filename)
    # file.save(UPLOAD_FOLDER / filename)
    # return redirect(url_for('download_file', name=filename))
    response = jsonify(transcribe(model, files))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
        


@blueprint.route('/', methods=["POST"])
def predict_scores():
    # After db is setup, `data` should look like `{"audio_id", "..." "ref_id": "..."}` and the audio file is uploaded
    # y_pred = get_transcripts().json
    if 'audio' not in request.files:
        return jsonify(msg="No file part"), 400

    data = request.form
    y_true = data.getlist("ref")

    files = request.files.getlist("audio")
    
    if len(files) != len(y_true):
        return jsonify(msg="The number of audio files and reference does not match"), 400

    for f in files:
        if f.filename == '':
            return jsonify(msg="Not selected file exists"), 400
        if not allowed_file(f.filename):
            return jsonify(msg="Not allowed extension exists"), 400
    
    y_pred = transcribe(model, files)["transcriptions"]
    
    return intel_score.evaluate(y_pred, y_true)


@blueprint.route('/scores', methods=["POST"])
def get_scores():
    """
    Return scores with transcripts and reference provided.
    """
    y_pred, y_true = request.json["pred"], request.json["ref"]
    return intel_score.evaluate(y_pred, y_true)

