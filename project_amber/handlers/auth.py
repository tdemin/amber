from json import dumps

from flask import request

from project_amber.const import EMPTY_RESP
from project_amber.errors import BadRequest
from project_amber.helpers.auth import handleChecks, removeSession, \
    createSession

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
    if not request.is_json:
        raise BadRequest
    if not "name" in request.json or not "password" in request.json:
        raise BadRequest
    token = createSession(request.json["name"], request.json["password"])
    return dumps({ "token": token })

def logout():
    """
    Logout handler. Accepts empty JSON. Returns HTTP 200 on success.
    """
    user = handleChecks()
    removeSession(user.token, user.id)
    return EMPTY_RESP
