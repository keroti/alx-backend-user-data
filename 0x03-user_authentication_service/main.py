#!/usr/bin/env python3
"""
Main file
"""
import requests

EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


def register_user(email: str, password: str) -> None:
    """Tests registering a user
    """
    url = 'http://localhost:5000/users'
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)
    assert response.status_code == 201


def log_in_wrong_password(email: str, password: str) -> None:
    """Tests logging in with a wrong password
    """
    url = 'http://localhost:5000/sessions'
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)
    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Tests logging in
    """
    url = 'http://localhost:5000/sessions'
    data = {'email': email, 'password': password}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    session_id = response.cookies.get('session_id')
    return session_id


def profile_unlogged() -> None:
    """Tests retrieving profile information while logged out
    """
    url = 'http://localhost:5000/profile'
    response = requests.get(url)
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Tests retrieving profile information while logged in
    """
    url = 'http://localhost:5000/profile'
    cookies = {'session_id': session_id}
    response = requests.get(url, cookies=cookies)
    assert response.status_code == 200
    data = response.json()
    assert data['email'] == 'guillaume@holberton.io'


def log_out(session_id: str) -> None:
    """Tests logging out of a session
    """
    url = 'http://localhost:5000/sessions'
    cookies = {'session_id': session_id}
    response = requests.delete(url, cookies=cookies)
    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """Tests requesting a password reset
    """
    url = 'http://localhost:5000/reset_password'
    data = {'email': email}
    response = requests.post(url, data=data)
    assert response.status_code == 200
    data = response.json()
    return data['reset_token']


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Tests updating a user's password
    """
    url = 'http://localhost:5000/reset_password'
    data = {'email': email,
            'reset_token': reset_token,
            'new_password': new_password}
    response = requests.put(url, data=data)
    assert response.status_code == 200


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
