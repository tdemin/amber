from typing import List

from flask import request

from project_amber.const import MSG_TASK_NOT_FOUND, MSG_TASK_DANGEROUS
from project_amber.db import db
from project_amber.errors import NotFound, BadRequest
from project_amber.helpers import time
from project_amber.models.task import Task

def addTask(text: str, status: int, parent_id: int, deadline: int = None, \
    reminder: int = None) -> int:
    """
    Creates a new task. Returns its ID.
    """
    task_time = time()
    gen = 0
    # FIXME: dirty, and is really supposed to be fixed at another level
    if parent_id == 0:
        parent_id = None
    if not parent_id is None:
        parent = db.session.query(Task)\
            .filter_by(id=parent_id, owner=request.user.id).one_or_none()
        if parent is None:
            raise NotFound(MSG_TASK_NOT_FOUND)
        gen = parent.gen + 1
    task = Task(owner=request.user.id, text=text, creation_time=task_time, \
        last_mod_time=task_time, status=status, parent_id=parent_id, gen=gen, \
        deadline=deadline, reminder=reminder)
    db.session.add(task)
    db.session.commit()
    return task.id

def getTask(task_id: int) -> Task:
    """
    Returns an instance of `Task`, given the ID. Only returns tasks to
    their owner.
    """
    task_query = db.session.query(Task).filter_by(id=task_id)
    task = task_query.filter_by(owner=request.user.id).one_or_none()
    if task is None:
        raise NotFound(MSG_TASK_NOT_FOUND)
    return task

def getTasks(text: str = None) -> List[Task]:
    """
    Returns a list containing tasks from a certain user. If the second
    parameter is specified, this will return the tasks that have this text in
    their description (`text in Task.text`).
    """
    req = db.session.query(Task).filter_by(owner=request.user.id)
    if text is None:
        return req.all()
    return req.filter(Task.text.ilike("%{0}%".format(text))).all()

def updateChildren(task_id: int):
    """
    Updates generations for the children nodes of a task subtree. This is a very
    expensive recursive operation.
    """
    task = getTask(task_id)
    if not task.parent_id is None:
        parent = getTask(task.parent_id)
        task.gen = parent.gen + 1
    else:
        task.gen = 0
    children = db.session.query(Task).filter_by(parent_id=task_id).all()
    for child in children:
        updateChildren(child.id)

def updateTask(task_id: int, **kwargs) -> int:
    """
    Updates the task details. Returns its ID.
    """
    task = getTask(task_id)
    if "text" in kwargs and not kwargs["text"] is None:
        task.text = kwargs["text"]
    if "status" in kwargs and not kwargs["status"] is None:
        task.status = kwargs["status"]
    if "parent_id" in kwargs and not kwargs["parent_id"] is None:
        if kwargs["parent_id"] == 0:
            # promote task to the top level
            task.parent_id = None
            updateChildren(task.id)
        else:
            # TODO: we limit changing parent IDs to prevent circular deps,
            # can this be done better?
            new_parent = getTask(kwargs["parent_id"])
            if new_parent.gen > task.gen and task.is_child():
                raise BadRequest(MSG_TASK_DANGEROUS)
            task.parent_id = new_parent.id
            updateChildren(task.id)
    if "deadline" in kwargs and not kwargs["deadline"] is None:
        task.deadline = kwargs["deadline"]
    if "reminder" in kwargs and not kwargs["reminder"] is None:
        task.reminder = kwargs["reminder"]
    task.last_mod_time = time()
    db.session.commit()
    return task_id

def removeTask(task_id: int) -> int:
    """
    Removes a task. Returns its ID on success. Removes all children as well. Is
    recursive, and so is expensive.
    """
    children = db.session.query(Task).filter_by(parent_id=task_id).all()
    for child in children:
        removeTask(child.id)
    task = getTask(task_id)
    db.session.delete(task)
    db.session.commit()
    return task_id
