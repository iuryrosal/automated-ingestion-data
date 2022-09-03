from flask import Flask, request
import json

from src.models.vehicle import Vehicle
from src import app
from src.models.vehicle import *
from src.data.database import Database
from src.conf.config import config_variables
from src.conf.utils import convert_dumps

config = config_variables()

def get_query_params() -> dict:
  args_dict = {}
  args = ["region"]
  for arg in args:
    args_dict[arg] = request.args.get(arg)
  return args_dict

@app.route("/vehicles", methods=["POST"])
def create_individual_item():
  content_type = request.headers.get("Content-Type")
  if content_type == "application/json":
    req_body = request.get_json()
    vehicle_record = Vehicle(**req_body)
    database.session.add(vehicle_record)
    database.session.commit()
    database.session.refresh(vehicle_record)
    return {"item created": f"/vehicles/{vehicle_record.id}"}
  else:
    return "Content Type Not Supported!"

@app.route("/vehicles/<id>", methods=["GET"])
def get_item(id):
  item = Vehicle.query.get(id)
  del item.__dict__["_sa_instance_state"]
  return item.__dict__

@app.route("/vehicles", methods=["GET"])
def get_items():
  query_params = get_query_params()

  if query_params["region"]:
    results = database.engine.execute(f"""
                                          SELECT * FROM vehicles_records
                                          WHERE region = '{query_params["region"]}'
                                      """)      
  else:
    results = database.engine.execute("SELECT * FROM vehicles_records")
  return {"data": [{key: value for (key, value) in results.items()} for results in results]}
app.run(debug=True)