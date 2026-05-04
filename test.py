from src.logger import get_logger
from src.custom_exception import CustomException
import sys


# # test logger.py
# logger is created by the name logger
# logger=get_logger(__name__)

# logger.info('hello')


# # test custom_exception.py
# logger=get_logger(__name__)

# def divide_number(a, b):
#     try:
#         logger.info("Dividing 2 numbers")
#         result=a/b
        
#         return result
#     except Exception as e:
#         logger.error("Error accured")
#         raise CustomException("Custom error zero", sys)
        
    

# if __name__=="__main__":
#     try:
#         logger.info("start main")
#         divide_number(10, 0)
#     except CustomException as ce:
#         logger.error(str(ce))
        