import pickle
import os.path as path

class Configuration(dict):
    def __init__(self):
        super().__init__(self)
        with open(f'{path.dirname(__file__)}/config.conf', 'rb') as f:
            self.update()
