from datetime import datetime
from Sensor.constant.training_pipeline import *
from Sensor.constant.training_pipeline.data_ingestion_constants import *
import os

class TrainingPipelineConfig:
    def __init__(self,timestamp=datetime.now()):
        timestamp=datetime.now().strftime("%m_%d_%Y_%M_%S")
        self.pipeline_name:str=PIPELINE_NAME
        self.artifact_dir:str=os.path.join(ARTIFACT_DIR,timestamp)
        self.timestamp:str=timestamp

class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        #data ingestion directory path
        self.data_ingestion_dir:str=os.path.join(training_pipeline_config.artifact_dir,DATA_INGESTION_DIR_NAME)
        #feature store file path
        self.feature_store_file_path:str=os.path.join(self.data_ingestion_dir,DATA_INGESTION_FEATURE_STORE_DIR,FILE_NAME)
        #training file path
        self.training_file_path:str=os.path.join(self.data_ingestion_dir,DATA_INGESTION_INGESTED_DIR,TRAIN_FILE_NAME)
        #testing file path
        self.testing_file_path:str=os.path.join(self.data_ingestion_dir,DATA_INGESTION_INGESTED_DIR,TEST_FILE_NAME)
        #train test split ratio
        self.train_test_split_ratio:float=DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
        #collection name for mongodb connection
        self.collection_name:str=DATA_INGESTION_COLLECTION_NAME
