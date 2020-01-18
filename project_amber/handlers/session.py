from json import dumps

from flask import request, Blueprint

from project_amber.const import MATURE_SESSION, MSG_IMMATURE_SESSION, EMPTY_RESP
from project_amber.errors import Forbidden
from project_amber.handlers import login_required
from project_amber.helpers import time
from project_amber.controllers.auth import UserController
from project_amber.logging import log

session_handlers = Blueprint("session_handlers", __name__)


@session_handlers.route("/session", methods=["GET"])
@login_required
def get_sessions():
    """
    Request handler for `/api/session`. Only accepts GET requests. Returns a
    list of sessions like the one below:
    ```
    [
        {
            "id": 1,
            "login_time": 123456, // timestamp
            "address": "127.0.0.1"
        }
        {
            "id": 2,
            "login_time": 123457,
            "address": "10.0.0.1"
        }
    ]
    ```
    """
    uc = UserController(request.user)
    sessions = uc.get_sessions()
    sessionList = list()
    for session in sessions:
        sessionList.append(session.to_json())
    return dumps(sessionList)


@session_handlers.route("/session/<session_id>", methods=["GET", "DELETE"])
@login_required
def session_by_id(session_id: int):
    """
    Login handler for `/api/session/<id>`. Accepts GET and DELETE
    requests. Returns 404 if this session does not exist. On successful
    GET, returns JSON like this:
    ```
    {
        "id": 1,
        "login_time": 123456, // timestamp
        "address": "127.0.0.1"
    }
    ```
    On DELETE, this will return HTTP 200 with empty JSON. There is a special
    case here: if a client session is too recent, this will respond with
    HTTP 403.
    """
    uc = UserController(request.user)
    if request.method == "GET":
        session = uc.get_session(session_id)
        return dumps(session.to_json())
    if request.method == "DELETE":
        if (time() - uc.user.login_time) < MATURE_SESSION:
            raise Forbidden(MSG_IMMATURE_SESSION)
        uc.remove_session_by_id(session_id)
        log(f"User {uc.user.name} deleted session {session_id}")
    return EMPTY_RESP
