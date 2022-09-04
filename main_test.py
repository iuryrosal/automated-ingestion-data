from src.data.database import Database
from src.conf.config import config_variables
from src.data.ingestion_process import IngestionProcess


config = config_variables()

query_attr = {}
query_attr["dataset"] = "teste"

ing = IngestionProcess("data/raw/*.csv", config)
#ing.start()
print("processo iniciado")

database = Database(config_dict=config)
conn = database.get_conn_att()["CONNECTION"]
results_2 = conn.execute("""
                            SELECT * FROM vehicles_records
                        """)
for record in results_2:
    print("\n", record)