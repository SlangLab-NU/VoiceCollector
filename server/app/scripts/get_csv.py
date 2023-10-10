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


sample_audio = [
    {
        'audio_id': 1,
        'session_id': '90.5452132089414',
        's3_url': 'test90.5452132089414.webm',
        'date': '2023-08-15 22:53:12',
        'ref_id': 3
    },
    {
        'audio_id': 2,
        'session_id': '15.950413213527415',
        's3_url': 'test15.950413213527415.webm',
        'date': '2023-08-16 00:11:09',
        'ref_id': 2
    },
    {
        'audio_id': 3,
        'session_id': '86.14580150748988',
        's3_url': 'test86.14580150748988.webm',
        'date': '2023-08-16 00:13:58',
        'ref_id': 1
    },]


sample_references = [
    {
        'ref_id': 1,
        'section': 'Image',
        'prompt': 'Read the following book pages',
        'promptNum': 1,
        'image_url': 'thomas_birthday_1.jpg'
    },
    {
        'ref_id': 2,
        'section': 'Image',
        'prompt': 'Read the following book pages',
        'promptNum': 2,
        'image_url': 'thomas_birthday_2.jpg'
    },
    {
        'ref_id': 3,
        'section': 'Image',
        'prompt': 'Read the following book pages',
        'promptNum': 3,
        'image_url': 'thomas_birthday_3.jpg'
    },
    {
        'ref_id': 4,
        'section': 'Image',
        'prompt': 'Read the following book pages',
        'promptNum': 4,
        'image_url': 'thomas_birthday_4.jpg'
    },
    {
        'ref_id': 5,
        'section': 'Image',
        'prompt': 'Read the following book pages',
        'promptNum': 5,
        'image_url': 'thomas_birthday_5.jpg'
    }
]


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


mapped_table = map_audio_to_transcription(sample_audio, sample_references)

