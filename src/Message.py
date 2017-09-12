import json


class Message:
    def __init__(self, message):
        self._file = json.loads(message)