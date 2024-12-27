import yaml
from box import ConfigBox
from pathlib import Path
from src.textsummarization.logger import Logger
from src.textsummarization.exception import TSException

import os,sys


logger = Logger()

def read_yaml(file_path:Path)->ConfigBox:
    try:
        with open(file_path,'r') as handle:
            file = yaml.safe_load(handle)
            file_name = os.path.basename(file_path)
            logger.info(f"{file_name} has been loaded successfully.")
            return file
    except Exception as exc:
        logger.error(TSException(exc, sys))
        raise TSException(exc, sys)


if __name__=="__main__":
    __all__ = ['read_yaml']