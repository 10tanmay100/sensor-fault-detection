from datetime import datetime
from Sensor.constant import *
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

class DataValidationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        #data validation directory path
        self.data_validation_dir:str=os.path.join(training_pipeline_config.artifact_dir,DATA_VALIDATION_DIR_NAME)
        #defining valid data directory
        self.valid_data_directory:str=os.path.join(self.data_validation_dir,DATA_VALIDATION_VALID_DIR)
        #defining invalid data directory
        self.invalid_data_directory:str=os.path.join(self.data_validation_dir,DATA_VALIDATION_INVALID_DIR)
        #defining the valid train file path
        self.valid_train_file_path:str=os.path.join(self.valid_data_directory,TRAIN_FILE_NAME)
        #defining the invalid train file path
        self.invalid_train_file_path:str=os.path.join(self.invalid_data_directory,TRAIN_FILE_NAME)
        #defining the valid test file path
        self.valid_test_file_path:str=os.path.join(self.valid_data_directory,TEST_FILE_NAME)
        #defining the invalid test file path
        self.invalid_test_file_path:str=os.path.join(self.invalid_data_directory,TEST_FILE_NAME)
        #defining drift report file path
        self.drift_report_file_path:str=os.path.join(self.data_validation_dir,DATA_VALIDATION_DRIFT_REPORT_DIR,DATA_VALIDATION_DRIFT_REPORT_FILE_NAME)

class DataTransformationConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        #defining the root directory of data transformation
        self.data_transformation_dir:str=os.path.join(training_pipeline_config.artifact_dir,DATA_TRANSFORMATION_DIR_NAME)
        #defining the train file path
        self.data_transformed_train_dir:str=os.path.join(self.data_transformation_dir,TRAIN_FILE_NAME.replace('.csv','.npy'))
        #defining the test file path
        self.data_transformed_test_dir:str=os.path.join(self.data_transformation_dir,TEST_FILE_NAME.replace('.csv','.npy'))
        #defining the directory to store the transformation pickle file in my system
        self.data_transformation_transformed_obj_dir:str=os.path.join(self.data_transformation_dir,DATA_TRANSFORMATION_TRANSFORMED_OBJECT_DIR)


