from json import dumps

from flask import request, Blueprint

from project_amber.const import EMPTY_RESP, MSG_MISSING_AUTH_INFO
from project_amber.errors import BadRequest
from project_amber.handlers import login_required, accepts_json
from project_amber.handlers.const import API_PASSWORD, API_USER, API_TOKEN
from project_amber.helpers.auth import removeSession, createSession
from project_amber.logging import log

auth_handlers = Blueprint("auth_handlers", __name__)


@auth_handlers.route("/login", methods=["POST"])
@accepts_json
def login():
    """
    Login handler. Accepts this JSON:
    ```
    {
        "username": "some_user_name",
        "password": "some_password"
    }
    ```
    Returns HTTP 200 with the JSON below on success:
    ```
    {
        "token": "some_auth_token"
    }
    ```
    Drops HTTP 401 on fail.
    """
    if not API_USER in request.json or not API_PASSWORD in request.json:
        raise BadRequest(MSG_MISSING_AUTH_INFO)
    token = createSession(request.json[API_USER], request.json[API_PASSWORD])
    return dumps({API_TOKEN: token})


@auth_handlers.route("/logout", methods=["POST"])
@login_required
def logout():
    """
    Logout handler. Returns HTTP 200 on success.
    """
    removeSession(request.user.token)
    log("User %s logged out" % request.user.name)
    return EMPTY_RESP
