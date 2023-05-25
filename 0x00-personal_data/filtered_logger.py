#!/usr/bin/env python3
"""
Module for filtering log data
"""

import re
from typing import List


def filter_datum(fields, redaction, message, separator):
    """
    use a regex to replace occurrences of certain field values
    and returns the log message obfuscated.
    """
    pattern = r'({0}=).*?({1})'.format('|'.join(fields), separator)
    return re.sub(pattern, r'\1{0}'.format(redaction), message)