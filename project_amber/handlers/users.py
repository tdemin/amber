from flask import request

from project_amber.const import EMPTY_RESP
from project_amber.errors import BadRequest
from project_amber.helpers.auth import addUser

def signup():
    """
    Signup request handler. Accepts this JSON:
    ```
    {
        "name": "some_user_name",
        "password": "some_password"
    }
    ```
    Returns HTTP 200 with empty JSON on success, 400 on missing params,
    500 otherwise.
    """
    if not request.is_json:
        raise BadRequest
    if not "name" in request.json or not "password" in request.json:
        raise BadRequest
    addUser(request.json["name"], request.json["password"])
    return EMPTY_RESP
