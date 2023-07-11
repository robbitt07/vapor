# Vapor

Vapor, an elegantly simple AI, NLP and blockchain solutions that can help leadership
save countless hours of wasted time.  Stop sitting through useless tech demos that 
promise the world and offer nothing of real value.  With Vapor just plug in the 
transcript and get a simple score of whether the tech if Legit or Vaporware.

## Usage

Install
```
pip install vaporware
```

Train a Model

```python
from vapor.config import StorageConfig
from vapor.model import train_pipeline

from decouple import Config, RepositoryEnv

config = Config(RepositoryEnv(".env"))


storage_config = StorageConfig(
    aws_access_key_id=config("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=config("AWS_SECRET_ACCESS_KEY")
)

train_pipeline(model_name="vapor", version="001", config=storage_config)
```

Load and predict action.
```python
from vapor.model import load_model, download_model

download_model(model_name="vapor", version="001")
model = load_model(model_name="vapor", version="001")

transcript = """Vapor, an elegantly simple AI, NLP and blockchain solutions that can help leadership
save countless hours of wasted time.  Stop sitting through useless tech demos that 
promise the world and offer nothing of real value.  With Vapor just plug in the 
transcript and get a simple score of whether the tech if Legit or Vaporware.
"""

print(model.predict(transcript))
>>> {'Legit': 0.383206307888031, 'Vapor': 0.616793692111969}
```


## Up Next

- [ ] Build out larger dataset, actual sales pitches and descriptions of failed companies.
- [ ] Accompanying API and Simple UI