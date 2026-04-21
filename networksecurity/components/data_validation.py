from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.entity.artifact_entity import DataValidationArtifact, DataIngestionArtifact
from networksecurity.constants.trainingpipeline import SCHEMA_FILE_PATH
from networksecurity.logger.logger import logging
from networksecurity.utils.main_utils.utils import read_yaml_file,write_yaml_file
from networksecurity.exceptionhandling.exception import networkSecurityException
import sys
from scipy.stats import ks_2samp
import os

import pandas as pd
class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema = read_yaml_file(SCHEMA_FILE_PATH)
            logging.info(f"Data Validation component initialized with data ingestion artifact: {data_ingestion_artifact} and data validation config: {data_validation_config}")
        except Exception as e:
            raise networkSecurityException(e, sys)
    
    def initiate_data_validation(self)->DataValidationArtifact:
        try:
           train_file_path=self.data_ingestion_artifact.train_file_path
           test_file_path=self.data_ingestion_artifact.test_file_path
           ##reading from this file path
           train_dataframe=self.read_data(train_file_path)
           test_dataframe=self.read_data(test_file_path)
            #checking for the columns
           is_train_valid=self.validate_number_of_columns(dataframe=train_dataframe)
           if not is_train_valid:
              error=f"train file is not having the same number of columns as mentioned in the schema file"

           is_test_valid=self.validate_number_of_columns(dataframe=test_dataframe)
           if not is_test_valid:
                 error=f"test file is not having the same number of columns as mentioned in the schema file"

           is_numerical_train_valid=self.validate_numerical_columns(dataframe=train_dataframe)
           if not is_numerical_train_valid:
                    error=f"train file is not having the same numerical columns as mentioned in the schema file"
           is_numerical_test_valid=self.validate_numerical_columns(dataframe=test_dataframe)
           if not is_numerical_test_valid:
                    error=f"test file is not having the same numerical columns as mentioned in the schema file"

           is_data_drift_detected=self.detect_data_drift(base_dataframe=train_dataframe,current_dataframe=test_dataframe)

           validation_status = is_train_valid and is_test_valid and is_numerical_train_valid and is_numerical_test_valid and is_data_drift_detected

           if validation_status:
               os.makedirs(self.data_validation_config.valid_data_dir, exist_ok=True)
               train_dataframe.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
               test_dataframe.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)
           else:
               os.makedirs(self.data_validation_config.invalid_data_dir, exist_ok=True)
               train_dataframe.to_csv(self.data_validation_config.invalid_train_file_path, index=False, header=True)
               test_dataframe.to_csv(self.data_validation_config.invalid_test_file_path, index=False, header=True)

           data_validation_artifact = DataValidationArtifact(
               validation_status=validation_status,
               valid_train_file_path=self.data_validation_config.valid_train_file_path,
               valid_test_file_path=self.data_validation_config.valid_test_file_path,
               invalid_train_file_path=self.data_validation_config.invalid_train_file_path,
               invalid_test_file_path=self.data_validation_config.invalid_test_file_path,
               drift_report_file_path=self.data_validation_config.drift_report_file_path
           )
           return data_validation_artifact

        except Exception as e:
                raise networkSecurityException(e, sys)

    def detect_data_drift(self,base_dataframe:pd.DataFrame,current_dataframe:pd.DataFrame)->bool:
        try:
            status=True
            report={}
            for column in base_dataframe.columns:
                d1=base_dataframe[column]
                d2=current_dataframe[column]
                is_same_dist=ks_2samp(d1,d2)
                if is_same_dist.pvalue>=0.05:
                    isfound=False
                else:
                    isfound=True
                    status=False
                report.update({column:{
                    "p_value":float(is_same_dist.pvalue),
                    "drift":isfound
                }})

            write_yaml_file(file_path=self.data_validation_config.drift_report_file_path, data=report)
            logging.info(f"writing yaml file {report}")
            return status

        except Exception as e:
             raise networkSecurityException(e, sys)
    
       
    
        
    def validate_number_of_columns(self,dataframe: pd.DataFrame)->bool:
        try:
            numberofcol=len(self.schema['columns'])
            logging.info(f"number of columns in the dataframe is {numberofcol}")
            logging.info(f"number of columns in the dataframe is {dataframe.shape[1]}")
            if numberofcol==dataframe.shape[1]:
                return True
            else:
                return False


        except Exception as e:
            raise networkSecurityException(e, sys)  
    
    def validate_numerical_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            numerical_columns=self.schema['numerical_columns']
            logging.info(f"numerical columns in the dataframe are {numerical_columns}")
            for column in numerical_columns:
                if column not in dataframe.columns:
                    return False
                if not pd.api.types.is_numeric_dtype(dataframe[column]):
                    return False
            return True

        except Exception as e:
            raise networkSecurityException(e, sys)

    


    
    @staticmethod
    def read_data(file_path):
        try:
            import pandas as pd
            return pd.read_csv(file_path)
        except Exception as e:
            raise networkSecurityException(e, sys)

  







