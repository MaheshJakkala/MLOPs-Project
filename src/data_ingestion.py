import os
import sys
import pandas as pd
from config.paths_config import *
from src.logger import get_logger


from src.custom_exception import CustomException
# import pandas
from sklearn.model_selection import train_test_split

logger = get_logger(__name__)

class DataIngestion:
    def __init__(self,raw_data_path,ingested_data_dir):
        self.raw_data_path = raw_data_path
        self.ingested_data_dir = ingested_data_dir
        logger.info("Data Ingestion started")
    
    def create_ingestion_dir(self):
        try:
            os.makedirs(self.ingested_data_dir,exist_ok= True)

            logger.info("Directory for Ingestion Created ! ")

        except Exception as e:
            raise CustomException("Error while creating directory:{e}",sys)
        
    def split_data(self,train_path,test_path,test_size=0.2,random_state=42):
        try:
            data = pd.read_csv(self.raw_data_path)
            logger.info("Raw data loaded successfully!")

            train_data,test_data = train_test_split(data,test_size=test_size,random_state=random_state)
            logger.info("Data splitted succefully! ")

            train_data.to_csv(train_path,index=False)
            test_data.to_csv(test_path,index=False)
            logger.info("Training and Testing data saved successfully")

        except Exception as e:
            raise CustomException("Error while while splitting data: {e}",sys)
    

if __name__ == "__main__":
    try:
        ingestion= DataIngestion(raw_data_path=RAW_DATA_PATH,ingested_data_dir=INGESTED_DATA_DIR)
        ingestion.create_ingestion_dir()
        ingestion.split_data(train_path=TRAIN_DATA_PATH,test_path=TEST_DATA_PATH)

    except Exception as ce:
        raise CustomException(str(ce),sys)
        