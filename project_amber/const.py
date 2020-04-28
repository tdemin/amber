from json import dumps

EMPTY_RESP = dumps({})  # Empty response, to be used in requests.

AUTH_TOKEN_HEADER = "Authorization"
AUTH_TOKEN_SCHEME = "Bearer"

DAY_SECONDS = 60 * 60 * 24
MATURE_SESSION = DAY_SECONDS * 2  # The difference in times between the login
# time and the time when a session is considered "mature" (e.g can remove other
# sessions).

MSG_INVALID_JSON = "Payload needs to contain valid JSON"
MSG_MISSING_AUTH_INFO = "Missing 'username' or 'password'"
MSG_NO_TOKEN = f"No {AUTH_TOKEN_HEADER} header present"
MSG_INVALID_TOKEN = "Invalid token"
MSG_USER_NOT_FOUND = "This user does not exist"
MSG_USER_EXISTS = "The user with this name already exists"
MSG_IMMATURE_SESSION = "This session is too new, and cannot remove others"
MSG_SIGNUP_FORBIDDEN = "Signup is disabled on this server"

MSG_TASK_NOT_FOUND = "This task does not exist"
MSG_TEXT_NOT_SPECIFIED = "No text specified"
MSG_TASK_DANGEROUS = "Potentially dangerous operation"

VERSION = "0.0.5"
