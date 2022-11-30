import sys

import numpy as np
import pandas as pd
from imblearn.combine import SMOTETomek
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import RobustScaler
from sklearn.pipeline import Pipeline
from Sensor.constant.training_pipeline import TARGET_COLUMN
from Sensor.entity.artifact_entity import (DataTransformationArtifact,DataValidationArtifact,)
from Sensor.entity.config_entity import DataTransformationConfig
from Sensor.exception import SensorException
from Sensor.logger import logging
from Sensor.ml.model.estimator import TargetValueMapping
from Sensor.utils.main_utils import save_numpy_array, save_object



class DataTransformation:
          def __init__(self,data_validation_artifact:DataValidationArtifact,data_transformation_config:DataTransformationConfig):
                    try:
                              self.data_validation_artifact=data_validation_artifact
                              self.data_tranformation_config=data_transformation_config
                    except Exception as e:
                              raise SensorException(e,sys) from e

          @staticmethod
          def read_data(file_path):
                    try:
                              return pd.read_csv(file_path)
                    except Exception as e:
                              raise SensorException(e,sys) from e
          @classmethod
          def get_data_transformer_object(cls)->Pipeline:
                    try:
                              robust_scaler=RobustScaler()
                              simple_imputer=SimpleImputer(strategy="constant",fill_value=0)
                              preprocessor=Pipeline(
                                        steps=[('imputer',simple_imputer),
                                        ('RobustScaler',robust_scaler)]
                              )
                              return preprocessor
                    except Exception as e:
                              raise SensorException(e,sys) from e
          
          def initiate_data_transformation(self)->DataTransformationArtifact:
                    try:
                              train_dataframe=DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
                              test_dataframe=DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
                              preprocessor=self.get_data_transformer_object()
                              #training dataframe
                              input_feature_train_df=train_dataframe.drop(columns=[TARGET_COLUMN])
                              target_feature_train_df=train_dataframe[TARGET_COLUMN]
                              target_feature_train_df=target_feature_train_df.replace(TargetValueMapping().to_dict())
                              #getting the preprocessor obj
                              preprocessor_obj=preprocessor.fit(input_feature_train_df)
                              save_object(file_path=self.data_tranformation_config.data_transformation_transformed_obj_dir,obj=preprocessor_obj)
                              transformed_feature_train_df=preprocessor.transform(input_feature_train_df)
                              #testing dataframe
                              input_feature_test_df=test_dataframe.drop(columns=[TARGET_COLUMN])
                              target_feature_test_df=test_dataframe[TARGET_COLUMN]
                              target_feature_test_df=target_feature_test_df.replace(TargetValueMapping().to_dict())
                              transformed_feature_test_df=preprocessor.transform(input_feature_test_df)



                              smt=SMOTETomek(sampling_strategy="minority")
                              input_feature_train_final,target_feature_train_final=smt.fit_resample(transformed_feature_train_df,target_feature_train_df)
                              
                              
                              input_feature_test_final,target_feature_test_final=smt.fit_resample(transformed_feature_test_df,target_feature_test_df)

                              transformed_train_arr=np.c_[input_feature_train_final,np.array(target_feature_train_final)]

                              
                              transformed_test_arr=np.c_[input_feature_test_final,np.array(target_feature_test_final)]

                              #saving numpy arrays
                              save_numpy_array(file_path=self.data_tranformation_config.data_transformed_train_dir,array=transformed_train_arr)
                              save_numpy_array(file_path=self.data_tranformation_config.data_transformed_test_dir,array=transformed_test_arr)

                              data_transformation_artifact=DataTransformationArtifact(transformed_object_file_path=self.data_tranformation_config.data_transformation_transformed_obj_dir,transformed_train_file_path=self.data_tranformation_config.data_transformed_train_dir,transformed_test_file_path=self.data_tranformation_config.data_transformed_test_dir)

                              return data_transformation_artifact

                    except Exception as e:
                              raise SensorException(e,sys) from e