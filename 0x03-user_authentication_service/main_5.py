#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

email = 'me@meish.com'
password = 'mySecuredPwd'

auth = Auth()

try:
    user = auth.register_user(email, password)
    print("successfully created a new user!")
except ValueError as err:
    print("could not create a new user: {}".format(err))

try:
    user = auth.register_user('sljakdjfkl@gmail.com', 'samson')
    print("successfully created a new user!")
except ValueError as err:
    print("could not create a new user: {}".format(err))
