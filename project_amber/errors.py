from http import HTTPStatus

from project_amber.logging import logError

class HTTPError(Exception):
    """
    Base class for all possible errors.
    """
    def __init__(self, code: int, message: str):
        """
        Initialize the error object.
        `code` - HTTP code.
        `message` - Descriptive error message (string).
        """
        self.code = code
        self.message = message
        logError(self.message)
        super(HTTPError, self).__init__()

class BadRequest(HTTPError):
    """
    Exception class for payload data parsing errors.
    """
    code = HTTPStatus.BAD_REQUEST
    def __init__(self, message="Bad request payload"):
        super().__init__(self.code, message)

class InternalServerError(HTTPError):
    """
    Exception class for DB errors. Probably going to be left unused.
    """
    code = HTTPStatus.INTERNAL_SERVER_ERROR
    def __init__(self, message="Internal error"):
        super().__init__(self.code, message)

class NotFound(HTTPError):
    """
    Exception class for entities not found.
    """
    code = HTTPStatus.NOT_FOUND
    def __init__(self, message="Entity not found"):
        super().__init__(self.code, message)

class NoAccess(HTTPError):
    """
    Exception class for restricted access areas.
    """
    code = HTTPStatus.FORBIDDEN
    def __init__(self, message="Forbidden"):
        super().__init__(self.code, message)

class Unauthorized(HTTPError):
    """
    Exception class for login/auth check errors.
    """
    code = HTTPStatus.UNAUTHORIZED
    def __init__(self, message="Unauthorized"):
        super().__init__(self.code, message)
