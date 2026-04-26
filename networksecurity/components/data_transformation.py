from networksecurity.exceptionhandling.exception import networkSecurityException
import sys
import os
from networksecurity.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact,DataTransformationArtifact
from networksecurity.logger.logger import logging
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline
from networksecurity.constants.trainingpipeline import TARGET_COLUMN
from networksecurity.constants.trainingpipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.utils.main_utils.utils import save_object,save_numpy_array
import numpy as np
import pandas as pd

class DataTransformation:
    def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
            logging.info(f"Data Transformation component initialized with data validation artifact: {data_validation_artifact } and data transformation config: {data_transformation_config}")
        except Exception as e:
            raise networkSecurityException(e, sys)

    def get_data_transformer_object(self)->Pipeline:
        try:
            logging.info("Creating data transformer object")
            imputer_params = DATA_TRANSFORMATION_IMPUTER_PARAMS
            knn_imputer = KNNImputer(**imputer_params)
            preprocessor = Pipeline(steps=[("imputer", knn_imputer)])
            logging.info(f"Data transformer object created with imputer parameters: {imputer_params}")
            return preprocessor
        except Exception as e:
            raise networkSecurityException(e, sys)
        
    def initiate_data_transformation(self)->DataTransformationArtifact:
        try:
            logging.info("Initiating data transformation")
            valid_train_file_path=self.data_validation_artifact.valid_train_file_path
            valid_test_file_path=self.data_validation_artifact.valid_test_file_path
            train_dataframe=pd.read_csv(valid_train_file_path)
            test_dataframe=pd.read_csv(valid_test_file_path)
            X_train=train_dataframe.drop(columns=[TARGET_COLUMN])
            y_train=train_dataframe[TARGET_COLUMN]
            y_train.replace(-1,0,inplace=True)
            X_test=test_dataframe.drop(columns=[TARGET_COLUMN])
            y_test=test_dataframe[TARGET_COLUMN]
            y_test.replace(-1,0,inplace=True)
            preproccessor=self.get_data_transformer_object()
            X_train_transformed=preproccessor.fit_transform(X_train)
            X_test_transformed=preproccessor.transform(X_test)
            X_train_transformed=np.c_[X_train_transformed,y_train]
            X_test_transformed=np.c_[X_test_transformed,y_test]
            save_numpy_array(file_path=self.data_transformation_config.transformed_train_file_path,array=X_train_transformed)

            save_numpy_array(file_path=self.data_transformation_config.transformed_test_file_path,array=X_test_transformed)
            
            save_object(file_path=self.data_transformation_config.preprocessor_object_file_path,obj=preproccessor)
            self.data_transformation_artifact=DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                preprocessor_object_file_path=self.data_transformation_config.preprocessor_object_file_path
            )
            
            logging.info(f"Data transformation completed and data transformation artifact created: {self.data_transformation_artifact}")
            return self.data_transformation_artifact
        except Exception as e:
            raise networkSecurityException(e, sys)
        

         






