from json import dumps

EMPTY_RESP = dumps({}) # Empty response, to be used in requests.

MSG_NO_TOKEN = "No X-Auth-Token present"
MSG_INVALID_TOKEN = "Invalid token"
MSG_USER_NOT_FOUND = "This user does not exist"

MSG_TASK_NOT_FOUND = "This task does not exist"
