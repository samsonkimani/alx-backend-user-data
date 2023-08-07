#!/usr/bin/env python3
""" Auth module """
from flask import request
from typing import List, TypeVar
from models.user import User

class Auth:
    """ class auth for authenticating users"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ require auth function that returns false"""
        return False

    def authorization_header(self, request=None) -> str:
        """ authorization header"""
        if request is None:
            return None
        else:
            return request

    def current_user(self, request=None) -> TypeVar('User'):
        """ return current user else None"""
        return None

