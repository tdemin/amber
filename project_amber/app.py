from json import dumps

from flask import Flask

from project_amber.config import config
from project_amber.db import db
from project_amber.errors import HTTPError
from project_amber.handlers.auth import login, logout, login_check
from project_amber.handlers.users import signup

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config["database"]
db.init_app(app)

app.add_url_rule("/api/login", "login", login, methods=["POST"])
app.add_url_rule("/api/logout", "logout", logout, methods=["POST"])
app.add_url_rule("/api/login_check", "login_check", login_check, methods=["GET"])
app.add_url_rule("/api/signup", "signup", signup, methods=["POST"])

@app.before_first_request
def create_tables():
    db.create_all() # create all tables on first run

@app.errorhandler(HTTPError)
def handle_HTTP_errors(e):
    return dumps({
        "message": e.message
    }), e.code
