from Sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from Sensor.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from Sensor.entity.config_entity import DataValidationConfig
from Sensor.utils.main_utils import read_yaml_file,write_yaml_file
from Sensor.constant.training_pipeline import SCHEMA_FILE_PATH
from scipy.stats import ks_2samp
from Sensor.exception import SensorException
from Sensor.logger import logging
import os,sys
import pandas as pd



class DataValidation:

    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self.__schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise SensorException(e,sys) from e

    def validate_number_of_columns(self,dataframe:pd.DataFrame)->bool:
        try:
            number_of_columns=len(self.__schema_config["columns"])
            if len(dataframe.columns)==number_of_columns:
                return True
            else:
                return False
        except Exception as e:
            raise SensorException(e,sys) from e


    def is_numerical_column_exist(self,dataframe:pd.DataFrame)->bool:
        try:
            numerical_columns=self.__schema_config["numerical_columns"]
            dataframe_columns=dataframe.columns
            missing_numerical_columns_status=False
            missing_column_names=[]
            for cols in numerical_columns:
                if cols not in dataframe_columns:
                    missing_numerical_columns_status=True
                    missing_column_names.append(cols)
            logging.info(f"Missing numerical columns are [{missing_column_names}]")
            return missing_numerical_columns_status
        except Exception as e:
            raise SensorException(e,sys) from e

    @staticmethod
    def read_data(file_path)->pd.DataFrame:
        try:
            df=pd.read_csv(file_path)
            return df
        except Exception as e:
            raise SensorException(e,sys) from e
    
    def detect_dataset_drift(self,base_df,current_df,threshold=0.5):
        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=base_df[column]
                is_same_dist=ks_2samp(d1,d2)
                if threshold<=is_same_dist.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False
                report.update({column:{"p_value":float(is_same_dist.pvalue),"drift_status":is_found}})
            

            #defining the drift report file path
            drift_report_file_path=self.data_validation_config.drift_report_file_path

            dir_path=os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path,exist_ok=True)
            write_yaml_file(drift_report_file_path,report,replace=True)
            return status


        except Exception as e:
            raise SensorException(e,sys) from e


    def initiate_data_validation(self)->DataValidationArtifact:
        try:
            error_msg=""
            train_file_path=self.data_ingestion_artifact.train_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path
            #reading train and test file location
            train_dataframe=DataValidation.read_data(train_file_path)
            test_dataframe=DataValidation.read_data(test_file_path)
            
            #validation number of columns
            train_status=self.validate_number_of_columns(train_dataframe)
            if not train_status:
                error_msg=f"{error_msg}Train dataframe does not contain all columns"
            test_status=self.validate_number_of_columns(test_dataframe)
            if not test_status:
                error_msg=f"{error_msg}Test dataframe does not contain all columns"
            

            #validate numerical col exist
            train_status=self.is_numerical_column_exist(dataframe=train_dataframe)
            if train_status:
                error_msg=f"{error_msg}Train dataframe does not contain all numeric columns"
            test_status=self.is_numerical_column_exist(dataframe=test_dataframe)
            if test_status:
                error_msg=f"{error_msg}Test dataframe does not contain all numeric columns"


            if len(error_msg) > 0:
                with open(self.data_validation_config.invalid_train_file_path,"w") as f:
                    f.read()
                    train_dataframe.to_csv(self.data_validation_config.invalid_train_file_path)
                with open(self.data_validation_config.invalid_test_file_path,"w") as f:
                    f.read()
                    test_dataframe.to_csv(self.data_validation_config.invalid_test_file_path)
                raise Exception(error_msg)

            #check data drift
            status=self.detect_dataset_drift(base_df=train_dataframe,current_df=test_dataframe)
            if not os.path.exists(self.data_validation_config.invalid_train_file_path):
                train_path_invalid=None
            else:
                train_path_invalid=self.data_validation_config.invalid_train_file_path
            
            if not os.path.exists(self.data_validation_config.invalid_test_file_path):
                test_path_invalid=None
            else:
                test_path_invalid=self.data_validation_config.invalid_test_file_path




            data_validation_artifact=DataValidationArtifact(
                    validation_status=status,valid_train_file_path=self.data_ingestion_artifact.train_file_path,valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                    invalid_train_file_path=train_path_invalid,invalid_test_file_path=test_path_invalid,
                    drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            return data_validation_artifact


        except Exception as e:
            raise SensorException(e,sys) from e

