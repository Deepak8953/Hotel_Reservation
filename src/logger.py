import logging
import os
from datetime import datetime

# create a logs directory to store all logs
LOGS_DIR='logs'
os.makedirs(LOGS_DIR, exist_ok=True)

# We want separate log file for each day, say we are running today, so all logs will appended in a log file named log_2026-04-28.log
LOG_FILE_PATH = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

logging.basicConfig(

    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO

)

# format means in what format we want logs to be written in logs file. 
# for logging we have 3 levels ERROR, WARNING, INFO. On specifying level as logging.INFO it will log all logs of INFO and above.

# this function is used to initialize our logger in different files, Run test.py as demo, it will create a log file in logs folder
def get_logger(name):
    
    # create a logger by the given 'name'
    logger=logging.getLogger(name)
    logger.setLevel(logging.INFO)
    return logger


