import os
import pandas as pd
from google.cloud import storage
from sklearn.model_selection import train_test_split
from src.logger import get_logger
from src.custom_exception import CustomException
from config.paths_config import *
from utils.common_functions import read_yaml

logger=get_logger(__name__)

class DataIngestion:
    # so the argument to constructor config represent config.yaml and by config['data_ingestion'] we choose configuration of data ingestion part
    def __init__(self, config):
        self.config=config['data_ingestion']
        self.bucket_name = self.config['bucket_name']
        self.file_name = self.config['bucket_file_name']
        self.train_test_ratio = self.config['train_ratio']

        # next we want to create raw directory under artifacts
        os.makedirs(RAW_DIR, exist_ok = True)

        logger.info(f"data ingestion started with {self.bucket_name} and file is {self.file_name}")
    
    def download_csv_from_gcp(self):
        try:
            client = storage.Client
            bucket = client.bucket(self.bucket_name)
            blob = bucket.blob(self.file_name)

            blob.download_to_filename(RAW_FILE_PATH)

            logger.info(f"csv file successfully downloaded to {RAW_FILE_PATH}")
        
        except Exception as e:
            logger.error("error while downloading the csv file")
            raise CustomException('failed to download csv', e)
        
    # Now we have downloaded the data from bucket to raw directory. Next split the data into train and test

    def split_data(self):
        try:
            logger.info("starting the splitting process")
            data = pd.read_csv(RAW_FILE_PATH)
            
            train_data, test_data=train_test_split(data, test_size=1-self.train_test_ratio, random_state=42)

            # finally save the train_data, test_data into artifacts dir
            train_data.to_csv(TRAIN_FILE_PATH)
            test_data.to_csv(TEST_FILE_PATH)
            logger.info(f"train_data saved to {TRAIN_FILE_PATH} and test_data saved to {TEST_FILE_PATH}")

        except Exception as e:
            logger.error("error while splitting data")
            raise CustomException('failed to split data into train and test sets', e)
        
# reason to create run method to keep code less complex I have called intermediate finctions inside run() then down below in the main() only run is called.
# Notice I have commented call to download_csv_from_gcp(), since I have not configured GCP yet, I have directly, placed a file raw.csv inside raw folder
    def run(self): 
        try:
            logger.info("starting data ingestion process") 
            #self.download_csv_from_gcp()  
            self.split_data()

            logger.info('data ingestion completed successfully')
        
        except CustomException as ce:
            logger.error(f"CustomException : {str(ce)}")
            
        finally:

            logger.info("data ingestion completed")

# Now we want to run data ingestion file using python src/data_ingestion.py

if __name__=="__main__":

    data_ingestion_obj = DataIngestion(read_yaml(CONFIG_PATH))

    data_ingestion_obj.run()

        



                        

        