#!/usr/bin/env python3
""" hashed password method"""

import bcrypt


def _hash_password(password):
    """ function to hash a password"""
    _bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()

    return bcrypt.hashpw(_bytes, salt)

