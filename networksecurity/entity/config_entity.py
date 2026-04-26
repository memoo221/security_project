from networksecurity.logger.logger import logging
from networksecurity.constants import trainingpipeline
import os
from datetime import datetime

class trainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        logging.info(f"Training Pipeline Config initialized with timestamp: {timestamp}")
        self.pipeline_name = trainingpipeline.PIPELINE_NAME
        self.artifact_name = trainingpipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name,timestamp.strftime("%m_%d_%Y_%H_%M_%S"))
        self.timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:trainingPipelineConfig):
        logging.info(f"Data Ingestion Config initialized with training pipeline config: {training_pipeline_config}")
        self.data_ingestion_dir:str=os.path.join(
            training_pipeline_config.artifact_dir,trainingpipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_file_path: str = os.path.join(
                self.data_ingestion_dir, trainingpipeline.DATA_INGESTION_FEATURE_STORE_DIR, trainingpipeline.FILE_NAME
            )
        self.training_file_path: str = os.path.join(
                self.data_ingestion_dir, trainingpipeline.DATA_INGESTION_INGESTED_DIR, trainingpipeline.TRAIN_FILE_NAME
            )
        self.testing_file_path: str = os.path.join(
                self.data_ingestion_dir, trainingpipeline.DATA_INGESTION_INGESTED_DIR, trainingpipeline.TEST_FILE_NAME
            )
        self.train_test_split_ratio: float = trainingpipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        self.collection_name: str = trainingpipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name: str = trainingpipeline.DATA_INGESTION_DATABASE_NAME

class DataValidationConfig:
    def __init__(self,training_pipeline_config:trainingPipelineConfig):
        logging.info(f"Data Validation Config initialized with training pipeline config: {training_pipeline_config}")
        self.data_validation_dir:str=os.path.join(
            training_pipeline_config.artifact_dir,trainingpipeline.DATA_VALIDATION_DIR_NAME
        )
        self.valid_data_dir:str=os.path.join(
            self.data_validation_dir,trainingpipeline.DATA_VALIDATION_VALID_DIR
        )
        self.invalid_data_dir:str=os.path.join(
            self.data_validation_dir,trainingpipeline.DATA_VALIDATION_INVALID_DIR
        )
        self.valid_train_file_path:str=os.path.join(
            self.valid_data_dir,trainingpipeline.TRAIN_FILE_NAME
        )
        self.valid_test_file_path:str=os.path.join(
            self.valid_data_dir,trainingpipeline.TEST_FILE_NAME
        )
        self.invalid_train_file_path:str=os.path.join(
            self.invalid_data_dir,trainingpipeline.TRAIN_FILE_NAME
        )
        self.invalid_test_file_path:str=os.path.join(
            self.invalid_data_dir,trainingpipeline.TEST_FILE_NAME
        )
        self.drift_report_dir:str=os.path.join(
            self.data_validation_dir,trainingpipeline.DATA_VALIDATION_DRIFT_REPORT_DIR
        )
        self.drift_report_file_path:str=os.path.join(
            self.drift_report_dir,trainingpipeline.DATA_VALIDATION_DRIFT_REPORT_FILE_NAME
        )


class DataTransformationConfig:
    def __init__(self,training_pipeline_config:trainingPipelineConfig):
        logging.info(f"Data Transformation Config initialized with training pipeline config: {training_pipeline_config}")
        self.data_transformation_dir:str=os.path.join(
            training_pipeline_config.artifact_dir,trainingpipeline.DATA_TRANSFORMATION_DIR_NAME
        )
        self.transformed_train_file_path:str=os.path.join(
            self.data_transformation_dir,trainingpipeline.DATA_TRANSFORMATION_TRANSFORMED_DIR,trainingpipeline.TRAIN_FILE_NAME.replace("csv","npy")
        )
        self.transformed_test_file_path:str=os.path.join(
            self.data_transformation_dir,trainingpipeline.DATA_TRANSFORMATION_TRANSFORMED_DIR,trainingpipeline.TEST_FILE_NAME.replace("csv","npy")
        )
        self.preprocessor_object_file_path:str=os.path.join(
            self.data_transformation_dir,trainingpipeline.DATA_TRANSFORMATION_TRANSFORMED_DIR,"preprocessor.pkl"
        )