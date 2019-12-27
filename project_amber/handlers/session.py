from json import dumps

from flask import request, Blueprint

from project_amber.const import MATURE_SESSION, MSG_IMMATURE_SESSION, EMPTY_RESP
from project_amber.errors import Forbidden
from project_amber.handlers.const import API_ID, API_LOGIN_TIME, API_ADDRESS
from project_amber.helpers import time
from project_amber.helpers.auth import getSessions, getSession, removeSessionById
from project_amber.logging import log

session_handlers = Blueprint("session_handlers", __name__)


@session_handlers.route("/session", methods=["GET"])
def session():
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
    sessions = getSessions()
    sessionList = []
    for session in sessions:
        sessionList.append({
            API_ID: session.id,
            API_LOGIN_TIME: session.login_time,
            API_ADDRESS: session.address
        })
    return dumps(sessionList)


@session_handlers.route("/session/<session_id>", methods=["GET", "DELETE"])
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
    if request.method == "GET":
        session = getSession(session_id)
        return dumps({
            API_ID: session.id,
            API_LOGIN_TIME: session.login_time,
            API_ADDRESS: session.address
        })
    if request.method == "DELETE":
        if (time() - request.user.login_time) < MATURE_SESSION:
            raise Forbidden(MSG_IMMATURE_SESSION)
        removeSessionById(session_id)
        log(
            "User {0} deleted session {1}".format(
                request.user.name, session_id
            )
        )
    return EMPTY_RESP
