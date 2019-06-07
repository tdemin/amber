from http import HTTPStatus

from project_amber.logging import logError

# TODO: remake these into Werkzeug exceptions

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
    message = "Bad request"
    def __init__(self):
        super().__init__(self.code, self.message)

class InternalServerError(HTTPError):
    """
    Exception class for DB errors. Probably going to be left unused.
    """
    code = HTTPStatus.INTERNAL_SERVER_ERROR
    message = "Internal server error"
    def __init__(self):
        super().__init__(self.code, self.message)

class NotFound(HTTPError):
    """
    Exception class for entities not found.
    """
    code = HTTPStatus.NOT_FOUND
    message = "Resource not found"
    def __init__(self):
        super().__init__(self.code, self.message)

class NoAccess(HTTPError):
    """
    Exception class for restricted access areas.
    """
    code = HTTPStatus.FORBIDDEN
    message = "Access denied"
    def __init__(self):
        super().__init__(self.code, self.message)

class Unauthorized(HTTPError):
    """
    Exception class for login/auth check errors.
    """
    code = HTTPStatus.UNAUTHORIZED
    message = "Unauthorized"
    def __init__(self):
        super().__init__(self.code, self.message)
