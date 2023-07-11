import boto3
from botocore import UNSIGNED
from botocore.client import Config
import spacy
from spacy.lang.en import English

from ...config import StorageConfig

import logging
import os
from pathlib import Path
from typing import Any, Dict
import sys

logger = logging.getLogger("vapor.model")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class VaporModel(object):
    def __init__(self, nlp: English):
        self.nlp: English = nlp

    def predict(self, transcript: str) -> Dict[Any, float]:
        doc = self.nlp(transcript)
        return doc.cats


def download_model(model_name: str, version: str, config: StorageConfig = StorageConfig()) -> bool:

    s3 = boto3.resource(
        "s3", config=Config(signature_version=UNSIGNED), **config
    )
    BUCKET = "vapor-app"

    logger.info(f"Downloading model={model_name}.{version}...")
    for obj in s3.Bucket(BUCKET).objects.filter(Prefix=f"models/{model_name}.{version}/"):
        filename = obj.key.replace("models/", "")

        filename = os.path.join(Path.home(), ".vapor", "models", filename)

        Path(os.path.dirname(filename)).mkdir(parents=True, exist_ok=True)
        logger.info(f"Downloading file=`{os.path.basename(obj.key)}` to={filename}...")
        with open(filename, "wb") as f:
            f.write(obj.get()["Body"].read())


def load_model(model_name: str, version: str) -> VaporModel:
    filename = os.path.join(
        Path.home(
        ), ".vapor", "models", f"{model_name}.{version}", "model-best"
    )
    # TODO: If doesn"t exist then pull down
    
    nlp = spacy.load(name=filename)
    return VaporModel(nlp)
