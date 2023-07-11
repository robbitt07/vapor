

class StorageConfig(object):
    def __init__(self,
                 aws_access_key_id: str,
                 aws_secret_access_key: str,
                 region_name: str = 'nyc3',
                 endpoint_url: str = 'https://nyc3.digitaloceanspaces.com') -> None:
        self.aws_access_key_id = aws_access_key_id
        self.aws_secret_access_key = aws_secret_access_key
        self.region_name = region_name
        self.endpoint_url = endpoint_url

    @property
    def valid(self):
        assert self.aws_access_key_id not in (None, ""), "`aws_access_key_id` missing"
        assert self.aws_secret_access_key not in (None, ""), "`aws_secret_access_key` missing"
        return True

    def keys(self):
        return list(self.__dict__.keys())

    def __getitem__(self, key):
        return getattr(self, key, None)
