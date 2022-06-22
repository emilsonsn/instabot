import logging
from logging import FileHandler, StreamHandler
from datetime import date

class LogConfig:

    @staticmethod 
    def get_logging():
        logging.basicConfig(
            level = logging.INFO, 
            format= "%(asctime)s::%(levelname)s::%(filename)s::%(lineno)d - %(message)s",
            datefmt='%m/%d/%Y %I:%M:%S',
            handlers=[FileHandler("./logs/instabot-"+str(date.today())+".log", 'a'), StreamHandler()]
        )
        return logging