from project_amber.app import db

class User(db.Model):
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
    loginTime = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return "<Session token='%s' user='%d' loginTime='%d'>" % \
            self.token, self.user, self.loginTime
