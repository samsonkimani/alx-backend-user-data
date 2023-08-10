#!/usr/bin/env python3
""" sessionauth module"""

from api.v1.auth.auth import Auth
from uuid import uuid4
from typing import TypeVar
from models.user import User


class SessionAuth(Auth):
    """ session auth"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ creating a session id for a user"""
        if user_id is None:
            return None
        if not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ get the userid based on session id"""
        if session_id is None:
            return None
        if not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None) -> TypeVar('User'):
        """ return a user based on the session id"""
        cookie = self.session_cookie(request)
        if cookie:
            user_id = self.user_id_for_session_id(cookie)
            if user_id:
                user = User.get(user_id)
                return user
        return

    def destroy_session(self, request=None) -> bool:
        """ destroy a session"""
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False

        del self.user_id_by_session_id[session_id]
        return True
