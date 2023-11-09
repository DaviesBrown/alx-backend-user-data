#!/usr/bin/env python3
"""
SessionDbAuth module
"""
from datetime import datetime, timedelta
from typing import Dict

from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth class"""
    def __init__(self):
        super().__init__()

    def create_session(self, user_id: str = None) -> str:
        session_id = super().create_session(user_id=user_id)
        print(session_id)
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ gets user id from session"""
        if session_id is None:
            return None
        user_session = UserSession.search({"session_id": session_id})
        if user_session is None:
            return None
        user_session = user_session[0].to_json()
        if self.session_duration <= 0:
            return user_session["user_id"]
        if not user_session.get("created_at"):
            return None
        created_at = datetime.fromisoformat(user_session.get("created_at"))
        print(created_at)
        session_duration = timedelta(seconds=self.session_duration)
        print(session_duration)
        session_datetime = created_at + session_duration
        print(session_datetime)
        current_datetime = datetime.now()
        print(current_datetime)
        if current_datetime > session_datetime:
            return None
        return user_session["user_id"]

    def destroy_session(self, request=None):
        """ detroy user session"""
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        user_session = UserSession(session_id=session_id, user_id=user_id)
        user_session.remove()
        return True
