#!/usr/bin/env python3
"""
Main file
"""
import requests


url = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    """ register user test"""
    data = {'email': email, 'password': password}
    res = requests.post(f"{url}/users", data=data)
    assert res.status_code == 200
    assert res.json() == {
        "email": "guillaume@holberton.io",
        "message": "user created"
    }


def log_in_wrong_password(email: str, password: str) -> None:
    """ login wrong password test"""
    data = {'email': "guillaume@holberton.io", 'password': password}
    res = requests.post(f"{url}/sessions", data=data)
    assert res.status_code == 401


def log_in(email: str, password: str) -> str:
    """ login user test"""
    data = {'email': email, 'password': password}
    res = requests.post(f"{url}/sessions", data=data)
    assert res.status_code == 200
    assert res.json() == {"email": email, "message": "logged in"}
    return res.cookies.get("session_id")


def profile_unlogged() -> None:
    """ profile unlogged test"""
    res = requests.get(f"{url}/profile")
    assert res.status_code == 403


def profile_logged(session_id: str) -> None:
    """ profile logged test"""
    jar = requests
    cookies = dict(session_id=session_id)
    res = requests.get(f"{url}/profile", cookies=cookies)
    assert res.status_code == 200
    assert res.json() == {"email": "guillaume@holberton.io"}


def log_out(session_id: str) -> None:
    """ logout user test"""
    cookies = dict(session_id=session_id)
    res = requests.delete(f"{url}/sessions", cookies=cookies)
    assert res.status_code == 200


def reset_password_token(email: str) -> str:
    """reset password test"""
    data = {'email': email}
    res = requests.post(f"{url}/reset_password", data=data)
    assert res.status_code == 200
    return res.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ update user password test"""
    data = {
        'email': email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    res = requests.put(f"{url}/update_password", data=data)
    assert res.status_code == 200
    assert res.json() == {
        "email": "guillaume@holberton.io",
        "message": "Password updated"
    }


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


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
