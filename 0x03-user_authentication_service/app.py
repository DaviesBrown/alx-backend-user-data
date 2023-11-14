#!/usr/bin/env python3
"""
flask app
"""
from auth import Auth
from flask import Flask, abort, jsonify, redirect, request

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def welcome():
    """ welcome payload"""
    return jsonify({"message": "Bienvenue"}), 200


@app.route("/users", methods=["POST"], strict_slashes=False)
def users():
    """ endpoint for registering a user"""
    email = request.form.get("email")
    password = request.form.get("password")
    if email is None and password is None:
        return abort(403)
    try:
        user = AUTH.register_user(email=email, password=password)
        return jsonify({"email": email, "message": "user created"}), 200
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login():
    """ login user"""
    email = request.form.get("email")
    password = request.form.get("password")
    if email is None and password is None:
        return abort(403)
    is_valid = AUTH.valid_login(email=email, password=password)
    if is_valid:
        ses_id = AUTH.create_session(email=email)
        res = jsonify({"email": email, "message": "logged in"}), 200
        res.set_cookie("session_id", ses_id)
        return res
    else:
        abort(401)


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout():
    """ logout user"""
    session_id = request.cookies.get("session_id")
    if session_id is None:
        return abort(403)
    try:
        user = AUTH.get_user_from_session_id(session_id)
        AUTH.destroy_session(user.id)
        return redirect("/", 302)
    except Exception:
        return abort(403)


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile():
    """ user profile"""
    session_id = request.cookies.get("session_id")
    if session_id is None:
        return abort(403)
    try:
        user = AUTH.get_user_from_session_id(session_id)
        return jsonify({"email": user.email}), 200
    except Exception:
        return abort(403)


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token():
    """ get reset password token"""
    email = request.form.get("email")
    if email is None:
        return abort(403)
    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token}), 200
    except ValueError:
        return abort(403)


@app.route("/update_password", methods=["PUT"], strict_slashes=False)
def reset_password():
    """ reset and update password"""
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")
    if email is None and reset_token is None and new_password is None:
        return abort(403)
    AUTH.update_password(reset_token, password=new_password)
    return jsonify({"email": email, "message": "Password updated"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
