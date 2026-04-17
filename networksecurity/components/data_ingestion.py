import numpy as np
import os
import sys
import pandas as pd
from pymongo import MongoClient
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.logger.logger import logging
from networksecurity.exceptionhandling.exception import networkSecurityException
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()

mongo_uri = os.getenv("MONGO_URI")

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
      try:
         self.data_ingestion_config = data_ingestion_config
      except Exception as e:
            raise networkSecurityException(e, sys)
      
    def extract_collection_as_dataframe(self):
        try:
            data_base_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongoclient = MongoClient(mongo_uri)
            collection= self.mongoclient[data_base_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df.drop(columns=["_id"], inplace=True)
            df.replace({"na": np.nan}, inplace=True)
            logging.info(f"Data has been read from database: {data_base_name} and collection: {collection_name}")
            return df
         

        except Exception as e:
            raise networkSecurityException(e, sys)
    def export_data_to_feature_store(self, dataframe:pd.DataFrame):
        try:
            FILE_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(FILE_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(FILE_path, index=False, header=True)
            return dataframe
        except Exception as e:
            raise networkSecurityException(e, sys)
    
    def split_data_as_train_test(self, dataframe:pd.DataFrame):
        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info(f"Data has been split into train and test sets with test size ratio: {self.data_ingestion_config.train_test_split_ratio}")
            logging.info(f"exiting the split_data_as_train_test method of DataIngestion class")

            train_file_path=self.data_ingestion_config.training_file_path
            test_file_path=self.data_ingestion_config.testing_file_path
            dir_path=os.path.dirname(train_file_path)
            os.makedirs(dir_path, exist_ok=True)
            train_set.to_csv(train_file_path, index=False, header=True)
            test_set.to_csv(test_file_path, index=False, header=True)
        except Exception as e:
            raise networkSecurityException(e, sys)
        

    def initiate_data_ingestion(self):
        try:
            dataframe=self.extract_collection_as_dataframe()
            dataframe=self.export_data_to_feature_store(dataframe=dataframe)
            self.split_data_as_train_test(dataframe=dataframe)
            artifact=DataIngestionArtifact(
                train_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            return artifact

        except Exception as e:
            raise networkSecurityException(e, sys)  
        