"""
Functions that performs CRUD operations in database and handles file storage.

"""
import json
import pymysql
from dotenv import load_dotenv
import os
import boto3
import threading
import sqlite3


lock = threading.Lock()


def connect_to_ec2():
    """
    Connect to mysql in EC2 and return the connection.
    """
    # Load environment variables from .env file in root directory
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
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
    return conn


def connect_to_s3():
    """
    Connect to S3 and return the bucket that stores audio files.
    """
    # Load environment variables from .env file in root directory
    dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
    load_dotenv(dotenv_path)

    # Read S3 configuration from environment variables
    s3_access_key = os.environ.get('S3_ACCESS_KEY')
    s3_secret_key = os.environ.get('S3_SECRET_KEY')
    s3_bucket = os.environ.get('S3_BUCKET')
    region_name = os.environ.get('REGION_NAME')

    # Create a S3 connection
    s3 = boto3.resource(
        service_name='s3',
        region_name=region_name,
        aws_access_key_id=s3_access_key,
        aws_secret_access_key=s3_secret_key
    )
    return s3.Bucket(s3_bucket)


def write_record(data, conn):
    """
    Write a record into the database.
    """
    query = """INSERT INTO audio (
                session_id, s3_url, date, validated, ref_id, 
                sequence_matcher, cer, metaphone_match)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
    lock.acquire()
    with conn.cursor() as cursor:
        cursor.execute(
            query, ((
                data.get("session_id"),
                data.get("s3_url"),
                data.get("date"),
                data.get("validated"),
                data.get("ref_id"),
                data.get("sequence_matcher"),
                data.get("cer"),
                data.get("metaphone_match"),
            )),
        )
    conn.commit()
    lock.release()

def get_db_connection():
    """
    Connect to local database (database.db) and returns connection
    """
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def write_local_record(data):
    """
    Connects audio recordings to local database (database.db) and writes metadata to audio table
    """
    conn = get_db_connection()
    # input values must be a tuple
    conn.execute("""INSERT INTO audio 
                    (session_id, s3_url, date, validated, ref_id, sequence_matcher, cer, metaphone_match) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""", 
            (data.get("session_id"),
            data.get("s3_url"),
            data.get("date"),
            data.get("validated"),
            data.get("ref_id"),
            data.get("sequence_matcher"),
            data.get("cer"),
            data.get("metaphone_match")),)
    conn.commit()
    conn.close()

def write_file():
    """
    Write a file into 
    """
    pass


def write_references_to_db():
    """
    Takes in json data from references.txt and populates the reference table
    """
    with open('references.txt') as f:
        references_json = json.load(f)
    references = references_json.get("references")
    conn = get_db_connection()
    cursor = conn.cursor()
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

    connect = get_db_connection()
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM reference')
    res = cursor.fetchall()
    # fetchall for sqlite returns list of row objects, this step converts each row into a dictionary
    references = [dict(row) for row in res]
    connect.close()
    
    return references


def get_records():
    """
    Fetches references from the database and returns a list of records as dictionaries
    """
    connect = get_db_connection()
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM audio')
    res = cursor.fetchall()
    results = [dict(row) for row in res]
    connect.close()

    return results
