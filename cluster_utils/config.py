import json


# config class to get basic data to and from a json file
class Config:
    def __init__(self, override_path='configs/cluster_main.json'):
        self.path = override_path
        with open(self.path, 'r') as fstream:
            self.json_obj = json.load(fstream)

    @property
    def listen_path(self):
        return self.json_obj["listen_path"]

    @property
    def tmp_path(self):
        return self.json_obj["temp_path"]

    @property
    def port(self):
        return self.json_obj["port"]
