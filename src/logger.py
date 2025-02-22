# for logging purpose 
import logging 
import os 
from datetime import datetime 

# naming convention for the log file which will be created 

LOG_FILE=f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log" #this is the file name of the log
#file which will be created 
logs_path=os.path.join(os.getcwd(),"logs",LOG_FILE) 
os.makedirs(logs_path,exist_ok=True) 

LOG_FILE_PATH=os.path.join(logs_path,LOG_FILE)  

logging.basicConfig(
    filename=LOG_FILE_PATH, 
    format="[%(asctime)s] %(lineno)d %(name)s -%(levelname)s - %(message)s",
    level=logging.INFO,
)   


# Done in 267
# if __name__=="__main__": 
#     logging.info("Logging has started")
    












