# Any functionalities that i  am writting in common way which will be used in the entire application,
# that i will say thatas utils.py 

# let's say i want to  read a data from db then i can create my mongo client over here. 
# or i want to save my model over a cloud over here then i can save the code related to that over here. 
#  and then this utils code i will then try to call this code in the components itself.

import sys
import os 
import pandas as pd   
import numpy as np
import dill #used to create the pickle file 

from src.exception import CustomException 

def save_object(file_path,obj):
    try: 
        dir_path=os.path.dirname(file_path)
        
        os.makedirs(dir_path, exist_ok=True) 
        
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
            
    except Exception as e:
        raise CustomException(e,sys)  

