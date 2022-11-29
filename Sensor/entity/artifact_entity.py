from dataclasses import dataclass


@dataclass(frozen=True)
class DataIngestionArtifact:
    train_file_path:str
    test_file_path:str
