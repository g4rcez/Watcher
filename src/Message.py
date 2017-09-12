import json


class Message:
    def __init__(self, db, lang='pt-br'):
        self._file = json.loads(db)[lang]
        self._lang = lang

    def get_lang(self):
        return self._lang

    def get_message(self, msg):
        return self._file[msg]
