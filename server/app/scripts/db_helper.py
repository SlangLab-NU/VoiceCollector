"""
Functions that performs CRUD operations in database and handles file storage.

"""

import pymysql
from dotenv import load_dotenv
import os
import datetime

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


def write_record(record, conn):
    """
    Write a record into the database.
    """
    # Get the required data from the dictionary
    audio_id = record["audio_id"]
    user_id = record["user_id"]
    url = record["url"]
    date = record["Date"]
    validated = record["validated"]
    ref_id = record["ref_id"]
    sequence_matcher_score = record["sequence_matcher_score"]
    cer_score = record["cer_score"]
    metaphone_match_score = record["metaphone_match_score"]
    # Convert date string to a datetime object
    date_obj = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    # Create the SQL query to insert the record into the database
    query = f"""INSERT INTO reference (audio_id, user_id, url, Date, validated, ref_id, sequence_matcher_score, cer_score, metaphone_match_score)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    # Insert the record into the database
    with conn.cursor() as cursor:
        cursor.execute(query, (audio_id, user_id, url, date_obj, validated, ref_id, sequence_matcher_score, cer_score, metaphone_match_score))
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