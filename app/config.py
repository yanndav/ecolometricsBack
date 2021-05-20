from os import environ
from dotenv import load_dotenv

class Config():
    load_dotenv()
    SECRET_KEY = environ.get("SECRET_KEY")
    DEBUG = environ.get("DEBUG")
    ENV = environ.get("FLASK_ENV")
    # SERVER_NAME = environ.get("SERVER_NAME")
    MONGO_URI = environ.get("MONGO_URI")
    MAIL_SERVER = environ.get("MAIL_SERVER")
    MAIL_PORT = environ.get("MAIL_PORT")
    MAIL_USE_SSL = environ.get("MAIL_USE_SSL")
    MAIL_USERNAME = environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = environ.get("MAIL_PASSWORD")
    MAIL_DEBUG = environ.get("MAIL_DEBUG")