from threading import Thread
from src import ingestion_process, logging

# abort functions
from src.utils.api_abort import abort_with_error


def post_routes(app):
    @app.route("/vehicles", methods=["POST"])
    def start_ingest_data():
        '''
            Start ingestion process with CSVs file in data/raw.
            This process will append new data in dataset.
        '''
        try:
            Thread(target=ingestion_process.start).start()
            return "Ingestion Started"
        except Exception as e:
            logging.error(str(e))
            abort_with_error()
