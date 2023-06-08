#!/usr/bin/env python3
"""
Auth module
"""
import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import NoResultFound
import uuid
from typing import Union


def _hash_password(password: str) -> bytes:
    """
    Hashes a password using bcrypt and
    Return the hashed password as bytes.
    """
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_password


def _generate_uuid() -> str:
    """Generate a new UUID and return its string representation."""
    return str(uuid.uuid4())


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
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        user_password = user.hashed_password
        passwd = password.encode("utf-8")
        return bcrypt.checkpw(passwd, user_password)

    def create_session(self, email):
        """Create a new session for the user and return the session ID"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Takes a session ID and returns its
        corresponding user or none
        """
        if session_id is None:
            return None

        user_id = self._db.get_user_from_session_id(session_id)

        if user_id is None:
            return None

        return self._db.find_user_by_id(user_id)

    def destroy_session(self, user_id: int) -> None:
        """Destroy session"""
        self._db.update_user_session_id(user_id, None)

    def get_reset_password_token(self, email: str) -> str:
        """Generate reset password token"""
        user = self._db.find_user_by(email=email)

        if not user:
            raise ValueError("User not found.")

        token = str(uuid.uuid4())
        self._db.update_user(user.id, reset_token=token)

        return token
