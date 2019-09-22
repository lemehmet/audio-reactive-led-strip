import json
import os


class Config:
    def __init__(self, filepath=None, defaults=None):
        self.bag = {}
        self.filepath = filepath
        if self.filepath is not None and os.path.exists(self.filepath):
            self._load()
        elif defaults is not None:
            self.set_all(bag=defaults)
        elif filepath is not None and defaults is None:
            raise FileNotFoundError(f"Config file path does not exist and no defaults are provided. {filepath}")

    def _load(self):
        with open(self.filepath, 'r') as config_file:
            self.bag = json.load(config_file)

    def set_all(self, bag):
        for k, v in bag.items():
            self[k] = v

    def get_all(self):
        return json.dumps(self.bag)

    def remove(self):
        if self.filepath is not None:
            os.remove(self.filepath)

    def store(self, filepath=None):
        path = filepath if filepath is not None else self.filepath
        if path is None:
            raise FileNotFoundError("Need a file store")
        with open(path, 'w') as config_file:
            json.dump(self.bag, config_file)
            self.filepath = path

    def __getitem__(self, item):
        return self.bag[item]

    def __setitem__(self, key, value):
        self.bag[key] = value

