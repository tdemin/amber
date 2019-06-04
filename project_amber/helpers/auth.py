from hashlib import sha256
from base64 import b64encode

from bcrypt import hashpw, gensalt, checkpw

from project_amber.app import db
from project_amber.models.auth import User

def addUser(name: str, password: str) -> int:
    """
    Creates a new user. Returns their ID on success.
    """
    prehashed_pw = b64encode(sha256(password).digest())
    hashed_pw = hashpw(prehashed_pw, gensalt())
    user = User(name=name, password=hashed_pw)
    db.session.add(user)
    db.session.commit()
    return user.id

def removeUser(uid: int) -> int:
    """
    Removes a user given their ID. Returns their ID on success.
    """
    user = db.session.query(User).filter_by(id=uid).one()
    db.session.delete(user)
    db.session.commit()
    return uid

def verifyPassword(uid: int, password: str) -> bool:
    """
    Verifies user's password with bcrypt's checkpw(). Returns `True`, if
    the passwords match, and False otherwise.
    """
    user = db.session.query(User).filter_by(id=uid).one()
    prehashed_pw = b64encode(sha256(password).digest())
    return checkpw(prehashed_pw, user.password)
