from json import dumps

from flask import Blueprint

from project_amber.config import config
from project_amber.const import VERSION
from project_amber.handlers.const import API_VERSION, API_SIGNUP

signup_allowed = False
if config["allow_signup"]: signup_allowed = True

misc_handlers = Blueprint("misc_handlers", __name__)


@misc_handlers.route("/version", methods=["GET"])
def version():
    return dumps({API_VERSION: VERSION, API_SIGNUP: signup_allowed})
