from ...config import StorageConfig

from .fetch_data import fetch_raw_data, build_spacy_datasets
from .push_model import push_model
from .train_model import train_model


def train_pipeline(model_name: str, version: str, config: StorageConfig = None):
    # Fetch Raw Data
    fetch_raw_data(model_name=model_name, version=version)
    
    # Build spaCy Datasets
    build_spacy_datasets(model_name=model_name, version=version)

    # Train Model
    train_model(model_name=model_name, version=version)

    # Push Model
    push_model(model_name=model_name, version=version, config=config)