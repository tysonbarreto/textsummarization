from src.textsummarization.logger import Logger
from src.textsummarization.exception import TSException

from src.textsummarization.entity import DataIngestionConfig
from src.textsummarization.constants import *
from src.textsummarization.utils import read_yaml, create_directories, get_size


logger = Logger()


class ConfigurationManager:

    def __init__(self, config_file_path: Path = CONFIG_FILE_PATH, params_file_path: Path = PARAMS_FILE_PATH):
        self.config = read_yaml(config_file_path, return_configbox=True)
        self.params = read_yaml(params_file_path, return_configbox=True)
        create_directories([self.config.artifacts_root])
   
    def get_data_ingestion_config(self)->DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir, config.source_dir])
        logger.info(f"<<<< {config.source_dir} intialized to work with datasets... >>>>")
        return DataIngestionConfig(
            root_dir = config.root_dir,
            source_dir = config.source_dir,
            file_name = config.file_name
        )

if __name__=="__main__":
    __all__=["ConfigurationManager"]