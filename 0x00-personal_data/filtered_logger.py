#!/usr/bin/env python3
"""
Module for filtering log data
"""

import re
from typing import List
import logging
import os
import mysql.connector


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


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    Returns a connector to the database.

    Returns:
        A mysql.connector.connection.MySQLConnection object.
    """
    username = os.environ.get("PERSONAL_DATA_DB_USERNAME", "root")
    password = os.environ.get("PERSONAL_DATA_DB_PASSWORD", "")
    host = os.environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    database = os.environ.get("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=database
    )


def main() -> None:
    """
    obtain a database connection using get_db and retrieve all
    rows in the users table and display each row under a filtered format
    """
    logger = get_logger()
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    logger.info("Filtered fields:\n%s", "\n".join(PII_FIELDS))

    for row in rows:
        log_message = "; ".join(
            [f"{field}={str(value)}" for field,
             value in zip(cursor.column_names, row)])
        logger.info(log_message)

    cursor.close()
    db.close()
