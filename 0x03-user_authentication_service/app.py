#!/usr/bin/env python3
""" creating a flask app"""

from flask import Flask, jsonify, request, abort
from auth import Auth

app = Flask(__name__)

AUTH = Auth()


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



if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
