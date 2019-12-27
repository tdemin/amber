from json import dumps

from flask import request, Blueprint

from project_amber.const import EMPTY_RESP
from project_amber.handlers.const import API_QUERY
from project_amber.helpers.task import addTask, getTask, getTasks, \
    updateTask, removeTask

task_handlers = Blueprint("task_handlers", __name__)


@task_handlers.route("/task", methods=["GET", "POST"])
def task_request():
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
        new_id = addTask(request.json)
        return dumps(new_id)
    return EMPTY_RESP


@task_handlers.route("/task/<task_id>", methods=["GET", "PATCH", "DELETE"])
def task_id_request(task_id: int):
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
        updateTask(task_id, request.json)
    if request.method == "DELETE":
        return dumps(removeTask(task_id))
    return EMPTY_RESP
