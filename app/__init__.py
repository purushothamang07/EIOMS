from flask import Flask
from .database import db

def create_app():

    app = Flask(__name__)

    app.config["SECRET_KEY"] = "eioms-secret-key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database/reports.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from .routes import main

    app.register_blueprint(main)

    return app