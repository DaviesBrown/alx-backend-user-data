#!/usr/bin/env python3
"""
Auth module
"""
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
        path_end = [i.split("/", -1)[-1][:-1] if i.endswith("*") else i for i in excluded_paths]
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
        """ returns session cokie from request"""
        if request is None:
            return None
        return request.cookies.get("_my_session_id")
