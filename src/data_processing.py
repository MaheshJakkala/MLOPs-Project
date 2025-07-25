import os
import pandas as pd
import sys
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *

logger = get_logger(__name__)

class DataProcessor:
    def __init__(self):
         self.data_path = TRAIN_DATA_PATH
         self.processed_data_path = PROCESSED_DATA_PATH
         logger.info("Data Processing started")
    
    def load_data(self):
        try:
            logger.info("Data loading started")
            df = pd.read_csv(self.data_path)
            logger.info(f"Data loading completed successfully: Shape :{df.shape}")
            return df

        except Exception as e:
            logger.error("Problem while loading data")
            raise CustomException("Error while loading Data:",sys)
    
    def drop_unnecessary_columns(self,df,columns):
        try:
            # logger.info(f"All columns: {df.columns}")
            logger.info(f"Dropping unnecessary columns:{columns}")
            df = df.drop(columns = columns,axis=1)
            logger.info(f"Dropped Unnecessary columns successfully: Shape:{df.shape}")
            return df
        
        except Exception as e:
            logger.error("Problem while dropping Unnecessary columns")
            raise CustomException("Error while dropping unncessary columns",sys)
        
    def handle_outliers(self,df,columns):
        try:
            logger.info(f"Handling outliers : Columns = {columns}")
            for column in columns:
                Q1 = df[column].quantile(0.25)
                Q3 = df[column].quantile(0.75)

                IQR = Q3 - Q1
                lower_bond= Q1 + 1.5*IQR
                upper_bond = Q3 - 1.5*IQR
                df[column] = df[column].clip(lower=lower_bond,upper=upper_bond)

            logger.info(f'Outliers Successfully Handled: Shape:{df.shape}')
            return df

        except Exception as e:
            logger.error("Problem while Outliers handling")
            raise CustomException(f"Error while handling outliers: {str(e)}",sys)
    
    def handle_nullvalues(self,df,columns):
        try:
            logger.info("Handling Null Values")
            df[columns] = df[columns].fillna(df[columns].median())
            logger.info(f'Missing values Successfully filled: Shape:{df.shape}')
            return df

        except Exception as e:
            logger.error("Problem while Missing Values handling")
            raise CustomException("Error while handling null values: ",sys)
    def save_data(self,df):
        try:
            os.makedirs(PROCESSED_DIR,exist_ok=True)
            df.to_csv(self.processed_data_path,index=False)
            logger.info('Saved Processed Data Successfully')
        except Exception as e:
            logger.error("Problem while Saving data")
            raise CustomException("Error while Saving Processed data",sys)


    def run(self):
        try:
            logger.info("Starting the pipeline of Data Proccessing")
            df = self.load_data()
            df = self.drop_unnecessary_columns(df,columns=["Unnamed: 0","id"])
            columns_to_handle = ['Flight Distance','Departure Delay in Minutes','Arrival Delay in Minutes', 'Checkin service']
            df = self.handle_outliers(df,columns=columns_to_handle)
            df = self.handle_nullvalues(df,columns='Arrival Delay in Minutes')
            self.save_data(df)

            logger.info(f"Data processing pipeline Successfully Created: Shape{df.shape}")

        except CustomException as ce:
            logger.error(f"Error ocuured in Data Processing Pipleine : {str(ce)}")

if __name__ == "__main__":
    try:
        processor = DataProcessor()
        processor.run()
    except CustomException as ce:
        raise CustomException(str(ce))