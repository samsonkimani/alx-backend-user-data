#!/usr/bin/env python3
""" hashed password method"""

import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import SQLAlchemyError

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
