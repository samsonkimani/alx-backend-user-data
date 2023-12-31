#!/usr/bin/env python3
""" hashed password method"""

import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4
from typing import TypeVar
from user import User


def _hash_password(password: str) -> str:
    """ function to hash a password"""
    _bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(_bytes, salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> TypeVar('User'):
        """ method to register a new user"""

        # try:
        #     user = self._db.find_user_by(email=email)
        #     raise ValueError(f"User {email} already exists")
        # except NoResultFound:
        #     pass

        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(
                email=email, hashed_password=hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """ ensure a valid user logs in"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                password = password.encode('utf-8')
                if bcrypt.checkpw(password, user.hashed_password):
                    return True
                return False
        except NoResultFound:
            return False

    def _generate_uuid(self) -> str:
        """ a function to generate uuid"""
        _uuid = uuid4()
        return str(_uuid)

    def create_session(self, email: str) -> str:
        """ creating a session"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = self._generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> TypeVar('User'):
        """ get a user from the session id"""
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: str) -> None:
        """ destroy a session"""
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """ generate a password reset token"""
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError()
        reset_token = self._generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """ update password"""
        user = None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError("value does not exist")
        hashed_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password)
        self._db.update_user(user.id, reset_token=None)
