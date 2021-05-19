# Packages imports
from flask import Flask
from app.config import Config
from flask_pymongo import PyMongo


# Configuration
mongo = PyMongo()

def create_app(config_class=Config):
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    mongo.init_app(app)

    from app.api.routes import api
    app.register_blueprint(api)

    return(app)