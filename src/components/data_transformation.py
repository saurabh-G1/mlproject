import sys 
from dataclasses import dataclass

import numpy as np 
import pandas as pd  

from sklearn.compose import ColumnTransformer 
from sklearn.impute import SimpleImputer 
from sklearn.pipeline import Pipeline 
from sklearn.preprocessing import  OneHotEncoder,StandardScaler 

from src.exception import CustomException 
from src.logger import logging 
import os

from src.utils import save_object  

@dataclass
class DataTransformationConfig:  
    preprocessor_obj_file_path=os.path.join('artifacts',"proprocessor.pkl")  
    
class DataTransformation:
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()
        
    def get_data_transformer_object(self):
        '''
        This function is responsible for data transformation (based on diffrent types of data)
        '''
        
        try:
            numerical_columns = ["writing_score", "reading_score"]
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course"
            ] 
            
             #this pipeline nees to run on training data set like fit_transform on training dataset & and just transform on test dataset.
            num_pipeline=Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="median")),#handles missing values
                    ("scaler",StandardScaler())                    #performs standard scalar
                ] 
                
            )  
            
            cat_pipeline=Pipeline(
                steps=[
                    ("imputer", SimpleImputer(strategy="most_frequent")), # here missing values are getting handled
                    ("one_hot_encoder",OneHotEncoder()), #onehotencoder bcz less no.of categories in categorical variables(i.e. features).
                    ("scaler",StandardScaler(with_mean=False))           # Scaling is Happening
                ] 
            )  
            
            logging.info(f"Numerical columns:{numerical_columns}") 
            logging.info(f"Categorical columns:{categorical_columns}")
            
            
            preprocessor=ColumnTransformer(
                [
                 ("num_pipeline",num_pipeline,numerical_columns), #(pipeline_name,pipeline,columns)
                 ("cat_pipeline",cat_pipeline,categorical_columns) #(pipeline_name,pipeline,columns)
                ]
            )
            return preprocessor
        
        except Exception as e:
            raise CustomException(e,sys)
    
    
    

    #train_path ,test_apth is obtained from data_ingestion file
    def initiate_data_transformation(self,train_path,test_path):
            
         try: 
           train_df=pd.read_csv(train_path) 
           test_df=pd.read_csv(test_path)
           
           logging.info("Read test and train data completed") 
           
           logging.info("Obtaining preprocessing object")
           
           preprocessing_obj=self.get_data_transformer_object()  # it can be (& needs to also be) converted into pickle file.
           
           target_column_name="math_score" 
           numerical_columns = ["writing_score", "reading_score"]  
           
           input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
           target_feature_train_df=train_df[target_column_name]
           
           input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
           target_feature_test_df=test_df[target_column_name]  
           
           logging.info(f"Applying preprocessing object on training dataframe and testing dataframe.") 
           
           input_feature_train_arr=preprocessing_obj.fit_transform(input_feature_train_df)
           input_feature_test_arr=preprocessing_obj.transform(input_feature_test_df) 
           
           train_arr = np.c_[
               input_feature_train_arr, np.array(target_feature_train_df)
           ] 
           
           test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]  
           
           logging.info(f"Saved preprocessing object") 
           
           save_object(
                
                 file_path=self.data_transformation_config.preprocessor_obj_file_path,
                 obj=preprocessing_obj #this object has the model w.r.t all the transformation.                 
           ) 
           
           return ( 
                   train_arr, 
                   test_arr,
                   self.data_transformation_config.preprocessor_obj_file_path,  #it is a pickle file path. 
                )
           
         except Exception as e:
             raise CustomException(e,sys)   


