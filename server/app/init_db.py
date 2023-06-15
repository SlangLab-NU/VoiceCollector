import sqlite3
from scripts import db_helper
"""
Connects local db file to store data locally
"""
connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cursor = connection.cursor()

connection.commit()
connection.close()

#  Writes the references to the db

db_helper.write_references_to_db()