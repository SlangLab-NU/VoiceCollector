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

    

    schema_path = current_dir / config['schema']
    db_path = config['database']
    
    if not pathlib.Path(db_path).exists():
        connection = sqlite3.connect(config['database'])
        with open(schema_path) as f:
            connection.executescript(f.read())

        cursor = connection.cursor()

        connection.commit()
        connection.close()
    else:
        print("Database file already exists. Skipping creation.")


create_db()
