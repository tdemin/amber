from project_amber.db import db

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
        if self.gen > 0:
            return True
        return False
