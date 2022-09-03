import pandas as pd
import glob

from pandas import DataFrame

class MakeDataframe:
    def __init__(self, direc: str) -> None:
        self.dir = direc

    def __pick_local_files(self) -> list:
        '''
            Make a list of files in some directory
        '''
        return glob.glob(self.dir)
    
    def __convert_local_files_to_df(self, files: list, index: int = 0, df_array: list = []) -> DataFrame:
        def convert_csv_to_dataframe(file: str) -> DataFrame:
            '''
                Convert CSV file to Pandas Dataframe
                using chucksize to improve performance
                for big files.
            '''
            chunks = pd.read_csv(file, chunksize=100000)
            pd_df = pd.concat(chunks)
            return pd_df

        if index >= len(files):
            return pd.concat(df_array, axis = 0)
        else:
            df_temp = convert_csv_to_dataframe(files[index])

            df_array.append(df_temp)
            return self.__convert_local_files_to_df(files, index + 1, df_array)

    def __extract_data(self) -> DataFrame:
        return self.__convert_local_files_to_df(self.__pick_local_files())
    
    def __transform_data(self, df: DataFrame) -> DataFrame:
        def make_point_tuple(record):
            ''' 
                Transform "POINT (123, 456)" to tuple "(123, 456)".
                The tuple structure is easier to make some manipulation than first format.
            '''
            record = record.lstrip("POINT ")
            first_coord = record[(record.find("(")+1):(record.find(" ")-1)]
            last_coord = record[(record.find(" ")+1):(record.find(")")-1)]
            tuple_point = (first_coord, last_coord)
            return tuple_point
        
        df.datetime = pd.to_datetime(df.datetime)
        df.origin_coord = df.origin_coord.apply(make_point_tuple)
        df.destination_coord = df.destination_coord.apply(make_point_tuple)
        df.rename(columns={"origin_coord": "origin_coord_point",
                           "destination_coord": "destination_coord_point"},
                  inplace=True)
        return df
    
    def build(self):
        return self.__transform_data(
                    self.__extract_data()
                )