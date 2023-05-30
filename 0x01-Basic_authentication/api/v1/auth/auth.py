#!/usr/bin/env python3
"""
Auth module
"""
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
        if path is None:
            return True
        if excluded_paths is None or len(excluded_paths) == 0:
            return False
        if path.endswith('/') and path[:-1] in excluded_paths:
            return False
        return path not in excluded_paths

    def authorization_header(self, request=None) -> str:
        """
        Retrieves the authorization header from the request
        Returns:
            The value of the authorization header or None if not found
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current user based on the request
        Returns:
            The current user object or None if not found
        """
        return None
