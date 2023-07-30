import sys
import json
import logging


def load_log_config():
    """
    Load logging configuration from config.json with error handling.
    """
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        config = config['LOGGING']
    except Exception as e:
        print('Failed to load logging configuration from config.json.')
        print(e)
        sys.exit(1)
    return config

def load_log():

    log_format = (
        '%(asctime)s - '
        '%(name)s - '
        '%(filename)s - '
        '%(lineno)s - '
        '%(funcName)s - '
        '%(levelname)s - '
        '%(message)s'
    )
    handlers = [logging.StreamHandler(sys.stdout)]
    logging.basicConfig(level=logging.INFO,
                        handlers=handlers,
                        format=log_format)
    logger = logging.getLogger('VoiceCollectorEntry')
    logger.setLevel(logging.INFO)
    return logger
