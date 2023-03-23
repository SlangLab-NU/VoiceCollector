"""
Speak API route handlers. They handle requests related to reference text, recording, receiving audio file and so on.

"""
# import os
# import sys

# # Add the parent directory of app to sys.path
# parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
# sys.path.append(parent_dir)

# # Now you can import the conn variable from app/__init__.py
# from app import conn



from flask import Blueprint, jsonify, request
from ..scripts import db_helper
import json

conn = db_helper.connect_to_ec2()

blueprint = Blueprint('speak', __name__, url_prefix="/speak")

@blueprint.route('/')
def speak():
    """Get all reference texts

    Args:

    Returns:
        _type_: _description_
    """
    return jsonify(dict())


@blueprint.route('/get_reference')
def get_reference():
    """Get all reference texts

    Args:

    Returns:
        _type_: _description_
    """
    with conn.cursor() as cursor:
        cursor.execute('use voice_collector')
        cursor.execute('select * from reference')
        result = cursor.fetchall()
        return jsonify(result)
    
@blueprint.route('/write_record', methods=['POST'])
def write_record_route():
    try:
        #db_helper.write_record(json.dumps(record), conn)
        query = """INSERT INTO audio (audio_id, user_id, url, date, validated, ref_id, sequence_matcher_score, cer_score, metaphone_match_score)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
        with conn.cursor() as cursor:
            cursor.execute(query, (1,1,"http://example.com/audio.mp3", '2020-01-03 00:00:00', True, 1, 0.5, 0.5, 0.5))
        conn.commit()
        return jsonify({"result": "success"})
    except Exception as e:
        return jsonify({"result": "error", "message": str(e)}), 400