from spacy.cli.train import train

from pathlib import Path
import os


def train_model(model_name: str, version: str):
    # Get Data Dir
    data_dir = os.path.join(Path.home(), ".vapor", "data", "clean", f"{model_name}.{version}")
    model_dir = os.path.join(Path.home(), ".vapor", "models", f"{model_name}.{version}")
    
    # Config Path
    train_dir = os.path.abspath(os.path.dirname(__file__))
    config_path = os.path.join(train_dir, "config.cfg")
    print(config_path)

    # Train
    train(
        config_path=config_path,
        output_path=model_dir,
        overrides={
            "paths.train": os.path.join(data_dir, "train.spacy"),
            "paths.dev": os.path.join(data_dir, "dev.spacy")
        }
    )