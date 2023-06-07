#!/usr/bin/env python3
"""
Flask app module
"""
from flask import Flask, jsonify, request
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def welcome():
    """
    Return a welcome message
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def register_user():
    """
    Implement endpoint to register user
    """
    email = request.form.get("email")
    password = request.form.get("password")

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError as err:
        return jsonify({"message": str(err)}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
