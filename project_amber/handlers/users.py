from flask import request, Blueprint

from project_amber.config import config
from project_amber.const import EMPTY_RESP, MSG_MISSING_AUTH_INFO, MSG_SIGNUP_FORBIDDEN
from project_amber.errors import BadRequest, Forbidden
from project_amber.handlers import accepts_json, login_required
from project_amber.handlers.const import API_PASSWORD, API_USER
from project_amber.helpers.auth import addUser, updateUser

user_handlers = Blueprint("user_handlers", __name__)


@user_handlers.route("/user", methods=["PATCH"])
@accepts_json
@login_required
def user_data():
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


@user_handlers.route("/signup", methods=["POST"])
@accepts_json
def signup():
    """
    Signup request handler. Accepts this JSON:
    ```
    {
        "username": "some_user_name",
        "password": "some_password"
    }
    ```
    Returns HTTP 200 with empty JSON on success, 400 on missing params, 403 if
    the method is disabled by a config parameter.
    """
    if not config.allow_signup:
        raise Forbidden(MSG_SIGNUP_FORBIDDEN)
    if not API_USER in request.json or not API_PASSWORD in request.json:
        raise BadRequest(MSG_MISSING_AUTH_INFO)
    addUser(request.json[API_USER], request.json[API_PASSWORD])
    return EMPTY_RESP
