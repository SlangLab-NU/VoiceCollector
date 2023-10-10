"""
Blueprint for API endpoints

"""
from flask import Blueprint
from .default import blueprint as default
from .speak import blueprint as speak_blueprint
from .validate import blueprint as validate_blueprint
from .format import blueprint as format_blueprint

api = Blueprint('api', __name__)

api.register_blueprint(default)
api.register_blueprint(speak_blueprint)
api.register_blueprint(validate_blueprint)
api.register_blueprint(format_blueprint)