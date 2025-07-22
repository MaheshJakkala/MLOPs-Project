# import traceback
# import sys

# class CustomException(Exception):
#     def __init__(self, error_message,error_detail:sys):
#         super().__init__(error_message)
#         self.error_message = self.get_detailed_error_message(error_message,error_detail)

#     @staticmethod
#     def get_detailed_error_message(error_message,error_detail:sys):
#         _,_,exec_tb = error_detail.exec_info()
#         line_number = exec_tb.tb_lineno
#         file_name = exec_tb.tb_frame.f_code.co_filename
#         return f"Error in {file_name} , line {line_number} : {error_message}"
    
#     def __str__(self):
#         return self.error_message
    

import traceback
import sys

class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message, error_detail)

    @staticmethod
    def get_detailed_error_message(error_message, error_detail: sys):
        _, _, exc_tb = error_detail.exc_info()
        # Get the last traceback (where the error occurred)
        tb = exc_tb
        while tb.tb_next is not None:
            tb = tb.tb_next
        line_number = tb.tb_lineno
        file_name = tb.tb_frame.f_code.co_filename
        return f"Error in {file_name}, line {line_number}: {error_message}"
    
    def __str__(self):
        return self.error_message
