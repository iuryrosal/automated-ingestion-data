from src.utils.api_factory import create_app, init_database
from src.conf.config import config_variables
from src.data.ingestion_process import IngestionProcess

import logging

format_log = ("%(asctime)s :: %(levelname)s "
              ":: %(filename)s :: %(lineno)d "
              ":: %(message)s")
logging.basicConfig(filename="api.log",
                    level=logging.DEBUG,
                    format=format_log)

logging.info("Loading app config...")
config = config_variables()
app = create_app(config)
database = init_database(app)
ingestion_process = IngestionProcess("data/raw/*.csv", config)
logging.info("App config loaded.")
