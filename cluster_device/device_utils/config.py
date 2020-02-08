import json


class Config:
    def __init__(self, path="config/config.json"):
        with open(path, 'r') as json_f:
            self.config = json.load(json_f)

    @property
    def port(self):
        return self.config["port"]

    @property
    def blender(self):
        return self.config["blender_command"]