from flask import request

from project_amber.const import EMPTY_RESP
from project_amber.errors import BadRequest
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
    if "password" in request.json:
        updateUser(password=request.json.get("password"))
    return EMPTY_RESP


def signup():
    """
    Signup request handler. Accepts this JSON:
    ```
    {
        "name": "some_user_name",
        "password": "some_password"
    }
    ```
    Returns HTTP 200 with empty JSON on success, 400 on missing params, 500
    otherwise.
    """
    if not "name" in request.json or not "password" in request.json:
        raise BadRequest("Missing 'name' or 'password'")
    addUser(request.json["name"], request.json["password"])
    return EMPTY_RESP
