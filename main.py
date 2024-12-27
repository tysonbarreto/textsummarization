from src.textsummarization.data_ingestion_stage import DataIngestionPipeline
from src.textsummarization.logger import Logger
from src.textsummarization.exception import TSException

import os, sys

logger = Logger()

try:
    logger.info("<<<< DataIngestionStageInitialized >>>>")
    DataIngestionPipeline()
    logger.info("==== DataIngestionStageCompleted ====")
except Exception as e:
    logger.error(TSException(e,sys))
    raise TSException(e,sys)