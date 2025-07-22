from utils.helpers import *

import json
import joblib
import mlflow
import mlflow.sklearn
import lightgbm as lgm
from sklearn.model_selection import train_test_split,GridSearchCV
from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,confusion_matrix

class ModelTrainer:
    def __init__(self,data_path,params_path,model_save_path,experiment_name="Model_Training_Environment"):
        self.data_path =data_path
        self.model_save_path = model_save_path
        self.params_path = params_path
        self.experiment_name = experiment_name

        self.best_model = None
        self.metrics = None
    
    def load_data(self):
        try:
            logger.info("Loading data")
            data = pd.read_csv(self.data_path)
            logger.info("Data Successfully Loaded")
            return data
        except Exception as e:
            logger.error(f"Problem while loading data:{e}")
            raise CustomException("Error while loading data",sys)
    
    def split_data(self,data):
        try:
            logger.info("Splitting Data")
            X = data.drop(columns='satisfaction')
            y = data['satisfaction']

            X_train,X_test,y_train,y_test= train_test_split(X,y,test_size=0.2,random_state=42)
            logger.info("Data splitted Successfully")
            return X_train,X_test,y_train,y_test

        except Exception as e:
            logger.error(f"Problem while splitting data:{e}")
            raise CustomException("Error while splitting data",sys)
        
    def train_model(self,X_train,y_train,params):
        try:
            logger.info("Model training Started")
            lgbm = lgm.LGBMClassifier()

            grid_search = GridSearchCV(lgbm,cv=3,param_grid=params,scoring='accuracy')
            grid_search.fit(X_train,y_train)

            self.best_model = grid_search.best_estimator_
            logger.info(f"Best model : {self.best_model}\t Trained Successfully")
            return grid_search.best_params_
        except Exception as e:
            logger.error(f"Problem while splitting data:{e}")
            raise CustomException("Error while splitting data",sys)
    
    def evaluate_model(self,X_test,y_test):
        try:
            y_preds = self.best_model.predict(X_test)

            accuracy = accuracy_score(y_pred=y_preds,y_true=y_test)
            precision = precision_score(y_pred=y_preds,y_true=y_test,average='weighted',zero_division=0)
            recall = recall_score(y_pred=y_preds,y_true=y_test,average='weighted',zero_division=0)
            f1 = f1_score(y_pred=y_preds,y_true=y_test,average='weighted',zero_division=0)

            self.metrics ={
                'accuracy' : accuracy,
                'precision' : precision,
                'recall' : recall,
                'f1_score':f1,
                "confusion_matrix":confusion_matrix(y_pred=y_preds,y_true=y_test).tolist()
            }

            logger.info(f"Evaluation metrics: {self.metrics}")

            return self.metrics
        except Exception as e:
            logger.error(f"Problem while evaluating model:{e}")
            raise CustomException("Error while evaluating model",sys)

    def save_model(self):
        try:
            logger.info("Saving model")
            os.makedirs(os.path.dirname(self.model_save_path),exist_ok=True)
            joblib.dump(self.best_model,self.model_save_path)

            logger.info("Model Successfully Saved!")
        except Exception as e:
            logger.error(f"Problem while Saving model:{e}")
            raise CustomException("Error while Saving model",sys)
    
    def run(self):
        try:
            logger.info("Model training Started")
            mlflow.set_experiment(self.experiment_name)
            with mlflow.start_run():

                data = self.load_data()
                X_train,X_test,y_train,y_test = self.split_data(data)

                with open(self.params_path,'r') as f:
                    params = json.load(f)

                logger.info(f"Loaded Hyperparameters: {params}")
                mlflow.log_params({f"grid_{key}": value for key,value in params.items()})

                best_params = self.train_model(X_train,y_train,params)

                logger.info(f"Best Hyperparameters: {best_params}")
                mlflow.log_params({f"best_{key}":value for key,value in best_params.items()})

                metrics = self.evaluate_model(X_test,y_test)

                for metric,value in metrics.items():
                    if metric!='confusion_matrix':
                        mlflow.log_metric(metric,value)

                self.save_model()
                mlflow.sklearn.log_model(self.best_model,'model')
        
        except CustomException as ce:
            logger.error(str(ce))
            mlflow.end_run(status="FAILED")

if __name__=="__main__":
    trainer = ModelTrainer(ENGINEERED_DATA_PATH,params_path=PARAMS_PATH,model_save_path=MODEL_SAVE_PATH)
    trainer.run()

        
