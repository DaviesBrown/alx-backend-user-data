#!/usr/bin/env python3
"""
Auth module
"""
import os
from typing import List, TypeVar
from flask import request


class Auth:
    """ Auth class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ check if auth is required"""
        if path is None:
            return True
        if excluded_paths is None:
            return True
        path = path + "/" if path[-1] != '/' else path
        if path not in excluded_paths:
            return True
        return False

    def authorization_header(self, request: request = None) -> str:
        """ auth headers"""
        if request is None:
            return None
        header = request.headers.get("Authorization", None)
        if not header:
            return None
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns current user"""
        return None

    def session_cookie(self, request=None):
        """ returns session cookie from request"""
        if request is None:
            return None
        session_name = os.getenv("SESSION_NAME")
        return request.cookies.get(session_name)
