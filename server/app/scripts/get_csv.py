"""
Get containing paths to audio files and their corresponding transcriptions

"""

import json
from dotenv import load_dotenv
import os
from minio import Minio
import threading
import sqlite3
import pathlib
from . import db_helper

try:
    # Try an absolute import first
    from log import logger
except ModuleNotFoundError:
    # If the absolute import fails, fallback to a relative import
    # This is for running flask in debug mode in its own environment
    from ..log import logger

logger = logger.load_log()

try:
    references = db_helper.get_reference()
    logger.info(f"references: {references}")
except Exception as e:
    error_message = str(e)
    logger.error(f"error: {error_message}")

try:
    records = db_helper.get_records()
    logger.info(f"records: {records}")
except Exception as e:
    error_message = str(e)
    logger.error(f"error: {error_message}")


def map_audio_to_transcription(records, references):
    """
    Map audio records to their corresponding transcriptions using references.

    Args:
        records (list): List of audio records (output of get_records()).
        references (list): List of reference records (output of get_reference()).

    Returns:
        list: List of audio records with an additional 'transcription' field.
    """
    mapped_records = []
    for record in records:
        ref_id = record['ref_id']
        # Find the corresponding reference based on ref_id
        reference = next((ref for ref in references if ref['ref_id'] == ref_id), None)
        if reference:
            record['transcription'] = reference['prompt']
        else:
            record['transcription'] = ''
        mapped_records.append(record)
    return mapped_records


mapped_table = map_audio_to_transcription(records, references)
logger.info(f"mapped_table: {mapped_table}")

