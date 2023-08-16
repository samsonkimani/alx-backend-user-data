#!/usr/bin/env python3
""" hashed password method"""

import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import SQLAlchemyError
from uuid import uuid4

def _hash_password(password):
    """ function to hash a password"""
    _bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(_bytes, salt)


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email, password):
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
            pass


        hashed_password = _hash_password(password)

        user = self._db.add_user(email=email, hashed_password=hashed_password)

        return user

    def valid_login(self, email, password):
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

    def _generate_uuid(self):
        """ a function to generate uuid"""
        _uuid = uuid4()
        return str(_uuid)

    def create_session(self, email):
        """ creating a session"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                session_id = self._generate_uuid()
                self._db.update_user(user.id, session_id=session_id)
                return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id):
        """ get a user from the session id"""
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id):
        """ destroy a session"""
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email):
        """ generate a password reset token"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                token = self._generate_uuid()
                self._db.update_user(user.id, reset_token=token)
                return token
            raise ValueError("no such values were found")
        except NoResultFound:
            return None

    def update_password(reset_token, password):
        """ update password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
            if user:
                hashed_password = _hash_password(password)
                self._db.update_user(user.id, hashed_password=hashed_password)
                self._db.update_user(user.id, reset_token=None)
            else:
                raise ValueError("value does not exist")
        except NoResultFound:
            return None
