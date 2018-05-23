import logging.handlers
import sys, os


LOG_FOLDER_PATH = os.path.dirname(os.path.abspath(__file__))
SERVER_LOG_FILE_PATH = os.path.join(LOG_FOLDER_PATH, 'log', 'server_messages.log')

logger = logging.getLogger('server.' + __name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s: %(levelname)s: %(name)s: %(message)s ')

file_handler = logging.handlers.TimedRotatingFileHandler(SERVER_LOG_FILE_PATH, when='d')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def server_logger(func):
    def wrapper(*args, **kwargs):
        wrapped_func = func(*args, **kwargs)
        logger.info('Calling %s with\n %s\n ' % (func.__name__, args))
        return wrapped_func
    return wrapper




