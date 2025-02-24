import os
import sys

class Log:
    
    @staticmethod
    def resource_path(relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(
            os.path.abspath(__file__)))
    
        return os.path.join(base_path, relative_path)


    @staticmethod
    def write_success(user_email: str, message: str) -> None:
        paste_name: str = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))) + "\\send_success"
        if not os.path.exists(paste_name):
            os.mkdir(paste_name)
        
        archive_name: str = fr"send_success\{user_email}_sucessos.txt"
        with open(Log.resource_path(archive_name), "a", encoding="utf-8") as log_file:
            log_file.write(f"{message}\n")
            
            
    @staticmethod
    def write_error(user_email: str, message: str) -> None:
        paste_name: str = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))) + "\\send_error"
        if not os.path.exists(paste_name):
            os.mkdir(paste_name)
        
        archive_name: str = fr"{paste_name}\{user_email}_erros.txt"      
        with open(Log.resource_path(archive_name), "a", encoding="utf-8") as log_file:
            log_file.write(f"{message}\n")