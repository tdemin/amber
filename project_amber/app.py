from json import dumps

from flask import Flask
from flask_cors import CORS

from project_amber.config import config
from project_amber.db import db
from project_amber.errors import HTTPError
from project_amber.handlers.const import API_V0
from project_amber.handlers.auth import auth_handlers as auth
from project_amber.handlers.session import session_handlers as session
from project_amber.handlers.misc import misc_handlers as misc
from project_amber.handlers.task import task_handlers as task
from project_amber.handlers.users import user_handlers as user

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config.database
db.init_app(app)
CORS(app, resources={r"/*": {"origins": config.domain}})

for blueprint in (auth, session, misc, task, user):
    app.register_blueprint(blueprint, url_prefix=API_V0)


@app.before_first_request
def create_tables():
    db.create_all()  # create all tables on first run


@app.errorhandler(HTTPError)
def handle_HTTP_errors(e):
    return dumps({"message": e.message}), e.code
