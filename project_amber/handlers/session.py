from json import dumps
from time import time

from flask import request

from project_amber.const import MATURE_SESSION, MSG_IMMATURE_SESSION, EMPTY_RESP
from project_amber.errors import Forbidden
from project_amber.helpers.auth import handleChecks, getSessions, getSession,\
    removeSessionById
from project_amber.logging import log

def handle_session_req():
    """
    Request handler for `/api/session`. Only accepts GET requests. Returns a
    list of sessions like the one below:
    ```
    {
        "sessions": [
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
    }
    ```
    """
    user = handleChecks()
    sessions = getSessions(user.id)
    sessionList = []
    for session in sessions:
        sessionList.append({
            "id": session.id,
            "login_time": session.login_time,
            "address": session.address
        })
    return dumps({
        "sessions": sessionList
    })

def handle_session_id_req(session_id: int):
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
    user = handleChecks()
    if request.method == "GET":
        session = getSession(session_id, user.id)
        return dumps({
            "id": session.id,
            "login_time": session.login_time,
            "address": session.address
        })
    if request.method == "DELETE":
        if (time() - user.login_time) < MATURE_SESSION:
            raise Forbidden(MSG_IMMATURE_SESSION)
        removeSessionById(session_id, user.id)
        log("User {0} deleted session {1}".format(
            user.name,
            session_id
        ))
        return EMPTY_RESP
