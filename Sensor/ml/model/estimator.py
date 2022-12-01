from Sensor.exception import SensorException
import os,sys
from Sensor.constant.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME

class TargetValueMapping:
          def __init__(self,):
                    self.neg:int=0
                    self.pos:int=1
          def to_dict(self):
                    return self.__dict__


class SensorModel:
          def __init__(self,preprocessor,model):
                    self.preprocessor=preprocessor
                    self.model=model
          
          def predict(self,X):
                    try:
                              x_transform=self.preprocessor.transform(X)
                              y_hat=self.model.predict(x_transform)
                              return y_hat
                    except Exception as e:
                              raise SensorException(e,sys) from e


class ModelResolver:
          def __init__(self,model_dir=SAVED_MODEL_DIR):

                    try:
                              self.model_dir=model_dir
                    except Exception as e:
                              raise SensorException(e,sys) from e

          def get_best_model_path(self):
                    try:
                              timestamps=list(map(int,os.listdir(self.model_dir)))
                              latest_timestamp=max(timestamps)
                              latest_model_path=os.path.join(self.model_dir,str(latest_timestamp),MODEL_FILE_NAME)
                              return latest_model_path
                    except Exception as e:
                              raise SensorException(e,sys) from e

          def is_model_exist(self)->str:
                    try:
                              if not os.path.exists(self.model_dir):
                                        return False
                              timestamps=os.listdir(self.model_dir)
                              if len(timestamps) ==0:
                                        return False
                              latest_model_path=self.get_best_model()
                              if not os.path.exists(latest_model_path):
                                        return False
                              return True
                    except Exception as e:
                              raise SensorException(e,sys) from e
          
