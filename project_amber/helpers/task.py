from time import time

from project_amber.const import MSG_TASK_NOT_FOUND
from project_amber.db import db
from project_amber.errors import NotFound
from project_amber.models.task import Task

def addTask(text: str, uid: int) -> int:
    """
    Creates a new task. Returns its ID.
    """
    task = Task(owner=uid, text=text, creation_time=time(), \
        last_mod_time=time())
    db.session.add(task)
    db.session.commit()
    return task.id

def updateTask(new_text: str, task_id: int, uid: int) -> int:
    """
    Updates the task text. Returns its ID.
    """
    task = db.session.query(Task).filter_by(id=task_id, owner=uid).one_or_none()
    if task is None:
        raise NotFound(MSG_TASK_NOT_FOUND)
    task.text = new_text
    task.last_mod_time = time()
    db.session.commit()
    return task_id


def removeTask(task_id: int, uid: int) -> int:
    """
    Removes a task. Returns its ID on success.
    """
    task = db.session.query(Task).filter_by(id=task_id, owner=uid).one_or_none()
    if task is None:
        raise NotFound(MSG_TASK_NOT_FOUND)
    db.session.delete(task)
    db.session.commit()
    return task_id
