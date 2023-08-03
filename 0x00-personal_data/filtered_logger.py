#!/usr/bin/env python3

"""
filter_datum module
"""

import re

def filter_datum(fields, redaction, message, separator):
    """ a function to filter out set values and add reductions"""
    for field in fields:
        message = re.sub(field+'=.*?'+separator,
                         field+'='+redaction+separator, message)
    return message
