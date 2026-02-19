import logging
import os
from datetime import datetime

# construct a format for log file name
log_file = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

logs_path = os.path.join(os.getcwd(), "logs", log_file)
os.makedirs(logs_path, exist_ok=True)

log_file_path = os.path.join(logs_path, log_file)
print(log_file_path)


# Handles logging information
logging.basicConfig(
    filename=log_file_path,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
    
)
logging.info('This is the first message.')
logging.warning('This is a warning message.')
logging.info('Another message to append.')