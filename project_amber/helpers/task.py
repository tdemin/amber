from time import time

from project_amber.const import MSG_TASK_NOT_FOUND
from project_amber.db import db
from project_amber.errors import NotFound
from project_amber.models.task import Task

def addTask(text: str, uid: int, **kwargs) -> int:
    """
    Creates a new task. Returns its ID.
    """
    status = 0
    if "status" in kwargs:
        status = kwargs["status"]
    task = Task(owner=uid, text=text, creation_time=time(), \
        last_mod_time=time(), status=status)
    db.session.add(task)
    db.session.commit()
    return task.id

def getTask(task_id: int, uid: int) -> Task:
    """
    Returns an instance of `Task`, given the ID and the owner UID.
    """
    task = db.session.query(Task).filter_by(id=task_id, owner=uid).one_or_none()
    if task is None:
        raise NotFound(MSG_TASK_NOT_FOUND)
    return task

def getTasks(uid: int, text: str = None) -> list:
    """
    Returns a list containing tasks from a certain user. If the second
    parameter is specified, this will return the tasks that have this text in
    their description (`text in Task.text`).
    """
    req = db.session.query(Task).filter_by(owner=uid)
    if text is None:
        return req.all()
    return req.filter(text in Task.text).all()

def updateTask(task_id: int, uid: int, **kwargs) -> int:
    """
    Updates the task details. Returns its ID.
    """
    task = getTask(task_id, uid)
    if "text" in kwargs and not kwargs["text"] is None:
        task.text = kwargs["text"]
    if "status" in kwargs and not kwargs["status"] is None:
        task.status = kwargs["status"]
    task.last_mod_time = time()
    db.session.commit()
    return task_id

def removeTask(task_id: int, uid: int) -> int:
    """
    Removes a task. Returns its ID on success.
    """
    task = getTask(task_id, uid)
    db.session.delete(task)
    db.session.commit()
    return task_id
