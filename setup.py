# -*- coding: utf-8 -*-
from setuptools import setup

packages = [
    "vapor.config", "vapor.model", "vapor.model.load", "vapor.model.train"
]

install_requires = ["spacy", "boto3"]

setup(
    name="vapor",
    version="1.0.0",
    author="YAT, LLC",
    author_email="rgoss@yat.ai",
    packages=packages,
    license="MIT",
    url="https://github.com/robbitt07/vapor",
    install_requires=install_requires,
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    package_dir={"vapor": "vapor"},
    package_data={
        "vapor": [
            "model/train/config.cfg"
        ]
    },
    description="A simple and effective Python model for detecting Vaporware",
    long_description=open("README.md").read(),
    zip_safe=True,
)