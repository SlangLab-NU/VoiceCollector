import pathlib
import sqlite3
import json
from scripts import db_helper
"""
Connects local db file to store data locally
"""
# TODO The cofig code is repeated. Find appropriate place to write function and import to appropriate files
current_dir = pathlib.Path(__file__).parent.resolve()
config_path = current_dir / "config.json"
config = json.loads(config_path.read_text())
config = config["DATABASE"]

connection = sqlite3.connect(config['database'])

with open(config['schema']) as f:
    connection.executescript(f.read())

cursor = connection.cursor()

connection.commit()
connection.close()
