"""
Primary Flask app

"""
import sqlite3
from flask import Flask, jsonify, render_template
from flask_cors import CORS

from .api import api as api_blueprint
from .errors import add_error_handlers



# def get_db_connection():
#     conn = sqlite3.connect('database.db')
#     conn.row_factory = sqlite3.Row
#     return conn


# @app.route('/record')
# def index():
#     conn = get_db_connection()
#     posts = conn.execute('SELECT * FROM audio').fetchall()
#     conn.close()
#     return render_template('index.html', posts=posts)

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r'/*': {'origins': '*'}})
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    add_error_handlers(app)
    return app

# Create a Flask app instance
application = create_app()
