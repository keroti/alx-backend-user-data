#!/usr/bin/env python3
"""
BasicAuth module
"""
import base64
from api.v1.auth.auth import Auth


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
