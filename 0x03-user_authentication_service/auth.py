#!/usr/bin/env python3
"""
auth module
"""
import uuid
from user import User
import bcrypt
from sqlalchemy.exc import NoResultFound, InvalidRequestError

from db import DB


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ registers a new user"""
        if email is None or password is None:
            return
        try:
            user_exist = self._db.find_user_by(email=email)
            if user_exist:
                raise ValueError(f"User {user_exist.email} already exists")
        except NoResultFound:
            hpasswd = _hash_password(password)
            user = self._db.add_user(email=email, hashed_password=hpasswd)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """ returns true is login details are valid"""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode("utf-8"),
                                  user.hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """ create a new user session"""
        try:
            id = _generate_uuid()
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=id)
            return id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """ get user from session id"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        """ destroys user session"""
        self._db.update_user(user_id=user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """ get reset password token"""
        try:
            user = self._db.find_user_by(email=email)
        except Exception:
            raise ValueError("User does not exist")
        rid = str(uuid.uuid4())
        self._db.update_user(user.id, reset_token=rid)
        return rid

    def update_password(self, reset_token: str, password: str) -> None:
        """ updates a user password"""
        if reset_token is None and type(reset_token) != str:
            return None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except Exception:
            raise ValueError("User does not exist")
        hpasswd = _hash_password(password=password)
        self._db.update_user(user.id, hashed_password=hpasswd)


def _hash_password(password: str) -> bytes:
    """ returns salted hash of password"""
    passwd_byte = password.encode('utf-8')
    salt = bcrypt.gensalt()
    h_passwd = bcrypt.hashpw(passwd_byte, salt)
    return h_passwd


def _generate_uuid() -> str:
    """ generates uid"""
    return str(uuid.uuid4())
