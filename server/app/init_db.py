import pathlib
import sqlite3
import json
"""
Connects local db file to store data locally
"""


def create_db():
    """
    Creates database and tables if it does not exist
    """
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


create_db()
