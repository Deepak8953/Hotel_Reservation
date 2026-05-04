# In this file we create generic functions, which would be used across the project like read_yaml etc

import os
from src.logger import get_logger
from src.custom_exception import CustomException
import yaml  # in requirement.txt add pyyaml
import pandas as pd

logger=get_logger(__name__)

def read_yaml(file_path):
    """
    Provide file_path of yaml file as argument. 
    Paths are specfied in paths_config.py
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not present in given path") 
        
        with open(file_path, "r") as yaml_file:
            # config variable contain all content of yaml file
            config = yaml.safe_load(yaml_file)
            logger.info("Successfully read yaml file")
            return config
    except Exception as e:
        logger.error("error while reading yaml file")
        raise CustomException("failed reading yaml file", e)
    
# for loading csv file as dataframe
def load_data(path):
    try:
        logger.info('loading data')
        return pd.read_csv(path)
    except Exception as e:
        logger.error(f"error in loading data {e}")
        raise CustomException("failed to load data", e)