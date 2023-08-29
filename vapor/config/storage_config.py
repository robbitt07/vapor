

class StorageConfig(object):
    def __init__(self,
                 region_name: str,
                 bucket_name: str,
                 endpoint_url: str,
                 aws_access_key_id: str = None,
                 aws_secret_access_key: str = None) -> None:

        self.region_name: str = region_name
        self.bucket_name: str = bucket_name
        self.endpoint_url: str = endpoint_url
        self.aws_access_key_id: str = aws_access_key_id
        self.aws_secret_access_key: str = aws_secret_access_key

    @property
    def cred_valid(self):
        assert self.aws_access_key_id not in (None, ""), "`aws_access_key_id` missing"
        assert self.aws_secret_access_key not in (None, ""), "`aws_secret_access_key` missing"
        return True

    def keys(self):
        return list(self.__dict__.keys())

    def __getitem__(self, key):
        return getattr(self, key, None)
