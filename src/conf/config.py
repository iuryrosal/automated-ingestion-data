import os
from src.data.database import Database

def config_variables():
  config = {}

  # Env variables of postgresql database
  config["POSTGRES_USER"] = os.getenv("POSTGRES_USER", "root")
  config["POSTGRES_PASSWORD"] = os.getenv("POSTGRES_PASSWORD", "password")
  config["POSTGRES_HOST"] = os.getenv("POSTGRES_HOST", "localhost")
  config["POSTGRES_PORT"] = os.getenv("POSTGRES_PORT", 5432)
  config["POSTGRES_DB"] = os.getenv("POSTGRES_DB", "data_vehicles")
  database = Database(config_dict=config)
  config["CONN_STR"] = database.get_conn_att()["CONN_STR"]

  return config