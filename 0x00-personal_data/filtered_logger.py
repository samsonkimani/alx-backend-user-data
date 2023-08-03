#!/usr/bin/env python3

"""
filter_datum module
"""
from typing import List
import re
import logging

PII_FIELDS = ('email', 'phone', 'ssn', 'password', 'ip')


def filter_datum(
        fields: List[str],
        redaction: str, message: str, separator: str) -> str:
    """ a function to filter out set values and add reductions"""
    for field in fields:
        message = re.sub(field + '=.*?' + separator,
                         field + '=' + redaction + separator, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ init method"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """a format method to print logs """
        message = super(RedactingFormatter, self).format(record)
        redacted = filter_datum(
            self.fields,
            self.REDACTION,
            message,
            self.SEPARATOR)
        return redacted


def get_logger() -> logging.Logger:
    """ a get logger function that returns a logger object"""
    logger = logging.LogRecord("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    formatter = RedactingFormatter(list(PII_FIELDS))

    stream_handler.addFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger
