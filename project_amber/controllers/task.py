from typing import List

from project_amber.const import MSG_TASK_NOT_FOUND, MSG_TASK_DANGEROUS, \
    MSG_TEXT_NOT_SPECIFIED
from project_amber.db import db
from project_amber.errors import NotFound, BadRequest
from project_amber.handlers import LoginUser
from project_amber.helpers import time
from project_amber.models.task import Task


class TaskController:
    user: LoginUser = None

    def __init__(self, user: LoginUser):
        self.user = user

    def add_task(self, data: dict) -> int:
        """
        Creates a new task. Returns its ID.
        """
        task = Task(self.user.id, data)
        if task.text is None: raise BadRequest(MSG_TEXT_NOT_SPECIFIED)
        if task.status is None: task.status = 0
        parent_id = task.parent_id
        if parent_id:
            parent = db.session.query(Task).filter_by(id=parent_id,
                                                      owner=self.user.id).one_or_none()
            if parent is None:
                raise NotFound(MSG_TASK_NOT_FOUND)
        task.add()
        db.session.commit()
        self.update_children(task.id)
        # TODO: can we remove the second commit here?
        db.session.commit()
        return task.id

    def get_task(self, task_id: int) -> Task:
        """
        Returns an instance of `Task`, given the ID.
        """
        task = db.session.query(Task).filter_by(id=task_id, owner=self.user.id).one_or_none()
        if task is None:
            raise NotFound(MSG_TASK_NOT_FOUND)
        return task

    def get_tasks(self, text: str = None) -> List[Task]:
        """
        Returns a list containing tasks from a certain user. If the second
        parameter is specified, this will return the tasks that have this text
        in their description (`text in Task.text`).
        """
        req = db.session.query(Task).filter_by(owner=self.user.id)
        if text is None:
            return req.all()
        return req.filter(Task.text.ilike("%{0}%".format(text))).all()

    def update_children(self, task_id: int):
        """
        Recursively updates children lists for the children nodes of
        a task subtree.
        """
        task = self.get_task(task_id)
        if task.parent_id:
            parent = self.get_task(task.parent_id)
            parent_list = parent.getParents()
            parent_list.append(parent.id)
            task.setParents(parent_list)
        else:
            task.setParents(list())
        children = db.session.query(Task).filter_by(parent_id=task_id).all()
        for child in children:
            self.update_children(child.id)

    def update_task(self, task_id: int, data: dict) -> int:
        """
        Updates the task details. Returns its ID.
        """
        task = self.get_task(task_id)
        new_details = Task(self.user.id, data)
        # will drop 404 on a non-existent PID
        # TODO: a little too hackish
        self.get_task(new_details.parent_id)
        task.merge(new_details)
        if not new_details.parent_id is None:
            if new_details.parent_id == 0:
                # promote task to the top level
                task.parent_id = None
                self.update_children(task.id)
            else:
                new_parent = self.get_task(new_details.parent_id)
                if task.id in new_parent.getParents() or task.id == new_parent.id:
                    raise BadRequest(MSG_TASK_DANGEROUS)
                task.parent_id = new_parent.id
                self.update_children(task.id)
        task.last_mod_time = time()
        db.session.commit()
        return task_id

    def remove_task(self, task_id: int) -> List[int]:
        """
        Removes a task, recursively removing its subtasks. Returns the list of
        removed task IDs.
        """
        removed = list()
        children = db.session.query(Task).filter_by(parent_id=task_id).all()
        for child in children:
            removed.extend(self.remove_task(child.id))
        task = self.get_task(task_id)
        task.delete()
        db.session.commit()
        removed.append(task.id)
        return removed
