from tracemalloc import start
import pandas as pd
import numpy as np
import glob
from threading import Thread
from pandas import DataFrame
from datetime import datetime

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
        print(glob.glob(self.dir))
        return glob.glob(self.dir)
    
    def convert_local_files_to_sql(self, files: list, index: int = 0, process_result_array: list = []) -> DataFrame:
        '''
            Pick a lot of CSV file and make the ingestion process
        '''
        if index >= len(files):
            self.status["review"] = "Process Finished"
            
            now = datetime.now()
            self.status["lead_time"] = str(now - self.status["start_time"])
            self.status["start_time"] = self.status["start_time"].strftime("%m/%d/%Y, %H:%M:%S")
            self.status["end_time"] = now.strftime("%m/%d/%Y, %H:%M:%S")

            return "Process Finished"
        else:
            df_process_result = self.convert_csv_to_sql(files[index])
            self.status["details"].append(df_process_result)
            return self.convert_local_files_to_sql(files, index + 1, process_result_array)
    
    def convert_csv_to_sql(self, file: str) -> DataFrame:
        '''
            Transform dataframe in SQL table using batch process
        '''
        start_time = datetime.now()
        len_file = np.zeros(1)
        threads = []
        self.status["review"] = f"{file}: In progress.."
        try:
            for chunk_df in pd.read_csv(file, chunksize=1000000):
                t = Thread(target=self.process_data, args=(chunk_df,))
                threads.append(t)
                t.start()
                len_file = np.append(len_file, chunk_df.shape[0])
                if len(threads) == 10:
                    for t in threads:
                        t.join()

            if len(threads) > 0: 
                for t in threads:
                    t.join()
            end_time = datetime.now()
            return {"file": file,
                    "lead_time": str(end_time - start_time),
                    "result": "Successful Data Ingestion",
                    "num_rows": np.sum(len_file)}
        except:
            return {"file": file,
                    "result": "Fail during Data Ingestion"}
    
    def process_data(self, df: DataFrame) -> DataFrame:
        def make_point_tuple(record):
            ''' 
                Transform "POINT (123, 456)" to "123, 456".
                The tuple structure is easier to make some manipulation than first format.
            '''
            record = record.lstrip("POINT ")
            first_coord = record[(record.find("(")+1):(record.find(" ")-1)]
            last_coord = record[(record.find(" ")+1):(record.find(")")-1)]
            tuple_point = str(first_coord) + "," + str(last_coord)
            return tuple_point
        
        df.datetime = pd.to_datetime(df.datetime)
        df.origin_coord = df.origin_coord.apply(make_point_tuple).str.split(",")
        df.destination_coord = df.destination_coord.apply(make_point_tuple).str.split(",")
        
        # Split array column into multiple columns pandas
        df_origin_coords = df.origin_coord.apply(pd.Series)
        df_origin_coords.columns = ["origin_coord_point_x", "origin_coord_point_y"]
        df_destination_coords = df.destination_coord.apply(pd.Series)
        df_destination_coords.columns = ["destination_coord_point_x", "destination_coord_point_y"]
        df = pd.concat([df, df_origin_coords, df_destination_coords], axis=1)

        # Remove unnecessary columns
        df.drop(columns=["origin_coord", "destination_coord"],
                inplace=True)
        
        # Send dataframe to SQL table
        df.to_sql("vehicles_records", self.conf["ENGINE"], if_exists="append", index=True, index_label='id')

    def start(self):
        '''
            Start the data ingestion process
        '''
        now = datetime.now()
        self.status["start_time"] = now
        self.status["review"] = "Data Ingestion in Progress."
        self.convert_local_files_to_sql(self.pick_local_files())

    def get_status(self):
        '''
            Get status attribute with information about the data ingestion process
        '''
        return self.status