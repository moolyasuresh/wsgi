import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

class LoggingHandler():

    file_handler = ''
    today_date = ''
    base_path = 'D:/Apps/wsgi/logs/'
    def __init__(self):
        self.today_date = datetime.today().strftime('%Y-%m-%d')
        self.file_handler = RotatingFileHandler(self.base_path + 'int-cc-custom-ml-service-app ' + self.today_date + '.log', maxBytes=1024 * 1024 * 100, backupCount=20)
        self.file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.file_handler.setFormatter(formatter)

    def log_config(self):
        return self.file_handler
        

