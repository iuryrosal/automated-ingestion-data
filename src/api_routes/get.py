from src import logging, ingestion_process
from src.models.vehicle import *
from src.utils.api_abort import *
from src.utils.api_utils import *
from src.models.vehicle import Vehicle

def get_routes(app):
  @app.route("/vehicles/ingest-data/status", methods=["GET"])
  def get_status_ingest_data():
    '''
      Get status of process' data ingestion.
    '''
    try:
      return ingestion_process.get_status()
    except Exception as e:
      logging.error(str(e))
      abort_with_error()

  @app.route("/vehicles/<id>", methods=["GET"])
  def get_item(id):
    '''
      Get specific vehicle record by specific (id).
    '''
    abort_get_item_if_id_not_exist(id)
    try:
      item = Vehicle.query.get(id)
      del item.__dict__["_sa_instance_state"]
      return item.__dict__
    except Exception as e:
      logging.error(str(e))
      abort_with_error()

  @app.route("/vehicles", methods=["GET"])
  def get_items():
    '''
      Get all vehicles records in dataset with query parameters.
    '''
    try:
      query_params = get_query_params()
      query_str = "SELECT * FROM vehicles_records"
      query_str = build_where_expr(query_str, query_params)
      query_str = build_limit_expr(query_str, query_params)
      results = database.engine.execute(query_str)
      return {"data": [{key: value for (key, value) in results.items()} for results in results]}
    except Exception as e:
      logging.error(str(e))
      abort_with_error()

  @app.route("/vehicles/<column>/count", methods=["GET"])
  def get_freq_items(column):
    '''
      Get count of elements by specif (column) in dataset.
    '''
    abort_get_freq_items_by_not_valid_column(column)
    try:
      query_str = f"SELECT {column}, COUNT({column}) FROM vehicles_records GROUP BY {column}"
      results = database.engine.execute(query_str)
      return {"data": [{key: value for (key, value) in results.items()} for results in results]}
    except Exception as e:
      logging.error(str(e))
      abort_with_error()

  @app.route("/vehicles/weekly_trips/region", methods=["GET"])
  def get_weekly_trips_by_region():
    '''
      Get count of elements per week (using datetime column) and region.
    '''
    try:
      query_str = f"""SELECT EXTRACT(WEEK FROM datetime)::integer as week_number,
                        region,
                        COUNT(*) AS freq_trip
                      FROM vehicles_records
                      GROUP BY EXTRACT(WEEK FROM datetime), region
                      ORDER BY EXTRACT(WEEK FROM datetime), region"""
      results = database.engine.execute(query_str)
      return {"data": [{key: value for (key, value) in results.items()} for results in results]}
    except Exception as e:
      logging.error(str(e))
      abort_with_error()

  @app.route("/vehicles/weekly_avg_trips/region", methods=["GET"])
  def get_weekly_avg_trips_by_region():
    '''
      Get average of elements per week (using datetime column) and region.
    '''
    try:
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
    except Exception as e:
      logging.error(str(e))
      abort_with_error()
