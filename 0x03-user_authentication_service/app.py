#!/usr/bin/env python3
""" creating a flask app"""

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)

AUTH = Auth()

def get_reset_password_token():
    """ a function to get the reset password token"""
    try:
        email = request.form.get("email")
        user = AUTH.find_user_by(email=email)
        if user:
            token = AUTH.get_reset_password_token(email)
            return jsonify({"email": email, "reset_token": token}), 200
        abort(403)
    except NoResutFound:
        return None


@app.route("/", methods=["GET"], strict_slashes=False)
def home():
    """ route to home page"""
    return jsonify({"message": "Bienvenue"})

@app.route("/users", methods=["POST"], strict_slashes=False)
def creating_user():
    """ function to create a user"""
    try:
        email = request.form.get("email")
        password = request.form.get("password")
        user = AUTH.register_user(email, password)
        if user:
            return jsonify({"email": f"{email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"})

@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """ method to login a user"""
    email = request.form.get("email")
    password = request.form.get("password")

    if AUTH.valid_login(email, password) is False:
        abort(401)
    else:
        session_id = AUTH.create_session(email)
        if session_id:
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie('session_id', session_id)
            return response

@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """ logout a user"""
    try:
        session_id = request.cookie.get("session_id")
        user = AUTH.get_user_from_session(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect("/")
    except NoResultFound:
        abort(403)

@app.route("/profile", methods=["GET"], strict_slashes=False)
def get_profile():
    """ return the user based on session id"""
    try:
        session_id = request.cookies.get("session_id")
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify({"email": user.email}), 200
        abort(403)
    except NoResultFound:
        return None

@app.route("/reset_password", methods=["PUT"], strict_slashes=False)
def update_password():
    """ function to update the password"""
    try:
        email = request.form.get('email')
        reset_token = request.form.get('reset_token')
        new_password = request.form.get('new_password')

        user = AUTH.find_user_by(email=email)
        if user:
            if user.reset_token == reset_token:
                AUTH.update_password(reset_token, new_password)
                return jsonify({"email": user.email, "message": "Password updated"})
    except ValueError:
        return None
    except NoResultFound:
        return None


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
