import traceback
import sys

# We are creating custom exception, but we also need predefined exception like 
# divide by zero which are already defined in Exception therefore our class is inheriting from Exception class,
class CustomException(Exception):
# constructor
    def __init__(self, error_message, error_detail:sys):
        
        super().__init__(error_message)
        self.error_message=self.get_detailed_error_message(error_message, error_detail)


    @staticmethod
    def get_detailed_error_message(error_message, error_detail:sys):
        
        # exc_info() returns 3 things we only need last one that is trackback
        _, _, exc_tab = error_detail.exc_info()
        
        # name of file where error occured
        file_name=exc_tab.tb_frame.f_code.co_filename

        # line number where error occured.
        line_number = exc_tab.tb_lineno

        return f"Error in {file_name}, line {line_number}: {error_message}"
    
# below is a magic method, it basically gives you text representation of your error message when you do str(e)
    def __str__(self):
        return self.error_message
    

# Check test.py for demo code