import sys
import logging
import logging.config
import yaml



def load_log():
    """
    Load logging configuration from config.json with error handling.
    """
    try:
        with open('./log/logging_config.yaml', 'r') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
            return logging.getLogger('speak')

    except Exception as e:
        print('Failed to load logging configuration from logging_config.yaml.')
        print(e)
        sys.exit(1)