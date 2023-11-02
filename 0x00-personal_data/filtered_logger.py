#!/usr/bin/env python3
"""
filtered datum
"""
import re
from typing import List
import logging


PII_FIELDS = ("email",
              "phone",
              "ssn",
              "password",
              "ip",
            )

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
        """ filter values in incoming log records using filter_datum"""
        log_message = super().format(record)
        if self.fields:
            for field in self.fields:
                log_message = filter_datum([field], self.REDACTION, log_message, self.SEPARATOR)
        return log_message


def filter_datum(fields, redaction, message, separator):
    """filtered dactum"""
    pattern = '|'.join(fields)
    regex = f'({pattern})=[^;]*'
    return re.sub(regex, f'\\1={redaction}', message)


def get_logger() -> logging.Logger:
    """ get logger function"""
    logger = logging.Logger("user_data", logging.INFO)
    logger.propagate = False
    formatter = RedactingFormatter(fields=PII_FIELDS)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger = logger.addHandler(stream_handler)
    return logger