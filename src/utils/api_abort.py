from flask import abort, Response
from src.data.database import Database
from src.models.vehicle import *
import json

def abort_with_error():
  error_message = json.dumps({'Message': 'Something went wrong..'})
  abort(Response(error_message, 400))

def abort_get_item_if_id_not_exist(id):
  query_str = f"SELECT id FROM vehicles_records WHERE id = {id}"
  results = database.engine.execute(query_str)
  id_ = [{key: value for (key, value) in results.items()} for results in results]
  if len(id_) == 0:
    error_message = json.dumps({'Message': 'The id element not exists...'})
    abort(Response(error_message, 400))

def abort_get_freq_items_by_not_valid_column(column):
  if column != "region" and column != "datasource":
    error_message = json.dumps({'Message': f'Column {column} is not valid in this operation.'})
    abort(Response(error_message, 400))