from time import time as time_lib


def time() -> int:
    """
    Wrapper around `time.time()`. Converts the result to `int` to prevent
    getting fractions of seconds on some platforms.
    """
    return int(time_lib())
