from typing import List

from flask import request

from project_amber.const import MSG_TASK_NOT_FOUND, MSG_TASK_DANGEROUS, \
    MSG_TEXT_NOT_SPECIFIED
from project_amber.db import db
from project_amber.errors import NotFound, BadRequest
from project_amber.helpers import time
from project_amber.models.task import Task


def addTask(data: dict) -> int:
    """
    Creates a new task. Returns its ID.
    """
    task = Task(request.user.id, data)
    if task.text is None: raise BadRequest(MSG_TEXT_NOT_SPECIFIED)
    if task.status is None: task.status = 0
    parent_id = task.parent_id
    if parent_id:
        parent = db.session.query(Task)\
            .filter_by(id=parent_id, owner=request.user.id).one_or_none()
        if parent is None:
            raise NotFound(MSG_TASK_NOT_FOUND)
    task.add()
    db.session.commit()
    updateChildren(task.id)
    # TODO: can we remove the second commit here?
    db.session.commit()
    return task.id


def getTask(task_id: int) -> Task:
    """
    Returns an instance of `Task`, given the ID. Only returns tasks to
    their owner.
    """
    task = db.session.query(Task).filter_by(id=task_id,
                                            owner=request.user.id).one_or_none()
    if task is None: raise NotFound(MSG_TASK_NOT_FOUND)
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
    Updates children lists for the children nodes of a task subtree. This is
    an expensive recursive operation.
    """
    task = getTask(task_id)
    if task.parent_id:
        parent = getTask(task.parent_id)
        parent_list = parent.getParents()
        parent_list.append(parent.id)
        task.setParents(parent_list)
    else:
        task.setParents(list())
    children = db.session.query(Task).filter_by(parent_id=task_id).all()
    for child in children:
        updateChildren(child.id)


def updateTask(task_id: int, data: dict) -> int:
    """
    Updates the task details. Returns its ID.
    """
    task = getTask(task_id)
    new_details = Task(request.user.id, data)
    task.merge(new_details)
    if not new_details.parent_id is None:
        if new_details.parent_id == 0:
            # promote task to the top level
            task.parent_id = None
            updateChildren(task.id)
        else:
            new_parent = getTask(new_details.parent_id)
            if task.id in new_parent.getParents() or task.id == new_parent.id:
                raise BadRequest(MSG_TASK_DANGEROUS)
            task.parent_id = new_parent.id
            updateChildren(task.id)
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
    task.delete()
    db.session.commit()
    return task_id
