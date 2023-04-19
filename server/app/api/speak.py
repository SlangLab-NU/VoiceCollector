"""
Speak API route handlers. They handle requests related to reference text, recording, receiving audio file and so on.

"""




import logging
import mimetypes
import pathlib

import jsonschema
from botocore.exceptions import ClientError
from flask import Blueprint, current_app, jsonify, request

from ..scripts import db_helper, intel_score
from .format import convert_to_wav_handler
from .intel import model, transcribe
from .validate import check_audio_format, check_volume_pause

import threading

lock = threading.Lock()

AUDIO_SCHEMA = {
    "type": "object",
    "properties": {
        "session_id": {"type": "string"},
        "s3_url": {"type": "string"},
        "date": {"type": "string", "format": "date-time"},
        "validated": {"type": "boolean"},
        "ref_id": {"type": "integer"},
        "sequence_matcher": {"type": "number"},
        "cer": {"type": "number"},
        "metaphone_match": {"type": "number"}
    },
    "required": [
        "session_id",
        "s3_url",
        "date",
        "validated",
        "ref_id",
        "sequence_matcher",
        "cer",
        "metaphone_match"
    ],
    "additionalProperties": False
}

current_dir = pathlib.Path(__file__).parent.resolve()
tmp_dir = current_dir.parent.parent / "tmp"

conn = db_helper.connect_to_ec2()
s3 = db_helper.connect_to_s3()

blueprint = Blueprint('speak', __name__, url_prefix="/speak")


@blueprint.route('/get_reference')
def get_reference_hanlder():
    """Get all reference texts

    Args:

    Returns:
        _type_: _description_
    """
    try:
        with conn.cursor() as cursor:
            lock.acquire()
            cursor.execute('select * from reference')
            result = cursor.fetchall()
            lock.release()
            return jsonify(result)
    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 500
        

@blueprint.route('/get_records')
def get_records():
    """Get all records

    Args:

    Returns:
        _type_: _description_
    """
    try:
        with conn.cursor() as cursor:
            lock.acquire()
            cursor.execute('select * from audio')
            result = cursor.fetchall()
            lock.release()
            return jsonify(result)
    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 500


@blueprint.route('/write_record', methods=['POST'])
def write_record_route():
    data = request.json
    try:
        jsonschema.validate(instance=data, schema=AUDIO_SCHEMA)
    except jsonschema.ValidationError as e:
        return jsonify({"result": "error", "message": str(e)}), 400

    try:
        db_helper.write_record(data, conn)
        return jsonify({"result": "success"})
    except Exception as e:
        return jsonify({"result": "error", "message": str(e)}), 400


def get_content_type(filename):
    mimetype, _ = mimetypes.guess_type(filename)
    if mimetype is not None:
        return mimetype
    else:
        return 'application/octet-stream'
    
@blueprint.route('/write_file/<url>', methods=['POST'])
def write_file_route(url):
    if request.method == 'POST' :
            # check if the post request has the file part
        if 'audio' not in request.files:
            response = jsonify(dict(msg="Error: No audio files in request")), 400
            return response
        
    # Upload file to S3 bucket
    try:
        # url: the name of the file in S3, must be the same as url in audio table in mysql.
        file = request.files['audio']
        if file.filename == '':
            return jsonify(msg="Not selected file exists"), 400
        content_type = get_content_type(file.filename)
        s3.upload_fileobj(file, url, ExtraArgs={'ContentType': content_type})       
    except ClientError as e:
        current_app.logger.error(e)
        response = jsonify(msg="Error: Failed to upload file to S3"), 400
    return jsonify(msg="Success: File uploaded to S3"), 200


@blueprint.route('/submit/<url>', methods=['POST'])
def submit_handler(url):
    # Example of data submitted by frontend
    # data = {
    #     "session_id": "session_id234",
    #     "date": "2023-03-23 12:34:56",
    #     "ref_id": 3,
    # }
    data = dict(request.form)
    data["s3_url"] = url
    data["ref_id"] = int(data["ref_id"])
    
    # Convert audio file to wav format
    response = convert_to_wav_handler()
    if type(response) is tuple and response[1] == 400:
        return response

    file = request.files['audio']
    filename = file.filename.split(".")[0]
    file_path = tmp_dir / f"{filename}.wav"
    assert file_path.exists(), "Converted file does not exist"

    # Validate audio file
    result, info = check_audio_format(file_path)
    if not result:
        return jsonify(info), 400

    result, info = check_volume_pause(str(file_path))
    if not result:
        return jsonify(info), 400

    # Get intelligibility scores
    reference = db_helper.get_reference(conn)
    ref = [r["prompt"] for r in reference if r["ref_id"] == data["ref_id"]][0]

    y_pred = transcribe(model, [file_path])["transcriptions"][0]
    scores = intel_score.evaluate(y_pred, ref)

    data["validated"] = True
    for k, v in scores.items():
        data[k] = v
    
    # Upload file to S3 bucket
    try:
        content_type = get_content_type(file_path.name)
        s3.upload_file(file_path, url, ExtraArgs={'ContentType': content_type})       
    except ClientError as e:
        current_app.logger.error(e)
        return jsonify(msg="Error: Failed to upload file to S3"), 400
    
    # Write record to database
    try:
        db_helper.write_record(data, conn)
        return jsonify(msg="Success: audio submitted"), 200
    except Exception as e:
        return jsonify(msg="Error: " + str(e)), 400
