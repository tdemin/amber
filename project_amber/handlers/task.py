from json import dumps

from flask import request

from project_amber.const import EMPTY_RESP, MSG_TEXT_NOT_SPECIFIED
from project_amber.errors import BadRequest
from project_amber.handlers.const import API_PID, API_TEXT, API_STATUS, \
    API_DEADLINE, API_REMINDER, API_QUERY
from project_amber.helpers.task import addTask, getTask, getTasks, \
    updateTask, removeTask


def handle_task_request():
    """
    Handles requests to `/api/task`. Accepts GET and POST.
    The request JSON may contain a `query` parameter in a GET request, in this
    case only the tasks which text contains things from `query` will be sent.
    With a GET request, this will be returned to an authenticated user:
    ```
    [
        {
            "id": 123,
            "text": "Some task",
            "status:": 1,
            "last_mod": 12345, // timestamp
            "deadline": 123456
        },
        {
            "id": 456,
            "text": "Some text",
            "status": 0,
            "last_mod": 12346,
            "parent_id": 123,
            "reminder": 123457
        }
    ]
    ```
    With a POST request, the client will get HTTP 200 on this body:
    ```
    {
        "text": "Some task",
        "status": 0,
        ...
    }
    ```
    with a task ID (a literal integer value like `35213`).
    """
    if request.method == "GET":
        query = request.args.get(API_QUERY, None)
        # `query` is OK to be `None`
        tasks = getTasks(query)
        tasksList = []
        for task in tasks:
            tasksList.append(task.toDict())
        return dumps(tasksList)
    if request.method == "POST":
        text = request.json.get(API_TEXT)
        if text is None: raise BadRequest(MSG_TEXT_NOT_SPECIFIED)
        status = request.json.get(API_STATUS)
        # if only I could `get("status", d=0)` like we do that with dicts
        if status is None: status = 0
        deadline = request.json.get(API_DEADLINE)
        reminder = request.json.get(API_REMINDER)
        parent_id = request.json.get(API_PID)  # ok to be `None`
        new_id = addTask(text, status, parent_id, deadline, reminder)
        return dumps(new_id)


def handle_task_id_request(task_id: int):
    """
    Handles requests to `/api/task/<id>`. Accepts GET, PATCH, and DELETE.
    On GET, the user gets this response with HTTP 200 (or 404, if the task
    does not exist):
    ```
    {
        "id": 123,
        "text": "Some text",
        "status": 1,
        "last_mod": 123456, // timestamp
        "parent_id": 11, // if applicable
        "reminder": 123456, // if applicable
        "deadline": 123457 // if applicable
    }
    ```
    On PATCH and DELETE the user will get HTTP 200 with an empty response. On
    PATCH, this request body is expected (all of the parameters are optional):
    ```
    {
        "text": "New task text",
        "status": 1, // new status
        "parent_id": 123, // if applicable
        "deadline": 123456, // if applicable
        "reminder": 123457, // if applicable
    }
    ```
    """
    if request.method == "GET":
        task = getTask(task_id)
        response = task.toDict()
        return dumps(response)
    if request.method == "PATCH":
        text = request.json.get(API_TEXT)
        status = request.json.get(API_STATUS)
        parent_id = request.json.get(API_PID)
        deadline = request.json.get(API_DEADLINE)
        reminder = request.json.get(API_REMINDER)
        # these are fine to be `None`
        updateTask(task_id, text=text, status=status, parent_id=parent_id, \
            deadline=deadline, reminder=reminder)
        return EMPTY_RESP
    if request.method == "DELETE":
        removeTask(task_id)
        return EMPTY_RESP
