from typing import Callable, Any, Union
import json
from pymongo import MongoClient


class MongoDB:
    def __init__(self, config: dict):
        config = config['queue']
        self.connection = MongoClient(host=config['ipAddress'], port=config['port'])


    def __del__(self):
        self.connection.close()