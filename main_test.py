from src.data.database import Database
from src.conf.config import config_variables

config = config_variables()

query_attr = {}
query_attr["dataset"] = "teste"


database = Database(config_dict=config)
conn = database.get_conn_att()["CONNECTION"]
results = conn.execute("""SELECT * FROM information_schema.tables 
                        WHERE table_schema = 'public'""")

results_2 = conn.execute("""SELECT * FROM vehicles_records""")
for record in results_2:
    print("\n", record)