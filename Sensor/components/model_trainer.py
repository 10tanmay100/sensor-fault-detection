from Sensor.utils.main_utils import load_numpy_array_data
from Sensor.exception import SensorException
from Sensor.logger import logging
from Sensor.entity.artifact_entity import *
from Sensor.entity.config_entity import *
from xgboost import XGBClassifier
import os,sys
from Sensor.ml.metrics.classification_metrics import get_classification_metrics
from Sensor.ml.model.estimator import SensorModel
from Sensor.utils.main_utils import load_object,save_object



class ModelTrainer:
          def __init__(self,data_transformation_artifact:DataTransformationArtifact,model_trainer_config:ModelBuilderConfig):
                    try:
                              self.data_transformation_artifact = data_transformation_artifact
                              self.model_trainer_config=model_trainer_config

                    except Exception as e:
                              raise SensorException(e,sys) from e
          def train_model(self,X_train,y_train):
                    try:
                              xgb_clf=XGBClassifier()
                              xgb_clf.fit(X_train,y_train)
                              return xgb_clf
                    except Exception as e:
                              raise SensorException(e,sys) from e

          def initiate_model_trainer(self)->ModelTrainerArtifact:
                    try:      #loading training array and testing array
                              train_arr=load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_file_path)
                              test_arr=load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_file_path)
                              #spltting the data
                              X_train=train_arr[:,:-1]
                              y_train=train_arr[:,-1]
                              X_test=test_arr[:,:-1]
                              y_test=test_arr[:,-1]
                              #model training
                              model=self.train_model(X_train,y_train)
                              y_train_pred=model.predict(X_train)
                              classification_metrics_train=get_classification_metrics(y_train,y_train_pred)
                              y_test_pred=model.predict(X_test)
                              classification_metrics_test=get_classification_metrics(y_test,y_test_pred)

                              if classification_metrics_train.f1_Score < self.model_trainer_config.model_threshold_accuracy:
                                        raise Exception("f1 score is not accpetable!!")

                              #overfitting and underfitting
                              diff=abs(classification_metrics_train.f1_Score-classification_metrics_train.f1_Score)

                              if diff>self.model_trainer_config.model_over_underfit_thershold_diff:
                                        raise Exception("Model Might be overfitted or underfitted")

                              preprocessor=load_object(self.data_transformation_artifact.transformed_object_file_path)

                              model_dir_path=os.path.dirname(self.model_trainer_config.model_trained_dir)
                              os.makedirs(model_dir_path,exist_ok=True)

                              sensor_model=SensorModel(preprocessor=preprocessor,model=model)
                              save_object(file_path=self.model_trainer_config.model_trained_dir,obj=sensor_model)


                              return ModelTrainerArtifact(trained_model_file_path=self.model_trainer_config.model_trained_dir,trained_metric_artifact=classification_metrics_train,test_metric_artifact=classification_metrics_test)

                    except Exception as e:
                              raise SensorException(e,sys) from e



