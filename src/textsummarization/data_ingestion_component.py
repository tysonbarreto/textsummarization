from src.textsummarization.entity import DataIngestionConfig
from src.textsummarization.logger import Logger
from src.textsummarization.exception import TSException

from pathlib import Path
import os, sys, zipfile

logger=Logger()

class DataIngestion:

    def __init__(self, config:DataIngestionConfig):
        self.config = config

    def extract_zip_file(self, file_name:str):
        try:
            unzip_path = os.path.join(self.config.source_dir, file_name)
            
            with zipfile.ZipFile(unzip_path, 'r') as handle:
                handle.extractall(self.config.source_dir)
                logger.info(f"{file_name} has been unzipped in path {unzip_path}")
        except Exception as e:
            logger.info(TSException(e,sys))
            raise TSException(e,sys)


if __name__=="__main__":
    __all__=["DataIngestion"]