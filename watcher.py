#!/usr/bin/python3
import hashlib
from src.CredentialsAndDirectory import CredentialsAndDirectory
from src.Connection import Connection


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

manipulate = CredentialsAndDirectory()
if not manipulate.status_configuration():
    exit()

manipulate.set_all_directories()
manipulate.set_all_files()

print(len(manipulate.get_all_directories()))
print(len(manipulate.get_all_files()))
print()

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
        print('[!] ' + file_server + ' ' + file)

connection.close()
