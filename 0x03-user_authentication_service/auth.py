#!/usr/bin/env python3
"""
Hash password module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound


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
        except NoResultFound:
            hashed = _hash_password(password)
            usr = self._db.add_user(email, hashed)
            return usr
        raise ValueError(f"User {email} already exists")
