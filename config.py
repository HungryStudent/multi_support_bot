from pydantic import BaseModel
import configparser

config = configparser.ConfigParser()
config.read("settings.ini")
MAIN_BOT_TOKEN = config["settings"]["MAIN_BOT_TOKEN"]
ADMINS = config["settings"]["admins"].split(",")
ADMINS = [int(admin) for admin in ADMINS]
BASE_URL = config["settings"]["BASE_URL"]
WEB_SERVER_HOST = config["settings"]["WEB_SERVER_HOST"]
WEB_SERVER_PORT = int(config["settings"]["WEB_SERVER_PORT"])
MAIN_BOT_PATH = config["settings"]["MAIN_BOT_PATH"]
OTHER_BOTS_PATH = config["settings"]["OTHER_BOTS_PATH"]
OTHER_BOTS_URL = f"{BASE_URL}{OTHER_BOTS_PATH}"


class DB(BaseModel):
    user = config["db"]["user"]
    password = config["db"]["password"]
    database = config["db"]["database"]
    host = config["db"]["host"]
    port = config["db"]["port"]


SQLALCHEMY_DATABASE_URL = "postgresql://{user}:{password}@{host}:{port}/{database}".format(**DB().dict())
