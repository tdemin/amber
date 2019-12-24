from http import HTTPStatus

from project_amber.logging import warn, error


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
        warn(self.message)
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

    ## pylint: disable=super-init-not-called
    def __init__(self, message="Internal error"):
        error(message)


class NotFound(HTTPError):
    """
    Exception class for entities not found.
    """
    code = HTTPStatus.NOT_FOUND

    def __init__(self, message="Entity not found"):
        super().__init__(self.code, message)


class Forbidden(HTTPError):
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


class Conflict(HTTPError):
    """
    Essentially reverse for HTTP 404: HTTP 409 Conflict. To be used on "entity
    already exists" situations.
    """
    code = HTTPStatus.CONFLICT

    def __init__(self, message="This entity already exists"):
        super().__init__(self.code, message)
