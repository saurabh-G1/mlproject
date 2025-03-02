# all the data related to reading of the data from diffrent data sources i.e. databases. 
# step1) is data ingestion 
# step2) is data transformation 
import os 
import sys 
import pandas as pd 
from src.logger import logging 
from src.exception import CustomException 

from sklearn.model_selection  import train_test_split 
from dataclasses import dataclass  #used for create classvariables i.e. very cool way of using things  

from src.components.data_transformation import DataTransformation  
from src.components.data_transformation import DataTransformationConfig 

from src.components.model_trainer import ModelTrainerConfig
from src.components.model_trainer import ModelTrainer 

# Whenever we perform data ingestion component their should be some i/p's that may be required by this data ingestion components.  
#the i/p can be like where i have to save the training part, where i have to save the test part, where i've to save the raw data, 
#  those type of i/p i will be creatingt in another class which is  

@dataclass #used to define the class variable directly inside the class w/o init method otherwise omit it also.
class DataIngestionConfig: #this is for providing all the i/p things required for this data ingestion components.
      train_data_path: str=os.path.join('artifacts',"train.csv")  #this line is i/p and later on dataingestion component will save train.csv file in this particular path
      test_data_path: str=os.path.join('artifacts',"test.csv")  
      raw_data_path: str=os.path.join('artifacts',"data.csv") 
      
class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig()  
        
        
    def initiate_data_ingestion(self): 
        logging.info('Entered the data ingestion method or the component') 
        try:
            #Here you can write the code to read data from mongodb or mysql etc.
            df=pd.read_csv('notebook\data\stud.csv')
            logging.info('Read the dataset as dataframe')
            
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            
            df.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            
            logging.info('Train test split initiated')
            train_set,test_set=train_test_split(df,test_size=0.2,random_state=42) 
            
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            
            logging.info("Ingestion of the data is completed")
            
            return( 
                   self.ingestion_config.train_data_path,
                   self.ingestion_config.test_data_path
           ) 
           #returning  this above to my next step v.i.z my data transformation  
          
        except Exception as e:
            raise CustomException(e,sys)  
        
if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()  
    
    data_transformation=DataTransformation()  
    train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)   
    
    modeltrainer=ModelTrainer() 
    print(modeltrainer.initiate_model_trainer(train_arr,test_arr)) 
    
    
    
        

    
    
        
        









