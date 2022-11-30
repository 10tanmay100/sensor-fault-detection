from Sensor.configuration.mongodb_connection import MongoDBClient
from Sensor.logger import logging
from Sensor.entity.config_entity import *
from Sensor.exception import SensorException
from Sensor.pipeline.training_pipeline import TrainPipeline
import os,sys



if __name__ == '__main__':
    try:
        training_pipeline=TrainPipeline()
        print(training_pipeline.run_pipeline())
    except Exception as e:
        raise SensorException(e,sys) from e

