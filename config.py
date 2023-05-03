from orjson import loads, dumps

from os.path import isfile

if isfile("config.json"):
    with open("config.json") as config_file:
        config = loads(config_file.read())
else:
    config = {
        "token": input("Token >"),
        "adb": input("ADB Host >")
    }

TOKEN = config.get("token")
HOST_NAME = config.get("adb")
