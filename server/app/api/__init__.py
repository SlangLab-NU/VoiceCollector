"""
Blueprint for API endpoints

"""
from flask import Blueprint


api = Blueprint('api', __name__)


from .speak import blueprint as speak_blueprint
from .validate import blueprint as validate_blueprint
api.register_blueprint(speak_blueprint)
api.register_blueprint(validate_blueprint)

