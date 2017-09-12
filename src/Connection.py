import paramiko


class Connection:
    def __init__(self, user, passwd, server, port_ssh=22):
        self._ssh = paramiko.SSHClient()
        self._ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._ssh.connect(server, username=user, password=passwd, port=port_ssh)
        del passwd

    def command(self, command):
        stdin, stdout, stderr = self._ssh.exec_command(command)
        if stderr.channel.recv_exit_status() != 0:
            return stderr.read()
        else:
            return stdout.read()

    def put(self, origin, destiny):
        sftp = self._ssh.open_sftp()
        sftp.put(origin, destiny)
        sftp.close()

    def close(self):
        self._ssh.close()
        del self._ssh
