from json import dumps

EMPTY_RESP = dumps({}) # Empty response, to be used in requests.

DAY_SECONDS = 60 * 60 * 24
MATURE_SESSION = DAY_SECONDS * 2 # The difference in times between the login
# time and the time when a session is considered "mature" (e.g can remove other
# sessions).

MSG_NO_TOKEN = "No X-Auth-Token present"
MSG_INVALID_TOKEN = "Invalid token"
MSG_USER_NOT_FOUND = "This user does not exist"
MSG_USER_EXISTS = "The user with this name already exists"
MSG_IMMATURE_SESSION = "This session is too new, and cannot remove others"

MSG_TASK_NOT_FOUND = "This task does not exist"
MSG_TEXT_NOT_SPECIFIED = "No text specified"
