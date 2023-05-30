#!/usr/bin/env python3
"""
BasicAuth module
"""
import base64
from api.v1.auth.auth import Auth
from typing import Tuple, TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    BasicAuth class that inherits from Auth
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        Extracts the Base64 part of the Authorization
        header for Basic Authentication
        Returns:
            The Base64 part of the Authorization header or None
        """
        if authorization_header is None or not isinstance(authorization_header,
                                                          str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split("Basic ")[1].strip()

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        Decodes a Base64 string
        Returns:
            The decoded value as a UTF-8 string or None
        """
        header = base64_authorization_header
        if header is None or not isinstance(header, str):
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            decoded_string = decoded.decode('utf-8')
            return decoded_string
        except base64.binascii.Error:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str) -> Tuple[str, str]:  # nopep8
        """
        Extracts user credentials from a decoded Base64
        Returns:
            A tuple containing the user email and password
            or none if the header is invalid
        """
        decoded = decoded_base64_authorization_header
        if decoded is None or not isinstance(decoded, str):
            return None, None
        if ':' not in decoded:
            return None, None
        email, password = decoded.split(':', 1)
        return email, password

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        Retrieves a User instance based on email and password credentials
        Returns:
            The User instance and credentials if valid, None otherwise
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None

        users = User.search({'email': user_email})
        if not users:
            return None

        user = users[0]
        if not user.is_valid_password(user_pwd):
            return None

        return user
