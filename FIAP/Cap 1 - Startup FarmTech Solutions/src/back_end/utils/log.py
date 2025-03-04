import os
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
            
            log_dir = os.path.join(str(start_datetime.year), str(start_datetime.month), str(start_datetime.day))
            os.makedirs(log_dir, exist_ok=True)
            
            machine_name = socket.gethostname()
            user_name = getpass.getuser()
            
            log_filename = f"Log-{machine_name}_{user_name}_{start_datetime.strftime('%Y-%m-%d')}.txt"
            log_filepath = os.path.join(log_dir, log_filename)
            
            log_entry = (
                f"Class: {func.__qualname__.split('.')[0]}\n"
                f"Function: {func.__name__}\n"
                f"Message: {log_message}\n"
                f"Start Time: {start_str}\n"
                f"End Time: {end_str}\n"
                f"Execution Time: {execution_time:.2f} seconds\n"
                "----------------------------------------\n"
            )
            
            with open(log_filepath, 'a') as log_file:
                log_file.write(log_entry)
            
            print(log_entry)
            
            return result
        
        return wrapper
    return decorator