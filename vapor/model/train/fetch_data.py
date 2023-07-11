import spacy
from spacy.tokens import DocBin
import boto3
from botocore import UNSIGNED
from botocore.client import Config

from glob import glob
from itertools import islice
from pathlib import Path
import os
import random
import shutil


BUCKET = "vapor-data"


def fetch_raw_data(model_name: str, version: str) -> bool:

    s3 = boto3.resource(
        's3',
        region_name='nyc3',
        endpoint_url='https://nyc3.digitaloceanspaces.com',
        config=Config(signature_version=UNSIGNED)
    )

    # Remove directory
    data_dir = os.path.join(Path.home(), ".vapor", "data")
    if os.path.exists(data_dir):
        shutil.rmtree(data_dir)

    # Copy Down all Files
    for obj in s3.Bucket(BUCKET).objects.filter(Prefix=f"{model_name}/{version}/"):
        filename = obj.key.replace(f"{model_name}/{version}/data/", "")

        filename = os.path.join(data_dir, filename)

        Path(os.path.dirname(filename)).mkdir(parents=True, exist_ok=True)
        with open(filename, "wb") as f:
            f.write(obj.get()["Body"].read())


def build_spacy_datasets(model_name: str, version: str, train_size: float = .70):
    data_dir = os.path.join(Path.home(), ".vapor", "data")
    
    output_dir = os.path.join(data_dir, "clean", f"{model_name}.{version}")
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    meta_fls = glob(os.path.join(data_dir,  "raw", "*.meta"))
    
    num_items = len(meta_fls)
    random.shuffle(meta_fls)

    nlp = spacy.blank("en")

    # Train/Test Split
    num_train_items = int(num_items * train_size)
    num_dev_items = num_items - num_train_items
    train_dev_split = (num_train_items, num_dev_items)

    train_fls, dev_fls = [list(islice(meta_fls, i)) for i in train_dev_split]

    # Map Categories
    categories = ["Legit", "Vapor"]
    category_map = {
        "True": "Legit",
        "False": "Vapor",
        "Legit": "Legit",
        "Vapor": "Vapor"
    }

    # Train Data
    db = DocBin()

    for meta_fl in train_fls:
        with open(meta_fl, "r", encoding="utf-8") as f:
            meta = {
                line.split("=")[0]: line.split("=")[1]
                for line in f.read().split("\n")
            }
            
        record_id = meta.get("id")
        label = meta.get("label")
        with open(os.path.join(data_dir, "raw", f"{record_id}.transcript"), "r", encoding="utf-8") as f:
            transcript = f.read()
            
        doc = nlp.make_doc(transcript)
        doc.cats = {
            category: (category_map[label] == category) * 1 
            for category in categories
        }
        db.add(doc)
        
    db.to_disk(os.path.join(output_dir, "train.spacy"))


    # Dev Data
    db = DocBin()
    for meta_fl in dev_fls:
        with open(meta_fl, "r", encoding="utf-8") as f:
            meta = {
                line.split("=")[0]: line.split("=")[1]
                for line in f.read().split("\n")
            }
            
        record_id = meta.get("id")
        label = meta.get("label")
        with open(os.path.join(data_dir, "raw", f"{record_id}.transcript"), "r", encoding="utf-8") as f:
            transcript = f.read()
            
        doc = nlp.make_doc(transcript)
        doc.cats = {
            category: (category_map[label] == category) * 1 
            for category in categories
        }
        db.add(doc)
        
    db.to_disk(os.path.join(output_dir, "dev.spacy"))