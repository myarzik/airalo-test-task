from loguru import logger
import sys
import os

class Logger:
    """ Centralized logging class for the entire project """

    def __init__(self, log_file="logs/test_log.log", level="DEBUG"):
        if not os.path.exists("logs"):
            os.makedirs("logs")
        logger.remove()
        logger.add(sys.stdout, format="{time} {level} {message}", level="INFO")
        logger.add(log_file, format="{time} {level} {message}", level=level, rotation="10 MB", retention=5)

    def get_logger(self):
        """ Returns the logger instance """
        return logger

log_instance = Logger().get_logger()
