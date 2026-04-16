import os
import sys
import certifi
import pandas as pd
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from networksecurity.logger.logger import logging
from networksecurity.exceptionhandling.exception import networkSecurityException

load_dotenv()

DATABASE_NAME = "NetworkSecurity"
COLLECTION_NAME = "NetworkData"


class NetworkDataExtract:
    def __init__(self):
        try:
            uri = os.getenv("MONGO_URI")
            self.client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
            self.database = self.client[DATABASE_NAME]
            self.collection = self.database[COLLECTION_NAME]
            logging.info("Connected to MongoDB Atlas successfully.")
        except Exception as e:
            raise networkSecurityException(e, sys)

    def csv_to_json(self, file_path: str) -> list:
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True, inplace=True)
            records = list(df.to_dict(orient="records"))
            logging.info(f"Converted {len(records)} records from {file_path}.")
            return records
        except Exception as e:
            raise networkSecurityException(e, sys)

    def push_to_mongodb(self, records: list) -> int:
        try:
            self.collection.insert_many(records)
            logging.info(f"Inserted {len(records)} records into {DATABASE_NAME}.{COLLECTION_NAME}.")
            return len(records)
        except Exception as e:
            raise networkSecurityException(e, sys)


if __name__ == "__main__":
    FILE_PATH = "Network_DATA/phisingData.csv"
    try:
        extractor = NetworkDataExtract()
        records = extractor.csv_to_json(FILE_PATH)
        count = extractor.push_to_mongodb(records)
        print(f"Successfully pushed {count} records to MongoDB.")
    except Exception as e:
        logging.error(f"Failed to push data: {e}")
        print(f"Error: {e}")
