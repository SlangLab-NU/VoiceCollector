"""
Functions that performs CRUD operations in database and handles file storage.

"""
import json
from dotenv import load_dotenv
import os
from minio import Minio
import threading
import sqlite3
import pathlib

try:
    # Try an absolute import first
    from log import logger
except ModuleNotFoundError:
    # If the absolute import fails, fallback to a relative import
    # This is for running flask in debug mode in its own environment
    from ..log import logger


logger = logger.load_log()

current_dir = pathlib.Path(__file__).parent.resolve()
config_path = current_dir / ".." / "config.json"
with open(config_path, "r") as f:
    config = json.load(f)
config = config["DATABASE"]
db_type = config["db_type"]
reference_path = current_dir / ".." / config["references"]

lock = threading.Lock()


def connect_to_s3():
    """
    Connect to S3 and return the bucket that stores audio files.
    """
    # Load environment variables from .env file in root directory
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(dotenv_path)

    # Read S3 configuration from environment variables
    s3_hostname = os.environ.get('S3_HOSTNAME')
    s3_access_key = os.environ.get('S3_ACCESS_KEY')
    s3_secret_key = os.environ.get('S3_SECRET_KEY')
    s3_bucket = os.environ.get('S3_BUCKET')
    region_name = os.environ.get('REGION_NAME')
    secure = (os.environ.get('SECURE') == 'True')
    # Create a S3 connection
    client = Minio(
        endpoint=s3_hostname,
        access_key=s3_access_key,
        secret_key=s3_secret_key,
        region=region_name,
        secure=secure,
    )

    return client, s3_bucket


def connect_to_local_db():
    """
    Connect to local database (database.db) and returns connection
    """
    conn = sqlite3.connect(config['database'])
    conn.row_factory = sqlite3.Row
    return conn


def connect_to_db():
    """
    Merges the db connections for ec2, S3 and local databases. Pulls db_type variable from config.json
    identifying which db type the connection is being made to and returns that connection
    """
    if db_type == "s3":
        return connect_to_s3()
    elif db_type == "local":
        return connect_to_local_db()


def write_record(data):
    """
    Write a record into the database.
    """
    conn = connect_to_db()
    lock.acquire()
    conn.execute("""INSERT INTO audio 
                    (session_id, s3_url, date, ref_id) 
                    VALUES (?, ?, ?, ?)""",
                    (data.get("session_id"),
                    data.get("s3_url"),
                    data.get("date"),
                    data.get("ref_id")),
            )          
    conn.commit()
    lock.release()


def write_file():
    """
    Write a file into 
    """
    pass


def write_references_to_db():
    """
    Takes in json data from references.txt and populates the reference table
    """
    with open(reference_path) as f:
        references_json = json.load(f)
    references = references_json.get("references")
    conn = connect_to_local_db()
    cursor = conn.cursor()
    
    # Clear any data from previous references
    cursor.execute("DELETE FROM reference;")

    for reference in references:
        cursor.execute("""INSERT INTO reference
                        (section, prompt, promptnum, image_url) 
                        VALUES (?, ?, ?, ?)""",
                        (reference.get("section"),
                        reference.get("prompt"),
                        reference.get("promptNum"),
                        reference.get("image_url")),)
    conn.commit()
    conn.close()


def get_reference():
    """
    Fetches references from the database and returns a list of references as dictionaries
    """

    connect = connect_to_local_db()
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM reference')
    res = cursor.fetchall()
    # fetchall for sqlite returns list of row objects, this step converts each row into a dictionary
    references = [dict(row) for row in res]
    connect.close()
    
    return references


def get_records():
    """
    Fetches references from the records and returns a list of records as dictionaries
    """
    connect = connect_to_local_db()
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM audio')
    res = cursor.fetchall()
    results = [dict(row) for row in res]
    connect.close()

    return results
