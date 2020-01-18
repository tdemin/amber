from typing import List

from project_amber.db import db
from project_amber.errors import BadRequest
from project_amber.handlers.const import API_ID, API_TEXT, API_STATUS, \
    API_LASTMOD, API_PID, API_DEADLINE, API_REMINDER
from project_amber.helpers import time

SEPARATOR = ","


class Task(db.Model):
    """
    Task model. Contains a task ID, the owner, the subject, and the lastmod /
    creation time.
    """
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    text = db.Column(db.String(65536))
    parent_id = db.Column(db.Integer, db.ForeignKey("task.id"))
    status = db.Column(db.Integer, nullable=False)
    creation_time = db.Column(db.BigInteger, nullable=False)
    last_mod_time = db.Column(db.BigInteger, nullable=False)
    deadline = db.Column(db.BigInteger)
    reminder = db.Column(db.BigInteger)
    parents = db.Column(db.String(2048), nullable=False)

    def isChild(self) -> bool:
        """
        Helper method. Simply checks whether the task is of gen 0 or not.
        """
        if self.gen > 0: return True
        return False

    def toDict(self) -> dict:
        """
        Helper method that converts public task data (ID, text, PID, status,
        modtime, deadline and reminders) to a dict that can be safely used in
        JSON serialization. Returns the resulting dict.
        """
        result = {
            API_ID: self.id,
            API_TEXT: self.text,
            API_STATUS: self.status,
            API_LASTMOD: self.last_mod_time
        }
        if self.parent_id: result[API_PID] = self.parent_id
        if self.deadline: result[API_DEADLINE] = self.deadline
        if self.reminder: result[API_REMINDER] = self.reminder
        return result

    def merge(self, task: "Task"):
        """
        Copies public data from another task.

        Does not update task generations; this has to be done manually.
        """
        for i in ("parent_id", "text", "status", "reminder", "deadline"):
            new_value = getattr(task, i)
            if new_value is not None:
                setattr(self, i, new_value)

    def __init__(self, owner: int, data: dict = None):
        if not isinstance(data, dict): raise BadRequest
        self.text = data.get(API_TEXT)
        self.status = data.get(API_STATUS)
        self.creation_time = time()
        self.last_mod_time = self.creation_time
        self.parent_id = data.get(API_PID)
        # SQLite is fine with 0 in foreign key, Postgres isn't,
        # and this needs a workaround
        if self.parent_id == 0: self.parent_id = None
        self.deadline = data.get(API_DEADLINE)
        self.reminder = data.get(API_REMINDER)
        self.parents = ""
        self.owner = owner

    def add(self):
        """
        Adds the task to the database. Wraps SQLAlchemy's `db.session.add()`
        """
        db.session.add(self)

    def delete(self):
        """
        Removes the task from the database. Wraps SQLAlchemy's `db.session.delete()`
        """
        db.session.delete(self)

    def getParents(self) -> List[int]:
        """
        Retrieves a list of connected parent IDs that have a higher tree level.
        The list is deserialized from a string contained in the database.
        """
        if len(self.parents) == 0:
            return list()
        return list(map(lambda x: int(x), self.parents.split(SEPARATOR)))

    def setParents(self, pids: List[int]) -> str:
        """
        Serializes the provided list of connected parent IDs that have a higher
        tree level into a string. Returns the resulting string.
        """
        pids_str = map(lambda x: str(x), pids)
        self.parents = SEPARATOR.join(pids_str)
        return self.parents
