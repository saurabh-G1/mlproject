# for exception handling purpose  (common code) 
import sys 
import logging

# this function does is  whenever an exception gets raised i want to push this on my own custom message
# error means whatever message i am getting 
# error_detail will be present inside sys i.e. what module we have basically imported


#function give you message of how your message should look like inside your file w.r.t your custom
# exception & then we created our own custom class
def error_message_detail(error,error_detail:sys):
    _,_,exc_tb=error_detail.exc_info()
    file_name=exc_tb.tb_frame.f_code.co_filename  #this all is in exception documentation and is a fixed part
    error_message="Error occured in python script name [{0}] line number [{1}] error message[{2}]".format(
    file_name,exc_tb.tb_lineno,str(error))
    
    return error_message      
        

    
class CustomException(Exception):
     def __init__(self,error_message,error_detail:sys):
         super().__init__(error_message)  
         self.error_message=error_message_detail(error_message,error_detail=error_detail) 
         
         
     def __str__(self):
         return self.error_message  
     
     
    
     
#  done in 267    
# if __name__=="__main__":  
    
#     try:
#         a=1/0
#     except Exception as e:
#         # logging.info("Divide by Zero") 
#         raise CustomException(e,sys) 
    
     
     
         
    
    
    
    
    
    