#!/usr/bin/env python3
""" user views model"""

from api.v1.views import app_views
from flask import request, jsonify, make_response
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login_authentication():
    """ all """
    email = request.form.get('email')
    if email is None:
        return jsonify({"error": "email missing"})
    password = request.form.get('password')
    if password is None:
        return jsonify({"error": "password missing"})
    if email and password:
        users = User.search({"email": email})
        user = None
        if not users:
            return jsonify({"error": "no user found for this email"}), 404
        for user in users:
            if user.is_valid_password(password):
                user = user
        if user is None:
            return jsonify({"error": "wrong password"})
        if user:
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            response_data = user.to_json()
            response = make_response(jsonify(response_data))
            session_name = os.environ.get('SESSION_NAME', '_my_session_id')
            response.set_cookie(session_name, session_id)
            return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def logout():
    """ logging out a user"""
    from api.v1.app import auth
    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
