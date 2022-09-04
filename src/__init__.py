from flask import Flask
from src.conf.config import config_variables
from src.data.ingestion_process import IngestionProcess
from src.models.vehicle import *
import logging

logging.basicConfig(filename="api.log",
                    level=logging.DEBUG,
                    format="%(asctime)s :: %(levelname)s :: %(filename)s :: %(lineno)d :: %(message)s")

logging.info("Loading app config...")
config = config_variables()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = config["CONN_STR"]
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.app_context().push()
database.init_app(app)
database.create_all()
database.session.commit()
ingestion_process = IngestionProcess("data/raw/*.csv", config)
logging.info("App config loaded.")
