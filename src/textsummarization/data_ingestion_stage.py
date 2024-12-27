from src.textsummarization.config import ConfigurationManager
from src.textsummarization.data_ingestion_component import DataIngestion
from src.textsummarization.logger import Logger
from src.textsummarization.exception import TSException

import os, sys

logger = Logger()

def DataIngestionPipeline():
    try:
        config = ConfigurationManager()
        data_ingestion_config = config.get_data_ingestion_config()
        if data_ingestion_config.file_name.endswith('.zip'):
            DataIngestion(data_ingestion_config).extract_zip_file(data_ingestion_config.file_name)
        elif data_ingestion_config.file_name in ['',' ',None]:
            raise FileNotFoundError('Please ensure dataset file_name is provided in config.yml and dataset itself is available in data/datasets directory')
    except Exception as e:
        logger.error(TSException(e,sys))
        raise TSException(e,sys)
        
if __name__=="__main__":
    __all__=["DataIngestionPipeline"]

