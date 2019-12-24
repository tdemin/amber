from json import dumps

from project_amber.const import VERSION
from project_amber.handlers.const import API_VERSION


def version():
    return dumps({API_VERSION: VERSION})
