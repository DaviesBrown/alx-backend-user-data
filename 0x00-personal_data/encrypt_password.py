#!/usr/bin/env python3
"""
hash password
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ hashes password with salt"""
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    """checks validity of password"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password)
