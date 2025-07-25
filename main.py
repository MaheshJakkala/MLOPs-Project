from src.custom_exception import CustomException
from src.data_ingestion import DataIngestion
from src.data_processing import DataProcessor
from src.feature_engineering import FeatureEngineer
# from src.model_selection import ModelSelector
from src.model_training import ModelTrainer

from utils.helpers import *
from config.paths_config import *

if __name__ =="__main__":
    try:
        logger.info("Full pipeline Starting")
        #ingestion of data
        ingestion= DataIngestion(raw_data_path=RAW_DATA_PATH,ingested_data_dir=INGESTED_DATA_DIR)
        ingestion.create_ingestion_dir()
        ingestion.split_data(train_path=TRAIN_DATA_PATH,test_path=TEST_DATA_PATH)

        #data processing
        processor = DataProcessor()
        processor.run()

        #feature engineering
        engineer = FeatureEngineer()
        engineer.run()

        # #model selection
        # model_selection = ModelSelector(ENGINEERED_DATA_PATH)
        # model_selection.run()

        #model training
        trainer = ModelTrainer(ENGINEERED_DATA_PATH,params_path=PARAMS_PATH,model_save_path=MODEL_SAVE_PATH)
        trainer.run()
        
        logger.info("Full pipeline Successfully Completed")

    except Exception as ce:
        raise CustomException(str(ce),sys)