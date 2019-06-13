from project_amber.const import MSG_TASK_NOT_FOUND, MSG_TASK_DANGEROUS
from project_amber.db import db
from project_amber.errors import NotFound, BadRequest
from project_amber.helpers import time
from project_amber.models.task import Task

def addTask(text: str, status: int, uid: int) -> int:
    """
    Creates a new task. Returns its ID.
    """
    task_time = time()
    task = Task(owner=uid, text=text, creation_time=task_time, \
        last_mod_time=task_time, status=status, gen=0)
    db.session.add(task)
    db.session.commit()
    return task.id

def getTask(task_id: int, uid: int = None) -> Task:
    """
    Returns an instance of `Task`, given the ID and the owner UID. If the UID
    is `None`, returns the instance no matter who the owner is.
    """
    task_query = db.session.query(Task).filter_by(id=task_id)
    if not uid is None:
        task = task_query.filter_by(owner=uid).one_or_none()
    else:
        task = task_query.one_or_none()
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
    return req.filter(Task.text.ilike("%{0}%".format(text))).all()

def updateChildren(task_id: int):
    """
    Updates generations for the children nodes of a task subtree. This is a very
    expensive recursive operation.
    """
    task = getTask(task_id, None)
    if not task.parent_id is None:
        parent = getTask(task.parent_id, None)
        task.gen = parent.gen + 1
    else:
        task.gen = 0
    children = db.session.query(Task).filter_by(parent_id=task_id).all()
    for child in children:
        updateChildren(child.id)

def updateTask(task_id: int, uid: int, **kwargs) -> int:
    """
    Updates the task details. Returns its ID.
    """
    task = getTask(task_id, uid)
    if "text" in kwargs and not kwargs["text"] is None:
        task.text = kwargs["text"]
    if "status" in kwargs and not kwargs["status"] is None:
        task.status = kwargs["status"]
    if "parent_id" in kwargs and not kwargs["parent_id"] is None:
        # TODO: we limit changing parent IDs to prevent circular deps,
        # can this be done better?
        new_parent = getTask(kwargs["parent_id"], uid)
        if new_parent.gen > task.gen:
            raise BadRequest(MSG_TASK_DANGEROUS)
        task.parent_id = new_parent.id
        updateChildren(task.id)
    task.last_mod_time = time()
    db.session.commit()
    return task_id

def removeTask(task_id: int, uid: int) -> int:
    """
    Removes a task. Returns its ID on success. Removes all children as well. Is
    recursive, and so is expensive.
    """
    children = db.session.query(Task).filter_by(parent_id=task_id).all()
    for child in children:
        removeTask(child.id, uid)
    task = getTask(task_id, uid)
    db.session.delete(task)
    db.session.commit()
    return task_id
