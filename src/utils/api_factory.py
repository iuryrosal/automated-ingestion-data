from src.models.vehicle import database
from flask import Flask


def create_app(config: dict) -> Flask:
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = config["CONN_STR"]
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.app_context().push()
    return app


def init_database(app: Flask):
    database.init_app(app)
    database.create_all()
    database.session.commit()
    return database
