from flask import Flask
from src.conf.config import config_variables
from src.models.vehicle import *

config = config_variables()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config["CONN_STR"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.app_context().push()
database.init_app(app)
database.create_all()
database.session.commit()
ingestion_process = IngestionProcess("data/raw/*.csv", config)
