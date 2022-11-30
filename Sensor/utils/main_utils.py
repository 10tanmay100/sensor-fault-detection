import yaml
import sys
from Sensor.exception import SensorException
import os
import pandas as pd
import numpy as np
import pickle



def read_yaml_file(file_path:str)->dict:
    try:
        with open(file_path,"rb") as f:
            return yaml.safe_load(f)
    except Exception as e:
        raise SensorException(e,sys) from e


def write_yaml_file(file_path:str,content:object,replace:bool)->None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"w") as f:
            yaml.dump(content,f)
    except Exception as e:
        raise SensorException(e,sys) from e
        


def save_numpy_array(file_path:str,array:np.array)->None:
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    except Exception as e:
        raise SensorException(e,sys) from e


def load_numpy_array_data(file_path:str)->np.array:
    try:
        with open(file_path,"rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise SensorException(e,sys) from e


def save_object(file_path:str,obj:object)->None:
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,"wb") as pickle_obj:
            pickle.dump(obj,pickle_obj)
    except Exception as e:
        raise SensorException(e,sys) from e





