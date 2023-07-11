import spacy
from spacy.lang.en import English

import os
from pathlib import Path
from typing import Any, Dict


class VaporModel(object):
    def __init__(self, nlp: English):
        self.nlp: English = nlp

    def predict(self, transcript: str) -> Dict[Any, float]:
        doc = self.nlp(transcript)
        return doc.cats


def load_model(model_name: str, version: str) -> VaporModel:
    filename = os.path.join(
        Path.home(
        ), ".vapor", "models", f"{model_name}.{version}", "model-best"
    )
    # TODO: If doesn't exist then pull down
    
    nlp = spacy.load(name=filename)
    return VaporModel(nlp)
