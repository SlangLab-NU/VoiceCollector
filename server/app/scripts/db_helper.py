"""
Functions that performs CRUD operations in database and handles file storage.

"""

import pymysql
from dotenv import load_dotenv
import os

def connect_to_ec2():
    """
    Connect to mysql in EC2 and return the connection.
    """
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
    return conn


def write_record(data, conn):
    """
    Write a record into the database.
    """
    query = """INSERT INTO audio (
                audio_id, user_id, url, date, validated, ref_id, 
                sequence_matcher_score, cer_score, metaphone_match_score)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    with conn.cursor() as cursor:
        cursor.execute(
            query,((
                data.get("audio_id"),
                data.get("user_id"),
                data.get("url"),
                data.get("date"),
                data.get("validated"),
                data.get("ref_id"),
                data.get("sequence_matcher_score"),
                data.get("cer_score"),
                data.get("metaphone_match_score"),
                )),
        )
    conn.commit()
    

def write_file():
    """
    Write a file into 
    """
    pass

def get_all_records():
    """
    """
    pass

def update_record(record_id):
    """
    """
    pass

def delete_record(record_id):
    """
    """
    pass