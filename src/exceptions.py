import sys
    
def error_message_detail(error_message, error_detail : sys):

    exception_type, exception_value, exception_traceback = error_detail.exc_info()
    
    exception_filename = exception_traceback.tb_frame.f_code.co_filename
    
    exception_linenumber = exception_traceback.tb_lineno
    
    return f"Exception occurred in {exception_filename} at line {exception_linenumber}"

class CustomException(Exception):
    
    def __init__(self, error_message, error_detail : sys):    
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail)
            
    def __str__(self):
        return self.error_message
            

