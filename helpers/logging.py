import logging

from helpers.utils import build_path


def setup_logging():
    formatter = logging.Formatter('%(asctime)s [%(name)-12.12s] %(levelname)s : %(message)s')
    file_handler = logging.FileHandler(build_path(['logs', 'log2gsheet.log']), encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO, handlers=[stream_handler, file_handler])


def get_main_logger():
    return logging.getLogger('log2gsheet')


main_logger = get_main_logger()
