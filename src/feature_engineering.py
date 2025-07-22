from utils.helpers import *
from sklearn.feature_selection import mutual_info_classif
# import os
# import sys
# from src.logger import get_logger
# from src.custom_exception import CustomException
# from config.paths_config import *
# from sklearn.preprocessing import LabelEncoder
# import pandas as pd

logger = get_logger(__name__)

class FeatureEngineer:
    def __init__(self):
        self.data_path = PROCESSED_DATA_PATH
        self.df = None
        self.label_mapping = {}

    def load_data(self):
        try:
            logger.info("Data loading started")
            self.df = pd.read_csv(self.data_path)
            logger.info("Data loaded Successfully")

        except Exception as e:
            logger.error(f"Problem while loading data: {e}")
            raise CustomException("Error while loading data: ",sys)
        
    def feature_construction(self):
        try:
            logger.info("Starting Feature Construction")
            self.df['Total Delay'] = self.df["Arrival Delay in Minutes"] + self.df["Departure Delay in Minutes"]
            self.df['Delay Ratio'] = self.df['Total Delay'] / (self.df['Flight Distance'] +1)
            logger.info(f"Feature Construction completed Successfully: features:{['Total Delay','Delay Ratio']}")
        except Exception as e:
            logger.error(f"Problem while Constructing Feature: {e}")
            raise CustomException("Error while constructing Features: ",sys)
    
    def label_encoding(self):
        try:
            col_to_encode = ["Gender","Customer Type","Type of Travel","Class","satisfaction","Age Group"]
            logger.info(f"Performing label encoding on coloumns: {col_to_encode}")
            self.df,self.label_mapping = label_encode(self.df,columns=col_to_encode)
            
            for col,mapping in self.label_mapping.items():
                logger.info(f"Mapping for {col}: {mapping}")
            logger.info(f"Label Encoding Successfully completed")
        except Exception as e:
            logger.error(f"Problem while Label Encoding: {e}")
            raise CustomException("Error while Encoding Labels: ",sys)
        
    def bins_age(self):
        try:
            logger.info("Starting Binning of Age Column")
            self.df["Age Group"] = pd.cut(self.df["Age"],bins=[10,18,30,50,100],labels=["Child","Youngstar","Adult","Senior"])
            logger.info("Binning of Age Column Successfully Completed")
        except Exception as e:
            logger.error(f"Problem while Binning: {e}")
            raise CustomException("Error while Binning: ",sys)
    
    def feature_selection(self):
        try:
            logger.info("FE started")
            X = self.df.drop(columns=["satisfaction"])
            Y =self.df["satisfaction"]

            X_train,X_test,Y_train,Y_test = train_test_split(X,Y,test_size=0.2,random_state=42)

            logger.info(f"Y_train shape: {Y_train.shape} ")
            mutual_info = mutual_info_classif(X=X_train,y=Y_train,discrete_features=True)
            mutual_info_df = pd.DataFrame(data=
                            {"Features":X.columns,
                             "Mutual Information":mutual_info}
            ).sort_values(by="Mutual Information",ascending=False)
            
            logger.info(f"Mutual information table: \n{mutual_info_df}")

            top_features = mutual_info_df.head(12)["Features"].to_list()
            self.df = self.df[top_features+["satisfaction"]]

            logger.info(f"Feature Selection completed Successfully")

        except Exception as e:
            logger.error(f"Problem in Feature selection: {e}")
            raise CustomException("Error while Selecting Features: ",sys)
    
    def save_data(self):
        try:
            logger.info("Saving data")
            os.makedirs(ENGINEERED_DIR,exist_ok=True)
            self.df.to_csv(ENGINEERED_DATA_PATH,index=False)
            logger.info("Engineered Data Saved Successfully")
        except Exception as e:
            logger.error(f"Problem while saving data: {e}")
            raise CustomException("Error while Saving Data: ",sys)
    
    def run(self):
        try:
            logger.info("FE pipeline setup started")
            self.load_data()
            self.feature_construction()
            self.bins_age()
            self.label_encoding()
            self.feature_selection()
            self.save_data()
            logger.info("FE pipeline setup Successfully Completed")
        
        except Exception as e:
            logger.error(f"Problem in FE pipeline setup: {e}")
            raise CustomException("Error while FE pipeline setup: ",sys)


if __name__ == "__main__":
    engineer = FeatureEngineer()
    engineer.run()