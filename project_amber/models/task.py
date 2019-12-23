from project_amber.db import db
from project_amber.handlers.const import API_ID, API_TEXT, API_STATUS, \
    API_LASTMOD, API_PID, API_DEADLINE, API_REMINDER


class Task(db.Model):
    """
    Task model. Contains a task ID, the owner, the subject, and the lastmod /
    creation time.
    """
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    text = db.Column(db.String(65536))
    gen = db.Column(db.Integer, nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey("task.id"))
    status = db.Column(db.Integer, nullable=False)
    creation_time = db.Column(db.Integer, nullable=False)
    last_mod_time = db.Column(db.Integer, nullable=False)
    deadline = db.Column(db.Integer)
    reminder = db.Column(db.Integer)

    def is_child(self) -> bool:
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
