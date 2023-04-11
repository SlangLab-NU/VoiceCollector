"""
Speak API route handlers. They handle requests related to reference text, recording, receiving audio file and so on.

"""
# import os
# import sys


import logging
from botocore.exceptions import ClientError
from flask import Blueprint, jsonify, request
from ..scripts import db_helper
import mimetypes

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

    
@blueprint.route('/write_record', methods=['POST'])
def write_record_route():
    data = request.json
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
        if 'file' not in request.files:
            response = jsonify(dict(msg="Error: No audio files in request"))
            return response
        
    # Upload file to S3 bucket
    try:
        # url: the name of the file in S3, must be the same as url in audio table in mysql.
        file = request.files['file']
        content_type = get_content_type(file.filename)
        response = s3.upload_fileobj(file, url, ExtraArgs={'ContentType': content_type})       
    except ClientError as e:
        response = logging.error(e)
    return jsonify(response)


