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



from flask import Blueprint, jsonify
from ..scripts import db_helper

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
        cursor.execute('use voicecollector')
        cursor.execute('select * from reference')
        result = cursor.fetchall()
        return jsonify(result)