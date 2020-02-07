import json


class Config:
    def __init__(self, override_path=None):
        if override_path is None:
            self.path = 'configs/cluster_main.json'
        else:
            self.path = override_path
        with open(self.path, 'r') as fstream:
            self.json_obj = json.load(fstream)

    @property
    def listen_path(self):
        return self.json_obj["listen_path"]

    @property
    def tmp_path(self):
        return self.json_obj["temp_path"]
