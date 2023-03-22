"""
Speak API route handlers. They handle requests related to reference text, recording, receiving audio file and so on.

"""
from flask import Blueprint, jsonify
from .. import conn 

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
        # cursor.execute('SELECT * FROM reference')
        cursor.execute('use voicecollector')
        cursor.execute('select * from reference')
        result = cursor.fetchall()
        return jsonify(result)
    #return jsonify(dict(texts=["The cat sat on the mat.", ]))