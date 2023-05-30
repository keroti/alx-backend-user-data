#!/usr/bin/env python3
"""
Auth module
"""
import re
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth class for API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Checks if authentication is required for a given path
        Returns:
            True if authentication is required, False otherwise
        """
        if path is not None and excluded_paths is not None:
            for exclusion_path in map(lambda x: x.strip(), excluded_paths):
                pattern = ''
                if exclusion_path[-1] == '*':
                    pattern = '{}.*'.format(exclusion_path[0:-1])
                elif exclusion_path[-1] == '/':
                    pattern = '{}/*'.format(exclusion_path[0:-1])
                else:
                    pattern = '{}/*'.format(exclusion_path)
                if re.match(pattern, path):
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request
        Returns:
            The value of the authorization header or None if not found
        """
        if request is None or "Authorization" not in request.headers:
            return None
        return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on the request
        Returns:
            The current user object or None if not found
        """
        return None
