from Sensor.exception import SensorException
from Sensor.logger import logging
from Sensor.entity.artifact_entity import *
from Sensor.entity.config_entity import *
import os,sys
from Sensor.ml.metrics.classification_metrics import get_classification_metrics
from Sensor.ml.model.estimator import SensorModel
from Sensor.utils.main_utils import load_object,save_object,write_yaml_file
from Sensor.ml.model.estimator import ModelResolver
from Sensor.ml.model.estimator import TargetValueMapping
import pandas as pd

class ModelEvaluation:

          def __init__(self,model_eval_config:ModelEvaluationConfig,data_validation_artifact:DataValidationArtifact,model_trainer_artifact:ModelTrainerArtifact):
                    try:
                              self.model_eval_config=model_eval_config
                              self.data_validation_artifact=data_validation_artifact
                              self.model_trainer_artifact=model_trainer_artifact
                    except Exception as e:
                              raise SensorException(e,sys) from e
          
          def initiate_model_evaluation(self)->ModelEvaluationArtifact:
                    try:      #takig the valid train and test file
                              valid_train_file_path=self.data_validation_artifact.valid_train_file_path
                              valid_test_file_path=self.data_validation_artifact.valid_test_file_path
                              #taking training and testing df
                              train_df=pd.read_csv(valid_train_file_path)
                              test_df=pd.read_csv(valid_test_file_path)


                              df=pd.concat([train_df,test_df],axis=0)
                              #taking the model
                              train_model_file_path=self.model_trainer_artifact.trained_model_file_path
                              model=load_object(file_path=train_model_file_path)


                              model_resolver=ModelResolver()
                              if not model_resolver.is_model_exist():
                                        model_evaluation_artifact=ModelEvaluationArtifact(is_model_accepted=True,changed_accuracy=None,
                                        best_model_path=None,
                                        trained_model_file_path=train_model_file_path,
                                        trained_model_metric_artifact=self.model_trainer_artifact.test_metric_artifact,best_model_metric_artifact=None)
                                        return model_evaluation_artifact
                              latest_model_path=model_resolver.get_best_model_path()
                              latest_model=load_object(file_path=latest_model_path)
                              train_model=load_object(file_path=train_model_file_path)

                              y_true=df[TARGET_COLUMN]
                              y_true=y_true.replace(TargetValueMapping().to_dict())
                              df.drop(TARGET_COLUMN,axis=1,inplace=True)
                              y_train_pred=train_model.predict(df)
                              y_latest_pred=latest_model.predict(df)


                              trained_metric=get_classification_metrics(y_true,y_train_pred)
                              latest_metric=get_classification_metrics(y_true,y_latest_pred)

                              improved_accuracy=trained_metric.f1_Score-latest_metric.f1_Score
                              if improved_accuracy>=self.model_eval_config.model_evaluator_threshold:
                                         model_evaluation_artifact=ModelEvaluationArtifact(is_model_accepted=True,changed_accuracy=improved_accuracy,
                                        best_model_path=latest_model_path,
                                        trained_model_file_path=train_model_file_path,
                                        trained_model_metric_artifact=trained_metric,best_model_metric_artifact=latest_metric)
                                        
                              else:
                                        model_evaluation_artifact=ModelEvaluationArtifact(is_model_accepted=False,changed_accuracy=improved_accuracy,
                                        best_model_path=latest_model_path,
                                        trained_model_file_path=train_model_file_path,
                                        trained_model_metric_artifact=trained_metric,best_model_metric_artifact=latest_metric)
                              model_eval_report=model_evaluation_artifact.__dict__
                              write_yaml_file(file_path=self.model_eval_config.report_file_path,content=model_eval_report,replace=True)
                              return model_evaluation_artifact

                    except Exception as e:
                              raise SensorException(e,sys) from e
          

          


