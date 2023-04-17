"""
Functions that performs CRUD operations in database and handles file storage.

"""

import pymysql
from dotenv import load_dotenv
import os
import boto3
import threading

lock = threading.Lock()


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

def connect_to_s3():
    """
    Connect to S3 and return the bucket that stores audio files.
    """
    # Load environment variables from .env file in root directory
    dotenv_path = os.path.join(os.path.dirname(__file__), '..','.env')
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
            query,((
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
    

def write_file():
    """
    Write a file into 
    """
    pass


def get_reference(conn):
    with conn.cursor() as cursor:
        cursor.execute('select * from reference')
        result = cursor.fetchall()
        return result


def get_records(conn):
    with conn.cursor() as cursor:
        cursor.execute('select * from audio')
        result = cursor.fetchall()
        return result

