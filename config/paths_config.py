import os

ARTIFACTS_DIR = "./artifacts"
RAW_DATA_PATH = os.path.join(ARTIFACTS_DIR,'raw','data.csv')
INGESTED_DATA_DIR = os.path.join(ARTIFACTS_DIR,'ingested_data')
TRAIN_DATA_PATH = os.path.join(INGESTED_DATA_DIR,'train.csv')
TEST_DATA_PATH = os.path.join(INGESTED_DATA_DIR,'test.csv')

PROCESSED_DIR = os.path.join(ARTIFACTS_DIR,"processed_data")
PROCESSED_DATA_PATH= os.path.join(PROCESSED_DIR,"processed_data.csv")

ENGINEERED_DIR = os.path.join(ARTIFACTS_DIR,'engineered_data')
ENGINEERED_DATA_PATH = os.path.join(ENGINEERED_DIR,'final_df.csv')

PARAMS_PATH = os.path.join('./config','params.json')
MODEL_SAVE_PATH = os.path.join(ARTIFACTS_DIR,"models",'trained_model.pkl')