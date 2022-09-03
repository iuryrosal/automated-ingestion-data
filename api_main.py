from flask import Flask, request
import json
from threading import Thread

from src.models.vehicle import Vehicle
from src.models.vehicle import *
from src.data.database import Database
from src.conf.config import config_variables
from src.data.ingestion_process import IngestionProcess
from src import app

config = config_variables()
ingestion_process = IngestionProcess("data/raw/*.csv", config)

def get_query_params() -> dict:
  args_dict = {}
  args = ["region", "datasource", "date", "limit",
          "origin_coord_point_x", "origin_coord_point_y",
          "destination_coord_point_x", "destination_coord_point_y"]
  for arg in args:
    args_dict[arg] = request.args.get(arg)
  return args_dict

@app.route("/vehicles", methods=["POST"])
def start_ingest_data():
  Thread(target=ingestion_process.start).start()
  return "Ingestion Started"

@app.route("/vehicles/ingest-data/status", methods=["GET"])
def get_status_ingest_data():
  return ingestion_process.get_status()

@app.route("/vehicles/<id>", methods=["GET"])
def get_item(id):
  item = Vehicle.query.get(id)
  del item.__dict__["_sa_instance_state"]
  return item.__dict__

@app.route("/vehicles", methods=["GET"])
def get_items():
  query_params = get_query_params()
  query_str = "SELECT * FROM vehicles_records"
  where_expr = []

  if query_params["region"]:
    where_expr.append(f"region = '{query_params['region']}'")
  if query_params["datasource"]:
    where_expr.append(f"datasource = '{query_params['datasource']}'")
  if query_params["origin_coord_point_x"]:
    where_expr.append(f"origin_coord_point_x LIKE '{str(query_params['origin_coord_point_x'])}%%'")
  if query_params["origin_coord_point_y"]:
    where_expr.append(f"origin_coord_point_y LIKE '{str(query_params['origin_coord_point_y'])}%%'")
  if query_params["destination_coord_point_x"]:
    where_expr.append(f"destination_coord_point_x LIKE '{str(query_params['destination_coord_point_x'])}%%'")
  if query_params["destination_coord_point_y"]:
    where_expr.append(f"destination_coord_point_y LIKE '{str(query_params['destination_coord_point_y'])}%%'")
  if query_params["date"]:
    where_expr.append(f"datetime::TIMESTAMP::DATE = '{str(query_params['date'])}%%'")

  if len(where_expr) > 0:  # There is where expression
    count = 0
    while count < len(where_expr):
      if count == 0:  # first where condition 
        query_str = query_str + (f" WHERE {where_expr[count]}")        
      else:
        query_str = query_str + (f" AND {where_expr[count]}")
      count += 1
  
  results = database.engine.execute(query_str)
  return {"data": [{key: value for (key, value) in results.items()} for results in results]}

@app.route("/vehicles/<column>/count", methods=["GET"])
def get_freq_items(column):
  query_str = f"SELECT {column}, COUNT({column}) FROM vehicles_records GROUP BY {column}"
  results = database.engine.execute(query_str)
  return {"data": [{key: value for (key, value) in results.items()} for results in results]}

@app.route("/vehicles/weekly_trips/region", methods=["GET"])
def get_weekly_trips_by_region():
  query_str = f"""SELECT EXTRACT(WEEK FROM datetime)::integer as week_number,
                    region,
                    COUNT(*) AS freq_trip
                  FROM vehicles_records
                  GROUP BY EXTRACT(WEEK FROM datetime), region
                  ORDER BY EXTRACT(WEEK FROM datetime), region"""
  results = database.engine.execute(query_str)
  return {"data": [{key: value for (key, value) in results.items()} for results in results]}

@app.route("/vehicles/weekly_avg_trips/region", methods=["GET"])
def get_weekly_avg_trips_by_region():
  query_str = f"""
                  SELECT region, AVG(freq_trip)::VARCHAR(255) AS freq_avg_weekly_trips
                  FROM
                  (
                      SELECT EXTRACT(WEEK FROM datetime)::INTEGER as week_number,
                          region,
                          COUNT(*) AS freq_trip
                      FROM vehicles_records
                      GROUP BY EXTRACT(WEEK FROM datetime), region
                      ORDER BY EXTRACT(WEEK FROM datetime), region) AS weekly_freq_trips
                  GROUP BY region
              """
  results = database.engine.execute(query_str)
  return {"data": [{key: value for (key, value) in results.items()} for results in results]}



app.run(debug=True)