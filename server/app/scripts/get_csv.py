"""
Get containing paths to audio files and their corresponding transcriptions

"""

import json
from dotenv import load_dotenv
import os
from minio import Minio
from minio.error import S3Error
import threading
import sqlite3
import pathlib
from . import db_helper
import csv

try:
    # Try an absolute import first
    from log import logger
except ModuleNotFoundError:
    # If the absolute import fails, fallback to a relative import
    # This is for running flask in debug mode in its own environment
    from ..log import logger

logger = logger.load_log()


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


def generate_csv_file():
    """
    Generates a CSV file containing information about audio records and their transcriptions.

    Returns:
    str: The file path of the generated CSV file.

    Raises:
    S3Error: If there is an error while interacting with the S3 bucket.
    """
    
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

    client, s3_bucket = db_helper.connect_to_s3()

    current_dir = pathlib.Path(__file__).parent.resolve()
    tmp_dir = current_dir.parent.parent / f"tmp"
    logger.info(f"tmp_dir: {tmp_dir}")

    if not tmp_dir.exists():
        tmp_dir.mkdir()
        logger.info(f"get_csv: tmp_dir created")


    mapped_table = map_audio_to_transcription(records, references)
    logger.info(f"mapped_table: {mapped_table}")

    for entry in mapped_table:
        s3_url = entry['s3_url']
        filename = entry['s3_url'].split(".")[0]
        object_name = f"{filename}.wav"
        filepath = f"{tmp_dir}/{object_name}"

        logger.info(f's3_url:{s3_url}')
        logger.info(f'filename:{filename}')
        logger.info(f"object_name: {object_name}")
        logger.info(f'filepath:{filepath}')

        # Download file from S3 bucket
        try:
            client.fget_object(
                bucket_name=s3_bucket,
                object_name= object_name,
                file_path=filepath,
            )
            entry['audio_path'] = filepath
        except S3Error as e:
            error_message = str(e)
            logger.error(f"error: {error_message}")


    output_csv_path = f'{tmp_dir}/output.csv'
    # Create and write the data to the CSV file
    with open(output_csv_path, 'w', newline='') as csvfile:
        fieldnames = ['audio_id', 'session_id', 's3_url', 'date', 'ref_id', 'transcription', 'audio_path']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        for entry in mapped_table:
            writer.writerow(entry)

    logger.info(f"CSV file written to {output_csv_path}")
    return output_csv_path