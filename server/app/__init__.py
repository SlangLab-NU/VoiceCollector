"""
Primary Flask app

"""
import sqlite3
from flask import Flask, jsonify, render_template
from flask_cors import CORS

from .api import api as api_blueprint
from .errors import add_error_handlers

app = Flask(__name__)

def create_app(): 
    CORS(app, resources={r'/*': {'origins': '*'}})
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    add_error_handlers(app)
    return app

# Create a Flask app instance
application = create_app()
