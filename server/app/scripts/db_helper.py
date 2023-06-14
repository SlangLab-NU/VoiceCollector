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
from .referencesDB import (references) 


lock = threading.Lock()

# Task 2 is to create a function that adds items to a local db (sqlLite) instead of EC2
# This is executed in speak.py

def connect_to_local_db():
    connection = sqlite3.connect('database.db')
    # Changes directory to access schema table
    # path = os.path.realpath(__file__)
    # dir = os.path.dirname(path)
    # dir = dir.replace('scripts', 'dbTables')
    # os.chdir(dir)

    with open('schema.sql') as f:
        connection.executescript(f.read())

    cursor = connection.cursor()
    # Practice post
    # cursor.execute("INSERT INTO audio (session_id, s3_url, date, validated, ref_id, sequence_matcher, cer, metaphone_match) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
    #             ('1', '1', 'First Post', '', '1', '1', '1.0', '1.0', '1.0')
    #             )
    # for row in cursor.execute("select * from audio"):
    #     print(row)
    connection.commit()
    connection.close()

    return cursor


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
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def write_local_record(data):
    conn = get_db_connection()
    lock.acquire()
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
    lock.release()
    conn.close()

def write_file():
    """
    Write a file into 
    """
    pass

def write_references_to_db():
    with open('references.txt') as f:
        references_json = json.load(f)
    # print(references_json)
    references = references_json.get("references")
    # print(references.get("section"))
    conn = get_db_connection()
    conn.execute("""INSERT INTO reference
                    (section, prompt, promptnum, image_url) 
                    VALUES (?, ?, ?, ?)""",
                    (references.get("section"),
                     references.get("prompt"),
                     references.get("promptnum"),
                     references.get("image_url")),)
    conn.commit()
    conn.close()

# def get_reference():
#     write_references_to_db()


# Issue is mock data doesnt include all keys from table. Determine where the ec2 database gets that.
def get_reference(conn):
    write_references_to_db()
    with conn.cursor() as cursor:
        cursor.execute('select * from reference')
        result = cursor.fetchall()
        # print(result)
        return result


def get_records(conn):
    with conn.cursor() as cursor:
        cursor.execute('select * from audio')
        result = cursor.fetchall()
        return result
