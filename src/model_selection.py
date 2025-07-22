from utils.helpers import *

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier,AdaBoostClassifier,GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
import xgboost as xgb
import lightgbm as lgb

from sklearn.metrics import accuracy_score,precision_score,recall_score,f1_score,confusion_matrix

from torch.utils.tensorboard import SummaryWriter

class ModelSelector:
    def __init__(self,data_path):
        self.data_path = data_path
        run_id = time.strftime("%Y%m%d - %H%M%S")
        self.writer = SummaryWriter(log_dir=f"tensorboard_logs/run_{run_id}")
        self.results = {}
        self.models = {
            "Logistic Regression":LogisticRegression(),
            "SVC" : SVC(),
            "Decistion Tree Classifier": DecisionTreeClassifier(),
            "Random Forest Classifier" : RandomForestClassifier(n_estimators=50,n_jobs=-1),
            "AdaBoost Classifier" : AdaBoostClassifier(n_estimators=50),
            "Gradient Boosting Classifier" : GradientBoostingClassifier(n_estimators=50),
            "XGBoost" : xgb.XGBClassifier(eval_metric='mlogloss'),
            "LightGBM" : lgb.LGBMClassifier(),
            "KNeighbors" : KNeighborsClassifier(),
            "Naive Bayes" : GaussianNB()
        }

    def load_data(self):
        try:
            df = pd.read_csv(self.data_path)
            fra =0.1
            df_sample = df.sample(frac=fra, random_state=42)
            
            X = df.drop(columns='satisfaction')
            y = df['satisfaction']

            logger.info(f"loaded {fra*100}% data and sampled successfully")
            return X,y

        except Exception as e:
            logger.error(f"problem while loading data :{e}")
            raise CustomException("Error while loading data",sys)
    
    def split_data(self,X,y):
        try:
            logger.info("Splitting Data")
            return train_test_split(X,y,test_size=0.2,random_state=42)
        
        except Exception as e:
            logger.error(f"problem while splitting data :{e}")
            raise CustomException("Error while splitting data",sys)
    
    def log_confusion_matrix(self , y_true , y_pred , step , model_name):
        cm = confusion_matrix(y_true,y_pred)

        fig , ax = plt.subplots(figsize=(5,5))
        ax.matshow(cm , cmap=plt.cm.Blues , alpha=0.7)

        for i in range(cm.shape[0]):
            for j in range(cm.shape[1]):
                ax.text(x=j,y=i,s=cm[i,j] , va="center" ,ha="center")
        
        plt.xlabel("Predicted Labels")
        plt.ylabel("True/Actual Labels")
        plt.title(f"Confusion matrix for {model_name}")

        self.writer.add_figure(f"Confusion_Matrix/{model_name}" , fig , global_step=step)
        plt.close(fig)


    def train_and_evaluate(self,X_train,X_test,y_train,y_test):
        try:
            logger.info("Model training  and evaluation started")
            for idx, (name,model) in enumerate(self.models.items()):
                try:
                    model.fit(X_train,y_train)
                    y_pred = model.predict(X_test)

                    accuracy = accuracy_score(y_pred=y_pred,y_true=y_test)
                    precision = precision_score(y_pred=y_pred,y_true=y_test,average="weighted",zero_division=0)
                    recall = recall_score(y_pred=y_pred,y_true=y_test,average="weighted",zero_division=0)
                    f1 = f1_score(y_pred=y_pred,y_true=y_test,average='weighted',zero_division=0)

                    self.results[name] = {
                        'accuracy':accuracy,
                        'precision':precision,
                        'recall' : recall,
                        'f1_score':f1
                    }

                    logger.info(f"{name} model trained Successfully\t"
                                f"Metrics: Accuracy:{accuracy}, Precision :{precision}, Recall: {recall}, F1_Score: {f1}")
                    self.writer.add_scalar(f"Accuracy/{name}", accuracy, idx)
                    self.writer.add_scalar(f"Precision/{name}", precision, idx)
                    self.writer.add_scalar(f"Recall/{name}", recall, idx)
                    self.writer.add_scalar(f"F1_Score/{name}", f1, idx)

                    self.writer.add_text(f"Model Details/{name} ", f"Name : {name}" f"Metrics: Accuracy: {accuracy}, Precision: {precision}, Recall: {recall}, F1_Score: {f1}",global_step=idx)

                    self.log_confusion_matrix(y_test,y_pred,idx,name)
                except Exception as e:
                    logger.error(f"Error training model {name}: {e}")

            self.writer.close()

        except Exception as e:
            logger.error("Problem while training and evaluating Models")
            raise CustomException("Error while training and evaluating",sys)
        
    def run(self):
        try:
            logger.info("Model Selection Pipeline Started")
            X,y = self.load_data()
            X_train,X_test,Y_train,Y_test = self.split_data(X,y)
            self.train_and_evaluate(X_train,X_test,Y_train,Y_test)

            logger.info("Model Selection Pipeline completed Successfully")

        except Exception as e:
            logger.error("Problem in Model Selection Pipeline")
            raise CustomException("Error occured in Model Selection Pipeline",sys)
    
if __name__=="__main__":
    model_selection = ModelSelector(ENGINEERED_DATA_PATH)
    model_selection.run()

                
                
