from project_amber.db import db
from project_amber.handlers.const import API_ID, API_LOGIN_TIME, API_ADDRESS


class User(db.Model):
    """
    Holds the usual user details (username, password). The password is
    hashed with bcrypt and a random salt.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(256))

    def __repr__(self):
        return "<User id='%d' name='%s'>" % self.id, self.name


class Session(db.Model):
    """
    Holds auth session details (auth token, the time of login, etc).
    """
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(256), unique=True, nullable=False)
    user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    login_time = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return "<Session token='%s' user='%d' login_time='%d' ip='%s'>" % \
            self.token, self.user, self.login_time, self.address

    def to_json(self) -> dict:
        """
        Returns a dictionary containing a JSON representation of the session.
        """
        return {API_ID: self.id, API_LOGIN_TIME: self.login_time, API_ADDRESS: self.address}
