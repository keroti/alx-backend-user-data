#!/usr/bin/env python3
"""
Module for filtering log data
"""

import re
from typing import List

def filter_datum(fields: List[str], redaction: str, message: str, separator: str) -> str:
    """
    use a regex to replace occurrences of certain field values
    and returns the log message obfuscated.
    """
    data = r'({}=)[^{}]+'.format('|'.join(fields), separator)
    return re.sub(data, r'\1' + redaction, message)
