#!/usr/bin/env python3
"""
Flask app module
"""
from flask import Flask, jsonify, request, make_response, redirect
from auth import Auth

app = Flask(__name__)
AUTH = Auth()


@app.route("/")
def welcome():
    """
    Return a welcome message
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """
    Implement endpoint to register new user
    """
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400

    return jsonify({"email": f"{email}", "message": "user created"})


@app.route("/sessions", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    if AUTH.valid_login(email, password):
        session_id = AUTH.create_session(email)
        response = jsonify({"email": email, "message": "logged in"})
        response.set_cookie("session_id", session_id)
        return response
    else:
        return make_response("Unauthorized", 401)
    

@app.route('/sessions', methods=['DELETE'])
def logout():
    """Logout route"""
    session_id = request.cookies.get('session_id')

    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect('/')
    
    return jsonify(message='Forbidden'), 403


@app.route('/profile', methods=['GET'])
def profile():
    """Profile route"""
    session_id = request.cookies.get('session_id')

    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            return jsonify(email=user.email), 200

    return jsonify(message='Forbidden'), 403


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
