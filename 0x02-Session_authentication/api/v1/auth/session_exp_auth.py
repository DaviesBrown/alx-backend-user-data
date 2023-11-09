#!/usr/bin/env python3
"""
SessionExpAuth module
"""
from datetime import datetime, timedelta
import os
from typing import Dict
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """ SessionExpAuth class"""
    def __init__(self):
        """ initialize"""
        try:
            self.session_duration = int(os.getenv("SESSION_DURATION"))
        except Exception as e:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """ create new session"""
        try:
            session_id = super().create_session(user_id=user_id)
        except Exception:
            return None
        self.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ gets user id from session"""
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        session_dict: Dict = self.user_id_by_session_id.get(session_id)
        if self.session_duration <= 0:
            return session_dict["user_id"]
        if not session_dict.get("created_at"):
            return None
        created_at = session_dict.get("created_at")
        session_duration = timedelta(seconds=self.session_duration)
        session_datetime = created_at + session_duration
        current_datetime = datetime.utcnow()
        if current_datetime > session_datetime:
            return None
        return session_dict["user_id"]
