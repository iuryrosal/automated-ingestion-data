import pandas as pd
import numpy as np
import glob
from threading import Thread
from queue import Queue
from pandas import DataFrame
from datetime import datetime
import logging


class IngestWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self) -> None:
        while True:
            engine, dataframe = self.queue.get()
            try:
                process_data(engine, dataframe)
            finally:
                self.queue.task_done()


class IngestionProcess:
    def __init__(self, direc: str, config: dict) -> None:
        self.dir = direc
        self.conf = config
        self.status = {"review": "Nothing in processing",
                       "details": []}

    def pick_local_files(self) -> list:
        '''
            Make a list of files in directory (dir object attribute)
        '''
        logging.debug("Detect files: " + str(self.dir))
        return glob.glob(self.dir)

    def convert_local_files_to_sql(self, queue,
                                   files: list,
                                   index: int = 0) -> DataFrame:
        '''
            Pick a all CSVs files and make the ingestion process
        '''

        try:
            if index >= len(files):
                self.status["review"] = "Process Finished"
                now = datetime.now()
                self.status["lead_time"] = str(now - self.status["start_time"])
                self.status["start_time"] = (self
                                             .status["start_time"]
                                             .strftime("%m/%d/%Y, %H:%M:%S"))
                self.status["end_time"] = now.strftime("%m/%d/%Y, %H:%M:%S")
                logging.debug(f"""Process Finished.
                              Lead time: {self.status['lead_time']}""")
                return "Process Finished"
            else:
                logging.debug(f"{files[index]} in progress...")
                self.status["review"] = f"{files[index]}: In progress.."
                df_process_result = (self
                                     .convert_csv_to_sql(queue, files[index]))
                self.status["details"].append(df_process_result)
                logging.debug(f"{files[index]} Finished.")
                return self.convert_local_files_to_sql(queue, files, index + 1)
        except Exception as e:
            logging.error(str(e))

    def convert_csv_to_sql(self, queue, file: str) -> DataFrame:
        '''
            Transform dataframe in SQL table using batch process
        '''
        start_time = datetime.now()
        len_file = np.zeros(1)
        try:
            for chunk_df in pd.read_csv(file, chunksize=100000):
                logging.info('Queueing {}'.format(str(chunk_df.shape)))
                queue.put((self.conf["ENGINE"], chunk_df))
                len_file = np.append(len_file, chunk_df.shape[0])
            queue.join()
            end_time = datetime.now()
            return {"file": file,
                    "lead_time": str(end_time - start_time),
                    "result": "Successful Data Ingestion",
                    "num_rows": np.sum(len_file)}
        except Exception as e:
            logging.error(str(e))
            return {"file": file,
                    "result": "Fail during Data Ingestion"}

    def start(self):
        '''
            Start the data ingestion process
        '''
        now = datetime.now()
        self.status["start_time"] = now
        self.status["review"] = "Data Ingestion in Progress."
        queue = Queue()
        logging.info("Loading workers...")
        for x in range(10):
            worker = IngestWorker(queue)
            worker.daemon = True
            worker.start()
        self.convert_local_files_to_sql(queue, self.pick_local_files())

    def get_status(self):
        '''
            Get status attribute with information
            about the data ingestion process
        '''
        return self.status


def process_data(engine, df: DataFrame) -> DataFrame:
    def make_point_tuple(record):
        '''
            Transform "POINT (123, 456)" to "123, 456".
            The tuple structure is easier to make some
            manipulation than first format.
        '''
        record = record.lstrip("POINT ")
        first_coord = record[(record.find("(")+1):(record.find(" ")-1)]
        last_coord = record[(record.find(" ")+1):(record.find(")")-1)]
        tuple_point = str(first_coord) + "," + str(last_coord)
        return tuple_point
    df.datetime = pd.to_datetime(df.datetime)
    df.origin_coord = df.origin_coord.apply(make_point_tuple).str.split(",")
    df.destination_coord = (df.destination_coord
                            .apply(make_point_tuple)
                            .str.split(","))

    # Split array column into multiple columns pandas
    df_origin_coords = df.origin_coord.apply(pd.Series)
    df_origin_coords.columns = ["origin_coord_point_x", "origin_coord_point_y"]
    df_destination_coords = df.destination_coord.apply(pd.Series)
    df_destination_coords.columns = ["destination_coord_point_x",
                                     "destination_coord_point_y"]
    df = pd.concat([df, df_origin_coords, df_destination_coords], axis=1)

    # Remove unnecessary columns
    df.drop(columns=["origin_coord", "destination_coord"],
            inplace=True)

    # Send dataframe to SQL table
    df.to_sql("vehicles_records", engine,
              if_exists="append",
              index=True,
              index_label='id')
