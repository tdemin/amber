from json import dumps

from flask import request

from project_amber.const import EMPTY_RESP
from project_amber.helpers.auth import handleChecks
from project_amber.helpers.task import addTask, updateTask, removeTask

def handle_task_request():
    """
    Handles requests to `/api/task`. Accepts GET and POST.
    The request JSON may contain a `query` parameter in a GET request, in this
    case only the tasks which text contains things from `query` will be sent.
    With a GET request, this will be returned to an authenticated user:
    ```
    {
        "tasks": [
            {
                "id": 123,
                "text": "Some task",
                "last_mod": 12345 // timestamp
            },
            {
                "id": 456,
                "text": "Some text",
                "last_mod": 12346
            }
        ]
    }
    ```
    With a POST request, the client will get HTTP 200 on this body:
    ```
    {
        "text": "Some task"
    }
    ```
    """
    user = handleChecks()
    if request.method == "GET":
        pass
    elif request.method == "POST":
        pass

def handle_task_id_request(task_id: int):
    """
    Handles requests to `/api/task/<id>`. Accepts GET, PATCH, and DELETE.
    """
    user = handleChecks()
    if request.method == "GET":
        pass
    elif request.method == "PATCH":
        pass
    elif request.method == "DELETE":
        pass
