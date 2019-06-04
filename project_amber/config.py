import os
from json import load

if os.name == "posix":
    configPaths = ["./config.json", "/etc/amber.json"]
else:
    configPaths = ["config.json"]

config = {
    "database": "",
    "loglevel": 0
}

# search for every file name and load the config from the first file
# that exists
for testedFileName in configPaths:
    if os.path.isfile(testedFileName):
        # holds the actual config file name
        configFileName = testedFileName
        break
if not "configFileName" in globals():
    print("No configuration file found, exiting")
    exit(1)

try:
    with open(configFileName, encoding="utf8") as configFile:
        # holds the new configuration variables which replace the
        # default ones
        loadedConfig = load(configFile)
except OSError as ioerr:
    print("Could not open config file", configFileName)
    print(ioerr.strerror)
    exit(1)

for entry in config:
    if entry in loadedConfig:
        config[entry] = loadedConfig[entry]
