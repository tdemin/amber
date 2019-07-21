from hashlib import sha256
from base64 import b64encode

from bcrypt import hashpw, gensalt, checkpw
from flask import request

from project_amber.const import MSG_USER_NOT_FOUND, MSG_USER_EXISTS
from project_amber.db import db
from project_amber.helpers import time
from project_amber.errors import Unauthorized, BadRequest, NotFound, \
    InternalServerError, Conflict
from project_amber.logging import log
from project_amber.models.auth import User, Session

def addUser(name: str, password: str) -> int:
    """
    Creates a new user. Returns their ID on success.
    """
    # does a user with this name already exist?
    if not db.session.query(User).filter_by(name=name).one_or_none() is None:
        raise Conflict(MSG_USER_EXISTS)
    prehashed_pw = b64encode(sha256(password.encode("utf8")).digest())
    hashed_pw = hashpw(prehashed_pw, gensalt())
    user = User(name=name, password=hashed_pw)
    log("Adding user %s..." % name)
    db.session.add(user)
    db.session.commit()
    return user.id

def removeUser(uid: int) -> int:
    """
    Removes a user given their ID. Returns their ID on success.
    """
    user = db.session.query(User).filter_by(id=uid).one_or_none()
    if user is None:
        raise NotFound(MSG_USER_NOT_FOUND)
    log("Removing user %s..." % user.name)
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
    user = db.session.query(User).filter_by(name=name).one_or_none()
    if user is None:
        raise Unauthorized # this may present no sense, but the app doesn't
        # have to reveal the presence or absence of a user in the system
    if verifyPassword(user.id, password):
        token = sha256(gensalt() + bytes(str(time()).encode())).hexdigest()
        session = Session(token=token, user=user.id, login_time=time(), \
            address=request.remote_addr)
        log("User {0} logged in from {1}".format(
            user.name,
            request.remote_addr
        ))
        db.session.add(session)
        db.session.commit()
        return token
    raise Unauthorized

def removeSession(token: str, uid: int) -> str:
    """
    Removes a user session by token. Returns the token on success.
    """
    session = db.session.query(Session).filter_by(token=token, user=uid)\
        .one_or_none()
    if session is None:
        raise NotFound
    db.session.delete(session)
    db.session.commit()
    return token

def removeSessionById(session_id: int, uid: int) -> int:
    """
    Removes a user session by session ID. Returns the session ID on success.
    """
    session = db.session.query(Session).filter_by(id=session_id, user=uid)\
        .one_or_none()
    if session is None:
        raise NotFound
    db.session.delete(session)
    db.session.commit()
    return session_id

def getSessions(uid: int) -> list:
    """
    Returns a list of sessions of a user (class `Session`).
    """
    sessions = db.session.query(Session).filter_by(user=uid).all()
    return sessions

def getSession(session_id: int, uid: int) -> Session:
    """
    Returns a single `Session` by its ID.
    """
    session = db.session.query(Session).filter_by(id=session_id, user=uid)\
        .one_or_none()
    if session is None:
        raise NotFound
    return session
