from loguru import logger
import sys
import os

class Logger:
    """ Класс для централизованного логирования во всех частях проекта """

    def __init__(self, log_file="logs/test_log.log", level="DEBUG"):
        # Создаём папку для логов (если её нет)
        if not os.path.exists("logs"):
            os.makedirs("logs")

        # Удаляем стандартный логгер (чтобы избежать дублирования)
        logger.remove()

        # Логируем в консоль
        logger.add(sys.stdout, format="{time} {level} {message}", level="INFO")

        # Логируем в файл (ротация: 10 MB, максимум 5 файлов)
        logger.add(log_file, format="{time} {level} {message}", level=level, rotation="10 MB", retention=5)

    def get_logger(self):
        """ Возвращает объект логгера """
        return logger

# 🔥 Создаём стандартный логгер (используется по умолчанию)
log_instance = Logger().get_logger()