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

    @property
    def tmp_path(self):
        return self.config["tmp_path"]

    @property
    def nmnt(self):
        return self.config["network_mount"]

    @property
    def server_address(self):
        return self.config["server_address"]

    @property
    def server_port(self):
        return str(self.config["server_port"])

    @property
    def hwid(self):
        return self.config["hwid"]