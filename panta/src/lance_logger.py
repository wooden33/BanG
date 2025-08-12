import logging
import os


class LanceLogger:
    log_file = "lance.log"

    @classmethod
    def initialize_logger(cls, name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False

        if not logger.handlers:
            file_handler = logging.FileHandler(cls.log_file, mode="w")
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

            # Stream handler for console output
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            stream_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            stream_handler.setFormatter(stream_formatter)
            logger.addHandler(stream_handler)

        return logger
