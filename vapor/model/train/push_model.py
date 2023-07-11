from ...config import StorageConfig

import boto3
from glob import glob
import os
from pathlib import Path


BUCKET = "vapor-app"


def push_model(model_name: str, version: str, config: StorageConfig) -> bool:

    # Check config valid
    if not config.valid:
        return 

    s3 = boto3.resource('s3', **config)
        
    # Get Local Files
    model_dir = os.path.join(
        Path.home(), ".vapor", "models", f"{model_name}.{version}"
    )
    fls = glob(os.path.join(model_dir, "**", "*"), recursive=True)
    fls = [fl for fl in fls if os.path.isfile(fl)]

    for fl in fls:
        remote_fl = fl.replace(
            os.path.join(Path.home(), ".vapor"), ""
        ).replace("\\", "/")
        s3.Bucket(BUCKET).upload_file(
            fl, remote_fl, ExtraArgs={'ACL': 'public-read'}
        )
        print(fl, remote_fl)
