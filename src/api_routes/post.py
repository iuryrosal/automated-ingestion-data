from threading import Thread
from src import ingestion_process, logging
from src.utils.api_abort import *

def post_routes(app):
  @app.route("/vehicles", methods=["POST"])
  def start_ingest_data():
    try:
      Thread(target=ingestion_process.start).start()
      return "Ingestion Started"
    except Exception as e:
      logging.error(str(e))
      abort_with_error()