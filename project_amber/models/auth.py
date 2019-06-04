from project_amber.app import db

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
    token = db.Column(db.String(256), primary_key=True)
    user = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    login_time = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return "<Session token='%s' user='%d' login_time='%d'>" % \
            self.token, self.user, self.login_time
