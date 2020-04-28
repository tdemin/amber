from hashlib import sha256
from base64 import b64encode
from typing import List

from bcrypt import hashpw, gensalt, checkpw

from project_amber.const import MSG_USER_EXISTS
from project_amber.db import db
from project_amber.helpers import time
from project_amber.handlers import LoginUser
from project_amber.handlers.const import API_PASSWORD
from project_amber.errors import Unauthorized, NotFound, Conflict
from project_amber.logging import error
from project_amber.models.auth import User, Session


def prehash(password: str) -> bytes:
    """
    Returns a "normalized" representation of the password that works
    with bcrypt even when the password is longer than 72 chars.
    """
    return b64encode(sha256(password.encode()).digest())


def gen_hashed_pw(password: str) -> bytes:
    """
    Returns a bcrypt password hash with random salt.
    """
    return hashpw(prehash(password), gensalt()).decode()


def gen_token() -> str:
    """
    Returns a new freshly generated auth token.
    """
    return sha256(gensalt() + bytes(str(time()).encode())).hexdigest()


class UserController:
    user: LoginUser

    def __init__(self, user: LoginUser):
        self.user = user

    def add_user(self, name: str, password: str) -> int:
        """
        Creates a new user. Returns their ID on success.
        """
        # does a user with this name already exist?
        if not db.session.query(User).filter_by(name=name).one_or_none() is None:
            raise Conflict(MSG_USER_EXISTS)
        hashed_pw = gen_hashed_pw(password)
        user = User(name=name, password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        return user.id

    def update_user(self, **kwargs) -> int:
        """
        Updates user data in the database. Returns their ID on success.
        """
        user_record = db.session.query(User).filter_by(id=self.user.id).one()
        for attribute in kwargs:
            if attribute == API_PASSWORD:
                user_record.password = gen_hashed_pw(kwargs[API_PASSWORD])
        db.session.commit()
        return self.user.id

    def remove_user(self) -> int:
        """
        Removes a user from the database. Returns their ID.
        """
        user = db.session.query(User).filter_by(id=self.user.id).one_or_none()
        try:
            db.session.delete(user)
            db.session.commit()
        # pylint: disable=bare-except
        except:
            error("Failed to remove user %s!" % user.name)
        return self.user.id

    def verify_pw(self, uid: int, password: str) -> bool:
        """
        Verifies user's password with bcrypt's checkpw(). Returns `True`, if
        the passwords match, and False otherwise.
        """
        user = db.session.query(User).filter_by(id=uid).one()
        user_pass = user.password
        if isinstance(user_pass, str):
            user_pass = user_pass.encode()
        return checkpw(prehash(password), user_pass)

    def create_session(self, name: str, password: str, ip_addr: str) -> str:
        """
        Creates a new user session. Returns an auth token.
        """
        user = db.session.query(User).filter_by(name=name).one_or_none()
        token: str
        if user is None:
            raise Unauthorized
        if self.verify_pw(user.id, password):
            token = gen_token()
            session = Session(token=token, user=user.id, login_time=time(), address=ip_addr)
            db.session.add(session)
            db.session.commit()
        else:
            raise Unauthorized
        return token

    def remove_session(self) -> str:
        """
        Logs the user out by removing their token from the database. Returns
        the token on success.
        """
        session = db.session.query(Session).filter_by(token=self.user.token,
                                                      user=self.user.id).one_or_none()
        if session is None:
            raise NotFound
        db.session.delete(session)
        db.session.commit()
        return self.user.token

    def remove_session_by_id(self, sid: int) -> int:
        """
        Removes a user session by session ID. Returns the session ID on success.
        """
        session = db.session.query(Session).filter_by(id=sid, user=self.user.id).one_or_none()
        if session is None:
            raise NotFound
        db.session.delete(session)
        db.session.commit()
        return sid

    def get_sessions(self) -> List[Session]:
        """
        Returns a list of sessions of a user (class `Session`).
        """
        sessions = db.session.query(Session).filter_by(user=self.user.id).all()
        return sessions

    def get_session(self, sid: int) -> Session:
        """
        Returns a single `Session` by its ID.
        """
        session = db.session.query(Session).filter_by(id=sid, user=self.user.id).one_or_none()
        if session is None:
            raise NotFound
        return session
