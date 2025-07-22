from src.logger import get_logger
from src.custom_exception import CustomException
import sys

logger = get_logger(__name__)

def dividing_zero(a,b):
    try:
        result = a/b
        logger.info("Divided the numbers")
        return result
    except Exception as e:
        logger.error("Error occured")
        raise CustomException("Division with zero",sys)
    
if __name__ =="__main__":
    try:
        logger.info("starting the main program")
        dividing_zero(10,0)
    except CustomException as ce:
        logger.error(str(ce))
    finally:
        logger.info("end of Program")
        


