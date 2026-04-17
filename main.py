from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.logger.logger import logging
from networksecurity.exceptionhandling.exception import networkSecurityException
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import trainingPipelineConfig
import sys
if __name__ == "__main__":
    try:
       trainingpipeline=trainingPipelineConfig()
       DataIngestion_config=DataIngestionConfig(training_pipeline_config=trainingpipeline)
       Data_ingestion=DataIngestion(data_ingestion_config=DataIngestion_config)
       DataIngestionartifact=Data_ingestion.initiate_data_ingestion()
       print(DataIngestionartifact)
    except Exception as e:
        raise networkSecurityException(e, sys)
    