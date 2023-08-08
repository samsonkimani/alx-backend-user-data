#!/usr/bin/env python3
"""
creating the basic auth module
"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ for basic authentication"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ extracting the basic key"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        header_array = authorization_header.split(" ")
        if header_array[0] != "Basic":
            return None
        else:
            return header_array[1]
