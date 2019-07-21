from time import time as time_lib

from flask import request

from project_amber.db import db
from project_amber.const import MSG_NO_TOKEN, MSG_INVALID_TOKEN, \
    MSG_USER_NOT_FOUND, MSG_USER_EXISTS
from project_amber.errors import Unauthorized, BadRequest, NotFound, \
    InternalServerError, Conflict
from project_amber.models.auth import User, Session

class LoginUser:
    """
    Representational class for request checks. Contains the user name
    and ID. The corresponding fields are `name` and `id`, respectively.
    Also contains a token field.
    """
    def __init__(self, name: str, uid: int, token: str, login_time: int):
        self.name = name
        self.id = uid
        self.token = token
        self.login_time = login_time

def handleChecks() -> LoginUser:
    """
    Login handler. Works with Flask's `request`. Returns an object
    containing the user's name and their ID. Raises an exception if
    the auth token is not valid.

    This is essentially a request decorator that is implemented as a
    function. This also checks whether the request contains valid JSON,
    and drops HTTP 400 if not.
    """
    if not request.is_json and request.method in ["POST", "PUT", "PATCH"]:
        raise BadRequest
    token = request.headers.get("X-Auth-Token")
    if token is None:
        raise Unauthorized(MSG_NO_TOKEN)
    user_session = db.session.query(Session).filter_by(token=token).one_or_none()
    if user_session is None:
        raise Unauthorized(MSG_INVALID_TOKEN)
    user = db.session.query(User).filter_by(id=user_session.user).one_or_none()
    if user is None:
        raise InternalServerError(MSG_USER_NOT_FOUND)
    user_details = LoginUser(user.name, user.id, token, user_session.login_time)
    return user_details

def time() -> int:
    """
    Wrapper around `time.time()`. Converts the result to `int` to prevent
    getting fractions of seconds on some platforms.
    """
    return int(time_lib())
