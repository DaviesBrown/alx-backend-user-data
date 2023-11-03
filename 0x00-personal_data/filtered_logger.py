#!/usr/bin/env python3
"""Contains a filtering function"""

import logging
import re
from typing import List, Tuple
import os
import mysql.connector

PII_FIELDS: Tuple = ("name", "email", "phone", "ssn", "password")


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        filters incoming records
        :param record:
        :return:
            filtered result
        """
        return filter_datum(self.fields, self.REDACTION,
                            super().format(record), self.SEPARATOR)


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    Obfuscates the sensitive fields in a log message.
    """
    for field in fields:
        if field in message:
            message = re.sub(r"{}=.*?{}".format(field, separator),
                             '{}={}{}'.format(field, redaction, separator),
                             message)
    return message


def get_logger() -> logging.Logger:
    """
    :return:
        logging.logger object
    """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    stream_handler = logging.StreamHandler()
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ returns a secured connection"""
    USERNAME: str = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    PASSWORD: str = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    HOST: str = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    DATABASE: str = os.getenv("PERSONAL_DATA_DB_NAME")

    return mysql.connector.connect(
        host=HOST,
        user=USERNAME,
        password=PASSWORD,
        database=DATABASE
    )


def main() -> None:
    """ main function"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = [description[0] for description in cursor.description]
    logger = get_logger()
    for row in cursor:
        row_data = dict(zip(fields, row))
        string = []
        s = RedactingFormatter.SEPARATOR
        for field, value in row_data.items():
            if field in PII_FIELDS:
                string.append(f"{field}={RedactingFormatter.REDACTION}{s}")
            elif field == "last_login":
                string.append(f"{field}={value.isoformat()}{s}")
            else:
                string.append(f"{field}={value}{s}")
        logger.info(f" ".join(string))
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
