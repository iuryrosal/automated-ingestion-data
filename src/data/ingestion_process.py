import pandas as pd
import glob
import multiprocessing as mp
from pandas import DataFrame
from datetime import datetime

class IngestionProcess:
    def __init__(self, direc: str, config: dict) -> None:
        self.dir = direc
        self.conf = config
        self.status = {"review": "Nothing in processing"}

    def pick_local_files(self) -> list:
        '''
            Make a list of files in some directory
        '''
        print(glob.glob(self.dir))
        return glob.glob(self.dir)
    
    def convert_local_files_to_sql(self, files: list, index: int = 0, process_result_array: list = []) -> DataFrame:
        if index >= len(files):
            self.status["review"] = "Process Finished"
            
            now = datetime.now()
            self.status["lead_time"] = str(now - self.status["start_time"])
            self.status["start_time"] = self.status["start_time"].strftime("%m/%d/%Y, %H:%M:%S")
            self.status["end_time"] = now.strftime("%m/%d/%Y, %H:%M:%S")

            return "Process Finished"
        else:
            df_process_result = self.convert_csv_to_sql(files[index])
            return self.convert_local_files_to_sql(files, index + 1, process_result_array)
    
    def convert_csv_to_sql(self, file: str) -> DataFrame:
        mp.Pool(5)
        chunks = pd.read_csv(file, chunksize=1000000)
        for chunk in chunks:
            self.process_data(chunk)
        return "Successful Data Ingestion."
    
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

        df.drop(columns=["origin_coord", "destination_coord"],
                inplace=True)
        print(df.head(1))
        df.to_sql("vehicles_records", self.conf["ENGINE"], if_exists="replace", index=True, index_label='id')

    def start(self):
        now = datetime.now()
        self.status["start_time"] = now
        self.status["review"] = "Data Ingestion in Progress."
        self.convert_local_files_to_sql(self.pick_local_files())

    def get_status(self):
        return self.status