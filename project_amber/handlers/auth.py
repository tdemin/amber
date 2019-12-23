from json import dumps

from flask import request

from project_amber.const import EMPTY_RESP, MSG_MISSING_AUTH_INFO
from project_amber.errors import BadRequest
from project_amber.handlers.const import API_PASSWORD, API_USER, API_TOKEN
from project_amber.helpers.auth import removeSession, createSession
from project_amber.logging import log


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


def logout():
    """
    Logout handler. Accepts empty JSON. Returns HTTP 200 on success.
    """
    removeSession(request.user.token)
    log("User %s logged out" % request.user.name)
    return EMPTY_RESP
