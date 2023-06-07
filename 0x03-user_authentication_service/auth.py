#!/usr/bin/env python3
"""
Hash password module
"""
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound
from bcrypt import hashpw, gensalt, checkpw


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt and
    Return the hashed password as bytes.
    """
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_password


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a new user and
        return The User object for the newly registered user
        or raise ValueError if a user already exists with the same email.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user credentials."""
        user = self._db.find_user_by(email=email)
        if user:
            hashed_password = user.hashed_password.encode('utf-8')
            entered_password = password.encode('utf-8')
            return checkpw(entered_password, hashed_password)
        return False
