import yaml
from box import ConfigBox
from pathlib import Path
from src.textsummarization.logger import Logger
from src.textsummarization.exception import TSException

import os,sys
from typing import Any, List


logger = Logger()

def read_yaml(file_path:Path, return_configbox:bool)->Any:
    try:
        with open(file_path,'r') as handle:
            file = yaml.safe_load(handle)
            file_name = os.path.basename(file_path)
        logger.info(f"{file_name} has been loaded successfully.")
        if return_configbox:
            return ConfigBox(file)
        else:
            return file
    except Exception as exc:
        logger.error(TSException(exc, sys))
        raise TSException(exc, sys)

def create_directories(directory_path:List[Path]):
    for path_ in directory_path:
        if not os.path.exists(path_):
            os.makedirs(path_, exist_ok=True)
            logger.info(f"{path_} has been created successfully.")

def get_size(file_path:Path):
    size_in_kb = round(os.path.getsize(file_path)/1024)
    logger.info(f"~ {size_in_kb} KB")


def activate_root_directory():
    if os.path.split(os.getcwd())[-1] == 'research':
        os.chdir('..')
        logger.info("Root directory is active")
    else:
        pass
        logger.info("Root directory was active")

def which_is_file_running():
    try:
        from google.colab import drive
        IN_COLAB = True
        logger.info("Running in Google Colab")
    except:
        IN_COLAB = False
        logger.info("Running locally")

if __name__=="__main__":
    __all__ = ['read_yaml','create_directories','get_size','activate_root_directory','which_is_file_running']