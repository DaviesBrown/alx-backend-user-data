#!/usr/bin/env python3
"""
Basic Auth module
"""
import base64
import binascii
from typing import TypeVar
from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic Auth class"""
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """ extract auth header base64 part"""
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        return authorization_header.split("Basic ")[1]
    
    def decode_base64_authorization_header(self, base64_authorization_header: str) -> str:
        """ decode auth header in base64"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            decoded = base64.b64decode(base64_authorization_header)
            return decoded.decode('utf-8')
        except binascii.Error:
            return None
        
    def extract_user_credentials(self, decoded_base64_authorization_header: str) -> (str, str):
        """ extract the user credentials"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if type(decoded_base64_authorization_header) != str:
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        user_credential = decoded_base64_authorization_header.split(":", 1)
        return (user_credential[0], user_credential[1])
    
    def user_object_from_credentials(self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ create user object from credentials"""
        if user_email is None or type(user_email) is not str:
            return None
        if user_pwd is None or type(user_pwd) is not str:
            return None
        user = User()
        user_exist = user.search({"email": user_email})
        if not user_exist:
            return None
        if not user_exist[0].is_valid_password(user_pwd):
            return None
        return user_exist[0]
    
    def current_user(self, request=None) -> TypeVar('User'):
        """ returns the current user"""
        header = request.headers.get("Authorization")
        auth_header = self.authorization_header(request)
        extracted_b64_header = self.extract_base64_authorization_header(auth_header)
        auth_header = self.decode_base64_authorization_header(extracted_b64_header)
        email, password = self.extract_user_credentials(auth_header)
        user = self.user_object_from_credentials(email, password)
        return user
