"""
Speak API route handlers. They handle requests related to reference text, recording, receiving audio file and so on.

"""



import traceback
import mimetypes
import pathlib
import jsonschema
from minio.error import S3Error
from flask import Blueprint, current_app, jsonify, request

from ..scripts import db_helper
from ..scripts import get_csv
from .format import convert_to_wav_handler
from .validate import check_audio_format, check_volume_pause
from ..log import logger

logger = logger.load_log()

import threading

lock = threading.Lock()

AUDIO_SCHEMA = {
    "type": "object",
    "properties": {
        "session_id": {"type": "string"},
        "s3_url": {"type": "string"},
        "date": {"type": "string", "format": "date-time"},
        "ref_id": {"type": "integer"}
    },
    "required": [
        "session_id",
        "s3_url",
        "date",
        "ref_id"
    ],
    "additionalProperties": False
}

current_dir = pathlib.Path(__file__).parent.resolve()
tmp_dir = current_dir.parent.parent / "tmp"

client, s3_bucket = db_helper.connect_to_s3()

blueprint = Blueprint('speak', __name__, url_prefix="/speak")

# References get written to db here every time at start
# db_helper.write_references_to_db()

@blueprint.route('/')
def get_scores():
    return jsonify(dict(msg="Welcome to speaker route."))

@blueprint.route('/get_reference')
def get_reference_hanlder():
    """Get all reference texts

    Args:

    Returns:
        _type_: _description_
    """
    
    try:
        references = db_helper.get_reference()
        return jsonify(references)

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
        records = db_helper.get_records()
        return jsonify(records)

    except Exception as e:
        error_message = str(e)
        return jsonify({"error": error_message}), 500

@blueprint.route('/get_csv', methods=['GET'])
def get_csv():
    """Get containing paths to audio files and their corresponding transcriptions

    Args:

    Returns:
        _type_: _description_
    """
    return jsonify({'message': 'Hello, 1test!'})

@blueprint.route('/write_record', methods=['POST'])
def write_record_route():
    data = request.json
    try:
        jsonschema.validate(instance=data, schema=AUDIO_SCHEMA)
    except jsonschema.ValidationError as e:
        return jsonify({"result": "error", "message": str(e)}), 400

    try:
        db_helper.write_record(data)
        return jsonify({"result": "success"})
    except Exception as e:
        return jsonify({"result": "error", "message": str(e)}), 400


def get_content_type(filename):
    mimetype, _ = mimetypes.guess_type(filename)
    if mimetype is not None:
        return mimetype
    else:
        return 'application/octet-stream'


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
    
    # Upload file to S3 bucket
    try:
        content_type = get_content_type(file_path.name)
        client.fput_object(bucket_name=s3_bucket,
                           object_name=file_path.name,
                           file_path=file_path)
    except S3Error as e:
        current_app.logger.error(e)
        return jsonify(msg="Error: Failed to upload file to S3"), 400
    
    # Write record to database
    try:
        db_helper.write_record(data)
        return jsonify(msg="Success: audio submitted"), 200
    except Exception as e:
        logger.info(traceback.format_exc())
        return jsonify(msg="Error: " + str(e)), 400
