import os
import json


class CredentialsAndDirectory:
    def __init__(self, configure=os.path.abspath('config.json')):
        self._directoryPath = ''
        self._user = ''
        self._password = ''
        self._server = ''
        self._port = ''
        self._directory_serve = ''
        self._directories = []
        self._files = []
        self._ignore_directory = []
        self._ignore_file = []
        self.parse_json(configure)

    def get_user(self):
        return self._user

    def get_password(self):
        return self._password

    def get_server(self):
        return self._server

    def get_port(self):
        return int(self._port)

    def get_directory(self):
        return self._directoryPath + '/'

    def get_all_directories(self):
        return self._directories

    def get_all_files(self):
        return self._files

    def get_ignore_directory(self):
        return self._ignore_directory

    def get_ignore_files(self):
        return self._ignore_file

    def directory_server(self):
        return self._directory_serve

    """:parameter configure: configure file"""
    """:return void"""

    def parse_json(self, configure):
        try:
            tree = json.loads(open(configure, 'r').read())
        except json.decoder.JSONDecodeError:
            input("Insira o caminho correto do arquivo de configuração")
        self._user = tree["user"]
        self._password = tree["password"]
        self._server = tree["server"]
        self._port = tree["port"]
        self._directory_serve = tree["directory_serve"]
        directory = os.path.expanduser(tree["directory_local"])
        if os.path.exists(directory) and os.path.isdir(directory):
            self._directoryPath = os.path.abspath(directory)
        if len(tree["ignore_directory"]) > 0:
            for ignores in tree["ignore_directory"]:
                self._ignore_directory.append(self.get_directory() + ignores)
        if len(tree["ignore_file"]) > 0:
            for ignores in tree["ignore_file"]:
                self._ignore_file.append(self.get_directory() + ignores)

    """:return boolean"""

    def status_configuration(self):
        return os.path.exists(self._directoryPath)

    def set_all_directories(self):
        tmp = []
        for directory in os.walk(self.get_directory()):
            tmp.append(directory[0])
        sorted(set(tmp))
        removidos = []
        for string in tmp:
            for verify in self.get_ignore_directory():
                if verify in string:
                    removidos.append(string)
        tmp = set(tmp) - set(removidos)
        list(sorted(set(tmp))).sort()
        self._directories = tmp

    def set_all_files(self):
        tmp = []
        for directory in self.get_all_directories():
            all_files = os.listdir(directory + '/')
            for arq in all_files:
                if os.path.isfile(directory + '/' + arq):
                    string = directory + '/' + arq
                    tmp.append(string.replace('//', '/'))
        removidos = []
        for string in tmp:
            for verify in self.get_ignore_files():
                if verify in string:
                    removidos.append(string)
        tmp = set(tmp) - set(removidos)
        list(sorted(set(tmp))).sort()
        self._files = tmp
