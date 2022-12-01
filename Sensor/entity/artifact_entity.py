from dataclasses import dataclass


@dataclass(frozen=True)
class DataIngestionArtifact:
    train_file_path:str
    test_file_path:str

@dataclass(frozen=True)
class DataValidationArtifact:
    validation_status:bool
    valid_train_file_path:str
    invalid_train_file_path:str
    valid_test_file_path:str
    invalid_test_file_path:str
    drift_report_file_path:str

@dataclass(frozen=True)
class DataTransformationArtifact:
    transformed_object_file_path:str
    transformed_train_file_path:str
    transformed_test_file_path:str

@dataclass(frozen=True)
class ModelTrainerArtifact:
    trained_model_file_path:str
    trained_metric_artifact:str
    test_metric_artifact:str

@dataclass(frozen=True)
class ClassificationMetricsArtifact:
    f1_Score:float
    precision_Score:float
    recall_Score:float
    roc_auc_Score:float

@dataclass(frozen=True)
class ModelEvaluationArtifact:
    is_model_accepted:bool
    changed_accuracy:float
    best_model_path:str
    trained_model_file_path:str
    trained_model_metric_artifact:ClassificationMetricsArtifact
    best_model_metric_artifact:ClassificationMetricsArtifact

@dataclass(frozen=True)
class ModelPusherArtifact:
    saved_model_path:str
    model_file_path:str

