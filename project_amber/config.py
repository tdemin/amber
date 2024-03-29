import os
import sys
from json import load

class Config:
    database: str = ""
    loglevel: int = 0
    allow_signup: bool = False
    domain: str = "*"

config = Config()

configPaths = ["config.json"]
if os.name == "posix":
    configPaths.append("/etc/amber.json")

# search for every file name and load the config from the first file that exists
for testedFileName in configPaths:
    if os.path.isfile(testedFileName):
        # holds the actual config file name
        configFileName = testedFileName
        break
if not "configFileName" in globals():
    print("No configuration file found, exiting")
    sys.exit(1)

try:
    with open(configFileName, encoding="utf8") as configFile:
        # holds the new configuration variables which replace the
        # default ones
        loadedConfig = load(configFile)
except OSError as ioerr:
    print("Could not open config file", configFileName)
    print(ioerr.strerror)
    sys.exit(1)

for entry in dir(config):
    if entry in loadedConfig and not entry.startswith("__"):
        setattr(config, entry, loadedConfig[entry])


def string_to_bool(val: str) -> bool:
    """
    Converts a string containing a bool value to Python's bool. Serves as a
    helper in configuration code.
    """
    if val == "1" or val.lower() == "true":
        return True
    if val == "0" or val.lower() == "false":
        return False
    return False


# override config with environment variables in need, the first element of a
# tuple is the environment variable itself, the second is the corresponding
# `config` key, and the third one is the function to convert the possible values
for mapping in (
        ("AMBER_DATABASE", "database", lambda val: val),  # str -> str
        # pylint: disable=unnecessary-lambda
        ("AMBER_LOGLEVEL", "loglevel", lambda val: int(val)),  # str -> int
        ("AMBER_ALLOW_SIGNUP", "allow_signup", string_to_bool),  # str -> bool
        ("AMBER_DOMAIN", "domain", lambda val: val)  # str -> str
):
    env_value = os.getenv(mapping[0])
    if not env_value is None:
        setattr(config, mapping[1], mapping[2](env_value))

if not config.database:
    print("No database specified. Exiting.")
    sys.exit(1)
