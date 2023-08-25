"""
Primary Flask app

"""
import sqlite3
from flask import Flask, jsonify, render_template
from flask_cors import CORS

from .api import api as api_blueprint
from .errors import add_error_handlers
from .scripts import db_helper
from . import init_db

app = Flask(__name__)


def create_app():
    CORS(app, resources={r'/*': {'origins': '*'}})
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    add_error_handlers(app)
    return app


# Before starting the app, write the references to the database
# If the database does not exist, create it
try:
    db_helper.write_references_to_db()
except sqlite3.OperationalError:
    init_db.create_db()
    db_helper.write_references_to_db()

# Create a Flask app instance
application = create_app()
