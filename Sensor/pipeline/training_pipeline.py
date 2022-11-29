from Sensor.entity.config_entity import *
from Sensor.exception import SensorException
from Sensor.entity.artifact_entity import *
from Sensor.logger import logging
from Sensor.components.data_ingestion import DataIngestion
import sys

class TrainPipeline:
    def __init__(self,):
        self.training_pipeline_config=TrainingPipelineConfig()
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info("Starting data ingestion")
            self.data_ingestion_config=DataIngestionConfig(self.training_pipeline_config)
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info("data ingestion ended")
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e,sys)

    def start_data_validation(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)

    def start_data_transformation(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)

    def start_model_trainer(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)

    def start_model_pusher(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)

    def run_pipeline(self):
        try:
            self.start_data_ingestion()
        except Exception as e:
            raise SensorException(e,sys)






