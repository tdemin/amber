from flask import request

from project_amber.const import EMPTY_RESP, MSG_MISSING_AUTH_INFO
from project_amber.errors import BadRequest
from project_amber.handlers.const import API_PASSWORD, API_USER
from project_amber.helpers.auth import addUser, updateUser


def update_user_data():
    """
    User data PATCH request handler. Accepts JSON with these parameters:
    ```
    {
        "password": "my_new_password"
    }
    ```
    Returns HTTP 200 on success.
    """
    if API_PASSWORD in request.json:
        updateUser(password=request.json.get(API_PASSWORD))
    return EMPTY_RESP


def signup():
    """
    Signup request handler. Accepts this JSON:
    ```
    {
        "username": "some_user_name",
        "password": "some_password"
    }
    ```
    Returns HTTP 200 with empty JSON on success, 400 on missing params, 500
    otherwise.
    """
    if not API_USER in request.json or not API_PASSWORD in request.json:
        raise BadRequest(MSG_MISSING_AUTH_INFO)
    addUser(request.json[API_USER], request.json[API_PASSWORD])
    return EMPTY_RESP
