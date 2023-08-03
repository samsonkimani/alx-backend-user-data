#!/usr/bin/env python3
"""encrypt a password
"""
import bcrypt
from bcrypt import hashpw


def hash_password(password: str) -> bytes:
    """ a function to return an encrypted password"""
    passwd = password.encode()
    hashed = hashpw(passwd, bcrypt.gensalt())
    return hashed
