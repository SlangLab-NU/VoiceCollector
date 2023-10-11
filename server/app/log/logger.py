import sys
import logging
import logging.config
import pathlib
import yaml



def load_log():
    """
    Load logging configuration from config.json with error handling.
    """
    current_dir = pathlib.Path(__file__).parent.resolve()
    config_path = current_dir / "logging_config.yaml"
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
            return logging.getLogger('speak')

    except Exception as e:
        print('Failed to load logging configuration from logging_config.yaml.')
        print(e)
        sys.exit(1)