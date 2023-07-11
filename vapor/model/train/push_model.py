from ...config import StorageConfig

import boto3
from glob import glob
import logging
import os
from pathlib import Path
import sys

logger = logging.getLogger("vapor.model")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


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
        ).replace("\\", "/").lstrip("/")

        logger.info(f"Uploading file={remote_fl}")

        s3.Bucket(BUCKET).upload_file(
            fl, remote_fl, ExtraArgs={'ACL': 'public-read'}
        )
        print(fl, remote_fl)
