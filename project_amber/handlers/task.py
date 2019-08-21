from json import dumps

from flask import request

from project_amber.const import EMPTY_RESP, MSG_TEXT_NOT_SPECIFIED
from project_amber.errors import BadRequest
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
        "last_mod": 12346, // the latest last_mod from task list
        "tasks": [
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
    if request.method == "GET":
        query = request.args.get("query", None)
        # `query` is OK to be `None`
        tasks = getTasks(query)
        tasksList = []
        lastMod = 0
        for task in tasks:
            tasksList.append({
                "id": task.id,
                "text": task.text,
                "status": task.status,
                "last_mod": task.last_mod_time
            })
            currentTask = tasksList[len(tasksList) - 1]
            if not task.parent_id is None:
                currentTask["parent_id"] = task.parent_id
            if not task.deadline is None:
                currentTask["deadline"] = task.deadline
            if not task.reminder is None:
                currentTask["reminder"] = task.reminder
            if task.last_mod_time > lastMod: lastMod = task.last_mod_time
        return dumps({
            "last_mod": lastMod,
            "tasks": tasksList
        })
    if request.method == "POST":
        text = request.json.get("text")
        if text is None: raise BadRequest(MSG_TEXT_NOT_SPECIFIED)
        status = request.json.get("status")
        # if only I could `get("status", d=0)` like we do that with dicts
        if status is None: status = 0
        deadline = request.json.get("deadline")
        reminder = request.json.get("reminder")
        parent_id = request.json.get("parent_id") # ok to be `None`
        new_id = addTask(text, status, parent_id, deadline, reminder)
        return dumps({ "id": new_id })

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
        response = {
            "id": task.id,
            "text": task.text,
            "status": task.status,
            "last_mod": task.last_mod_time
        }
        if not task.parent_id is None: response["parent_id"] = task.parent_id
        if not task.deadline is None: response["deadline"] = task.deadline
        if not task.reminder is None: response["reminder"] = task.reminder
        return dumps(response)
    if request.method == "PATCH":
        text = request.json.get("text")
        status = request.json.get("status")
        parent_id = request.json.get("parent_id")
        deadline = request.json.get("deadline")
        reminder = request.json.get("reminder")
        # these are fine to be `None`
        updateTask(task_id, text=text, status=status, parent_id=parent_id, \
            deadline=deadline, reminder=reminder)
        return EMPTY_RESP
    if request.method == "DELETE":
        removeTask(task_id)
        return EMPTY_RESP
