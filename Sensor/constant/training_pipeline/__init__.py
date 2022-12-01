import os

SAVED_MODEL_DIR=os.path.join("SAVED_MODEL_DIR")
#defining common constant variables for training pipeline
TARGET_COLUMN="class"
PIPELINE_NAME:str="sensor"
ARTIFACT_DIR:str="artifact"
FILE_NAME:str="sensor.csv"
TRAIN_FILE_NAME:str="train.csv"
TEST_FILE_NAME:str="test.csv"

PREPROCESSING_OBJECT_FILE_NAME="preprocessing.pkl"
MODEL_FILE_NAME="model.pkl"
SCHEMA_FILE_PATH=os.path.join("config","schema.yaml")
SCHEMA_DROP_COLS="drop_columns"

