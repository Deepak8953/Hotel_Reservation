import os
import pandas as pd
import joblib
from sklearn.model_selection import RandomizedSearchCV
import lightgbm as lgb
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from config.model_params import *
from utils.common_functions import read_yaml, load_data
from scipy.stats import randint

import mlflow
import mlflow.sklearn

logger = get_logger(__name__)

class ModelTraining:
# note: now path of processed_train.csv and processed_test.csv will be our train_path and test_path
    def __init__(self, train_path, test_path, model_output_path):
        self.train_path=train_path
        self.test_path=test_path
        self.model_output_path=model_output_path

        self.params_dist = LIGHTGBM_PARAMS
        self.random_search_params = RANDOM_SEARCH_PARAMS
    
    def load_and_split_data(self):

        try:

            logger.info(f'loading data from {self.train_path}')
            train_df = load_data(self.train_path)

            logger.info(f'loading data from {self.test_path}')
            test_df = load_data(self.test_path)

            X_train = train_df.drop(columns=["booking_status"])
            y_train = train_df["booking_status"]

            X_test = test_df.drop(columns=["booking_status"])
            y_test = test_df["booking_status"]

            logger.info('Data spliting successful for model training')

            return X_train, y_train, X_test, y_test
        
        except Exception as e:
            logger.error("Error while loading data {e}")
            raise CustomException('failed to load data', e)
        
    def train_lgbm(self, X_train, y_train):
        try:
             logger.info('Initializing our model')
             lgbm_model = lgb.LGBMClassifier(random_state=self.random_search_params['random_state'])
             logger.info("starting hyperparameter tuning")
             random_search = RandomizedSearchCV(
                 
                estimator=lgbm_model, 
                param_distributions=self.params_dist,
                n_iter=self.random_search_params['n_iter'],
                cv=self.random_search_params['cv'],
                n_jobs=self.random_search_params['n_jobs'],
                verbose=self.random_search_params['verbose'],
                scoring=self.random_search_params['scoring'],
                )
             logger.info("Starting our Hyperparameter tuning")
             random_search.fit(X_train, y_train)

             logger.info("Hyperparameter tuning completed")
             best_params=random_search.best_params_
             best_lgbm_model = random_search.best_estimator_

             logger.info(f"best parameters are {best_params}")
             return best_lgbm_model
        
        except Exception as e:
            logger.error("Error while training model {e}")
            raise CustomException('failed to train model', e)
        
    def evaluate_model(self, model, X_test, y_test):
        try:
            logger.info("Evaluating our Model")
            
            y_pred = model.predict(X_test)
            
            accuracy = accuracy_score(y_test, y_pred)
            precision = precision_score(y_test, y_pred)
            recall = recall_score(y_test, y_pred)
            f1 = f1_score(y_test, y_pred)
            
            logger.info(f"Accuracy Score : {accuracy}")
            logger.info(f"Precision Score : {precision}")
            logger.info(f"Recall Score : {recall}")
            logger.info(f"F1 Score : {f1}")
            
            return {
                "accuracy": accuracy,
                "precision": precision,
                "recall": recall,
                "f1": f1
            }
        
        except Exception as e:
            logger.error(f"Error while evaluating model: {e}")
            raise CustomException("Failed to evaluate model", e)
    
    def save_model(self, model):
        try:
            os.makedirs(os.path.dirname(self.model_output_path), exist_ok=True)
            logger.info("Saving the model")
            joblib.dump(model, self.model_output_path)
            logger.info(f"Model saved to {self.model_output_path}")
             
        except Exception as e:
            logger.error(f"Error while saving the model: {e}")
            raise CustomException("Failed to save the model", e)
    
    def run(self):
        try:
            with mlflow.start_run():
                logger.info("Start Model training pipeline")
                
                logger.info("Starting MLFlow Experimentation")
                
                logger.info("Logging the training and testing dataset to MLFlow")
                # we want to log our dataset, so that we know which data was used to train this model
                # Inside mlflow folder named datasets will be created where both path will be stored
                mlflow.log_artifact(self.train_path, artifact_path='datasets')
                mlflow.log_artifact(self.test_path, artifact_path='datasets')
                
                X_train, y_train, X_test, y_test = self.load_and_split_data()
                best_lgbm_model = self.train_lgbm(X_train, y_train)
                metrics = self.evaluate_model(best_lgbm_model, X_test, y_test)
                self.save_model(best_lgbm_model)
                
                logger.info("Logging the model into MLFlow")
                
                mlflow.log_artifact(self.model_output_path)
                
                logger.info("Logging Params and Metrics into MLFlow")
                mlflow.log_params(best_lgbm_model.get_params())
                mlflow.log_metrics(metrics)
                
                logger.info("Model Training Successful")
            
        except Exception as e:
            logger.error(f"Error in model training pipeline {e}")
            raise CustomException("Error in model training pipeline", e)
      
   
     

if __name__ == "__main__":
    trainer = ModelTraining(train_path=PROCESSED_TRAIN_DATA_PATH,
                           test_path=PROCESSED_TEST_DATA_PATH,
                           model_output_path=MODEL_OUTPUT_PATH)
    trainer.run()

