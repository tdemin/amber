from hashlib import sha256
from base64 import b64encode
from time import time

from bcrypt import hashpw, gensalt, checkpw
from flask import request

from project_amber.db import db
from project_amber.errors import Unauthorized, BadRequest
from project_amber.models.auth import User, Session

class LoginUser:
    """
    Representational class for request checks. Contains the user name
    and ID. The corresponding fields are `name` and `id`, respectively.
    Also contains a token field.
    """
    def __init__(self, name: str, uid: int, token: str):
        self.name = name
        self.id = uid
        self.token = token

def handleChecks() -> LoginUser:
    """
    Login handler. Works with Flask's `request`. Returns an object
    containing the user's name and their ID. Raises an exception if
    the auth token is not valid.

    This is essentially a request decorator that is implemented as a
    function. This also checks whether the request contains valid JSON,
    and drops HTTP 400 if not.
    """
    if not request.is_json:
        raise BadRequest
    token = request.headers.get("X-Auth-Token")
    if token is None:
        raise Unauthorized
    user_session = db.session.query(Session).filter_by(token=token).one()
    user = db.session.query(User).filter_by(id=user_session.user).one()
    user_details = LoginUser(user.name, user.id, token)
    return user_details

def addUser(name: str, password: str) -> int:
    """
    Creates a new user. Returns their ID on success.
    """
    prehashed_pw = b64encode(sha256(password.encode("utf8")).digest())
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
    prehashed_pw = b64encode(sha256(password.encode("utf8")).digest())
    return checkpw(prehashed_pw, user.password)

def createSession(name: str, password: str) -> str:
    """
    Creates a new user session. Returns an auth token.
    """
    user = db.session.query(User).filter_by(name=name).one()
    if verifyPassword(user.id, password):
        token = sha256(gensalt()).hexdigest()
        session = Session(token=token, user=user.id, login_time=time())
        db.session.add(session)
        db.session.commit()
        return token
    raise Unauthorized

def removeSession(token: str) -> str:
    """
    Removes a user session by token. Returns the token on success.
    """
    session = db.session.query(Session).filter_by(token=token).one()
    db.session.delete(session)
    db.session.commit()
    return token
