from json import dumps

from flask import request

from project_amber.const import EMPTY_RESP
from project_amber.errors import BadRequest
from project_amber.helpers.auth import handleChecks
from project_amber.helpers.task import addTask, getTask, getTasks, \
    updateTask, removeTask

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
                "status:": 1,
                "last_mod": 12345 // timestamp
            },
            {
                "id": 456,
                "text": "Some text",
                "status": 0,
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
    with a task ID.
    """
    user = handleChecks()
    if request.method == "GET":
        query = None
        if "query" in request.json:
            query = request.json["query"]
        tasks = getTasks(user.id, query)
        tasksList = []
        for task in tasks:
            tasksList.append({
                "id": task.id,
                "text": task.text,
                "status": task.status,
                "last_mod": task.last_mod_time
            })
        return dumps({
            "tasks": tasksList
        })
    if request.method == "POST":
        if not "text" in request.json:
            raise BadRequest("No text specified")
        text = request.json["text"]
        status = request.json.get("status")
        # if only I could `get("status", d=0)` like we do that with dicts
        if status is None:
            status = 0
        new_id = addTask(text, status, user.id)
        return dumps({ "id": new_id })

def handle_task_id_request(task_id: int):
    """
    Handles requests to `/api/task/<id>`. Accepts GET, PATCH, and DELETE.
    On GET, the user gets this response with HTTP 200 (or 404, if the task
    does not exist):
    ```
    {
        "id": 1,
        "text": "Some text",
        "status": 1,
        "last_mod": 123456 // timestamp
    }
    ```
    On PATCH and DELETE the user will get HTTP 200 with an empty response. On
    PATCH, this request body is expected (all of the parameters are optional):
    ```
    {
        "text": "New task text",
        "status": 1 // new status
    }
    ```
    """
    user = handleChecks()
    if request.method == "GET":
        task = getTask(task_id, user.id)
        return dumps({
            "id": task.id,
            "text": task.text,
            "status": task.status,
            "last_mod": task.last_mod_time
        })
    if request.method == "PATCH":
        text = None
        status = None
        if "text" in request.json:
            text = request.json["text"]
        if "status" in request.json:
            status = request.json["status"]
        updateTask(task_id, user.id, text=text, status=status)
        return EMPTY_RESP
    if request.method == "DELETE":
        removeTask(task_id, user.id)
        return EMPTY_RESP
