from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation

from networksecurity.logger.logger import logging
from networksecurity.exceptionhandling.exception import networkSecurityException
from networksecurity.entity.config_entity import DataIngestionConfig,DataValidationConfig
from networksecurity.entity.config_entity import trainingPipelineConfig
import sys
if __name__ == "__main__":
    try:
       logging.info(f"training pipeline started")
       trainingpipeline=trainingPipelineConfig()
       DataIngestion_config=DataIngestionConfig(training_pipeline_config=trainingpipeline)
       Data_ingestion=DataIngestion(data_ingestion_config=DataIngestion_config)
       DataIngestionartifact=Data_ingestion.initiate_data_ingestion()
       logging.info(f"data intitianed and completed")
       DataValidation_config=DataValidationConfig(training_pipeline_config=trainingpipeline)
       Data_validation=DataValidation(data_ingestion_artifact=DataIngestionartifact,data_validation_config=DataValidation_config)
       DataValidationartifact=Data_validation.initiate_data_validation()
       logging.info(f"data validation intitianed and completed")

    except Exception as e:
        raise networkSecurityException(e, sys)
    