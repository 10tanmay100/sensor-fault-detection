from Sensor.configuration.mongodb_connection import MongoDBClient
from Sensor.logger import logging
from Sensor.entity.config_entity import *
from Sensor.pipeline.training_pipeline import TrainPipeline




if __name__ == '__main__':
    training_pipeline=TrainPipeline()
    print(training_pipeline.run_pipeline())

