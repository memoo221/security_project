import yaml
import pickle
import numpy as np
import os,sys
from networksecurity.exceptionhandling.exception import networkSecurityException


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise networkSecurityException(e, sys)


def write_yaml_file(file_path: str, data: dict) -> None:
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as yaml_file:
            yaml.dump(data, yaml_file)
    except Exception as e:
        raise networkSecurityException(e, sys)


def save_numpy_array(file_path: str, array: np.ndarray) -> None:
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file:
            np.save(file, array)
    except Exception as e:
        raise networkSecurityException(e, sys)


def save_object(file_path: str, obj: object) -> None:
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file:
            pickle.dump(obj, file)
    except Exception as e:
        raise networkSecurityException(e, sys)