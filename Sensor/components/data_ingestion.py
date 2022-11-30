from Sensor.exception import SensorException
from Sensor.logger import logging
from Sensor.entity.config_entity import *
from Sensor.entity.artifact_entity import *
import pandas as pd
from pandas import DataFrame
from Sensor.data_access.sensor_data import SensorData
import sys,os
from sklearn.model_selection import train_test_split


class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        self.data_ingestion_config = data_ingestion_config
    def export_data_into_feature_store(self)->DataFrame:
        """
        Export data into feature store from mongodb
        """
        try:
            logging.info("export_data_into_feature_store")
            sensor_data=SensorData()
            dataframe=sensor_data.export_collection_as_dataframe(collection_name=self.data_ingestion_config.collection_name)

            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            
            #creating feature store folders
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)

            dataframe.to_csv(feature_store_file_path,index=False)
            return dataframe
        except Exception as e:
            raise SensorException(e,sys) from e

    def split_data_as_train_test(self,dataframe:DataFrame)->None:
        """
        Split the data from feature store
        """
        try:
            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Dividing the data as train and test split")
            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False)
        except Exception as e:
            raise SensorException(e,sys) from e
            
    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:
            dataframe=self.export_data_into_feature_store()
            self.split_data_as_train_test(dataframe)
            data_ingestion_artifact=DataIngestionArtifact(train_file_path=self.data_ingestion_config.training_file_path,test_file_path=self.data_ingestion_config.testing_file_path)
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e,sys) from e



