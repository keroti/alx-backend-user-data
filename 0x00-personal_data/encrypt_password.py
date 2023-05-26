#!/usr/bin/env python3
"""
Module for encrypting passwords
"""

import bcrypt

def hash_password(password):
    """
    One string argument name password and return a
    salted, hashed password, which is a byte string
    """
    salted = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode(), salted)
    return hashed_password

def is_valid(hashed_password, password):
    """
    Check validity of password and
    return a boolean"""
    return bcrypt.checkpw(password.encode(), hashed_password)
