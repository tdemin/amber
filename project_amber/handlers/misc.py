from json import dumps

from project_amber.config import config
from project_amber.const import VERSION
from project_amber.handlers.const import API_VERSION, API_SIGNUP

signup_allowed = False
if config["allow_signup"]: signup_allowed = True


def version():
    return dumps({API_VERSION: VERSION, API_SIGNUP: signup_allowed})
