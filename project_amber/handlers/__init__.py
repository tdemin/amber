from functools import wraps
from re import fullmatch

from flask import request

from project_amber.db import db
from project_amber.const import MSG_NO_TOKEN, MSG_INVALID_TOKEN, \
    MSG_USER_NOT_FOUND, MSG_USER_EXISTS, MSG_INVALID_JSON
from project_amber.errors import Unauthorized, BadRequest, InternalServerError
from project_amber.models.auth import User, Session


class LoginUser:
    """
    Representational class for request checks. Contains the user name
    and ID. The corresponding fields are `name` and `id`, respectively.
    Also contains a token field.
    """
    def __init__(self, name: str, uid: int, token: str, login_time: int, remote_addr: str):
        self.name = name
        self.id = uid
        self.token = token
        self.login_time = login_time
        self.remote_addr = remote_addr


def accepts_json(f):
    """
    Checks whether the request payload contains valid JSON, drops errors
    on need.
    """
    @wraps(f)
    def decorated_json_checker(*args, **kwargs):
        if not request.is_json and request.method in ("POST", "PUT", "PATCH"):
            raise BadRequest(MSG_INVALID_JSON)
        return f(*args, **kwargs)

    return decorated_json_checker


def login_required(f):
    """
    Login handler. Works with Flask's `request`. Checks the auth token HTTP
    header. Sets `request.user` object containing the user's name and their ID.
    Raises an exception if the auth token is not valid.
    """
    @wraps(f)
    def decorated_login_function(*args, **kwargs):
        token = request.headers.get("X-Auth-Token")
        if token is None:
            raise Unauthorized(MSG_NO_TOKEN)
        user_s = db.session.query(Session).filter_by(token=token).one_or_none()
        if user_s is None:
            raise Unauthorized(MSG_INVALID_TOKEN)
        user = db.session.query(User).filter_by(id=user_s.user).one_or_none()
        if user is None:
            raise InternalServerError(MSG_USER_NOT_FOUND)
        user_details = LoginUser(user.name, user.id, token, user_s.login_time, request.remote_addr)
        request.user = user_details
        return f(*args, **kwargs)

    return decorated_login_function
