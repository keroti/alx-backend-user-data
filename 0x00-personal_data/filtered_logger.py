#!/usr/bin/env python3
"""
Module for filtering log data
"""

import re
from typing import List
import logging


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    use a regex to replace occurrences of certain field values
    and returns the log message obfuscated.
    """
    pattern = r'({}=)[^{}]+'.format('|'.join(fields), separator)
    return re.sub(pattern, r'\1' + redaction, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class. """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        Initialize class.
        """
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Return filtered values in incoming log records
        using filter_datum.
        """
        log_message = super().format(record)
        for field in self.fields:
            log_message = log_message.replace(
                field + "=", field + "=" + self.REDACTION)
        return log_message


def get_logger() -> logging.Logger:
    """
    Returns a logging.Logger object with specified configurations.
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)
    return logger


PII_FIELDS = ("name", "email", "phone", "ssn", "password")
