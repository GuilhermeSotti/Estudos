import time
import datetime
import socket
import getpass
from functools import wraps

def log_execution(log_message):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            start_time = time.time()
            start_datetime = datetime.datetime.now()
            start_str = start_datetime.strftime("%Y-%m-%d %H:%M:%S")
            
            result = func(*args, **kwargs)
            
            end_time = time.time()
            end_datetime = datetime.datetime.now()
            end_str = end_datetime.strftime("%Y-%m-%d %H:%M:%S")

            execution_time = end_time - start_time
            
            machine_name = socket.gethostname()
            user_name = getpass.getuser()            
            
            log_entry = (
                f"Class: {func.__qualname__.split('.')[0]}\n"
                f"Function: {func.__name__}\n"
                f"Message: {log_message}\n"
                f"Machine: {machine_name}\n"
                f"User: {user_name}\n"
                f"Start Time: {start_str}\n"
                f"End Time: {end_str}\n"
                f"Execution Time: {execution_time:.2f} seconds\n"
                "----------------------------------------\n"
            )
            
            print(log_entry)
            
            return result
        
        return wrapper
    return decorator