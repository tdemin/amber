from json import dumps

from flask import Flask, request

from project_amber.config import config
from project_amber.db import db
from project_amber.errors import HTTPError
from project_amber.helpers import handleLogin, middleware as checkRequest
from project_amber.handlers.auth import login, logout
from project_amber.handlers.session import handle_session_req, \
    handle_session_id_req
from project_amber.handlers.task import handle_task_id_request, \
    handle_task_request
from project_amber.handlers.users import signup

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config["database"]
db.init_app(app)

@app.before_request
def middleware():
    params = checkRequest()
    if params.authenticated:
        user = handleLogin()
        # add a global variable that every function will use from now on
        request.user = user

app.add_url_rule("/api/login", "login", login, methods=["POST"])
app.add_url_rule("/api/logout", "logout", logout, methods=["POST"])
app.add_url_rule("/api/task", "task", handle_task_request, \
    methods=["GET", "POST"])
app.add_url_rule("/api/task/<task_id>", "task_id", handle_task_id_request, \
    methods=["GET", "PATCH", "DELETE"])
app.add_url_rule("/api/session", "session", handle_session_req, methods=["GET"])
app.add_url_rule("/api/session/<session_id>", "session_id", \
    handle_session_id_req, methods=["GET", "DELETE"])

if config["allow_signup"]:
    app.add_url_rule("/api/signup", "signup", signup, methods=["POST"])

@app.before_first_request
def create_tables():
    db.create_all() # create all tables on first run

@app.errorhandler(HTTPError)
def handle_HTTP_errors(e):
    return dumps({
        "message": e.message
    }), e.code
