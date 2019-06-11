from project_amber.db import db

class Task(db.Model):
    """
    Task model. Contains a task ID, the owner, the subject, and the lastmod /
    creation time.
    """
    id = db.Column(db.Integer, primary_key=True)
    owner = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    text = db.Column(db.String(65536)) # TODO: probably subject to increase
    status = db.Column(db.Integer, nullable=False)
    creation_time = db.Column(db.Integer, nullable=False)
    last_mod_time = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return "<Task id='%d' owner='%d' text='%s' status='%d' created='%d'>" \
            % self.id, self.owner, self.text, self.status, self.creation_time
