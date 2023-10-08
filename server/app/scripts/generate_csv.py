import json
from dotenv import load_dotenv
import os
from minio import Minio
import threading
import sqlite3
import pathlib
import db_helper

try:
    # Try an absolute import first
    from log import logger
except ModuleNotFoundError:
    # If the absolute import fails, fallback to a relative import
    # This is for running flask in debug mode in its own environment
    from ..log import logger


references = db_helper.get_reference()
audio_records = db_helper.get_records()

