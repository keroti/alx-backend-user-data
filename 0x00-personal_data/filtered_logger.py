#!/usr/bin/env python3

"""
filtered_logger module
"""

import re
import logging
import os
import mysql.connector
from typing import List


def filter_datum(
        fields: List[str], redaction: str, message: str, separator: str
) -> str:
    """
    Use a regex to replace occurrences of certain field values
    and return the log message obfuscated.
    Args:
        fields (List[str]): List of fields to obfuscate
        redaction (str): String representing the redacted value
        message (str): Log line containing fields to be obfuscated
        separator (str): Separator character used in the log line

    Returns:
        str: The obfuscated log message
    """
    pattern = r'({}=)[^{}]+'.format('|'.join(fields), separator)
    return re.sub(pattern, r'\1' + redaction, message)


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super().__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        log_message = super().format(record)
        for field in self.fields:
            log_message = log_message.replace(
                field + "=", field + "=" + self.REDACTION)
        return log_message


def get_logger() -> logging.Logger:
    """
    Returns a logging.Logger object with specified configurations.

    Returns:
        A logging.Logger object.
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
    Retrieves data from the users table and displays filtered log records.
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


if __name__ == "__main__":
    main()
