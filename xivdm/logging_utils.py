import logging
from time import strftime, gmtime
from os import path, makedirs
import sys

def set_logging(logs_path, process_name, level=logging.DEBUG):
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        root_logger.removeHandler(handler)
    root_logger.setLevel(logging.NOTSET)

    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setFormatter(logging.Formatter('[ %(asctime)s - %(levelname)s ] %(message)s'))
    root_logger.addHandler(stream_handler)

    stream_handler.setLevel(logging.INFO)
    logging.info('Initializing logging with path[%s] process_name[%s] level[%s]', logs_path, process_name, logging.getLevelName(level))

    log_filename = path.join(logs_path, '%s_%s.log' % (process_name, strftime('%y%m%d_%H%M%S', gmtime())))

    if not path.exists(path.dirname(log_filename)):
        makedirs(path.dirname(log_filename))

    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s <%(filename)s %(lineno)d> %(funcName)s: %(message)s'))
    file_handler.setLevel(level)
    root_logger.addHandler(file_handler)

    logging.info('Logging initialized.')
    stream_handler.setLevel(logging.WARN)
