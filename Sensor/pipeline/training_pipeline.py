from Sensor.entity.config_entity import *
from Sensor.exception import SensorException
from Sensor.entity.artifact_entity import *
from Sensor.logger import logging
from Sensor.components.data_ingestion import DataIngestion
from Sensor.components.data_validation import DataValidation
from Sensor.components.data_transformation import DataTransformation
from Sensor.components.model_trainer import ModelTrainer
import sys

class TrainPipeline:
    def __init__(self,):
        self.training_pipeline_config=TrainingPipelineConfig()
    def start_data_ingestion(self)->DataIngestionArtifact:
        try:
            logging.info("Starting data ingestion!!!")
            self.data_ingestion_config=DataIngestionConfig(self.training_pipeline_config)
            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifact=data_ingestion.initiate_data_ingestion()
            logging.info("data ingestion ended!!!")
            return data_ingestion_artifact
        except Exception as e:
            raise SensorException(e,sys)

    def start_data_validation(self,data_ingestion_artifact:DataIngestionArtifact)->DataValidationArtifact:
        try:
            logging.info("Data Validation started!!!")
            self.data_validation_config=DataValidationConfig(self.training_pipeline_config)
            data_validation=DataValidation(data_ingestion_artifact=data_ingestion_artifact,data_validation_config=self.data_validation_config)
            data_validation_artifact=data_validation.initiate_data_validation()
            return data_validation_artifact
            logging.info("data validation ended!!!")
        except Exception as e:
            raise SensorException(e,sys)

    def start_data_transformation(self,data_validation_artifact:DataValidationArtifact):
        try:
            logging.info("Data Transformation started!!!")
            self.data_transformation_config=DataTransformationConfig(self.training_pipeline_config)
            data_transformation=DataTransformation(data_validation_artifact=data_validation_artifact,data_transformation_config=self.data_transformation_config)
            data_transformation_artifact=data_transformation.initiate_data_transformation()
            return data_transformation_artifact
            logging.info("data transformation ended!!!")
        except Exception as e:
            raise SensorException(e,sys)

    def start_model_trainer(self,data_transformation_artifact:DataTransformationArtifact):
        try:
            logging.info("Starting the Model Training!!!")
            self.model_trainer_config=ModelBuilderConfig(self.training_pipeline_config)
            model_training=ModelTrainer(data_transformation_artifact=data_transformation_artifact,model_trainer_config=self.model_trainer_config)
            model_training_artifact=model_training.initiate_model_trainer()
            return model_training_artifact
            logging.info("model training completed!!!")
        except Exception as e:
            raise SensorException(e,sys)

    def start_model_pusher(self):
        try:
            pass
        except Exception as e:
            raise SensorException(e,sys)

    def run_pipeline(self):
        try:
            data_ingestion_artifact=self.start_data_ingestion()
            data_validation_artifact=self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact=self.start_data_transformation(data_validation_artifact)
            model_trainer_artifact=self.start_model_trainer(data_transformation_artifact)
            return model_trainer_artifact
        except Exception as e:
            raise SensorException(e,sys)






