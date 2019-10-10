import logging

import graypy

from utils.config import get_config, get_config_default


def create_graylog_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(level=logging.INFO)
    return logger