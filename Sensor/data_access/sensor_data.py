import pymongo
from Sensor.constant.database import *
import pandas as pd
from Sensor.logger import logging
from Sensor.exception import SensorException
from Sensor.configuration.mongodb_connection import MongoDBClient
import sys,os
import numpy as np


class SensorData:
    def __init__(self,):
        """
        Help to export collection data in to dataframe
        """
        try:
            self.mongo_client=MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise SensorException(e,sys)
    def export_collection_as_dataframe(self,collection_name:str,database_name=None)->pd.DataFrame:
        try:
            """export entire collection as dataframe and return dataframe"""
            if database_name is None:
                collection=self.mongo_client.database[collection_name]
            else:
                collection=self.mongo_client[database_name][collection_name]
            df=pd.DataFrame(collection.find())

            if "_id" in df.columns.to_list():
                df=df.drop(columns=["_id"],axis=1)
            
            df.replace({"na":np.nan},inplace=True)

            return df
        except Exception as e:
            SensorException(e,sys)
