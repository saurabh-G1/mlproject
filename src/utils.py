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
from sklearn.metrics import r2_score 
from sklearn.model_selection import GridSearchCV

from src.exception import CustomException 

def save_object(file_path,obj):
    try: 
        dir_path=os.path.dirname(file_path)
        
        os.makedirs(dir_path, exist_ok=True) 
        
        with open(file_path, "wb") as file_obj:
            dill.dump(obj, file_obj)
            
    except Exception as e:
        raise CustomException(e,sys)  
    
    
def evaluate_models(X_train,y_train,X_test,y_test,models,param):
    try:
        report ={}
        
        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]] 
            
            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train) 
            
            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train) 

            
           # model.fit(X_train, y_train)  #Train model
            
            y_train_pred = model.predict(X_train)
            
            y_test_pred = model.predict(X_test)
            
            train_model_score=r2_score(y_train,y_train_pred) 
            
            test_model_score = r2_score(y_test,y_test_pred)
            
            report[list(models.keys())[i]] = test_model_score 
            
        return report 
    
    except Exception as e:
        raise CustomException(e,sys) 
    
            