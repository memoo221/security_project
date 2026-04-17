from networksecurity.constants import trainingpipeline
import os
from datetime import datetime

class trainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        self.pipeline_name = trainingpipeline.PIPELINE_NAME
        self.artifact_name = trainingpipeline.ARTIFACT_DIR
        self.artifact_dir = os.path.join(self.artifact_name,timestamp.strftime("%m_%d_%Y_%H_%M_%S"))
        self.timestamp = timestamp.strftime("%m_%d_%Y_%H_%M_%S")

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:trainingPipelineConfig):
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


       