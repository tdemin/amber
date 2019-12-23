from json import dumps

from flask import request

from project_amber.const import EMPTY_RESP
from project_amber.errors import BadRequest
from project_amber.helpers.auth import removeSession, createSession
from project_amber.logging import log


def login():
    """
    Login handler. Accepts this JSON:
    ```
    {
        "name": "some_user_name",
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
    if not "name" in request.json or not "password" in request.json:
        raise BadRequest
    token = createSession(request.json["name"], request.json["password"])
    return dumps({"token": token})


def logout():
    """
    Logout handler. Accepts empty JSON. Returns HTTP 200 on success.
    """
    removeSession(request.user.token)
    log("User %s logged out" % request.user.name)
    return EMPTY_RESP
