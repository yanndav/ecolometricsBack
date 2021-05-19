from os import environ
from dotenv import load_dotenv

class Config():
    load_dotenv()
    # SECRET_KEY = environ.get("SECRET_KEY")
    DEBUG = environ.get("DEBUG")
    ENV = environ.get("FLASK_ENV")
    # SERVER_NAME = environ.get("SERVER_NAME")
    MONGO_URI = environ.get("MONGO_URI")