#!/usr/bin/env python3

"""
filter_datum module
"""
from typing import List
import re


def filter_datum(
        fields: List[str],
        redaction: str, message: str, separator: str) -> str:
    """ a function to filter out set values and add reductions"""
    for field in fields:
        message = re.sub(field + '=.*?' + separator,
                         field + '=' + redaction + separator, message)
    return message
