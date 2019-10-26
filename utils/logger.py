import logging


def create_logger(logger_name):
    """ Additional function to handle logging in all application and
    can connect to Graylog to collect all logs in one place.

    :param logger_name:
    :return:
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(level=logging.INFO)
    return logger
