"""
Primary Flask app

"""
from flask import Flask, jsonify
from flask_cors import CORS

from .api import api as api_blueprint
from .errors import add_error_handlers


import pymysql
from dotenv import load_dotenv
import os

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r'/*': {'origins': '*'}})
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')
    add_error_handlers(app)
    return app

# connect to mysql
# Load environment variables from .env file in root directory
dotenv_path = os.path.join(os.path.dirname(__file__), '..','.env')
load_dotenv(dotenv_path)

# Read MySQL configuration from environment variables
mysql_host = os.environ.get('MYSQL_HOST')
mysql_port = os.environ.get('MYSQL_PORT')
mysql_user = os.environ.get('MYSQL_USER')
mysql_password = os.environ.get('MYSQL_PASSWORD')
mysql_db = os.environ.get('MYSQL_DB')

# Create a MySQL connection
conn = pymysql.connect(
    host=mysql_host,
    port=int(mysql_port),
    user=mysql_user,
    password=mysql_password,
    db=mysql_db,
    cursorclass=pymysql.cursors.DictCursor
)

# Create a Flask app instance
application = create_app()

# # Run the Flask app
# if __name__ == '__main__':
#     application.run()