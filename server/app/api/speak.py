"""
Speak API route handlers. They handle requests related to reference text, recording, receiving audio file and so on.

"""
# import os
# import sys


import logging
from botocore.exceptions import ClientError
from flask import Blueprint, jsonify, request
from ..scripts import db_helper


conn = db_helper.connect_to_ec2()
s3 = db_helper.connect_to_s3()


blueprint = Blueprint('speak', __name__, url_prefix="/speak")


@blueprint.route('/get_reference')
def get_reference():
    """Get all reference texts

    Args:

    Returns:
        _type_: _description_
    """
    with conn.cursor() as cursor:
        cursor.execute('select * from reference')
        result = cursor.fetchall()
        return jsonify(result)

@blueprint.route('/exists_user_id/<user_id>', methods=['GET'])
def get_all_user_id_route(user_id):
    with conn.cursor() as cursor:
        cursor.execute('select exists (select distinct user_id from audio where user_id = %s)', user_id)
        result = cursor.fetchall()
        # [{"exists (select distinct user_id from audio where user_id = '<user_id'>": 1}], where value of 1 means true, 0 means false.
        return jsonify(result)

    
@blueprint.route('/write_record', methods=['POST'])
def write_record_route():
    data = request.json
    # data = {
    #     "audio_id": 3,
    #     "user_id": 1,
    #     "url": "audio_id_user_id_ref_id.mp3",
    #     "date": "2023-03-23 12:34:56",
    #     "validated": True,
    #     "ref_id": 5,
    #     "sequence_matcher_score": 0.9,
    #     "cer_score": 0.8,
    #     "metaphone_match_score": 0.7
    # }
    try:
        db_helper.write_record(data, conn)
        return jsonify({"result": "success"})
    except Exception as e:
        return jsonify({"result": "error", "message": str(e)}), 400
    
@blueprint.route('/write_file/<url>', methods=['POST'])
def write_file_route(url):
    # data = request.json
    data = "test_recording.mp3"
    # Upload file to S3 bucket
    try:
        # data: the path of audio file that needs to be uploaded. 
        # url: the name of the file in S3, must be the same as url in audio table.
        response = s3.upload_file(data, Key=f'{url}') # <Response 5 bytes [200 OK]>
    except ClientError as e:
        response = logging.error(e)
    return jsonify(response)


