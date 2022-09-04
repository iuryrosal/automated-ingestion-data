from sqlalchemy import create_engine
import pandas as pd

class Database:
  def __init__(self, config_dict: dict) -> None:
    self.conf = config_dict
    self.connection_attr = self.connect_db()
  
  def build_conn_str(self):
        if self.conf["ENV"] != "local":
    return (f"postgresql+psycopg2://{self.conf['POSTGRES_USER']}:" + 
            f"{self.conf['POSTGRES_PASSWORD']}@" +
            f"{self.conf['POSTGRES_HOST']}:" +
            f"{self.conf['POSTGRES_PORT']}/" +
                    f"{self.conf['POSTGRES_DB']}")
        else:
            return "sqlite://"

  def create_engine_db(self, conn_str):
    engine = create_engine(conn_str)
    return engine

  def connect_db(self):
    conn_str = self.build_conn_str()
    engine = self.create_engine_db(conn_str)
    connection = engine.connect()
    return {"CONN_STR": conn_str,
            "ENGINE": engine,
            "CONNECTION": connection}
  
  def get_conn_att(self):
    return self.connection_attr
