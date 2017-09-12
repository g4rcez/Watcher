#!/usr/bin/python3
import hashlib
from src.Message import Message
from src.Connection import Connection
from src.CredentialsAndDirectory import CredentialsAndDirectory


def banner():
    print("""
██╗    ██╗ █████╗ ████████╗ ██████╗██╗  ██╗███████╗██████╗
██║    ██║██╔══██╗╚══██╔══╝██╔════╝██║  ██║██╔════╝██╔══██╗
██║ █╗ ██║███████║   ██║   ██║     ███████║█████╗  ██████╔╝
██║███╗██║██╔══██║   ██║   ██║     ██╔══██║██╔══╝  ██╔══██╗
╚███╔███╔╝██║  ██║   ██║   ╚██████╗██║  ██║███████╗██║  ██║
 ╚══╝╚══╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
 """)


banner()
notifications = Message(open('message.json', 'r').read())

manipulate = CredentialsAndDirectory()
# if not manipulate.status_configuration():
#     exit()

manipulate.set_all_directories()
manipulate.set_all_files()

print(notifications.get_message('dirs') + str(len(manipulate.get_all_directories())))
print(notifications.get_message('files') + str(len(manipulate.get_all_files())))


connection = Connection(
    manipulate.get_user(), manipulate.get_password(),
    manipulate.get_server(), manipulate.get_port()
)

for file in manipulate.get_all_files():
    local_hash = hashlib.md5(open(file, 'rb').read()).hexdigest()
    file_server = file.replace(manipulate.get_directory(),
                               manipulate.directory_server() + '/')
    signal = "md5sum " + file_server + "| cut -d ' ' -f1"
    hash_server = connection.command(signal).decode().replace('\n', '')
    if hash_server != local_hash:
        connection.put(file, file_server)
        print('[!] ' + notifications.get_message('thefile') + file_server + notifications.get_message('rescue') + file)

connection.close()
