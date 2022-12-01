from Sensor.exception import SensorException
import os,sys

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