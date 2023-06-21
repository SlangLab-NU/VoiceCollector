import sys
import logging


# TODO add error handling or debug output
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
