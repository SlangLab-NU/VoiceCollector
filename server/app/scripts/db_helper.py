"""
Functions that performs CRUD operations in database and handles file storage.

"""

import pymysql
from dotenv import load_dotenv
import os

def connect_to_ec2():
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
    return conn

    # # Define the MySQL connection as a global variable
    # conn = None

    # def create_mysql_connection():
    #     global conn
    #     conn = pymysql.connect(
    #         host=mysql_host,
    #         port=int(mysql_port),
    #         user=mysql_user,
    #         password=mysql_password,
    #         db=mysql_db,
    #         cursorclass=pymysql.cursors.DictCursor
    #     )

    # # Call the function to create the connection
    # create_mysql_connection()

def write_record(record):
    """
    Write a record into the database.
    """
    pass

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