#!/usr/bin/env python3
""" Module of Users views
"""
from typing import TypeVar
from api.v1.views import app_views
from flask import Response, abort, jsonify, request
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login_user() -> str:
    """ POST /api/v1/auth_session/login/
    JSON body:
      - email
      - password
    Return:
      - User object JSON represented
      - 400 if can't log in the new User
    """
    email = request.form.get("email")
    password = request.form.get("password")
    if not email or len(email) == 0:
        return jsonify({ "error": "email missing" }), 400
    if not password or len(password) == 0:
        return jsonify({ "error": "password missing" }), 400
    user = User()
    user = user.search({"email": email})
    if len(user) == 0:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({ "error": "wrong password" }), 401
    else:
        from api.v1.app import auth
        user = user[0].to_json()
        print(user)
        session_id = auth.create_session(user.get("id"))
        session = jsonify(user)
        session.set_cookie("_my_session_id", session_id)
        return session
    
@app_views.route('/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def delete_session() -> str:
    """ DELETE /api/v1/users/:id
    Path parameter:
      - User ID
    Return:
      - empty JSON is the User has been correctly deleted
      - 404 if the User ID doesn't exist
    """
    from api.v1.app import auth
    logout = auth.destroy_session(request)
    if logout is False:
        return abort(404)
    else:
        return jsonify({}), 200
